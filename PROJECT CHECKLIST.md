# SPOTIFY MUSIC TRENDS ANALYTICS PIPELINE

## Project Implementation Checklist

-----

## 📅 TIMELINE: 4 สัปดาห์ก่อนสอบ (2 May)

-----

## WEEK 1: SETUP & FOUNDATION (วันที่ 1-7)

### Day 1-2: Project Setup ✅

- [ ] Create GitHub repository
  - [ ] Initialize with README.md
  - [ ] Add .gitignore (Python template)
  - [ ] Create branch: `develop`
- [ ] Setup local environment
  
  ```bash
  mkdir spotify-pipeline
  cd spotify-pipeline
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```
- [ ] Create project structure
  
  ```bash
  mkdir -p data/raw data/staging logs schema notebooks dashboard
  touch config.py database.py data_quality.py
  touch ingest_raw_data.py etl_staging_to_curated.py main.py
  ```
- [ ] Install dependencies
  
  ```bash
  pip install pandas duckdb sqlalchemy streamlit plotly
  pip freeze > requirements.txt
  ```
- [ ] First Git commit
  
  ```bash
  git add .
  git commit -m "Initial project setup"
  git push origin develop
  ```

**Deliverable**: Project structure ready, Git repo initialized

-----

### Day 3-4: Data Collection 📊

- [ ] Research Spotify Charts
  - [ ] Visit <https://charts.spotify.com/>
  - [ ] Understand chart types (Top 200, Viral 50)
  - [ ] Check available countries
- [ ] Select countries (เลือก 5-10 ประเทศ)
  - [ ] Thailand (TH)
  - [ ] United States (US)
  - [ ] United Kingdom (GB)
  - [ ] Japan (JP)
  - [ ] South Korea (KR)
  - [ ] Add more…
- [ ] Download data (ย้อนหลัง 1-2 เดือน)
  - [ ] Download CSV files
  - [ ] Organize by date: `data/raw/2024-04-01/spotify_top200_TH.csv`
  - [ ] Document CSV structure in README
- [ ] Explore data
  - [ ] Open in Excel/pandas
  - [ ] Check columns: rank, song name, artist, streams, etc.
  - [ ] Note any data quality issues
  - [ ] Create `notebooks/data_exploration.ipynb`

**Deliverable**: 30-60 CSV files in `data/raw/`, initial data documentation

-----

### Day 5-7: Database Design 🗄️

- [ ] Choose database
  - [ ] **DuckDB** (recommended, easy setup) ✅
  - [ ] OR PostgreSQL (if you want more practice)
- [ ] Setup database
  
  ```bash
  # If DuckDB (no setup needed, just use it)
  # If PostgreSQL:
  # brew install postgresql (Mac)
  # sudo apt install postgresql (Linux)
  # Download from postgresql.org (Windows)
  ```
- [ ] Create schemas
  - [ ] Run `schema_staging.sql`
    
    ```bash
    duckdb data/spotify_analytics.duckdb < schema/staging_schema.sql
    ```
  - [ ] Run `schema_curated.sql`
    
    ```bash
    duckdb data/spotify_analytics.duckdb < schema/curated_schema.sql
    ```
  - [ ] Verify tables created
    
    ```sql
    SHOW TABLES;
    DESCRIBE staging_chart_entries;
    ```
- [ ] Test connection
  - [ ] Write simple Python script to connect
  - [ ] Insert test row
  - [ ] Query it back
- [ ] Document schema
  - [ ] Create `DATA_DICTIONARY.md`
  - [ ] Describe each table and column

**Deliverable**: Database ready with all tables created

-----

## WEEK 2: ETL DEVELOPMENT (วันที่ 8-14)

### Day 8-10: Raw → Staging Pipeline 🔄

- [ ] Implement `ingest_raw_data.py`
  - [ ] Write CSV reader function
  - [ ] Add data cleaning logic
    - [ ] Handle missing values
    - [ ] Convert data types
    - [ ] Standardize column names
  - [ ] Add validation
    - [ ] Check nulls in required columns
    - [ ] Validate rank range (1-200)
    - [ ] Check date formats
- [ ] Implement `data_quality.py`
  - [ ] Write null check function
  - [ ] Write duplicate check function
  - [ ] Write range validation function
  - [ ] Log issues to `staging_data_quality_log`
- [ ] Test ingestion
  - [ ] Run on 1 CSV file first
  - [ ] Check data loaded correctly
  - [ ] Verify data quality checks work
  - [ ] Run on all CSV files
- [ ] Add error handling
  - [ ] Try-except blocks
  - [ ] Logging to `logs/pipeline.log`
  - [ ] Rollback on failure

**Deliverable**: Working raw → staging pipeline, 1000+ rows in staging_chart_entries

-----

### Day 11-14: Staging → Curated Pipeline ⚙️

- [ ] Implement `etl_staging_to_curated.py`
- [ ] Populate `dim_date`
  - [ ] Generate date range (2024-01-01 to 2024-12-31)
  - [ ] Calculate all date attributes
  - [ ] Insert to table
  - [ ] Verify: `SELECT COUNT(*) FROM dim_date;`
- [ ] Populate `dim_country`
  - [ ] Create reference data for your countries
  - [ ] Add region, continent info
  - [ ] Insert to table
- [ ] Populate `dim_song`
  - [ ] Extract unique songs from staging
  - [ ] Handle SCD Type 2 (for now, just is_current=TRUE)
  - [ ] Insert to table
  - [ ] Verify: `SELECT COUNT(*) FROM dim_song;`
- [ ] Populate `dim_artist`
  - [ ] Extract unique artists from staging
  - [ ] Handle SCD Type 2
  - [ ] Insert to table
- [ ] Populate `fact_daily_chart_positions`
  - [ ] Join staging with all dimensions
  - [ ] Calculate derived metrics (days_on_chart, etc.)
  - [ ] Insert to fact table
  - [ ] Check for duplicates
  - [ ] Verify: `SELECT COUNT(*) FROM fact_daily_chart_positions;`
- [ ] Implement incremental loading
  - [ ] Check `MAX(chart_date)` in fact table
  - [ ] Only load new dates
  - [ ] Test by adding new CSV files
- [ ] Test queries
  - [ ] Query top 10 songs
  - [ ] Query artist with most countries
  - [ ] Verify join performance

**Deliverable**: Working ETL, curated zone populated with star schema

-----

## WEEK 3: ANALYTICS & DASHBOARD (วันที่ 15-21)

### Day 15-17: Data Analysis 📈

- [ ] Write analytical queries
  - [ ] Top songs globally
  - [ ] Rising artists
  - [ ] Country comparisons
  - [ ] Genre trends (if data available)
- [ ] Create aggregation tables
  - [ ] `agg_weekly_top_songs`
  - [ ] `agg_artist_performance`
  - [ ] Calculate trend indicators
- [ ] Test data quality
  - [ ] Check for missing FKs
  - [ ] Verify aggregation accuracy
  - [ ] Compare with raw data
- [ ] Create Jupyter notebook
  - [ ] `notebooks/analysis.ipynb`
  - [ ] Exploratory analysis
  - [ ] Create visualizations
  - [ ] Document insights

**Deliverable**: SQL queries working, aggregation tables populated

-----

### Day 18-21: Dashboard Development 🖥️

- [ ] Setup Streamlit app
  
  ```bash
  mkdir dashboard
  touch dashboard/app.py
  ```
- [ ] Build dashboard components
  - [ ] **Page 1: Overview**
    - [ ] KPI cards (total songs, artists, countries)
    - [ ] Latest chart date
    - [ ] Data freshness indicator
  - [ ] **Page 2: Global Top Songs**
    - [ ] Table: Top 50 songs globally
    - [ ] Chart: Streams by song (bar chart)
    - [ ] Filters: date range, country
  - [ ] **Page 3: Artist Performance**
    - [ ] Search artist by name
    - [ ] Show artist metrics
    - [ ] Chart: Artist rank over time (line chart)
    - [ ] Chart: Countries where artist charted (map/bar)
  - [ ] **Page 4: Country Comparison**
    - [ ] Select 2-3 countries
    - [ ] Compare top songs
    - [ ] Jaccard similarity score
    - [ ] Venn diagram or heatmap
  - [ ] **Page 5: Trends**
    - [ ] Chart: Top songs over time (animated racing bar)
    - [ ] Chart: Genre popularity (if available)
    - [ ] Chart: Weekend vs weekday preferences
- [ ] Add interactivity
  - [ ] Date range picker
  - [ ] Country multi-select
  - [ ] Artist search box
  - [ ] Refresh button
- [ ] Style dashboard
  - [ ] Custom CSS (optional)
  - [ ] Consistent color scheme
  - [ ] Mobile-responsive layout
- [ ] Test dashboard
  - [ ] Run: `streamlit run dashboard/app.py`
  - [ ] Test all interactions
  - [ ] Check performance with large data

**Deliverable**: Working Streamlit dashboard with 4-5 pages

-----

## WEEK 4: POLISH & PRESENTATION (วันที่ 22-28)

### Day 22-24: Documentation 📝

- [ ] Write comprehensive `README.md`
  - [ ] Project overview
  - [ ] Problem statement
  - [ ] Architecture diagram (insert image)
  - [ ] Tech stack
  - [ ] Setup instructions
  - [ ] Usage guide
  - [ ] Sample queries
  - [ ] Screenshots of dashboard
- [ ] Write `ARCHITECTURE.md`
  - [ ] Detailed architecture explanation
  - [ ] Zone descriptions (Raw/Staging/Curated)
  - [ ] Data flow diagram
  - [ ] Design decisions and trade-offs
- [ ] Create `DATA_DICTIONARY.md`
  - [ ] All tables and columns documented
  - [ ] Data types and constraints
  - [ ] Example values
- [ ] Code documentation
  - [ ] Add docstrings to all functions
  - [ ] Add inline comments for complex logic
  - [ ] Clean up unused code
- [ ] Create architecture diagram
  - [ ] Use draw.io, Lucidchart, or similar
  - [ ] Show all zones and data flow
  - [ ] Export as PNG/PDF
  - [ ] Add to README

**Deliverable**: Complete documentation, architecture diagram

-----

### Day 25-27: Presentation Preparation 🎤

- [ ] Create presentation slides (15-20 slides)
  
  **Slide Outline:**
1. Title slide (project name, your name, date)
1. Problem statement & motivation
1. Pain points
1. Objectives
1. Data sources
1. Architecture overview (diagram)
1. Zone-based architecture explained
1. Dimensional model (star schema diagram)
1. Tech stack & justification
1. Data quality framework
1. ETL pipeline flow
1. Dashboard demo (screenshots)
1. Interesting insights/findings
1. Challenges & solutions
1. What I learned
1. Future improvements
1. Demo (live if possible)
1. Q&A
- [ ] Prepare demo
  - [ ] Test dashboard on presentation laptop
  - [ ] Prepare sample queries to run live
  - [ ] Have backup screenshots/video
- [ ] Practice presentation
  - [ ] Time yourself (aim for 10-15 minutes)
  - [ ] Practice explaining architecture
  - [ ] Prepare for Q&A (anticipate questions)

**Deliverable**: Presentation slides ready, demo tested

-----

### Day 28: Buffer Day & Final Review 🔍

- [ ] Final testing
  - [ ] Run full pipeline end-to-end
  - [ ] Verify all data loaded correctly
  - [ ] Test dashboard thoroughly
- [ ] Git cleanup
  - [ ] Merge develop to main
  - [ ] Tag release: `v1.0`
  - [ ] Verify GitHub repo looks good
  - [ ] Add screenshots to README
- [ ] Final checks
  - [ ] All requirements.txt dependencies listed
  - [ ] .gitignore working (no large files committed)
  - [ ] README has clear setup instructions
  - [ ] All SQL scripts runnable
- [ ] Backup everything
  - [ ] Export database to file
  - [ ] Backup project folder
  - [ ] Have USB drive ready for presentation day

**Deliverable**: Project complete and ready to present!

-----

## 🎯 SUCCESS CRITERIA CHECKLIST

### Minimum Requirements (ต้องมี)

- [x] Public dataset with regular updates ✅ (Spotify daily charts)
- [x] Data architecture/pipeline ✅ (3-zone architecture)
- [x] Appropriate tool usage ✅ (Python, SQL, DuckDB, Git)
- [x] Code on Git ✅
- [x] Documentation ✅

### Architecture Quality (คะแนนสูง)

- [ ] Clear zone separation (Raw/Staging/Curated)
- [ ] Dimensional modeling (star schema)
- [ ] Data quality framework
- [ ] Incremental loading
- [ ] Proper indexes and performance optimization

### Code Quality (คะแนนสูง)

- [ ] Clean, modular code
- [ ] Error handling
- [ ] Logging
- [ ] Comments and docstrings
- [ ] Git best practices (meaningful commits, branches)

### Creativity (คะแนนพิเศษ)

- [ ] Unique insights from data
- [ ] Beautiful dashboard
- [ ] Advanced analytics (optional)
- [ ] Thoughtful data storytelling

-----

## 📊 PROJECT METRICS TRACKER

Track your progress:

```
WEEK 1: Setup & Foundation
├─ [✅] Git repo created
├─ [✅] Data collected (50/50 CSV files)
├─ [✅] Database setup
└─ [✅] Schema created

WEEK 2: ETL Development
├─ [✅] Raw → Staging pipeline (1000+ rows loaded)
├─ [✅] Staging → Curated pipeline
├─ [✅] Fact table populated (5000+ rows)
└─ [✅] Incremental loading works

WEEK 3: Analytics & Dashboard
├─ [✅] Analytical queries written (10+ queries)
├─ [✅] Aggregation tables created
├─ [✅] Dashboard built (5 pages)
└─ [✅] Visualizations working

WEEK 4: Polish & Presentation
├─ [✅] Documentation complete
├─ [✅] Presentation slides ready
├─ [✅] Demo prepared
└─ [✅] Everything tested
```

-----

## 🚨 RISK MITIGATION

### High-Priority Risks

**Risk 1: Data download incomplete**

- **Mitigation**: Start downloading NOW (Day 1)
- **Backup**: Use Kaggle Spotify datasets if needed

**Risk 2: Database performance issues**

- **Mitigation**: Use DuckDB (fast for analytics)
- **Backup**: Add indexes, pre-aggregate data

**Risk 3: Pipeline bugs on demo day**

- **Mitigation**: Test early and often
- **Backup**: Have screenshots/video of working dashboard

**Risk 4: Time management**

- **Mitigation**: Follow weekly schedule strictly
- **Backup**: Cut scope if needed (reduce countries/dates)

-----

## 💡 PRO TIPS

1. **Git Commits**: Commit daily with meaningful messages
   
   ```bash
   git commit -m "feat: Add data quality validation to staging pipeline"
   ```
1. **Test Incrementally**: Don’t wait until end to test
- Test each function as you write it
- Test on small data first, then scale up
1. **Document As You Go**: Don’t leave documentation for last week
- Add README sections as you complete each week
- Write code comments while coding
1. **Ask for Help Early**: If stuck, ask classmates/instructor
- Don’t wait until it’s too late
- Debugging takes time
1. **Keep It Simple**: Don’t over-engineer
- Start with basic implementation
- Add complexity only if time permits
1. **Backup Regularly**:
- Push to Git daily
- Keep local backups
- Export database periodically

-----

## 📞 FINAL CHECKLIST (วันก่อนสอบ)

- [ ] Project runs without errors
- [ ] Dashboard loads and works
- [ ] Presentation slides ready
- [ ] Demo tested
- [ ] Git repo clean and up-to-date
- [ ] README has screenshots
- [ ] All deliverables uploaded/accessible
- [ ] Laptop charged
- [ ] Backup on USB drive
- [ ] Good night’s sleep 😴

-----

## 🎉 YOU’VE GOT THIS!

Remember:

- This is a **learning project**, not production code
- Focus on **understanding concepts**, not perfection
- **Document your learning journey**
- Have fun with the data! 🎵

Good luck! 🚀