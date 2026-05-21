import pandas as pd
import logging

logger = logging.getLogger(__name__)

class StagingToCuratedETL:
    """ETL from staging to curated zone"""
    
    def __init__(self, config, db):
        self.config = config
        self.db = db
    
    def create_curated_tables(self):
        """สร้างตารางในส่วนของ Gold / Curated Zone ยืนพื้นไว้ก่อน"""
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
        
        if dates_df.empty:
            return
            
        dates = pd.to_datetime(dates_df['chart_date'])
        date_data = []
        for idx, date in enumerate(dates):
            date_data.append({
                'date_id': int(date.strftime('%Y%m%d')),
                'date': date.date(),
                'year': date.year,
                'quarter': (date.month - 1) // 3 + 1,
                'month': date.month,
                'month_name': date.strftime('%B'),
                'day_of_week': date.weekday() + 1,
                'day_name': date.strftime('%A'),
                'is_weekend': date.weekday() >= 5
            })
        df = pd.DataFrame(date_data)
        self.db.load_dataframe(df, 'dim_date', if_exists='append')
        
    def populate_dim_country(self):
        query = "SELECT DISTINCT country_code FROM staging_chart_entries WHERE is_valid = true"
        countries_df = self.db.execute_query(query)
        
        country_data = []
        for idx, row in countries_df.iterrows():
            cc = row['country_code']
            name = 'Thailand' if cc == 'TH' else ('United States' if cc == 'US' else 'Global')
            country_data.append({
                'country_id': idx + 1,
                'country_code': cc,
                'country_name': name,
                'region': 'Southeast Asia' if cc == 'TH' else 'International'
            })
        if country_data:
            df = pd.DataFrame(country_data)
            self.db.load_dataframe(df, 'dim_country', if_exists='append')

    def populate_dim_song(self):
        query = "SELECT DISTINCT uri, song_name FROM staging_chart_entries WHERE is_valid = true"
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
        # ใช้ SQL JOIN ใน DuckDB เพื่อสร้างตาราง Fact ยิงข้อมูลจาก Staging ร่วมกับ Dimension เข้าด้วยกัน
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
            JOIN dim_song ds ON sce.uri = ds.uri
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