import os
import random
import streamlit as st
from google import genai

# 페이지 기본 설정
st.set_page_config(page_title="AI Playlist", page_icon="🎧", layout="wide")

# ----------------------------------------------------
# 구름 바탕 폰트 & 블랙&실버 다크 테마 스타일 적용 🖤
# ----------------------------------------------------
font_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&display=swap');

/* 1. 사이드바 버그 텍스트(keyboard_double_...) 차단 */
[data-testid="stSidebarCollapseButton"] {
    color: transparent !important;
}
[data-testid="stSidebarCollapseButton"] button span {
    font-family: 'Material Symbols Outlined', 'Material Icons' !important;
    font-size: 0px !important;
}

/* 2. 전체 앱 배경 (딥 블랙) */
.stApp {
    background-color: #0e0e10;
    color: #e0e0e0;
}

/* 3. 사이드바 스타일링 */
[data-testid="stSidebar"] {
    background-color: #121214 !important;
    border-right: 1px solid #27272a !important;
}
[data-testid="stSidebar"] * {
    color: #e0e0e0 !important;
}

/* 4. 구름 바탕 폰트 글로벌 적용 */
html, body, [class*="css"], [class*="st-"], div, span, h1, h2, h3, h4, h5, h6, p, label, input, button {
    font-family: 'Gowun Batang', serif !important;
}

h1 { font-size: 42px !important; font-weight: 700; color: #ffffff !important; }
h2 { font-size: 32px !important; font-weight: 700; color: #d1d5db !important; }
h3 { font-size: 24px !important; font-weight: 700; color: #9ca3af !important; }
p, div, label { font-size: 18px; color: #c4c4c4; }

/* 5. 입력 컴포넌트(슬라이더, 멀티셀렉트 등) 다크 스타일 */
.stMultiSelect div[data-baseweb="select"] {
    background-color: #18181b !important;
    border: 1px solid #3f3f46 !important;
    color: #ffffff !important;
    border-radius: 8px !important;
}

/* 메인 버튼(맞춤 플레이리스트 생성하기) 글자 색상 검은색 설정 */
div.stButton > button {
    color: #000000 !important;
    font-weight: bold !important;
}

div.stButton > button p {
    color: #000000 !important;
    font-weight: bold !important;
}

/* 구분선 */
hr {
    border-color: #27272a !important;
}
</style>
"""
st.markdown(font_css, unsafe_allow_html=True)

# 1. API 키 설정 (Google GenAI 최신 SDK)
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

client = None
if api_key:
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        st.warning(f"Gemini API 연결 실패: {e}")

# 2. 메인 화면 구성
st.title("🎧 My Own Playlist 🖤")
st.caption("현재 내 기분, 날씨, 상황에 딱 맞는 맞춤형 트랙 리스트를 만들어줄게! 💙")

st.markdown("---")

# 3. 입력 세션: 슬라이더 & 선택버튼 (좌우 여백과 두 컬럼 사이의 간격을 대칭으로 예쁘게 맞춤!)
_, col_left, _, col_right, _ = st.columns([1, 4, 0.8, 4, 1])

with col_left:
    st.subheader("1. Condition Slider 🎚️")
    
    # 기분 슬라이더 (1~100)
    mood_score = st.slider(
        "Feeling",
        min_value=1,
        max_value=100,
        value=50,
        help="1에 가까울수록 차분/우울, 100에 가까울수록 극도로 신남!"
    )
    
    # 날씨 분위기 슬라이더 (1~100)
    weather_score = st.slider(
        "Weather",
        min_value=1,
        max_value=100,
        value=50,
        help="1: 비/어두움/쌀쌀함, 100: 화창함/맑음/무더움"
    )
    
    # 플레이리스트 길이 (분 단위)
    playlist_length = st.slider(
        "Length (minute)",
        min_value=15,
        max_value=180,
        value=60,
        step=15,
        format="%d분"
    )

with col_right:
    st.subheader("2. Situation & Genre 🎯")
    
    # 현재 상황 (단일 선택 버튼 라디오, 선택 안 함 가능)
    situation = st.radio(
        "Situation",
        options=["선택 안 함", "📖 Study/Work", "🏋️ Exercise/Walk", "☕ Break/Healing", "🌙 Sleep/Meditation", "🚗 Drive"],
        index=0
    )
    
    # 선호 장르 (복수 선택 가능 multiselect)
    selected_genres = st.multiselect(
        "Genre",
        options=["K-Pop", "Pop", "Lofi / Jazz", "Indie / Acoustic", "Hip-Hop / R&B", "EDM / Dance", "Classic / Instrumental", "Rock / Metal"],
        default=[]
    )

st.markdown("---")

# 4. 추천 생성 버튼 & 실행 로직 (버튼도 너무 길지 않게 가운데에 쏙 들어오도록 크기 조절!)
_, btn_col, _ = st.columns([2.5, 4, 2.5])
with btn_col:
    generate_clicked = st.button("✨ Make Playlist", type="primary", use_container_width=True)

if generate_clicked:
    
    #
