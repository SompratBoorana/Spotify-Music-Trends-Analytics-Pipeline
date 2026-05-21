import os
import logging
from pathlib import Path
import pandas as pd
import duckdb

# 1. ตั้งค่า Logging ให้แสดงผลสวยๆ ใน Terminal
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    def __init__(self, db_path):
        self.conn = duckdb.connect(db_path)
    def execute_query(self, query):
        return self.conn.execute(query).fetchdf()
    def load_dataframe(self, df, table_name, if_exists='append'):
        self.conn.register('df_view', df)
        if if_exists == 'replace':
            self.conn.execute(f"DROP TABLE IF EXISTS {table_name}")
            self.conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df_view")
        else:
            self.conn.execute(f"INSERT INTO {table_name} SELECT * FROM df_view")
        self.conn.unregister('df_view')

# 2. คลาสประมวลผล ETL (ดึงมาไว้ในนี้เลย จะได้ไม่ฟ้อง ModuleNotFoundError)
class StagingToCuratedETL:
    def __init__(self, config, db):
        self.config = config
        self.db = db
    
    def create_curated_tables(self):
        self.db.conn.execute("DROP TABLE IF EXISTS fact_daily_chart_positions")
        self.db.conn.execute("DROP TABLE IF EXISTS dim_date")
        self.db.conn.execute("DROP TABLE IF EXISTS dim_song")
        self.db.conn.execute("DROP TABLE IF EXISTS dim_artist")
        self.db.conn.execute("DROP TABLE IF EXISTS dim_country")
        
        self.db.conn.execute("""
            CREATE TABLE dim_date (
                date_id INTEGER PRIMARY KEY, date DATE, year INTEGER, quarter INTEGER, 
                month INTEGER, month_name VARCHAR, day_of_week INTEGER, day_name VARCHAR, is_weekend BOOLEAN
            )
        """)
        self.db.conn.execute("""
            CREATE TABLE dim_country (
                country_id INTEGER PRIMARY KEY, country_code VARCHAR, country_name VARCHAR, region VARCHAR
            )
        """)
        self.db.conn.execute("""
            CREATE TABLE dim_song (
                song_id INTEGER PRIMARY KEY, uri VARCHAR, song_name VARCHAR, is_current BOOLEAN
            )
        """)
        self.db.conn.execute("""
            CREATE TABLE dim_artist (
                artist_id INTEGER PRIMARY KEY, artist_name VARCHAR, is_current BOOLEAN
            )
        """)
        self.db.conn.execute("""
            CREATE TABLE fact_daily_chart_positions (
                fact_id INTEGER PRIMARY KEY, date_id INTEGER, song_id INTEGER, 
                artist_id INTEGER, country_id INTEGER, rank INTEGER, streams BIGINT
            )
        """)

    def populate_dim_date(self):
        query = "SELECT DISTINCT chart_date FROM staging_chart_entries WHERE is_valid = true"
        dates_df = self.db.execute_query(query)
        if dates_df.empty: return
        dates = pd.to_datetime(dates_df['chart_date'])
        date_data = []
        for idx, date in enumerate(dates):
            date_data.append({
                'date_id': int(date.strftime('%Y%m%d')), 'date': date.date(), 'year': date.year,
                'quarter': (date.month - 1) // 3 + 1, 'month': date.month, 'month_name': date.strftime('%B'),
                'day_of_week': date.weekday() + 1, 'day_name': date.strftime('%A'), 'is_weekend': date.weekday() >= 5
            })
        self.db.load_dataframe(pd.DataFrame(date_data), 'dim_date', if_exists='append')
        
    def populate_dim_country(self):
        query = "SELECT DISTINCT country_code FROM staging_chart_entries WHERE is_valid = true"
        countries_df = self.db.execute_query(query)
        country_data = []
        for idx, row in countries_df.iterrows():
            cc = row['country_code']
            name = 'Thailand' if cc == 'TH' else ('United States' if cc == 'US' else 'Global')
            country_data.append({
                'country_id': idx + 1, 'country_code': cc, 'country_name': name,
                'region': 'Southeast Asia' if cc == 'TH' else 'International'
            })
        if country_data: self.db.load_dataframe(pd.DataFrame(country_data), 'dim_country', if_exists='append')

    def populate_dim_song(self):
        query = "SELECT DISTINCT URL, song_name FROM staging_chart_entries WHERE is_valid = true"
        songs_df = self.db.execute_query(query)
        songs_df.insert(0, 'song_id', range(1, len(songs_df) + 1))
        songs_df['is_current'] = True
        self.db.load_dataframe(songs_df, 'dim_song', if_exists='append')

    def populate_dim_artist(self):
        query = "SELECT DISTINCT artist_name FROM staging_chart_entries WHERE is_valid = true"
        artists_df = self.db.execute_query(query)
        artists_df.insert(0, 'artist_id', range(1, len(artists_df) + 1))
        artists_df['is_current'] = True
        self.db.load_dataframe(artists_df, 'dim_artist', if_exists='append')

    def populate_fact_table(self):
        join_query = """
            INSERT INTO fact_daily_chart_positions
            SELECT 
                row_number() OVER() as fact_id,
                dd.date_id,
                ds.song_id,
                da.artist_id,
                dc.country_id,
                sce.rank,
                sce.streams
            FROM staging_chart_entries sce
            JOIN dim_date dd ON CAST(sce.chart_date AS DATE) = dd.date
            JOIN dim_song ds ON sce.URL = ds.uri
            JOIN dim_artist da ON sce.artist_name = da.artist_name
            JOIN dim_country dc ON sce.country_code = dc.country_code
            WHERE sce.is_valid = true
        """
        self.db.conn.execute(join_query)
        logger.info("Successfully populated fact_daily_chart_positions (Star Schema)!")

    def run_full_etl(self):
        logger.info("Starting staging to curated ETL...")
        self.create_curated_tables()
        self.populate_dim_date()
        self.populate_dim_country()
        self.populate_dim_song()
        self.populate_dim_artist()
        self.populate_fact_table()
        logger.info("Staging to curated ETL completed successfully!")

# 3. ฟังก์ชันหลักในการรันควบคุมท่อข้อมูล
def run_pipeline():
    logger.info("====================================================")
    logger.info("  STARTING SPOTIFY MUSIC TRENDS ANALYTICS PIPELINE   ")
    logger.info("====================================================")
    
    db_path = os.path.join(os.path.abspath(os.getcwd()), "spotify_analytics.duckdb")
    db = DatabaseConnection(db_path)
    
    csv_path = os.path.join(os.path.abspath(os.getcwd()), "spotify-charts.csv")
    if not os.path.exists(csv_path):
        logger.error(f"❌ ไม่พบไฟล์ข้อมูลดิบที่ตำแหน่ง: {csv_path}")
        return
        
    logger.info(f"💾 กำลังอ่านข้อมูลจากไฟล์ดิบ: {csv_path}")
    raw_df = pd.read_csv(csv_path)
    
    logger.info("🔄 กำลังแปลงชื่อคอลัมน์ (Mapping Schema)...")
    raw_df = raw_df.rename(columns={
        'Country': 'country_code',
        'Week': 'chart_date',
        'Position': 'rank',
        'Track Name': 'song_name',
        'Artist': 'artist_name',
        'Streams': 'streams'
    })
    
    # ดัดแปลงตัวย่อประเทศตามข้อมูลดิบของคุณ
    raw_df['country_code'] = raw_df['country_code'].replace({'Argentina': 'AR', 'South Africa': 'ZA', 'Thailand': 'TH'})
    raw_df['is_valid'] = True
    
    logger.info("📥 กำลังนำข้อมูลดิบเข้าสู่ชั้น Staging Zone...")
    db.load_dataframe(raw_df, 'staging_chart_entries', if_exists='replace')
    
    logger.info("✨ กำลังขับเคลื่อนระบบ ETL เข้าสู่ชั้น Curated Zone (Star Schema)...")
    etl = StagingToCuratedETL(config=None, db=db)
    etl.run_full_etl()
    
    print("\n============================================================")
    print(" 🎉 PIPELINE COMPLETED SUCCESSFULLY! ")
    print("============================================================\n")

if __name__ == "__main__":
    run_pipeline()