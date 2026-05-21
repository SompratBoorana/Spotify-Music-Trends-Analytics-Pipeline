import pandas as pd
import logging
from pathlib import Path
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class RawDataIngester:
    """Ingest raw Spotify chart CSV files"""
    
    def __init__(self, config, db, data_quality_checker):
        self.config = config
        self.db = db
        self.dq_checker = data_quality_checker
        self.batch_id = str(uuid.uuid4())[:8]
    
    def read_csv_file(self, file_path):
        try:
            # ใช้ pd.read_csv ตรงๆ พารามิเตอร์จะคำนวณวิธีการเปิดให้อัตโนมัติ 
            # และเพิ่ม encoding='utf-8' เพื่อรองรับชื่อเพลงภาษาไทย/ต่างประเทศไม่ให้ต่างดาว
            df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')
            logger.info(f"Read {len(df)} rows from {file_path}")
            return df
        except Exception as e:
            logger.error(f"Failed to read {file_path}: {e}")
            raise
    
    def clean_and_validate(self, df, source_file):
        # ปรับหัวคอลัมน์มาตรฐานเพื่อรองรับ Dataset ทั่วไป
        # หากชื่อคอลัมน์เป็นตัวพิมพ์ใหญ่ ให้แปลงเป็นตัวพิมพ์เล็ก
        df.columns = [c.lower() for c in df.columns]
        
        # Mapping คอลัมน์ยอดฮิตจาก Spotify Charts standard
        rename_map = {
            'rank': 'rank',
            'position': 'rank',
            'track_name': 'song_name',
            'artist_names': 'artist_name',
            'artist': 'artist_name',
            'uri': 'uri'
        }
        df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns}, inplace=True)
        
        # เพิ่มคอลัมน์ที่จำเป็นหากไม่มีในไฟล์ดิบ
        if 'chart_date' not in df.columns:
            # พยายามดึงวันที่จากชื่อไฟล์ หรือตั้งเป็นวันปัจจุบัน
            df['chart_date'] = datetime.now().strftime('%Y-%m-%d')
        if 'country_code' not in df.columns:
            df['country_code'] = 'TH'
        if 'uri' not in df.columns:
            df['uri'] = df['song_name']
        if 'streams' not in df.columns:
            df['streams'] = 0
            
        # สร้าง Metadata กำกับข้อมูล (Audit Trail)
        df['source_file'] = str(source_file.name)
        df['load_timestamp'] = datetime.now()
        df['load_batch_id'] = self.batch_id
        df['is_valid'] = True
        df['validation_notes'] = None
        
        # 5. ลบแถวที่เป็นค่าว่างในส่วนสำคัญทิ้งไปก่อนเพื่อไม่ให้ DataFrame ว่างเปล่า
        df = df.dropna(subset=['song_name', 'artist_name'], how='any').copy()
        
        # 6. ตรวจสอบ Data Quality
        # (เราจะไม่ส่งดาต้าเฟรมเปล่าให้ DQ เช็คเพื่อเลี่ยง Error)
        if not df.empty:
            required_cols = ['chart_date', 'country_code', 'rank', 'song_name', 'artist_name']
            self.dq_checker.check_nulls(df, required_cols)
            self.dq_checker.check_duplicates(df, ['chart_date', 'country_code', 'rank'])
            self.dq_checker.check_value_ranges(df, {'rank': (1, 250)}) # ขยายช่วงรองรับ Top 200
            
            if self.dq_checker.get_issues():
                df['is_valid'] = False
                df['validation_notes'] = str(self.dq_checker.get_issues()[:2])
            
        return df
    
    def load_to_staging(self, df):
        try:
            self.db.load_dataframe(df, 'staging_chart_entries', if_exists='append')
        except Exception as e:
            logger.error(f"Failed to load to staging: {e}")
            raise
    
    def process_directory(self, directory_path):
        csv_files = list(Path(directory_path).glob("*.csv"))
        logger.info(f"Found {len(csv_files)} CSV files to process")
        
        # สร้างตารางเปล่าไว้รอก่อนในรันครั้งแรก
        if csv_files:
            first_df = pd.read_csv(csv_files[0])
            first_df.columns = [c.lower() for c in first_df.columns]
            # เคลียร์ข้อมูลเก่าใน Staging table ก่อนเริ่มรอบใหม่
            self.db.conn.execute("DROP TABLE IF EXISTS staging_chart_entries")
            self.db.conn.execute("""
                CREATE TABLE staging_chart_entries (
                    rank INTEGER, song_name VARCHAR, artist_name VARCHAR, 
                    streams BIGINT, uri VARCHAR, chart_date TIMESTAMP, country_code VARCHAR,
                    source_file VARCHAR, load_timestamp TIMESTAMP, load_batch_id VARCHAR,
                    is_valid BOOLEAN, validation_notes VARCHAR
                )
            """)
            
        for csv_file in csv_files:
            logger.info(f"Processing {csv_file.name}")
            df = self.read_csv_file(csv_file)
            df = self.clean_and_validate(df, csv_file)
            self.load_to_staging(df)
            
        logger.info(f"Batch {self.batch_id} completed!")