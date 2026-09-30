import os
import random
import pandas as pd
import streamlit as st
from google import genai

# Page Configuration
st.set_page_config(
    page_title="Music Hub & AI Playlist",
    page_icon="🎵",
    layout="wide"
)

# ----------------------------------------------------
# 1. API 키 설정 (Google GenAI 최신 SDK)
# ----------------------------------------------------
# secrets.toml 이나 환경변수에서 API 키를 불러와!
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

client = None
if api_key:
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        st.warning(f"Gemini API 연결 실패: {e}")

# ----------------------------------------------------
# 2. 사이드바 다중 페이지 네비게이션
# ----------------------------------------------------
st.sidebar.title("🎵 Music Hub")
page = st.sidebar.radio(
    "페이지를 선택해줘!",
    ["📊 음악 데이터 분석", "🎧 AI 맞춤 플레이리스트 Generator"]
)

# ====================================================
# PAGE 1: 기존 음악 데이터 분석 웹앱
# ====================================================
if page == "📊 음악 데이터 분석":
    st.title("📊 음악 데이터 분석 Dashboard")
    st.write("기존에 만든 음악 분석 페이지야! 여기에 데이터 시각화 차트나 분석 도구를 연결하면 돼 💙")
    
    # 예시 요약 수치
    col1, col2, col3 = st.columns(3)
    col1.metric("총 재생 트랙", "1,240곡", "+12%")
    col2.metric("가장 많이 들은 장르", "K-Pop / Lofi", "")
    col3.metric("평균 듣는 시간", "3.5시간/일", "+0.5h")
    
    st.info("💡 오른쪽 사이드바에서 '🎧 AI 맞춤 플레이리스트 Generator'로 이동해봐!")

# ====================================================
# PAGE 2: 신규 AI 맞춤 플레이리스트 Generator
# ====================================================
elif page == "🎧 AI 맞춤 플레이리스트 Generator":
    st.title("🎧 나만의 AI 맞춤 플레이리스트 💙")
    st.caption("현재 내 기분, 날씨, 상황에 딱 맞는 맞춤형 트랙 리스트를 만들어줄게!")

    st.markdown("---")

    # ------------------------------------------------
    # 입력 세션: 슬라이더 & 선택버튼
    # ------------------------------------------------
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("1. 조건 슬라이더 🎚️")
        
        # 기분 슬라이더 (1~100)
        mood_score = st.slider(
            "현재 기분은 어때?",
            min_value=1,
            max_value=100,
            value=50,
            help="1에 가까울수록 울적/우울, 100에 가까울수록 극도로 신남!"
        )
        
        # 날씨 분위기 슬라이더 (1~100)
        weather_score = st.slider(
            "오늘 날씨 분위기는?",
            min_value=1,
            max_value=100,
            value=50,
            help="1: 비/어두움/쌀쌀함, 100: 화창함/맑음/무더움"
        )
        
        # 플레이리스트 길이 (분 단위)
        playlist_length = st.slider(
            "플레이리스트 길이 (분)",
            min_value=15,
            max_value=180,
            value=60,
            step=15,
            format="%d분"
        )

    with col_right:
        st.subheader("2. 상황 & 선호 장르 🎯")
        
        # 현재 상황 (단일 선택 버튼 라디오, 선택 안 함 가능)
        situation = st.radio(
            "현재 어떤 상황이야? (선택 안 해도 돼!)",
            options=["선택 안 함", "📖 공부/작업", "🏋️ 운동/산책", "☕ 휴식/힐링", "🌙 수면/명상", "🚗 드라이브"],
            index=0
        )
        
        # 선호 장르 (복수 선택 가능 multiselect)
        selected_genres = st.multiselect(
            "선호하는 장르를 골라줘! (복수 선택 가능)",
            options=["K-Pop", "Pop", "Lofi / Jazz", "Indie / Acoustic", "Hip-Hop / R&B", "EDM / Dance", "Classic / Instrumental", "Rock / Metal"],
            default=[]
        )

    st.markdown("---")

    # ------------------------------------------------
    # 추천 생성 버튼 & 실행 로직
    # ------------------------------------------------
    if st.button("✨ 맞춤 플레이리스트 생성하기", type="primary", use_container_width=True):
        
        # 조건 정리
        mood_desc = "평범함"
        if mood_score < 35: mood_desc = "차분하고 약간 차분/우울함"
        elif mood_score > 65: mood_desc = "매우 신나고 활기참"

        weather_desc = "보통 날씨"
        if weather_score < 35: weather_desc = "흐리거나 비가 오고 쌀쌀한 날씨"
        elif weather_score > 65: weather_desc = "맑고 화창하며 에너지가 넘치는 날씨"

        situation_str = situation if situation != "선택 안 함" else "특별한 제한 없음"
        genres_str = ", ".join(selected_genres) if selected_genres else "전 장르 자유"

        st.subheader("🎵 추천 플레이리스트 결과")

        # 1. Gemini AI를 활용한 고도화 추천
        if client:
            with st.spinner("Gemini가 너의 기분과 상황을 분석해서 최고의 곡들을 선곡 중이야... 💙"):
                prompt = f"""
                다음 조건에 완벽히 어울리는 음악 플레이리스트를 작성해줘.
                
                [사용자 조건]
                - 기분 상태: {mood_score}/100 ({mood_desc})
                - 날씨 분위기: {weather_score}/100 ({weather_desc})
                - 총 플레이리스트 길이: 약 {playlist_length}분 (대략 {max(3, playlist_length // 3)}~{max(5, playlist_length // 3 + 2)}곡 구성)
                - 현재 상황: {situation_str}
                - 선호 장르: {genres_str}
                
                [출력 형식]
                1. 추천 플레이리스트 제목 (감성적이고 센스 있는 제목)
                2. 선곡 이유 요약 (다정한 말투로 2~3줄)
                3. 곡 리스트 (번호, 곡명, 아티스트, 추천 이유 한 줄)
                """
                
                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt
                    )
                    st.success("너만을 위한 플레이리스트 완성! 💙")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"AI 추천 중 오류가 발생했어: {e}")
        
        # 2. API 키가 없거나 실패 시 Rule-based 알고리즘 대체 생성
        else:
            st.info("💡 Gemini API 키가 설정되지 않아 규칙 기반(알고리즘)으로 추천해줄게!")
            
            songs_db = [
                {"title": "Ditto", "artist": "NewJeans", "genre": "K-Pop", "vibe": "차분함"},
                {"title": "Night Dancer", "artist": "Imase", "genre": "Pop", "vibe": "신남"},
                {"title": "Event Horizon", "artist": "Younha", "genre": "K-Pop", "vibe": "벅참"},
                {"title": "Lofi Rain Beats", "artist": "Chillhop", "genre": "Lofi / Jazz", "vibe": "휴식"},
                {"title": "Super Shy", "artist": "NewJeans", "genre": "K-Pop", "vibe": "신남"},
                {"title": "Weightless", "artist": "Marconi Union", "genre": "Classic / Instrumental", "vibe": "수면"},
            ]
            
            # 간단 필터링 알고리즘
            recommended = random.sample(songs_db, min(len(songs_db), 4))
            
            st.write(f"### 🎧 [알고리즘 추천] {situation_str} 맞춤 리스트 ({playlist_length}분 분량)")
            for i, song in enumerate(recommended, 1):
                st.write(f"**{i}. {song['title']}** - {song['artist']} `[{song['genre']}]`")
