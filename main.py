import json
import pandas as pd
import plotly.express as px
import streamlit as st
from google import genai
from google.genai import types

# 페이지 기본 설정
st.set_page_config(
    page_title="AI 음악 감정 & 분위기 분석기",
    page_icon="🎵",
    layout="wide",
)

# 전체 글씨체 변경 (나눔손글씨 펜 / Nanum Pen Script 폰트)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gaegu&display=swap');
    
html, body, [class*="css"], div, span, h1, h2, h3, h4, h5, h6, p, label, input, button {
        font-family: "Gaegu", sans-serif;
        font-size: 20px; /* 손글씨 폰트 특성에 맞춰 기본 크기를 조금 키웠습니다 */
    }

    h1 { font-size: 42px !important; }
    h2 { font-size: 36px !important; }
    h3 { font-size: 30px !important; }
    
    /* 주요 테마 키워드 전용 커스텀 스타일 (글씨 크기 축소) */
    .keyword-card {
        background-color: #F0F4F8;
        border-radius: 8px;
        padding: 8px 12px;
        text-align: center;
        margin-bottom: 8px;
    }
    .keyword-label {
        font-size: 14px !important;
        color: #666666;
        margin-bottom: 2px;
    }
    .keyword-value {
        font-size: 18px !important;
        font-weight: bold;
        color: #1E293B;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎵 AI 기반 노래 가사 감정 & 분위기 분석기")
st.caption(
    "노래 제목과 가수를 입력하면 AI가 가사 속에 담긴 감정 비율, 분위기, 컬러 팔레트를 분석해 드립니다."
)

# Streamlit Secrets에서 API 키 가져오기
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = None

# 입력 폼
col1, col2 = st.columns(2)
with col1:
    song_title = st.text_input("노래 제목", placeholder="예: 봄날")
with col2:
    artist = st.text_input("가수 이름", placeholder="예: 방탄소년단")

btn_analyze = st.button("🎧 음악 감정 분석하기", use_container_width=True)

if btn_analyze:
    if not api_key:
        st.error(
            "Streamlit Secrets에 'GEMINI_API_KEY'가 설정되어 있지 않습니다. 설정 후 다시 시도해 주세요!"
        )
    elif not song_title or not artist:
        st.warning("노래 제목과 가수 이름을 모두 입력해 주세요.")
    else:
        with st.spinner("AI가 노래 가사를 분석하고 정서를 시각화하는 중입니다... 🎼"):
            try:
                # Gemini Client 생성
                client = genai.Client(api_key=api_key)

                # 프롬프트 구성 (JSON 형식으로 응답 받기)
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

                # API 호출 (최신 Gemini 3.8 Flash 모델 사용)
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                    ),
                )

                # JSON 파싱
                data = json.loads(response.text)

                st.success("분석이 완료되었습니다! 🎉")
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
                        <div style="background-color: {hex_code}; padding: 25px; border-radius: 12px; text-align: center; color: white; font-weight: bold;">
                            대표 분위기 컬러<br><br>{color_name}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.divider()

                # 📊 2. 가사 감정 비율 시각화 (세로 막대 그래프)
                st.subheader("📊 감정 구성 비율 (Emotion Analysis)")
                df_emotions = pd.DataFrame(data.get("emotions", []))

                if not df_emotions.empty:
                    col_chart, col_data = st.columns([2, 1])
                    with col_chart:
                        # Plotly 세로 막대 그래프
                        fig = px.bar(
                            df_emotions,
                            x="emotion",
                            y="ratio",
                            text="ratio",
                            color="emotion",
                            labels={"emotion": "감정 요소", "ratio": "비율 (%)"},
                        )
                        fig.update_traces(
                            texttemplate="%{text}%",
                            textposition="outside",
                            marker_line_color="rgb(8,48,107)",
                            marker_line_width=1.5,
                        )
                        fig.update_layout(
                            showlegend=False,
                            height=350,
                            xaxis_title=None,
                            yaxis_title="비율 (%)",
                            font=dict(family="Pretendard, sans-serif"),
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

                # 🔑 3. 주요 가사 테마 키워드
                st.subheader("🔑 가사 속 주요 테마 키워드 Top 5")
                keywords = data.get("keywords", [])
                if keywords:
                    kw_cols = st.columns(len(keywords))
                    for idx, kw in enumerate(keywords):
                        with kw_cols[idx]:
                            st.metric(
                                label=f"Keyword {idx+1}", value=f"# {kw}"
                            )

            except Exception as e:
                st.error(f"분석 중 오류가 발생했습니다: {e}")

import time
import google.generativeai as genai

# 에러 발생 시 재시도하는 예시 함수
def call_gemini_with_retry(model, prompt, retries=3, delay=5):
    for i in range(retries):
        try:
            response = model.generate_content(prompt)
            return response
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                print(f"서버에 요청이 몰려 잠시 대기 중... ({i+1}/{retries})")
                time.sleep(delay)  # delay초 동안 대기 후 재시도
            else:
                raise e
    raise Exception("여러 번 시도했지만 서버 응답을 받지 못했어 🥺")
