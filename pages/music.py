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

# 다크 테마 및 원형 텍스트 턴테이블 스타일 주입
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&display=swap');

    [data-testid="stSidebarCollapseButton"] {
        color: transparent !important;
    }
    [data-testid="stSidebarCollapseButton"] button span {
        font-family: 'Material Symbols Outlined', 'Material Icons' !important;
        font-size: 0px !important;
    }

    .stApp {
        background-color: #0e0e10;
        color: #e0e0e0;
    }

    [data-testid="stSidebar"] {
        background-color: #121214 !important;
        border-right: 1px solid #27272a !important;
    }
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }

    html, body, [class*="css"], div, span, h1, h2, h3, h4, h5, h6, p, label, input, button {
        font-family: 'Gowun Batang', serif !important;
    }

    h1 { font-size: 40px !important; font-weight: 700; color: #ffffff !important; }
    h2 { font-size: 30px !important; font-weight: 700; color: #d1d5db !important; }
    h3 { font-size: 24px !important; font-weight: 700; color: #9ca3af !important; }
    p, div, label { font-size: 18px; color: #c4c4c4; }

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
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
        position: relative;
    }

    .cd-disc {
        width: 170px;
        height: 170px;
        border-radius: 50%;
        background: radial-gradient(circle at center, transparent 30%, rgba(255, 255, 255, 0.05) 31%, transparent 32%), conic-gradient(from 0deg, #27272a, #52525b, #18181b, #a1a1aa, #27272a, #3f3f46, #18181b, #27272a);
        border: 2px solid #52525b;
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
        overflow: hidden;
    }

    .cd-text-svg {
        position: absolute;
        width: 100%;
        height: 100%;
    }

    .cd-curved-text {
        fill: #e4e4e7;
        font-size: 11px;
        font-weight: bold;
        letter-spacing: 2px;
        font-family: 'Gowun Batang', serif;
    }

    .cd-center-hole {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: #0e0e10;
        border: 4px solid #a1a1aa;
        position: absolute;
        z-index: 5;
    }

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
st.caption("노래 제목과 가수를 입력하면 AI가 가사 속에 담긴 감정 비율, 분위기, 컬러 팔레트를 분석해 드립니다.")

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = None

main_col_left, main_col_right = st.columns([7, 5])

with main_col_left:
    col1, col2 = st.columns(2)
    with col1:
        song_title = st.text_input("노래 제목", placeholder="예: BLUE")
    with col2:
        artist = st.text_input("가수 이름", placeholder="예: 윈터")

    btn_analyze = st.button("🎧 음악 감정 분석하기", use_container_width=True)

def render_turntable(display_text="MUSIC HUB * STREAMLIT *", is_fast=False):
    mode = "spin-fast" if is_fast else "spin-slow"
    html_code = f"""
    <div class="turntable-box">
        <div class="cd-disc {mode}">
            <svg class="cd-text-svg" viewBox="0 0 170 170">
              <path id="textPath" d="M 22,85 A 63,63 0 1,1 148,85 A 63,63 0 1,1 22,85" fill="none" />
              <text class="cd-curved-text">
                <textPath href="#textPath" startOffset="50%" text-anchor="middle">{display_text}  •  </textPath>
              </text>
            </svg>
            <div class="cd-center-hole"></div>
        </div>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

with main_col_right:
    current
