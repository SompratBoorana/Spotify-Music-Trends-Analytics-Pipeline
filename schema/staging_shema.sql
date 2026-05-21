-- พิมพ์เขียวสำหรับจัดเก็บน้ำดิบที่ผ่านการกรองขั้นแรก (Silver Layer)
CREATE TABLE staging_chart_entries (
    rank INTEGER,
    song_name VARCHAR(500),
    artist_name VARCHAR(500),
    streams BIGINT,
    uri VARCHAR(200),
    chart_date TIMESTAMP,
    country_code VARCHAR(2),
    source_file VARCHAR(250),
    load_timestamp TIMESTAMP,
    load_batch_id VARCHAR(50),
    is_valid BOOLEAN,
    validation_notes TEXT
);