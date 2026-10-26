import os
import random
import time
import urllib.parse
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

/* 1. 사이드바 버그 텍스트 차단 */
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

/* 5. 입력 컴포넌트 다크 스타일 */
.stMultiSelect div[data-baseweb="select"] {
    background-color: #18181b !important;
    border: 1px solid #3f3f46 !important;
    color: #ffffff !important;
    border-radius: 8px !important;
}

/* 메인 버튼 글자 색상 검은색 설정 */
div.stButton > button {
    color: #000000 !important;
    font-weight: bold !important;
}

div.stButton > button p {
    color: #000000 !important;
    font-weight: bold !important;
}

/* 🎶 오디오 파형(Equalizer) 애니메이션 스타일 */
.equalizer-container {
    display: inline-flex;
    align-items: flex-end;
    gap: 4px;
    height: 32px;
    margin-left: 15px;
    vertical-align: middle;
}

.bar {
    width: 4px;
    background-color: #e0e0e0;
    border-radius: 2px;
    animation: bounce 1.2s infinite ease-in-out;
}

.bar:nth-child(1) { animation-delay: 0.1s; height: 15px; }
.bar:nth-child(2) { animation-delay: 0.4s; height: 28px; }
.bar:nth-child(3) { animation-delay: 0.2s; height: 20px; }
.bar:nth-child(4) { animation-delay: 0.5s; height: 32px; }
.bar:nth-child(5) { animation-delay: 0.3s; height: 18px; }

@keyframes bounce {
    0%, 100% { transform: scaleY(0.4); opacity: 0.4; }
    50% { transform: scaleY(1); opacity: 1; }
}

/* 🎧 곡별 작고 시크한 유튜브 버튼 스타일 */
.yt-listen-btn {
    background-color: #18181b;
    color: #ffffff !important;
    border: 1px solid #3f3f46;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 13px;
    font-weight: bold;
    text-decoration: none;
    display: inline-block;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4);
    transition: all 0.2s ease;
    font-family: 'Gowun Batang', serif !important;
}
.yt-listen-btn:hover {
    border-color: #c0c0c0;
    background-color: #27272a;
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

# 2. 메인 화면 구성 (제목 옆에 오디오 파형 애니메이션 추가 🖤)
title_html = """
<div style="display: flex; align-items: center; flex-wrap: wrap;">
    <h1 style="margin: 0; padding: 0;">🎧 My Own Playlist 🖤</h1>
    <div class="equalizer-container">
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
    </div>
</div>
"""
st.markdown(title_html, unsafe_allow_html=True)
st.caption("당신의 무드와 순간에 맞춘 커스텀 플레이리스트 💙")

st.markdown("---")

# 3. 입력 세션: 슬라이더 & 선택버튼
_, col_left, _, col_right, _ = st.columns([1, 4, 0.8, 4, 1])

with col_left:
    st.subheader("1. Condition Slider 🎚️")
    
    mood_score = st.slider(
        "Feeling",
        min_value=1,
        max_value=100,
        value=50,
        help="1에 가까울수록 Down, 100에 가까울수록 Up"
