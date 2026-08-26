import streamlit as st
import pandas as pd
import random

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="365 성경 영어구문 암기",
    page_icon="📖",
    layout="centered"
)

# 2. 홈 화면 저장용 메타 태그 및 커스텀 CSS 설정
st.markdown("""
    <head>
        <meta name="apple-mobile-web-app-title" content="365 성경영어">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="application-name" content="365 성경영어">
    </head>
    <style>
    .card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        border-left: 6px solid #4A90E2;
    }
    .verse-ref {
        font-weight: bold;
        color: #4A90E2;
        font-size: 1.2rem;
        margin-bottom: 12px;
    }
    .english-text {
        font-size: 1.35rem;
        font-weight: 600;
        color: #2C3E50;
        margin-bottom: 15px;
        line-height: 1.6;
    }
    .korean-text {
        font-size: 1.1rem;
        color: #444444;
        margin-bottom: 15px;
        line-height: 1.5;
    }
    .grammar-point {
        background-color: #EBF5FB;
        padding: 12px 16px;
        border-radius: 8px;
        font-size: 0.95rem;
        color: #1B4F72;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 데이터 로드 함수
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data.csv")
        return df
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return None

df = load_data()

if df is not None:
    total_count = len(df)
    
    if 'current_idx' not in st.session_state:
        st.session_state.current_idx = 0

    st.title("📖 365 성경 영어구문 암기")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_day = st.slider("학습 일차 선택", 1, total_count, st.session_state.current_idx + 1)
        st.session_state.current_idx = selected_day - 1
    with col2:
        st.metric(label="진도율", value=f"{selected_day}/{total_count}")

    row = df.iloc[st.session_state.current_idx]
    
    day_num = row['일자']
    ref = row['출처']
    en_verse = row['NIV 영어 성경 구절']
    grammar = row['영어 구문 포인트']
    ko_verse = row['한글 번역']

    st.markdown(f"""
        <div class="card">
            <div class="verse-ref">Day {day_num} | {ref}</div>
            <div class="english-text">"{en_verse}"</div>
            <div class="korean-text">{ko_verse}</div>
            <div class="grammar-point">💡 <b>구문 포인트:</b> {grammar}</div>
        </div>
    """, unsafe_allow_html=True)

    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
    
    with btn_col1:
        if st.button("⬅️ 이전 구절", use_container_width=True):
            if st.session_state.current_idx > 0:
                st.session_state.current_idx -= 1
                st.rerun()
                
    with btn_col2:
        if st.button("🎲 랜덤 구절", use_container_width=True):
            st.session_state.current_idx = random.randint(0, total_count - 1)
            st.rerun()

    with btn_col3:
        if st.button("다음 구절 ➡️", use_container_width=True):
            if st.session_state.current_idx < total_count - 1:
                st.session_state.current_idx += 1
                st.rerun()
