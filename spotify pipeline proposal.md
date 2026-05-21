# Spotify Music Trends Analytics Pipeline

## Data Architecture Final Project Proposal

-----

## 📌 Executive Summary

โปรเจคนี้มุ่งเน้นการสร้าง **End-to-End Data Pipeline** สำหรับวิเคราะห์เทรนด์เพลงจาก Spotify เพื่อแสดงความเข้าใจในหลักการ Data Architecture ครอบคลุมตั้งแต่ Data Ingestion, Storage Zones, Data Transformation, Quality Assurance, จนถึง Analytics & Visualization

**Project Duration**: 4 สัปดาห์ (ก่อนสอบ 2 May)  
**Complexity Level**: Moderate (เหมาะกับการเรียนรู้)  
**Technology Stack**: Python, PostgreSQL/DuckDB, Git, Streamlit

-----

## 🎯 1. ความเป็นมาและความสำคัญ (Background & Significance)

### 1.1 ความเป็นมา

ในยุคที่ดนตรีถูกบริโภคผ่านแพลตฟอร์ม streaming เป็นหลัก **Spotify** ได้กลายเป็นหนึ่งในแพลตฟอร์มที่มีอิทธิพลต่อวงการเพลงมากที่สุด โดยมีผู้ใช้งานกว่า 500 ล้านคนทั่วโลก การเข้าใจเทรนด์ดนตรีจึงมีความสำคัญต่อหลายฝ่าย:

- **ศิลปิน/เลเบิล**: ต้องการเข้าใจตลาดและวางแผนการปล่อยเพลง
- **Playlist Curators**: ต้องการติดตามเพลงที่กำลังมาแรง
- **นักวิเคราะห์ตลาด**: ศึกษาพฤติกรรมการฟังเพลงของผู้บริโภค
- **นักเรียนด้าน Data**: ฝึกทักษะ data engineering ด้วย dataset จริง

อย่างไรก็ตาม ข้อมูลจาก Spotify กระจัดกระจายและไม่มีโครงสร้างที่พร้อมสำหรับการวิเคราะห์ขั้นสูง จึงจำเป็นต้องมี **Data Pipeline** ที่เหมาะสม

### 1.2 ความสำคัญของโปรเจค

โปรเจคนี้มีความสำคัญใน **3 มิติ**:

#### 🎓 **มิติการศึกษา (Academic Value)**

- แสดงความเข้าใจในหลัก **Data Architecture Principles**:
  - Data Zones (Raw/Staging/Curated)
  - ETL/ELT Pipelines
  - Data Quality & Governance
  - Dimensional Modeling
- ฝึกการเลือกใช้เครื่องมือที่เหมาะสมกับปัญหา
- เรียนรู้ Best Practices ในการจัดการ data lifecycle

#### 💼 **มิติเชิงธุรกิจ (Business Value)**

- สามารถนำไปประยุกต์ใช้กับ real-world scenarios:
  - Marketing analytics
  - Content strategy
  - Trend forecasting
- สร้าง insights ที่มีความหมายจากข้อมูล raw

#### 🛠️ **มิติเชิงเทคนิค (Technical Value)**

- Scalable architecture ที่รองรับข้อมูลที่เพิ่มขึ้น
- Maintainable codebase ที่สามารถพัฒนาต่อได้
- Portfolio piece สำหรับการสมัครงาน

-----

## ⚠️ 2. Pain Points และปัญหาที่ต้องแก้ไข

### 2.1 Pain Points ของ Raw Data

**P1: Data Fragmentation (ข้อมูลกระจัดกระจาย)**

- Spotify Charts แยกเป็นไฟล์ CSV รายวัน/รายประเทศ
- ไม่มี unified view สำหรับการวิเคราะห์ระยะยาว
- 💡 **แก้ไข**: สร้าง centralized data warehouse

**P2: Data Quality Issues (ปัญหาคุณภาพข้อมูล)**

- Missing values (เช่น artist name หาย)
- Inconsistent formats (date formats ต่างกัน)
- Duplicate entries (เพลงเดียวกันมีหลาย entries)
- 💡 **แก้ไข**: Implement data validation & cleaning pipelines

**P3: Lack of Historical Context (ขาดบริบททางประวัติศาสตร์)**

- CSV files เป็น snapshot ณ วันนั้น
- ไม่สามารถติดตามการเปลี่ยนแปลงได้ (เช่น เพลงขึ้น/ลงชาร์ต)
- 💡 **แก้ไข**: สร้าง slowly changing dimensions (SCD Type 2)

**P4: Manual Process (กระบวนการแบบ manual)**

- ต้องดาวน์โหลดและ merge data เอง
- ไม่มี automation
- Error-prone
- 💡 **แก้ไข**: สร้าง automated pipeline (แม้จะไม่เป็น real-time)

**P5: No Analytics-Ready Structure (ไม่พร้อมสำหรับการวิเคราะห์)**

- Raw CSV ไม่เหมาะกับการทำ complex queries
- ไม่มี pre-computed aggregations
- 💡 **แก้ไข**: สร้าง curated data marts

### 2.2 Pain Points ของ Analysts/Users

**U1: Difficult to Answer Business Questions**

- “Artist ไหนที่กำลังมาแรงที่สุดในเดือนนี้?”
- “Country ไหนมีรสนิยมเพลงคล้ายกัน?”
- “Genre ไหนกำลังจะ boom ในอนาคต?”
- ต้องใช้เวลามาก manual analysis

**U2: No Visualization Tools**

- ต้องใช้ Excel เปิด CSV ดู
- ไม่มี dashboard สำหรับ monitoring

**U3: Data Not Trusted**

- ไม่มีการ validate
- ไม่รู้ว่าข้อมูลล่าสุดเมื่อไหร่
- ไม่มี data lineage

-----

## 🎯 3. วัตถุประสงค์ (Objectives)

### 3.1 Primary Objectives

**O1: สร้าง Robust Data Pipeline**

- ✅ รับข้อมูลจาก Spotify Charts (manual export)
- ✅ จัดเก็บข้อมูลในรูปแบบ structured (PostgreSQL/DuckDB)
- ✅ ทำ data cleaning & transformation
- ✅ สร้าง analytics-ready datasets

**O2: แสดงความเข้าใจใน Data Architecture Concepts**

- ✅ Implement **3-Zone Architecture** (Raw/Staging/Curated)
- ✅ ออกแบบ **Dimensional Model** (Star Schema)
- ✅ ใช้ **Data Quality** frameworks
- ✅ Implement **Incremental Loading**

**O3: สร้าง Actionable Insights**

- ✅ Dashboard แสดงเทรนด์เพลงแบบ real-time
- ✅ Comparative analysis (country vs country, genre trends)
- ✅ Artist/Song performance metrics

### 3.2 Secondary Objectives (Bonus)

**O4: Demonstrate Software Engineering Best Practices**

- ✅ Clean, modular code
- ✅ Proper Git usage (branching, commits)
- ✅ Documentation (README, code comments)
- ✅ Error handling & logging

**O5: Creativity & Innovation**

- ✅ Unique visualizations
- ✅ Interesting analysis angles
- ✅ Thoughtful data storytelling

-----

## 📐 4. ขอบเขตโปรเจค (Project Scope)

### 4.1 In Scope ✅

**Data Sources**

- ✅ Spotify Daily Top 200 Charts (ประเทศหลัก 5-10 ประเทศ)
- ✅ Spotify Viral 50 Charts
- ✅ เริ่มจากข้อมูล 1-3 เดือนย้อนหลัง

**Features**

- ✅ Data ingestion (manual export to raw zone)
- ✅ ETL pipeline (raw → staging → curated)
- ✅ Data quality checks
- ✅ Dimensional model (star schema)
- ✅ Aggregated analytics tables
- ✅ Basic dashboard (Streamlit)
- ✅ Git version control

**Deliverables**

- ✅ Working pipeline code (Python)
- ✅ Database schema (SQL)
- ✅ Architecture documentation
- ✅ Dashboard/visualization
- ✅ Presentation slides
- ✅ README with setup instructions

### 4.2 Out of Scope ❌

**Not Included**

- ❌ Real-time streaming data
- ❌ ML/AI models (prediction, recommendation)
- ❌ Distributed computing (Spark clusters)
- ❌ Cloud deployment (AWS/GCP) - เว้นแต่มีเวลาเหลือ
- ❌ Web scraping automation (ใช้ manual export)
- ❌ Audio analysis (waveforms, BPM detection)
- ❌ Social media integration (Twitter sentiment)

### 4.3 Assumptions

- 📌 ข้อมูลจะ export เป็น CSV จาก Spotify Charts
- 📌 Pipeline จะรัน locally (not cloud-hosted)
- 📌 Data update frequency: Weekly หรือ manual trigger
- 📌 Focus on **architecture** มากกว่า advanced analytics
- 📌 Database จะใช้ PostgreSQL หรือ DuckDB (lightweight)

-----

## 🏗️ 5. Data Architecture Design

### 5.1 Overall Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA SOURCES                              │
│  • Spotify Charts (CSV Export)                                   │
│  • Kaggle Spotify Datasets (Optional Enrichment)                │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Manual Download / API Call
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RAW ZONE (Bronze Layer)                       │
│  • Storage: Local Filesystem / MinIO                            │
│  • Format: CSV, JSON (as-is from source)                        │
│  • No Transformation                                             │
│  • Timestamped folders: raw/YYYY-MM-DD/                         │
│                                                                  │
│  Example:                                                        │
│    raw/2024-04-01/spotify_top200_thailand.csv                   │
│    raw/2024-04-01/spotify_top200_usa.csv                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Python ETL Script
                         │ • Data validation
                         │ • Schema enforcement
                         │ • Deduplication
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  STAGING ZONE (Silver Layer)                     │
│  • Storage: PostgreSQL/DuckDB                                   │
│  • Cleaned & Validated Data                                      │
│  • Normalized Tables                                             │
│  • Data Quality Checks Applied                                   │
│                                                                  │
│  Tables:                                                         │
│    - staging_chart_entries (raw cleaned records)                │
│    - staging_songs (unique songs)                               │
│    - staging_artists (unique artists)                           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ dbt / SQL Transformations
                         │ • Business logic
                         │ • Aggregations
                         │ • Slowly Changing Dimensions
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  CURATED ZONE (Gold Layer)                       │
│  • Storage: PostgreSQL/DuckDB (Data Mart)                       │
│  • Star Schema / Dimensional Model                               │
│  • Analytics-Ready                                               │
│                                                                  │
│  Fact Tables:                                                    │
│    - fact_daily_chart_positions                                 │
│    - fact_song_streams                                          │
│                                                                  │
│  Dimension Tables:                                               │
│    - dim_song                                                    │
│    - dim_artist                                                  │
│    - dim_date                                                    │
│    - dim_country                                                 │
│                                                                  │
│  Aggregate Tables:                                               │
│    - agg_weekly_top_songs                                       │
│    - agg_artist_performance                                     │
│    - agg_country_trends                                         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              ANALYTICS & VISUALIZATION LAYER                     │
│  • Streamlit Dashboard                                          │
│  • Tableau/Power BI (Optional)                                  │
│  • Jupyter Notebooks (Ad-hoc Analysis)                          │
│                                                                  │
│  Dashboards:                                                     │
│    - Global Music Trends                                        │
│    - Artist Performance Tracker                                 │
│    - Country Comparison                                         │
│    - Genre Evolution                                            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    SUPPORTING COMPONENTS                         │
├─────────────────────────────────────────────────────────────────┤
│  • Git Repository (Version Control)                             │
│  • Logging & Monitoring (Python logging module)                 │
│  • Data Quality Framework (Great Expectations / Custom)         │
│  • Documentation (README, Architecture Diagrams)                │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Data Flow Diagram

```
[Manual Download] 
      ↓
[Raw CSV Files] → [Python Ingestion Script]
                         ↓
                  [Validation Layer]
                    ✓ Schema Check
                    ✓ Null Check
                    ✓ Duplicate Check
                         ↓
                  [Staging Tables]
                         ↓
              [Transformation Layer]
                    ✓ Join Artist Info
                    ✓ Calculate Trends
                    ✓ Create Dimensions
                         ↓
                  [Curated Tables]
                         ↓
                  [Analytics Layer]
                  (Dashboard/Reports)
```

### 5.3 Technology Stack Justification

|Component          |Technology                           |Reason for Selection                                                                                       |
|-------------------|-------------------------------------|-----------------------------------------------------------------------------------------------------------|
|**Raw Storage**    |Local Filesystem / MinIO             |• เบสิคและเข้าใจง่าย<br>• MinIO ใช้ได้ถ้าต้องการ S3-compatible                                                    |
|**Database**       |PostgreSQL **หรือ** DuckDB            |• PostgreSQL: Industry standard, เหมาะกับ OLAP<br>• DuckDB: Lightweight, ไม่ต้อง setup server, ดีสำหรับ analytics|
|**ETL/Scripting**  |Python (pandas, sqlalchemy)          |• เรียนรู้ง่าย<br>• Library ecosystem ดี<br>• Integration ดีกับ database                                          |
|**Transformation** |dbt (optional) **หรือ** SQL Scripts   |• dbt: Modern data transformation tool<br>• SQL: ถ้าอยากเบสิคกว่า                                             |
|**Data Quality**   |Great Expectations **หรือ** Custom    |• Great Expectations: Industry standard<br>• Custom: เบสิคกว่า ควบคุมได้เอง                                    |
|**Orchestration**  |Python Scripts + Cron **หรือ** Airflow|• Scripts: เบสิคที่สุด<br>• Airflow: ถ้าอยากโชว์มากกว่า (optional)                                                |
|**Visualization**  |Streamlit                            |• Python-native<br>• สร้าง dashboard ง่าย<br>• ไม่ต้องเขียน HTML/CSS/JS                                         |
|**Version Control**|Git + GitHub                         |• Standard practice<br>• Collaboration ready                                                               |
|**Documentation**  |Markdown (README.md)                 |• Simple, readable<br>• GitHub-friendly                                                                    |

-----

## 📊 6. Data Model Design

### 6.1 Staging Zone Schema

#### Table: `staging_chart_entries`

```sql
CREATE TABLE staging_chart_entries (
    entry_id SERIAL PRIMARY KEY,
    chart_date DATE NOT NULL,
    country_code VARCHAR(2) NOT NULL,
    rank INTEGER NOT NULL,
    song_name VARCHAR(500) NOT NULL,
    artist_name VARCHAR(500) NOT NULL,
    streams BIGINT,
    uri VARCHAR(200),
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Data quality columns
    is_valid BOOLEAN DEFAULT TRUE,
    validation_notes TEXT
);
```

#### Table: `staging_songs`

```sql
CREATE TABLE staging_songs (
    song_id SERIAL PRIMARY KEY,
    song_name VARCHAR(500) NOT NULL,
    uri VARCHAR(200) UNIQUE NOT NULL,
    first_seen_date DATE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Table: `staging_artists`

```sql
CREATE TABLE staging_artists (
    artist_id SERIAL PRIMARY KEY,
    artist_name VARCHAR(500) NOT NULL UNIQUE,
    first_seen_date DATE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 6.2 Curated Zone Schema (Star Schema)

#### Fact Table: `fact_daily_chart_positions`

```sql
CREATE TABLE fact_daily_chart_positions (
    fact_id SERIAL PRIMARY KEY,
    date_id INTEGER REFERENCES dim_date(date_id),
    song_id INTEGER REFERENCES dim_song(song_id),
    artist_id INTEGER REFERENCES dim_artist(artist_id),
    country_id INTEGER REFERENCES dim_country(country_id),
    
    -- Metrics
    rank INTEGER NOT NULL,
    streams BIGINT,
    days_on_chart INTEGER,
    rank_change INTEGER, -- vs previous day
    peak_rank INTEGER,
    
    -- Metadata
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for query performance
CREATE INDEX idx_fact_date ON fact_daily_chart_positions(date_id);
CREATE INDEX idx_fact_song ON fact_daily_chart_positions(song_id);
CREATE INDEX idx_fact_artist ON fact_daily_chart_positions(artist_id);
CREATE INDEX idx_fact_country ON fact_daily_chart_positions(country_id);
```

#### Dimension Table: `dim_date`

```sql
CREATE TABLE dim_date (
    date_id SERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    week_of_year INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    is_weekend BOOLEAN NOT NULL
);
```

#### Dimension Table: `dim_song`

```sql
CREATE TABLE dim_song (
    song_id SERIAL PRIMARY KEY,
    song_name VARCHAR(500) NOT NULL,
    uri VARCHAR(200) UNIQUE NOT NULL,
    release_date DATE,
    duration_ms INTEGER,
    
    -- SCD Type 2 columns
    effective_date DATE NOT NULL,
    end_date DATE,
    is_current BOOLEAN DEFAULT TRUE
);
```

#### Dimension Table: `dim_artist`

```sql
CREATE TABLE dim_artist (
    artist_id SERIAL PRIMARY KEY,
    artist_name VARCHAR(500) NOT NULL,
    genres TEXT[], -- Array of genres
    first_chart_appearance DATE,
    
    -- SCD Type 2
    effective_date DATE NOT NULL,
    end_date DATE,
    is_current BOOLEAN DEFAULT TRUE
);
```

#### Dimension Table: `dim_country`

```sql
CREATE TABLE dim_country (
    country_id SERIAL PRIMARY KEY,
    country_code VARCHAR(2) NOT NULL UNIQUE,
    country_name VARCHAR(100) NOT NULL,
    region VARCHAR(50),
    continent VARCHAR(50)
);
```

### 6.3 Aggregation Tables

#### Table: `agg_weekly_top_songs`

```sql
CREATE TABLE agg_weekly_top_songs (
    agg_id SERIAL PRIMARY KEY,
    week_start_date DATE NOT NULL,
    country_id INTEGER REFERENCES dim_country(country_id),
    song_id INTEGER REFERENCES dim_song(song_id),
    artist_id INTEGER REFERENCES dim_artist(artist_id),
    
    -- Aggregated metrics
    avg_rank DECIMAL(5,2),
    total_streams BIGINT,
    days_in_top_10 INTEGER,
    peak_rank INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Table: `agg_artist_performance`

```sql
CREATE TABLE agg_artist_performance (
    agg_id SERIAL PRIMARY KEY,
    artist_id INTEGER REFERENCES dim_artist(artist_id),
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    
    -- Metrics
    total_chart_entries INTEGER,
    unique_songs_charted INTEGER,
    total_streams BIGINT,
    avg_rank DECIMAL(5,2),
    countries_appeared INTEGER, -- How many countries they charted in
    
    -- Trend indicators
    trend_direction VARCHAR(20), -- 'rising', 'stable', 'declining'
    momentum_score DECIMAL(5,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

-----

## 🔧 7. Tools และเหตุผลการใช้

### 7.1 Data Ingestion & Processing Tools

#### **Python + Pandas**

**ใช้เพื่อ**: ETL scripting, data manipulation
**เหตุผล**:

- ✅ Industry standard สำหรับ data engineering
- ✅ pandas มี functions ครบสำหรับ clean/transform data
- ✅ Integration ดีกับ database (sqlalchemy)
- ✅ Easy to learn and debug

**Use Cases**:

- อ่าน CSV files จาก raw zone
- Data cleaning (handle nulls, duplicates)
- Type conversion
- Load data เข้า staging zone

#### **SQLAlchemy**

**ใช้เพื่อ**: Database ORM and connection management
**เหตุผล**:

- ✅ Pythonic way to interact with databases
- ✅ Connection pooling
- ✅ รองรับหลาย database backends

### 7.2 Storage & Database Tools

#### **PostgreSQL หรือ DuckDB**

**ใช้เพื่อ**: Staging & Curated zones storage
**เหตุผล**:

**PostgreSQL**:

- ✅ Production-grade RDBMS
- ✅ ACID compliant
- ✅ ดีสำหรับ concurrent access
- ✅ Industry standard
- ❌ ต้อง setup server

**DuckDB**:

- ✅ Embedded database (ไม่ต้อง setup server)
- ✅ Optimized สำหรับ analytics (OLAP)
- ✅ รองรับ Parquet, CSV direct query
- ✅ เร็วมากสำหรับ aggregations
- ❌ Single-user (ไม่ค่อยเหมาะกับ production)

**คำแนะนำ**: ใช้ **DuckDB** สำหรับ project นี้เพราะง่ายกว่าและเหมาะกับ analytics

### 7.3 Data Quality Tools

#### **Great Expectations (Optional)** หรือ **Custom Validation**

**ใช้เพื่อ**: Data validation and quality checks
**เหตุผล**:

**Great Expectations**:

- ✅ Framework สำหรับ data validation
- ✅ มี pre-built expectations (ไม่ต้องเขียนเอง)
- ✅ Generate data quality reports
- ❌ Learning curve สูงหน่อย

**Custom Validation**:

- ✅ ควบคุมได้เอง
- ✅ เบสิคกว่า เข้าใจง่าย
- ✅ เขียน Python functions เช็ค:
  - Not null checks
  - Data type validation
  - Range checks
  - Uniqueness constraints

**คำแนะนำ**: เริ่มจาก **Custom Validation** ก่อน ถ้ามีเวลาเหลือค่อยเพิ่ม Great Expectations

### 7.4 Transformation Tools

#### **SQL Scripts** หรือ **dbt (Data Build Tool)**

**ใช้เพื่อ**: Transform staging → curated data
**เหตุผล**:

**SQL Scripts**:

- ✅ เบสิคที่สุด
- ✅ ใช้ pure SQL
- ✅ Run ได้จาก Python script
- ❌ ไม่มี dependency management
- ❌ Testing ยาก

**dbt**:

- ✅ Modern data transformation tool
- ✅ มี dependency management (DAG)
- ✅ มี testing framework built-in
- ✅ Version control friendly
- ✅ Documentation generation
- ❌ Learning curve

**คำแนะนำ**: ถ้าต้องการ impress ให้ใช้ **dbt**, ถ้าอยากเบสิคให้ใช้ **SQL scripts**

### 7.5 Visualization Tools

#### **Streamlit**

**ใช้เพื่อ**: Create interactive dashboard
**เหตุผล**:

- ✅ Pure Python (ไม่ต้องเขียน HTML/CSS/JS)
- ✅ สร้าง UI ได้รวดเร็ว
- ✅ Interactive widgets (filters, sliders)
- ✅ รองรับ charts (matplotlib, plotly)
- ✅ Free และ easy to deploy

**Alternative**: Tableau/Power BI (ถ้ามี license)

### 7.6 Version Control

#### **Git + GitHub**

**ใช้เพื่อ**: Code versioning, collaboration
**เหตุผล**:

- ✅ Industry standard
- ✅ Track changes
- ✅ Branching strategies
- ✅ Portfolio showcase

### 7.7 Orchestration (Optional)

#### **Python Scripts + Logging** หรือ **Apache Airflow**

**ใช้เพื่อ**: Workflow orchestration
**เหตุผล**:

**Python Scripts**:

- ✅ เบสิคที่สุด
- ✅ Run manually or with cron
- ✅ ไม่ต้อง setup infrastructure

**Airflow**:

- ✅ Industry standard orchestration tool
- ✅ Web UI สำหรับ monitoring
- ✅ Retry logic, error handling
- ❌ Setup ค่อนข้างซับซ้อน

**คำแนะนำ**: เริ่มจาก **Python Scripts** ก่อน, ถ้ามีเวลาเหลือค่อยใช้ Airflow

-----

## 🎯 8. ปัญหาที่โปรเจคนี้แก้ไข

### 8.1 ปัญหาทางเทคนิค

|ปัญหา                 |วิธีแก้ด้วย Architecture                          |
|---------------------|----------------------------------------------|
|**ข้อมูลกระจัดกระจาย**  |รวมข้อมูลทุก source ใน centralized warehouse     |
|**ไม่มีโครงสร้างชัดเจน** |สร้าง star schema ที่ optimize สำหรับ queries      |
|**Data quality ต่ำ**   |ใช้ staging zone ทำ validation ก่อนเข้า curated   |
|**Query ช้า**         |Pre-aggregate data ใน agg tables, ใช้ indexes  |
|**Duplicate data**   |Deduplication ใน staging layer                |
|**ไม่รู้ว่าข้อมูลมาจากไหน**|Data lineage tracking (load_timestamp columns)|

### 8.2 ปัญหาทางธุรกิจ

|Business Question         |Solution                                 |
|--------------------------|-----------------------------------------|
|“เพลงไหนกำลังมาแรง?”        |`agg_weekly_top_songs` + trend indicators|
|“Artist ไหนกำลังโตเร็ว?”     |`agg_artist_performance` + momentum_score|
|“Country ไหนมีรสนิยมคล้ายกัน?”|Country comparison dashboard             |
|“เมื่อไหร่ควรปล่อยเพลง?”      |Time series analysis จาก fact table      |

-----

## 📈 9. การแสดงความเข้าใจในโครงสร้าง

### 9.1 Data Architecture Concepts ที่แสดงให้เห็น

#### **Concept 1: Zone-Based Architecture (Medallion Architecture)**

```
Raw Zone (Bronze) → Staging Zone (Silver) → Curated Zone (Gold)
```

- **Raw**: เก็บข้อมูลดิบแบบ as-is, immutable
- **Staging**: ทำ cleaning, validation, normalization
- **Curated**: สร้าง business-ready datasets

**แสดงความเข้าใจ**: การแยก zones ช่วยให้ pipeline มี clear separation of concerns

#### **Concept 2: Dimensional Modeling**

- ใช้ **Star Schema** (fact table + dimension tables)
- **Fact**: measurements/events (chart positions)
- **Dimensions**: descriptive attributes (songs, artists, dates, countries)

**แสดงความเข้าใจ**: Schema design ที่เหมาะสำหรับ analytics queries

#### **Concept 3: Slowly Changing Dimensions (SCD)**

- Type 2 SCD สำหรับ `dim_artist`, `dim_song`
- Track historical changes (effective_date, end_date, is_current)

**แสดงความเข้าใจ**: จัดการข้อมูลที่เปลี่ยนแปลงตามเวลา

#### **Concept 4: Data Quality & Validation**

- Schema validation
- Business rule validation
- Audit columns (load_timestamp)

**แสดงความเข้าใจ**: Data quality เป็นส่วนสำคัญของ pipeline

#### **Concept 5: Incremental Loading**

- ไม่ load ข้อมูลทั้งหมดใหม่ทุกครั้ง
- เช็ค `max(chart_date)` แล้ว load เฉพาะวันใหม่

**แสดงความเข้าใจ**: Efficiency และ scalability

#### **Concept 6: Aggregation Layer**

- Pre-compute metrics ใน `agg_*` tables
- ลด query time สำหรับ common requests

**แสดงความเข้าใจ**: Performance optimization

### 9.2 ระดับความเข้าใจที่แสดงออก

|ระดับ            |หัวข้อ                |แสดงได้อย่างไร                                        |
|----------------|--------------------|----------------------------------------------------|
|**Basic**       |Data storage        |ใช้ database แทน CSV files                           |
|**Intermediate**|Pipeline design     |แยก zones, ใช้ SQL joins, aggregations               |
|**Advanced**    |Dimensional modeling|Star schema, SCD, incremental loading               |
|**Expert**      |Production-ready    |Data quality, logging, error handling, documentation|

**Project นี้ target ระดับ Intermediate-Advanced** เพื่อให้เหมาะกับระดับการเรียน

-----

## 🚀 10. แผนการดำเนินงาน (4 สัปดาห์)

### Week 1: Setup & Foundation (7 วัน)

- ✅ Day 1-2: Project setup
  - Create Git repository
  - Setup Python environment
  - Install dependencies
- ✅ Day 3-4: Data collection
  - Download Spotify charts (1-2 เดือนย้อนหลัง)
  - Explore data structure
  - Document data schema
- ✅ Day 5-7: Database design
  - Design staging schema
  - Design curated schema (star schema)
  - Write CREATE TABLE statements
  - Setup DuckDB/PostgreSQL

### Week 2: ETL Development (7 วัน)

- ✅ Day 8-10: Raw → Staging pipeline
  - Write ingestion script (CSV → staging)
  - Implement data validation
  - Handle duplicates
- ✅ Day 11-14: Staging → Curated pipeline
  - Create dimensions (date, song, artist, country)
  - Load fact table
  - Implement incremental loading
  - Create aggregation tables

### Week 3: Analytics & Dashboard (7 วัน)

- ✅ Day 15-17: Data analysis
  - Write SQL queries for common questions
  - Test data quality
  - Fix any pipeline bugs
- ✅ Day 18-21: Dashboard development
  - Build Streamlit app
  - Create visualizations:
    - Top songs/artists over time
    - Country comparisons
    - Genre trends
  - Add filters and interactivity

### Week 4: Polish & Presentation (7 วัน)

- ✅ Day 22-24: Documentation
  - Write comprehensive README
  - Code comments
  - Architecture diagrams
  - Data dictionary
- ✅ Day 25-27: Presentation prep
  - Create slides
  - Prepare demo
  - Practice presentation
- ✅ Day 28: Buffer day (for unexpected issues)

-----

## 📋 11. Deliverables Checklist

### 11.1 Code Deliverables

- [ ] `ingest_raw_data.py` - Ingestion script
- [ ] `etl_staging.py` - Raw → Staging ETL
- [ ] `etl_curated.py` - Staging → Curated ETL
- [ ] `data_quality_checks.py` - Validation functions
- [ ] `dashboard.py` - Streamlit dashboard
- [ ] `schema/staging_schema.sql` - Staging DDL
- [ ] `schema/curated_schema.sql` - Curated DDL
- [ ] `requirements.txt` - Python dependencies
- [ ] `.gitignore` - Ignore unnecessary files

### 11.2 Documentation Deliverables

- [ ] `README.md` - Project overview, setup instructions
- [ ] `ARCHITECTURE.md` - Detailed architecture documentation
- [ ] `DATA_DICTIONARY.md` - Schema documentation
- [ ] Architecture diagram (PNG/PDF)
- [ ] Data flow diagram

### 11.3 Presentation Deliverables

- [ ] Presentation slides (PPTX/PDF)
- [ ] Demo video (optional)
- [ ] Screenshots of dashboard

-----

## 🎨 12. Creative Elements (ทำให้โปรเจคไม่จำเจ)

### 12.1 Unique Analysis Ideas

1. **“Music Culture Similarity Map”**
- หา countries ที่มีรสนิยมเพลงคล้ายกัน
- ใช้ Jaccard similarity หรือ cosine similarity
- แสดงเป็น heatmap
1. **“Breakout Artist Detector”**
- Identify artists ที่กำลัง momentum เพิ่มขึ้นเร็ว
- Calculate “velocity” metric: change in avg_rank per week
1. **“Chart Longevity Analysis”**
- วิเคราะห์ว่าเพลงอยู่ในชาร์ตได้นานแค่ไหน
- Survival analysis curves
1. **“Weekend vs Weekday Preferences”**
- เปรียบเทียบเพลงยอดนิยมช่วงวันธรรมดา vs วันหยุด

### 12.2 Dashboard Creative Elements

- 🎵 **Animated Charts**: แสดงการเปลี่ยนแปลงตามเวลา (racing bar chart)
- 🌍 **Interactive Map**: คลิกประเทศดู top songs ในประเทศนั้น
- 🎨 **Color Coding**: ใช้สีแสดง genre หรือ mood
- 📊 **KPI Cards**: แสดง key metrics (total songs tracked, countries covered)

-----

## ⚠️ 13. Risks & Mitigation

|Risk                       |Impact|Mitigation                               |
|---------------------------|------|-----------------------------------------|
|**ดาวน์โหลดข้อมูลไม่เสร็จ**     |High  |เริ่มเก็บข้อมูลตั้งแต่เนิ่นๆ, มี backup dataset     |
|**Database performance ช้า**|Medium|ใช้ DuckDB, สร้าง indexes, pre-aggregate   |
|**Code bugs ในวันสุดท้าย**    |High  |ทดสอบตั้งแต่เนิ่นๆ, มี version control         |
|**Streamlit ทำไม่ทัน**        |Medium|เตรียม backup viz (matplotlib plots)      |
|**Git conflicts**          |Low   |Work on feature branches, merge carefully|

-----

## 📚 14. Learning Outcomes

เมื่อเสร็จโปรเจคนี้ คุณจะได้เรียนรู้:

### Technical Skills

- ✅ Data pipeline development (ETL/ELT)
- ✅ Database design (normalization, star schema)
- ✅ SQL (DDL, DML, aggregations, joins)
- ✅ Python (pandas, sqlalchemy, data manipulation)
- ✅ Data quality & validation
- ✅ Git version control

### Conceptual Understanding

- ✅ Data architecture patterns (zone-based, dimensional modeling)
- ✅ Data warehousing concepts
- ✅ Incremental loading strategies
- ✅ Trade-offs (normalization vs performance)
- ✅ Scalability considerations

### Soft Skills

- ✅ Problem decomposition
- ✅ Documentation
- ✅ Technical presentation
- ✅ Time management

-----

## 🎓 15. Grading Criteria Alignment

ตาม rubric ของอาจารย์ที่บอกว่า “คะแนนจะขึ้นอยู่กับความสามารถในการเลือกใช้เครื่องมือต่างๆได้อย่างเหมาะสมกับ project”

โปรเจคนี้จะได้คะแนนดีเพราะ:

### ✅ Appropriate Tool Selection

- ใช้ **zones architecture** แทนการทำทุกอย่างใน 1 ที่
- ใช้ **database** แทน CSV files
- ใช้ **dimensional model** แทน flat tables
- ใช้ **validation layer** แทนปล่อยให้ dirty data ผ่าน

### ✅ Demonstrates Understanding

- แสดงความเข้าใจใน **data lifecycle**
- แสดงการใช้ **best practices** (logging, error handling, documentation)
- มี **clear separation of concerns**

### ✅ Practical & Implementable

- ไม่ซับซ้อนเกินไป (ไม่ใช่ distributed system)
- ใช้เครื่องมือที่หาได้ฟรี (Python, DuckDB, Git)
- สามารถทำเสร็จใน 4 สัปดาห์

### ✅ Creative & Interesting

- Dataset น่าสนใจ (เพลง)
- Analysis มี business value
- Dashboard มี storytelling

-----

## 📞 16. Success Criteria

โปรเจคนี้จะถือว่าสำเร็จเมื่อ:

### Minimum Viable Product (MVP)

- ✅ สามารถ ingest data จาก CSV ได้
- ✅ มี staging และ curated zones
- ✅ มี dimensional model (star schema)
- ✅ มี dashboard แสดงข้อมูลได้
- ✅ Code อยู่บน Git
- ✅ มี README และ documentation

### Stretch Goals (ถ้าทำได้จะได้คะแนนเพิ่ม)

- 🌟 ใช้ dbt สำหรับ transformations
- 🌟 ใช้ Great Expectations สำหรับ data quality
- 🌟 ใช้ Airflow สำหรับ orchestration
- 🌟 มี advanced analytics (similarity, prediction)
- 🌟 Deploy dashboard online (Streamlit Cloud)

-----

## 📝 17. Next Steps

หลังจากอ่าน proposal นี้แล้ว:

1. **ตัดสินใจ Technology Stack**
- PostgreSQL หรือ DuckDB?
- dbt หรือ SQL scripts?
- Great Expectations หรือ custom validation?
1. **เริ่มเก็บข้อมูล**
- ไปที่ <https://charts.spotify.com/>
- เลือกประเทศที่สนใจ (5-10 ประเทศ)
- Download CSV ย้อนหลัง 1-2 เดือน
1. **Setup Environment**
- Create Git repo
- Setup Python venv
- Install dependencies
1. **เริ่มเขียนโค้ด**
- เริ่มจาก ingestion script (simple ที่สุด)
- Test กับข้อมูลจริง
- Iterate และ improve

-----

## 🎯 Summary

**Spotify Music Trends Analytics Pipeline** เป็นโปรเจคที่:

- ✅ เหมาะสมกับวิชา Data Architecture
- ✅ แสดงความเข้าใจใน core concepts (zones, dimensional modeling, data quality)
- ✅ ใช้เครื่องมือที่เหมาะสม (Python, database, Git)
- ✅ มีความคิดสร้างสรรค์ (music analytics, interesting insights)
- ✅ ไม่ยากเกินไปแต่ไม่ง่ายเกินไป
- ✅ ทำเสร็จได้ใน 4 สัปดาห์
- ✅ เป็น portfolio piece ที่ดี

**ขอให้โปรเจคสำเร็จครับ! 🎵🚀**