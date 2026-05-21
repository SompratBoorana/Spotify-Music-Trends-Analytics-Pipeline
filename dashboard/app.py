import streamlit as st
import duckdb
import plotly.express as px
import os

st.set_page_config(page_title="Spotify Music Trends Analytics", layout="wide")
st.title("🎵 Spotify Music Trends Analytics Dashboard")
st.markdown("ระบบรายงานสถิติและเทรนด์เพลงยอดนิยมด้วย **Data Architecture Blueprint**")

# ล็อคเป้าหมายไปที่โฟลเดอร์ปัจจุบันแบบเป๊ะๆ (Absolute Path)
current_dir = os.path.abspath(os.getcwd())
db_path = os.path.join(current_dir, "spotify_analytics.duckdb")

# --- ส่วนเช็คความถูกต้อง ---
if not os.path.exists(db_path):
    st.error(f"❌ ระบบหาไฟล์ฐานข้อมูลไม่เจอครับ!")
    st.warning(f"มันกำลังพยายามหาที่โฟลเดอร์นี้: {db_path}")
else:
    try:
        # เชื่อมต่อฐานข้อมูลแบบ read_only=True
        conn = duckdb.connect(db_path, read_only=True)
        
        # ดึงข้อมูลภาพรวม (KPIs)
        total_songs = conn.execute("SELECT COUNT(*) FROM dim_song").fetchone()[0]
        total_artists = conn.execute("SELECT COUNT(*) FROM dim_artist").fetchone()[0]
        total_entries = conn.execute("SELECT COUNT(*) FROM fact_daily_chart_positions").fetchone()[0]
        
        col1, col2, col3 = st.columns(3)
        col1.metric("จำนวนเพลงทั้งหมดในระบบ", f"{total_songs:,} เพลง")
        col2.metric("จำนวนศิลปินที่ติดชาร์ต", f"{total_artists:,} คน")
        col3.metric("บันทึกอันดับรายวัน (Fact)", f"{total_entries:,} แถว")
        
        st.markdown("---")
        
        # ชาร์ตอันดับยอดฮิต (Top Chart)
        st.subheader("📊 อันดับเพลงที่ได้อันดับดีที่สุดสูงสุด (Top Songs Summary)")
        query = """
            SELECT ds.song_name, da.artist_name, MIN(f.rank) as peak_rank, COUNT(*) as days_on_chart
            FROM fact_daily_chart_positions f
            JOIN dim_song ds ON f.song_id = ds.song_id
            JOIN dim_artist da ON f.artist_id = da.artist_id
            GROUP BY ds.song_name, da.artist_name
            ORDER BY peak_rank ASC, days_on_chart DESC
            LIMIT 10
        """
        df_top = conn.execute(query).fetchdf()
        st.dataframe(df_top, use_container_width=True)
        
        # กราฟศิลปินที่มีเพลงติดชาร์ตมากที่สุด
        st.subheader("🎤 ศิลปินผู้ทรงอิทธิพลบนชาร์ต (Top Artists Chart)")
        query_artist = """
            SELECT da.artist_name, COUNT(*) as chart_appearances
            FROM fact_daily_chart_positions f
            JOIN dim_artist da ON f.artist_id = da.artist_id
            GROUP BY da.artist_name
            ORDER BY chart_appearances DESC
            LIMIT 10
        """
        df_artist = conn.execute(query_artist).fetchdf()
        fig = px.bar(df_artist, x='artist_name', y='chart_appearances', 
                     title="จำนวนครั้งที่เพลงของศิลปินติดอันดับชาร์ต (Top 10)",
                     labels={'artist_name': 'ชื่อศิลปิน', 'chart_appearances': 'จำนวนครั้งที่ปรากฏบนชาร์ต'},
                     color_discrete_sequence=['#1DB954'])
        st.plotly_chart(fig, use_container_width=True)
        
        conn.close()
        
    except Exception as e:
        st.error(f"❌ เจอไฟล์ฐานข้อมูลแล้ว แต่ตารางข้างในมีปัญหา: {e}")
        conn_debug = duckdb.connect(db_path, read_only=True)
        st.write("ตารางที่มีในระบบตอนนี้คือ:", conn_debug.execute("SHOW TABLES").fetchdf())
        conn_debug.close()