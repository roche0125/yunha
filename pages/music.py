import json
import time
import pandas as pd
import plotly.express as px
import streamlit as st
from google import genai
from google.genai import types

# 페이지 기본 설정
st.set_page_config(
    page_title="AI 음악 감정 & 분위기 분석기",
    page_icon="🖤",
    layout="wide",
)

# 구름 바탕 폰트 & 다크 테마 & 턴테이블 시디 CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&display=swap');

    /* 1. 사이드바 버튼 깨짐 현상 차단 */
    [data-testid="stSidebarCollapseButton"] {
        color: transparent !important;
    }
    [data-testid="stSidebarCollapseButton"] button span {
        font-family: 'Material Symbols Outlined', 'Material Icons' !important;
        font-size: 0px !important;
    }

    /* 2. 전체 앱 배경 */
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

    /* 4. 구름 바탕 폰트 */
    html, body, [class*="css"], div, span, h1, h2, h3, h4, h5, h6, p, label, input, button {
        font-family: 'Gowun Batang', serif !important;
    }

    h1 { font-size: 40px !important; font-weight: 700; color: #ffffff !important; }
    h2 { font-size: 30px !important; font-weight: 700; color: #d1d5db !important; }
    h3 { font-size: 24px !important; font-weight: 700; color: #9ca3af !important; }
    p, div, label { font-size: 18px; color: #c4c4c4; }

    /* 5. 텍스트 입력창 다크 스타일 */
    .stTextInput input {
        background-color: #18181b !important;
        color: #ffffff !important;
        border: 1px solid #3f3f46 !important;
        border-radius: 8px !important;
    }
    .stTextInput input:focus {
        border-color: #c0c0c0 !important;
        box-shadow: 0 0 8px rgba(192, 192, 192, 0.3) !important;
    }

    /* 6. 키워드 커스텀 카드 */
    .keyword-card {
        background: linear-gradient(145deg, #18181b, #121214);
        border: 1px solid #3f3f46;
        border-radius: 10px;
        padding: 12px 16px;
        text-align: center;
        margin-bottom: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    .keyword-label {
        font-size: 14px !important;
        color: #a1a1aa;
        margin-bottom: 4px;
    }
    .keyword-value {
        font-size: 20px !important;
        font-weight: bold;
        color: #ffffff;
    }

    /* 7. 정사각형 턴테이블 카드 박스 */
    .turntable-box {
        width: 100%;
        max-width: 220px;
        aspect-ratio: 1 / 1;
        margin: 0 auto;
        background: linear-gradient(145deg, #18181b, #0e0e10);
        border: 1px solid #3f3f46;
        border-radius: 20px;
        padding: 15px;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8), inset 0 1px 1px rgba(255, 255, 255, 0.1);
        position: relative;
    }

    /* 디테일이 강화된 CD / 바이닐 디자인 */
    .cd-disc {
        width: 170px;
        height: 170px;
        border-radius: 50%;
        background: 
            radial-gradient(circle at center, transparent 30%, rgba(255, 255, 255, 0.05) 31%, transparent 32%),
            conic-gradient(from 0deg, #27272a, #52525b, #18181b, #a1a1aa, #27272a, #3f3f46, #18181b, #27272a);
        border: 2px solid #52525b;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.9), 0 0 2px rgba(255, 255, 255, 0.3);
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
    }

    /* 회전을 명확하게 보여주는 상단 라벨 패턴 */
    .cd-label-bar {
        position: absolute;
        width: 100%;
        height: 38px;
        background: rgba(24, 24, 27, 0.85);
        border-top: 1px solid #71717a;
        border-bottom: 1px solid #71717a;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 12px;
        color: #e4e4e7;
        font-size: 11px;
        font-weight: bold;
        letter-spacing: 1px;
    }

    /* CD 중앙 구멍 */
    .cd-center-hole {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: #0e0e10;
        border: 4px solid #a1a1aa;
        box-shadow: inset 0 0 5px rgba(0,0,0,0.8);
        z-index: 5;
    }

    /* 회전 애니메이션 */
    .spin-slow {
        animation: rotateCD 12s linear infinite;
    }
    .spin-fast {
        animation: rotateCD 2s linear infinite;
    }

    @keyframes rotateCD {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    hr {
        border-color: #27272a !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🖤 음악 감정 & 분위기 분석기")
st.caption(
    "노래 제목과 가수를 입력하면 AI가 가사 속에 담긴 감정 비율, 분위기, 컬러 팔레트를 분석해 드립니다."
)

# Streamlit Secrets에서 API 키 가져오기
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = None

#
