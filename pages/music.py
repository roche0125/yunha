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

# 구름 바탕 폰트 & 다크 테마 & 턴테이블 회전 애니메이션 CSS
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

    /* 7. 턴테이블 & 회전 CD CSS */
    .turntable-container {
        display: flex;
        justify-content: center;
        align-items: center;
        background: #121214;
        border: 1px solid #27272a;
        border-radius: 16px;
        padding: 20px;
        box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.8), 0 8px 25px rgba(0, 0, 0, 0.5);
        height: 100%;
        min-height: 220px;
    }

    .vinyl-record {
        width: 170px;
        height: 170px;
        border-radius: 50%;
        background: radial-gradient(circle, #27272a 18%, #09090b 20%, #18181b 40%, #000000 70%, #27272a 100%);
        border: 4px solid #3f3f46;
        box-shadow: 0 0 15px rgba(192, 192, 192, 0.15);
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
    }

    /* CD 중앙 홀/라벨 */
    .vinyl-center {
        width: 55px;
        height: 55px;
        border-radius: 50%;
        background: linear-gradient(135deg, #c0c0c0, #52525b);
        border: 3px solid #000;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #000;
        font-weight: bold;
        font-size: 12px;
    }

    /* 회전 애니메이션 클래스 */
    .spinning {
        animation: spin 3초 linear infinite;
    }

    @keyframes spin {
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

# 메인 상단 레이아웃 (왼쪽 50%: 입력 폼 / 오른쪽 50%: 턴테이블 시디)
main_col_left, main_col_right = st.columns([1, 1])

with main_col_left:
    col1, col2 = st.columns(2)
    with col1:
        song_title = st.text_input("노래 제목", placeholder="예: BLUE")
    with col2:
        artist = st.text_input("가수 이름", placeholder="예: 윈터")

    btn_analyze = st.button("🎧 음악 감정 분석하기", use_container_width=True)

# 턴테이블 CD 플레이어 컴포넌트 렌더링 함수
def render_turntable(is_spinning=False):
    spin_class = "spinning" if is_spinning else ""
    st.markdown(
        f"""
        <div class="turntable-container">
            <div class="vinyl-record {spin_class}">
                <div class="vinyl-center">MUSIC</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with main_col_right:
    # 기본 정지 상태의 턴테이블
    if not btn_analyze:
        render_turntable(is_spinning=False)

if btn_analyze:
    # 버튼이 눌렸을 때는 빙글빙글 회전하는 CD 보여주기
    with main_col_right:
        render_turntable(is_spinning=True)

    if not api_key:
        st.error(
            "Streamlit Secrets에 'GEMINI_API_KEY'가 설정되어 있지 않습니다. 설정 후 다시 시도해 주세요!"
        )
    elif not song_title or not artist:
        st.warning("노래 제목과 가수 이름을 모두 입력해 주세요.")
    else:
        with st.spinner(
            "AI가 노래 가사를 분석하고 정서를 시각화하는 중입니다... 🎼"
        ):
            try:
                client = genai.Client(api_key=api_key)

                prompt = f"""
                다음 노래의 가사와 전체적인 곡 분위기를 정밀 분석해서 반드시 지정된 JSON 규격으로만 응답해줘.
                
                노래 제목: {song_title}
                가수: {artist}
                
                응답할 JSON 구조:
                {{
                    "theme_summary": "이 노래의 전체적인 핵심 주제 및 서사 한 줄 요약",
                    "emotions": [
                        {{"emotion": "기쁨/희망", "ratio": 10}},
                        {{"emotion": "슬픔/그리움", "ratio": 50}},
                        {{"emotion": "불안/외로움", "ratio": 30}},
                        {{"emotion": "사랑/설렘", "ratio": 10}}
                    ],
                    "keywords": ["키워드1", "키워드2", "키워드3", "키워드4", "키워드5"],
                    "vibe_color": "이 곡에 어울리는 대표 색상 이름 (예: 새벽녘의 딥블루)",
                    "color_hex": "#1E3A8A",
                    "vibe_description": "곡의 분위기와 추천 감상 상황 설명"
                }}
                
                주의사항:
                - emotions의 ratio(비율) 합은 반드시 100이 되도록 설정할 것.
                - emotions에는 곡의 특성에 맞는 감정 3~5개를 자유롭게 뽑을 것.
                - color_hex는 Hex 컬러 코드 형태로 제공할 것.
                """

                response = None
                models_to_try = [
                    "gemini-3.8-flash",
                    "gemini-2.5-flash",
                    "gemini-1.5-flash",
                ]
                last_exception = None

                for model_name in models_to_try:
                    for attempt in range(3):
                        try:
                            response = client.models.generate_content(
                                model=model_name,
                                contents=prompt,
                                config=types.GenerateContentConfig(
                                    response_mime_type="application/json",
                                ),
                            )
                            break
                        except Exception as err:
                            last_exception = err
                            if (
                                "503" in str(err)
                                or "UNAVAILABLE" in str(err)
                                or "high demand" in str(err)
                            ):
                                time.sleep(2)
                                continue
                            else:
                                raise err
                    if response is not None:
                        break

                if response is None and last_exception is not None:
                    raise last_exception

                data = json.loads(response.text)

                st.success("분석이 완료되었습니다 🎧")
                st.divider()

                # 📌 1. 핵심 주제 요약 및 분위기 컬러 카드
                st.subheader("📌 곡 핵심 주제 & 이미지 테마")

                col_info, col_color = st.columns([3, 1])
                with col_info:
                    st.info(
                        f"**주제 요약:** {data.get('theme_summary', '정보 없음')}"
                    )
                    st.write(
                        f"**💡 어울리는 감상 분위기:** {data.get('vibe_description', '')}"
                    )
                with col_color:
                    hex_code = data.get("color_hex", "#3182CE")
                    color_name = data.get("vibe_color", "추천 컬러")
                    st.markdown(
                        f"""
                        <div style="background-color: {hex_code}; padding: 25px; border-radius: 12px; text-align: center; color: white; font-weight: bold; font-size: 26px;">
                            대표 분위기 컬러<br><br>{color_name}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.divider()

                # 📊 2. 가사 감정 비율 시각화
                st.subheader("📊 감정 구성 비율 (Emotion Analysis)")
                df_emotions = pd.DataFrame(data.get("emotions", []))

                if not df_emotions.empty:
                    hex_code = data.get("color_hex", "#3182CE")
                    
                    col_chart, col_data = st.columns([2, 1])
                    with col_chart:
                        fig = px.bar(
                            df_emotions,
                            x="emotion",
                            y="ratio",
                            text="ratio",
                            labels={"emotion": "감정 요소", "ratio": "비율 (%)"},
                        )
                        fig.update_traces(
                            texttemplate="%{text}%",
                            textposition="outside",
                            marker_color=hex_code,
                            marker_line_color="rgb(8,48,107)",
                            marker_line_width=1.5,
                        )
                        fig.update_layout(
                            showlegend=False,
                            height=350,
                            xaxis_title=None,
                            yaxis_title="비율 (%)",
                            font=dict(family="Gowun Batang, serif", size=18),
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    with col_data:
                        st.dataframe(
                            df_emotions.rename(
                                columns={
                                    "emotion": "감정 요소",
                                    "ratio": "비율(%)",
                                }
                            ),
                            use_container_width=True,
                        )

                st.divider()

                # 🔑 3. 주요 가사 테마 키워드 Top 5
                st.subheader("🔑 가사 속 주요 테마 키워드 Top 5")
                keywords = data.get("keywords", [])
                if keywords:
                    kw_cols = st.columns(len(keywords))
                    for idx, kw in enumerate(keywords):
                        with kw_cols[idx]:
                            st.markdown(
                                f"""
                                <div class="keyword-card">
                                    <div class="keyword-label">Keyword {idx+1}</div>
                                    <div class="keyword-value"># {kw}</div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

            except Exception as e:
                if (
                    "503" in str(e)
                    or "UNAVAILABLE" in str(e)
                    or "high demand" in str(e)
                ):
                    st.warning(
                        "⏳ 현재 AI 서버 사용량이 많아 응답이 지연되고 있습니다. 잠시 후 다시 시도해 주세요! 💙"
                    )
                else:
                    st.error(
                        "⚠️ 분석 도중 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해 주세요!"
                    )
