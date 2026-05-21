-- พิมพ์เขียวคลังข้อมูลแบบโมเดลจำลองดวงดาว (Gold Layer - Star Schema)
CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY,
    date DATE,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    month_name VARCHAR(20),
    day_of_week INTEGER,
    day_name VARCHAR(20),
    is_weekend BOOLEAN
);

CREATE TABLE dim_country (
    country_id INTEGER PRIMARY KEY,
    country_code VARCHAR(2),
    country_name VARCHAR(100),
    region VARCHAR(50)
);

CREATE TABLE dim_song (
    song_id INTEGER PRIMARY KEY,
    uri VARCHAR(200),
    song_name VARCHAR(500),
    is_current BOOLEAN
);

CREATE TABLE dim_artist (
    artist_id INTEGER PRIMARY KEY,
    artist_name VARCHAR(500),
    is_current BOOLEAN
);

CREATE TABLE fact_daily_chart_positions (
    fact_id INTEGER PRIMARY KEY,
    date_id INTEGER,
    song_id INTEGER,
    artist_id INTEGER,
    country_id INTEGER,
    rank INTEGER,
    streams BIGINT
);