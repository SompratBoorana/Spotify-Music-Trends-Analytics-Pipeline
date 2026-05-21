import os
from pathlib import Path

class Config:
    """Central configuration for the pipeline"""
    
    # Project Paths
    PROJECT_ROOT = Path(__file__).parent
    RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw"
    STAGING_DATA_PATH = PROJECT_ROOT / "data" / "staging"
    
    # Database Configuration (ใช้ DuckDB เป็นหลักตามสถาปัตยกรรมตัวเบา)
    DB_TYPE = "duckdb"
    DB_PATH = PROJECT_ROOT / "data" / "spotify_analytics.duckdb"
    
    # Data Quality Settings
    MAX_NULL_PERCENTAGE = 0.05  # ยอมให้มีค่าว่างได้ไม่เกิน 5%
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FILE = PROJECT_ROOT / "logs" / "pipeline.log"
    
    @classmethod
    def get_db_connection_string(cls):
        """Get database connection string"""
        if cls.DB_TYPE == "duckdb":
            return f"duckdb:///{cls.DB_PATH}"
        else:
            raise ValueError(f"Unsupported DB_TYPE: {cls.DB_TYPE}")