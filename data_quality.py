import pandas as pd
import logging

logger = logging.getLogger(__name__)

class DataQualityChecker:
    """Data quality validation framework"""
    
    def __init__(self, config):
        self.config = config
        self.issues = []
    
    def check_nulls(self, df, required_columns):
        """Check for null values in required columns"""
        for col in required_columns:
            if col not in df.columns:
                continue
            null_count = df[col].isnull().sum()
            null_pct = null_count / len(df) if len(df) > 0 else 0
            
            if null_pct > self.config.MAX_NULL_PERCENTAGE:
                issue = {
                    'check_type': 'missing_values',
                    'severity': 'error',
                    'column_name': col,
                    'issue_description': f"{null_pct*100:.2f}% null values",
                    'affected_rows': int(null_count)
                }
                self.issues.append(issue)
                logger.error(f"Column {col} has {null_pct*100:.2f}% null values")
        return len(self.issues) == 0
    
    def check_duplicates(self, df, subset_columns):
        """Check for duplicate rows"""
        # คัดกรองคอลัมน์ที่มีอยู่จริงใน df เท่านั้น
        cols = [c for c in subset_columns if c in df.columns]
        if not cols:
            return True
        duplicates = df.duplicated(subset=cols, keep=False)
        dup_count = duplicates.sum()
        
        if dup_count > 0:
            issue = {
                'check_type': 'duplicate',
                'severity': 'warning',
                'issue_description': f"Found {dup_count} duplicate rows",
                'affected_rows': int(dup_count)
            }
            self.issues.append(issue)
            logger.warning(f"Found {dup_count} duplicate rows")
            return False
        return True
    
    def check_value_ranges(self, df, range_rules):
        """Check if values are within expected ranges"""
        for col, (min_val, max_val) in range_rules.items():
            if col not in df.columns:
                continue
            out_of_range = df[(df[col] < min_val) | (df[col] > max_val)]
            if len(out_of_range) > 0:
                issue = {
                    'check_type': 'invalid_range',
                    'severity': 'error',
                    'column_name': col,
                    'issue_description': f"Values outside range [{min_val}, {max_val}]",
                    'affected_rows': len(out_of_range)
                }
                self.issues.append(issue)
                logger.error(f"{len(out_of_range)} rows in {col} outside valid range")
        return len(self.issues) == 0
    
    def get_issues(self):
        return self.issues