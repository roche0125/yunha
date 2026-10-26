import json
import time
import pandas as pd
import plotly.express as px
import streamlit as st
from google import genai
from google.genai import types

# 페이지 기본 설정
st.set_page_config(
    page_title="Sound Palette",
    page_icon="🖤",
    layout="wide",
)

# 다크 테마 및 원형 턴테이블 스타일 주입
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

st.title("🖤 Sound Palette")
st.caption("가사 속 감정 레이어와 바이브, 컬러 톤을 분석해드립니다.")

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = None

main_col_left, main_col_right = st.columns([7, 5])

with main_col_left:
    col1, col2 = st.columns(2)
    with col1:
        song_title = st.text_input("Title", placeholder="예: BLUE")
    with col2:
        artist = st.text_input("Singer", placeholder="예: Winter")

    btn_analyze = st.button("🎧 Decode Mood", use_container_width=True)

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
    current_label = f"{song_title} - {artist}" if (song_title and artist) else (song_title if song_title else "MUSIC HUB")
    if not btn_analyze:
        render_turntable(display_text=current_label, is_fast=False)

if btn_analyze:
    with main_col_right:
        active_label = f"{song_title} - {artist}" if (song_title and artist) else (song_title if song_title else "MUSIC HUB")
        render_turntable(display_text=active_label, is_fast=True)

    if not api_key:
        st.error("Streamlit Secrets에 'GEMINI_API_KEY'가 설정되어 있지 않습니다.")
    elif not song_title or not artist:
        st.warning("노래 제목과 가수 이름을 모두 입력해 주세요.")
    else:
        with st.spinner("Analyzing lyrical emotions and rendering the visual palette... 🖤"):
            try:
                client = genai.Client(api_key=api_key)
                
                prompt = (
                    "다음 노래의 가사와 전체적인 곡 분위기를 정밀 분석해서 반드시 지정된 JSON 규격으로만 응답해줘.\n\n"
                    f"노래 제목: {song_title}\n"
                    f"가수: {artist}\n\n"
                    "응답할 JSON 구조:\n"
                    "{\n"
                    '    "theme_summary": "한 줄 요약",\n'
                    '    "emotions": [\n'
                    '        {"emotion": "기쁨", "ratio": 50},\n'
                    '        {"emotion": "슬픔", "ratio": 50}\n'
                    "    ],\n"
                    '    "keywords": ["키워드1", "키워드2", "키워드3", "키워드4", "키워드5"],\n'
                    '    "vibe_color": "대표 색상 이름",\n'
                    '    "color_hex": "#1E3A8A",\n'
                    '    "vibe_description": "설명"\n'
                    "}"
                )

                # 503 과부하 에러 대비 자동 재시도(Retry) 로직 추가 🖤
                max_retries = 3
                response = None
                for attempt in range(max_retries):
                    try:
                        response = client.models.generate_content(
                            model="gemini-3.8-flash",
                            contents=prompt,
                            config=types.GenerateContentConfig(response_mime_type="application/json"),
                        )
                        break
                    except Exception as api_err:
                        if "503" in str(api_err) or "UNAVAILABLE" in str(api_err):
                            if attempt < max_retries - 1:
                                time.sleep(2) # 2초 대기 후 재시도
                                continue
                        raise api_err

                data = json.loads(response.text)

                st.success("Decode Complete 🎧")
                st.divider()

                st.subheader("📌 Subject & Theme")
                col_info, col_color = st.columns([3, 1])
                with col_info:
                    st.info(f"**Summary:** {data.get('theme_summary', '')}")
                    st.write(f"**💡 Vibe:** {data.get('vibe_description', '')}")
                with col_color:
                    hex_code = data.get("color_hex", "#3182CE")
                    color_name = data.get("vibe_color", "Color")
                    st.markdown(
                        f'<div style="background-color: {hex_code}; padding: 20px; border-radius: 12px; text-align: center; color: white; font-weight: bold;">대표 컬러<br><br>{color_name}</div>',
                        unsafe_allow_html=True,
                    )

                st.divider()
                st.subheader("📊 Emotion Ratio")
                df_emotions = pd.DataFrame(data.get("emotions", []))
                if not df_emotions.empty:
                    fig = px.bar(df_emotions, x="emotion", y="ratio", text="ratio")
                    fig.update_traces(marker_color=data.get("color_hex", "#3182CE"), textposition="outside")
                    fig.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#e0e0e0"))
                    st.plotly_chart(fig, use_container_width=True)

                st.divider()
                st.subheader("🔑 Keywords Top 5")
                keywords = data.get("keywords", [])
                if keywords:
                    kw_cols = st.columns(len(keywords))
                    for idx, kw in enumerate(keywords):
                        with kw_cols[idx]:
                            st.markdown(f'<div class="keyword-card"><div class="keyword-label">Keyword {idx+1}</div><div class="keyword-value"># {kw}</div></div>', unsafe_allow_html=True)

            except Exception as e:
                err_msg = str(e)
                if "503" in err_msg or "UNAVAILABLE" in err_msg:
                    st.warning("⏳ **Server Busy:** 현재 AI 서버가 붐비고 있어! 잠시 후(10~20초 뒤)에 다시 버튼을 눌러줘 🖤✨")
                else:
                    st.error(f"⚠️ 오류가 발생했습니다: {e}")
