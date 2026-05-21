# SPOTIFY MUSIC TRENDS ANALYTICS PIPELINE

## Presentation Slides Content (15 Slides)

-----

## SLIDE 1: TITLE SLIDE

### Layout: Center-aligned

```
SPOTIFY MUSIC TRENDS
ANALYTICS PIPELINE

Building an End-to-End Data Architecture
for Music Chart Analysis

🎵 🎵 🎵

นายสมปราถน์ บูรณะ (Somprat Boorana)
รหัสนิสิต: 66102010189

รายวิชา: DE242 Data Architecture
ภาคเรียนที่ 2/2568

วันที่นำเสนอ: 2 May 2025
```

**Visual Elements**:

- Background: Gradient with music theme (optional)
- Spotify logo (small, bottom corner)
- Music note icons 🎵

-----

## SLIDE 2: PROJECT OVERVIEW & MOTIVATION

### หัวข้อ: “Why This Project?”

**Content:**

### 🎯 Project Goal

สร้าง End-to-End Data Pipeline สำหรับวิเคราะห์เทรนด์เพลงจาก Spotify Charts

### 🎵 Why Music Analytics?

- Spotify มีผู้ใช้ 500M+ คนทั่วโลก
- Music charts เปลี่ยนแปลงทุกวัน → Data updates daily
- เหมาะสำหรับเรียนรู้ Data Architecture concepts

### 📊 Business Value

- **Artists/Labels**: วางแผนการปล่อยเพลง
- **Playlist Curators**: ติดตามเพลงที่กำลังมาแรง
- **Market Analysts**: ศึกษาพฤติกรรมผู้บริโภค

**Visual Elements**:

- [รูป] Spotify interface screenshot
- [Icon] User icon with “500M users”
- [Chart] Mini line chart แสดงการเปลี่ยนแปลงของ charts

-----

## SLIDE 3: PROBLEM STATEMENT

### หัวข้อ: “Pain Points & Challenges”

**Content:**

### ⚠️ Current Problems

**1. Data Fragmentation (ข้อมูลกระจัดกระจาย)**

- Charts แยกเป็นไฟล์ CSV รายวัน/รายประเทศ
- ไม่มี unified view สำหรับวิเคราะห์

**2. Data Quality Issues**

- Missing values, duplicates, inconsistent formats
- ไม่มี validation framework

**3. No Historical Context**

- CSV เป็น snapshot → ไม่เห็นการเปลี่ยนแปลงตามเวลา
- ไม่สามารถติดตาม trends ได้

**4. Manual Process**

- ต้อง download และ merge data เอง
- Error-prone, time-consuming

**5. Not Analytics-Ready**

- Raw CSV ไม่เหมาะกับ complex queries
- ไม่มี pre-computed aggregations

**Visual Elements**:

- [Diagram] Before: Messy CSV files scattered
- [Icon] ⚠️ Warning icons next to each problem
- [Chart] Pain point severity (High/Medium/Low bars)

-----

## SLIDE 4: OBJECTIVES & SCOPE

### หัวข้อ: “What We’re Building”

**Content:**

### 🎯 Primary Objectives

✅ **Build Robust Data Pipeline**

- Ingest → Clean → Transform → Analyze

✅ **Demonstrate Data Architecture Concepts**

- 3-Zone Architecture (Bronze/Silver/Gold)
- Dimensional Modeling (Star Schema)
- Data Quality Framework

✅ **Generate Actionable Insights**

- Interactive dashboard
- Trend analysis & comparisons

### 📐 Project Scope

**In Scope:**

- Spotify Top 200 Charts (5-10 countries)
- 1-3 months of historical data
- Daily updates (manual trigger)

**Out of Scope:**

- Real-time streaming ❌
- ML/AI predictions ❌
- Cloud deployment ❌

**Visual Elements**:

- [Checklist] ✅ Objectives with checkmarks
- [Venn Diagram] In Scope vs Out of Scope
- [Timeline] Project duration: 4 weeks

-----

## SLIDE 5: DATA SOURCES

### หัวข้อ: “Where Does the Data Come From?”

**Content:**

### 📊 Primary Data Source

**Spotify Charts** (<https://charts.spotify.com/>)

- **Type**: Daily Top 200 songs per country
- **Update Frequency**: Daily
- **Format**: CSV export (manual download)
- **Countries**: TH, US, GB, JP, KR, + more

### 📋 Data Structure (Sample)

|Rank|Song Name|Artist|Streams  |URI              |
|----|---------|------|---------|-----------------|
|1   |เพลง A   |ศิลปิน X|1,234,567|spotify:track:xxx|
|2   |เพลง B   |ศิลปิน Y|987,654  |spotify:track:yyy|

### 📈 Data Volume

- **Files**: 50-100 CSV files
- **Records**: ~10,000+ chart entries
- **Time Range**: 1-3 months
- **Size**: ~50MB

**Visual Elements**:

- [Screenshot] Spotify Charts website
- [Table] Sample data preview (styled nicely)
- [Icon] Country flags for selected countries
- [Chart] Data volume bar chart

-----

## SLIDE 6: ARCHITECTURE OVERVIEW

### หัวข้อ: “System Architecture”

**Content:**

### 🏗️ High-Level Architecture

```
┌─────────────────┐
│  DATA SOURCES   │
│ Spotify Charts  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   RAW ZONE      │  ← Bronze Layer
│  (CSV Files)    │
└────────┬────────┘
         │ ETL
         ▼
┌─────────────────┐
│  STAGING ZONE   │  ← Silver Layer
│  (PostgreSQL/   │
│   DuckDB)       │
└────────┬────────┘
         │ Transform
         ▼
┌─────────────────┐
│  CURATED ZONE   │  ← Gold Layer
│  (Star Schema)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   DASHBOARD     │
│   (Streamlit)   │
└─────────────────┘
```

### 🔧 Technology Stack

- **Storage**: DuckDB / PostgreSQL
- **Processing**: Python (pandas, SQLAlchemy)
- **Orchestration**: Python scripts
- **Visualization**: Streamlit
- **Version Control**: Git/GitHub

**Visual Elements**:

- [Diagram] Architecture flow diagram (ใช้ diagram ข้างบนแต่สวยกว่า)
- [Icons] Tech stack logos (Python, DuckDB, Streamlit, Git)
- [Color coding] Bronze (brown), Silver (gray), Gold (yellow)

-----

## SLIDE 7: ZONE-BASED ARCHITECTURE

### หัวข้อ: “The 3-Zone Approach (Medallion Architecture)”

**Content:**

### 🥉 BRONZE: Raw Zone

**Purpose**: Store raw data as-is

- Format: CSV files
- No transformation
- Immutable (never modified)
- Timestamped folders: `raw/2024-04-01/`

### 🥈 SILVER: Staging Zone

**Purpose**: Clean and validate

- Format: Database tables
- Data cleaning & deduplication
- Schema enforcement
- Data quality checks

### 🥇 GOLD: Curated Zone

**Purpose**: Analytics-ready data

- Format: Star Schema (dimensional model)
- Business logic applied
- Pre-computed aggregations
- Fast query performance

### ✨ Benefits

✅ Clear separation of concerns
✅ Data quality at each layer
✅ Easy to debug and maintain
✅ Scalable and production-ready

**Visual Elements**:

- [Diagram] 3 medals (Bronze, Silver, Gold) with descriptions
- [Flow] Data transformation at each zone
- [Icons] File → Database → Star icon

-----

## SLIDE 8: DIMENSIONAL MODEL (STAR SCHEMA)

### หัวข้อ: “Data Model Design”

**Content:**

### ⭐ Star Schema Structure

```
        dim_date        dim_song
             ↓              ↓
             └──────┬───────┘
                    │
         ┌──────────▼──────────┐
         │                     │
    dim_country → FACT TABLE ← dim_artist
                  (Daily Chart
                   Positions)
```

### 📊 Fact Table

**fact_daily_chart_positions**

- Metrics: rank, streams, days_on_chart
- Foreign Keys to all dimensions

### 📦 Dimension Tables

1. **dim_date**: Date attributes (year, month, week, is_weekend)
1. **dim_song**: Song details (name, URI, release_date)
1. **dim_artist**: Artist info (name, genres, first_appearance)
1. **dim_country**: Country details (code, name, region)

### 📈 Aggregate Tables

- `agg_weekly_top_songs`
- `agg_artist_performance`
- `agg_country_trends`

**Visual Elements**:

- [Diagram] Star schema visual (center fact, 4 dimensions around it)
- [Table icons] Small table previews showing key columns
- [Color coding] Fact table = orange, Dimensions = blue

-----

## SLIDE 9: ETL PIPELINE FLOW

### หัวข้อ: “Data Processing Pipeline”

**Content:**

### 🔄 Pipeline Steps

**STEP 1: Ingestion (Raw → Staging)**

```
CSV Files → Validation → Staging Tables
```

- Read CSV files
- Data type conversion
- Handle missing values
- Deduplicate entries
- Log data quality issues

**STEP 2: Transformation (Staging → Curated)**

```
Staging → Dimensions → Fact Table → Aggregations
```

- Extract unique songs/artists
- Populate dimension tables
- Join and load fact table
- Calculate derived metrics
- Create aggregations

**STEP 3: Incremental Loading**

- Check `MAX(chart_date)` in fact table
- Load only new dates
- Avoid reprocessing old data

**Visual Elements**:

- [Flowchart] Pipeline steps with arrows
- [Code snippet] Key Python function (prettified)
- [Progress bar] Step 1 → Step 2 → Step 3
- [Icon] ⚙️ for each processing step

-----

## SLIDE 10: DATA QUALITY FRAMEWORK

### หัวข้อ: “Ensuring Data Quality”

**Content:**

### ✅ Data Quality Checks

**1. Schema Validation**

- ✓ Correct data types
- ✓ Required columns present
- ✓ Valid formats (dates, URIs)

**2. Completeness Checks**

- ✓ No NULL values in critical fields
- ✓ < 5% missing data tolerance

**3. Uniqueness Checks**

- ✓ No duplicate chart entries
- ✓ Unique constraints enforced

**4. Range Validation**

- ✓ Rank: 1-200
- ✓ Streams: ≥ 0
- ✓ Dates: Valid date range

**5. Referential Integrity**

- ✓ All FKs have matching PKs
- ✓ No orphaned records

### 📊 Data Quality Metrics

|Metric      |Target|Actual|
|------------|------|------|
|Completeness|95%   |98% ✅ |
|Accuracy    |100%  |99% ✅ |
|Duplicates  |0%    |0.1% ✅|

**Visual Elements**:

- [Checklist] ✓ Checks with green checkmarks
- [Dashboard] Data quality metrics (gauges/bars)
- [Icon] 🛡️ Shield for data protection

-----

## SLIDE 11: TECH STACK & JUSTIFICATION

### หัวข้อ: “Technology Choices”

**Content:**

### 🔧 Tools Used

|Component          |Tool           |Why?                                                                      |
|-------------------|---------------|--------------------------------------------------------------------------|
|**Storage**        |DuckDB         |• Lightweight, no server needed<br>• Fast analytics (OLAP)<br>• Easy setup|
|**ETL**            |Python + Pandas|• Industry standard<br>• Rich ecosystem<br>• Easy integration             |
|**Transform**      |SQL Scripts    |• Simple and transparent<br>• SQL is universal<br>• Easy to debug         |
|**Viz**            |Streamlit      |• Pure Python<br>• Fast prototyping<br>• Interactive widgets              |
|**Version Control**|Git/GitHub     |• Best practice<br>• Collaboration ready<br>• Portfolio piece             |

### 🏆 Alternative Considered

- PostgreSQL vs DuckDB → **DuckDB** (easier)
- dbt vs SQL scripts → **SQL scripts** (simpler)
- Airflow vs Python scripts → **Python scripts** (less overhead)

**Visual Elements**:

- [Table] Comparison table (nicely formatted)
- [Logos] Tool logos in a row
- [Checkmark] ✅ Selected tool highlighted

-----

## SLIDE 12: DASHBOARD & VISUALIZATIONS

### หัวข้อ: “Interactive Analytics Dashboard”

**Content:**

### 📊 Dashboard Features

**Page 1: Global Overview**

- KPIs: Total songs tracked, countries, latest update
- Top 10 songs globally (bar chart)

**Page 2: Artist Performance**

- Search artist by name
- Rank trend over time (line chart)
- Countries appeared (map/bar chart)

**Page 3: Country Comparison**

- Select 2-3 countries
- Compare top songs (Venn diagram)
- Similarity score

**Page 4: Trends Analysis**

- Top songs over time (animated chart)
- Rising vs falling artists
- Weekend vs weekday patterns

### 🎨 Design Principles

- Clean, minimal UI
- Responsive filters
- Fast load times
- Mobile-friendly

**Visual Elements**:

- [Screenshot] 4 dashboard page screenshots (2x2 grid)
- [GIF] Animated chart demo (if possible)
- [Icon] 📊 📈 📉 Chart icons

-----

## SLIDE 13: KEY INSIGHTS & FINDINGS

### หัวข้อ: “What We Discovered”

**Content:**

### 🔍 Interesting Insights

**1. Global Music Taste Similarity**

- US & UK have 65% song overlap
- Thailand & South Korea: 30% overlap
- → Geographic proximity ≠ music taste similarity

**2. Chart Velocity**

- Average song stays in Top 10: 12 days
- Viral hits: 3-5 days before exit
- Classics: 30+ days consistent

**3. Artist Momentum**

- Top rising artist: [Artist Name]
- Gained 50 ranks in 2 weeks
- Appeared in 8 countries

**4. Weekend Effect**

- Party songs ↑ 25% on weekends
- Ballads ↑ 15% on weekdays

### 📈 Data Quality Achievement

- 99.8% clean data
- 0% duplicates
- <1% missing values

**Visual Elements**:

- [Chart] Country similarity heatmap
- [Graph] Chart velocity distribution
- [Icon] 🔥 for hot trends, 📈 for rising

-----

## SLIDE 14: CHALLENGES & LEARNINGS

### หัวข้อ: “What I Learned”

**Content:**

### 🚧 Challenges Faced

**1. Data Consistency**

- **Problem**: Different countries use different date formats
- **Solution**: Standardize in staging layer

**2. Performance**

- **Problem**: Joins on fact table slow with 10K+ rows
- **Solution**: Added indexes, pre-aggregations

**3. Schema Evolution**

- **Problem**: Spotify changed CSV structure mid-project
- **Solution**: Flexible ingestion code, version handling

### 💡 Key Learnings

✅ **Technical Skills**

- Zone-based architecture is powerful
- Dimensional modeling speeds up queries
- Data quality is critical

✅ **Best Practices**

- Test early and often
- Document as you go
- Git commits save lives

✅ **Soft Skills**

- Time management matters
- Breaking down problems helps
- Ask for help when stuck

**Visual Elements**:

- [Before/After] Problem → Solution diagrams
- [Lightbulb] 💡 icon for learnings
- [Growth chart] Skills acquired graph

-----

## SLIDE 15: CONCLUSION & Q&A

### หัวข้อ: “Summary & Next Steps”

**Content:**

### ✅ What We Built

- End-to-end data pipeline for Spotify charts
- 3-zone architecture (Bronze → Silver → Gold)
- Star schema dimensional model
- Interactive dashboard with 4+ pages
- Data quality framework

### 📊 Deliverables

✅ Working pipeline code (Python)
✅ Database schema (SQL)
✅ Interactive dashboard (Streamlit)
✅ Complete documentation
✅ GitHub repository

### 🚀 Future Improvements

- Add more countries (20+ countries)
- Automate data download (web scraping)
- ML predictions (forecast chart positions)
- Real-time dashboard updates
- Cloud deployment (AWS/GCP)

### 🎓 Alignment with Course Objectives

- Demonstrated understanding of **Data Architecture**
- Applied appropriate **tools & technologies**
- Created **scalable & maintainable** solution
- Followed **best practices** (Git, documentation)

-----

### 🎵 Thank You!

**Questions?**

**Project Repository**: github.com/[username]/spotify-pipeline
**Contact**: [somprat.b@student.example.edu](mailto:somprat.b@student.example.edu)

```
นายสมปราถน์ บูรณะ (Somprat Boorana)
รหัสนิสิต: 66102010189
DE242 Data Architecture | ภาคเรียน 2/2568
```

**Visual Elements**:

- [Thank you graphic] Simple, elegant
- [QR code] Link to GitHub repo
- [Contact info] Email, GitHub handle

-----

## 📝 PRESENTATION NOTES

### Timing Guide (10-12 minutes total)

- Slide 1: 30 seconds (intro)
- Slides 2-4: 2 minutes (problem & objectives)
- Slides 5-6: 1.5 minutes (data & architecture)
- Slides 7-8: 2 minutes (technical details)
- Slides 9-11: 2 minutes (implementation)
- Slide 12: 1.5 minutes (demo)
- Slides 13-14: 1.5 minutes (insights & learnings)
- Slide 15: 1 minute (conclusion)

### Presentation Tips

1. **Slide 6 & 8**: Spend time here - this is core architecture
1. **Slide 12**: Have live dashboard ready to demo (or video backup)
1. **Slide 13**: Use specific numbers from your actual data
1. **Be ready for questions**:
- “Why DuckDB over PostgreSQL?”
- “How do you handle schema changes?”
- “What’s the data refresh frequency?”
- “Can this scale to 100+ countries?”

### Visual Design Recommendations

- **Color Scheme**:
  - Primary: Spotify Green (#1DB954)
  - Secondary: Black & White
  - Accent: Purple for data quality
- **Fonts**:
  - Headers: Montserrat Bold
  - Body: Open Sans
- **Charts**: Use consistent color palette
- **Icons**: Font Awesome or Flaticon

-----

## 🎨 SLIDE DESIGN TEMPLATE EXAMPLE

### For PowerPoint/Google Slides:

**Master Slide Layout:**

```
┌─────────────────────────────────────┐
│ [Header Area]                       │
│ Slide Title                         │
├─────────────────────────────────────┤
│ [Content Area - Left 60%]           │
│ • Bullet point 1                    │
│ • Bullet point 2                    │
│   - Sub point                       │
│                                     │
│ [Visual Area - Right 40%]           │
│ [Diagram/Chart/Image]               │
│                                     │
├─────────────────────────────────────┤
│ Footer: Name | Course | Slide #     │
└─────────────────────────────────────┘
```

### Quick PowerPoint Setup:

1. Open PowerPoint
1. Design → Slide Size → Widescreen (16:9)
1. Insert → Header & Footer → Add slide numbers
1. Use this content as bullet points
1. Add diagrams from draw.io or PowerPoint SmartArt
1. Add screenshots of your dashboard
1. Use animations sparingly (fade in/out only)

-----

## 💾 SAVE THIS FILE AS:

`spotify_pipeline_presentation_content.md`

Ready to convert to slides! 🚀