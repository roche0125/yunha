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
    )
    
    weather_score = st.slider(
        "Weather",
        min_value=1,
        max_value=100,
        value=50,
        help="1: Dark / Cloudy, 100: Bright / Sunny"
    )
    
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
    
    situation = st.radio(
        "Situation",
        options=["선택 안 함", "📖 Study / Work", "🏋️ Exercise / Walk", "☕ Break / Healing", "🌙 Sleep / Meditation", "🚗 Drive"],
        index=0
    )
    
    selected_genres = st.multiselect(
        "Genre",
        options=["K-Pop", "Pop", "Lofi / Jazz", "Indie / Acoustic", "Hip-Hop / R&B", "EDM / Dance", "Classic / Instrumental", "Rock / Metal"],
        default=[]
    )

st.markdown("---")

# 4. 추천 생성 버튼 & 실행 로직
_, btn_col, _ = st.columns([2.5, 4, 2.5])
with btn_col:
    generate_clicked = st.button("✨ Make Playlist", type="primary", use_container_width=True)

if generate_clicked:
    mood_desc = "평범함"
    if mood_score < 35: 
        mood_desc = "차분하고 약간 차분/우울함"
    elif mood_score > 65: 
        mood_desc = "매우 신나고 활기참"

    weather_desc = "보통 날씨"
    if weather_score < 35: 
        weather_desc = "흐리거나 비가 오고 쌀쌀한 날씨"
    elif weather_score > 65: 
        weather_desc = "맑고 화창하며 에너지가 넘치는 날씨"

    situation_str = situation if situation != "선택 안 함" else "특별한 제한 없음"
    genres_str = ", ".join(selected_genres) if selected_genres else "전 장르 자유"

    st.subheader("🎵 Playlist")

    if client:
        with st.spinner("Analyzing your vibe and calibrating the ultimate tracklist... 💙"):
            prompt = f"""
            다음 조건에 완벽히 어울리는 음악 플레이리스트를 작성해줘. 반드시 JSON이나 줄글 형식이 아니라 깔끔한 리스트 형태로 작성해줘.
            
            [사용자 조건]
            - 기분 상태: {mood_score}/100 ({mood_desc})
            - 날씨 분위기: {weather_score}/100 ({weather_desc})
            - 총 플레이리스트 길이: 약 {playlist_length}분
            - 현재 상황: {situation_str}
            - 선호 장르: {genres_str}
            
            [출력 형식]
            ### 💿 [플레이리스트 제목]
            - 선곡 이유 요약 (2~3줄)
            
            그리고 각 곡은 아래 형식으로 정확히 5곡 이상 작성해줘:
            1. **곡명** - 아티스트 (추천 이유 한 줄)
            """
            
            max_retries = 3
            response = None
            for attempt in range(max_retries):
                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt
                    )
                    break
                except Exception as api_err:
                    err_str = str(api_err)
                    if "503" in err_str or "UNAVAILABLE" in err_str or "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                        if attempt < max_retries - 1:
                            time.sleep(3)
                            continue
                    raise api_err

            st.success("Build Complete 🖤")
            
            # AI 응답 텍스트를 파싱해서 각 곡마다 유튜브 버튼을 달아주기 위한 처리
            response_text = response.text
            lines = response_text.split("\n")
            
            for line in lines:
                if line.strip().startswith(tuple(f"{i}." for i in range(1, 20))):
                    clean_line = line.strip()
                    st.markdown(clean_line, unsafe_allow_html=True)
                    
                    parts = clean_line.split("-")
                    if len(parts) >= 2:
                        song_part = parts[0].replace("*", "").replace("1.", "").replace("2.", "").replace("3.", "").replace("4.", "").replace("5.", "").replace("6.", "").strip()
                        artist_part = parts[1].split("(")[0].replace("*", "").strip()
                        query_str = urllib.parse.quote(f"{artist_part} {song_part}")
                        yt_url = f"https://www.youtube.com/results?search_query={query_str}"
                        
                        st.markdown(f'<div style="margin-bottom: 10px;"><a href="{yt_url}" target="_blank" class="yt-listen-btn">▶ Listen on YouTube</a></div>', unsafe_allow_html=True)
                else:
                    st.markdown(line)
            
    else:
        st.info("💡 Gemini API 키가 설정되지 않아 규칙 기반(알고리즘)으로 추천해줄게!")
        
        songs_db = [
            {"title": "Ditto", "artist": "NewJeans", "genre": "K-Pop"},
            {"title": "Night Dancer", "artist": "Imase", "genre": "Pop"},
            {"title": "Event Horizon", "artist": "Younha", "genre": "K-Pop"},
            {"title": "Lofi Rain Beats", "artist": "Chillhop", "genre": "Lofi / Jazz"},
            {"title": "Super Shy", "artist": "NewJeans", "genre": "K-Pop"},
            {"title": "Weightless", "artist": "Marconi Union", "genre": "Classic / Instrumental"},
        ]
        
        recommended = random.sample(songs_db, min(len(songs_db), 4))
        
        st.write(f"### 🎧 [알고리즘 추천] {situation_str} 맞춤 리스트 ({playlist_length}분 분량)")
        for i, song in enumerate(recommended, 1):
            query_str = urllib.parse.quote(f"{song['artist']} {song['title']}")
            yt_url = f"https://www.youtube.com/results?search_query={query_str}"
            st.markdown(f"**{i}. {song['title']}** - {song['artist']} `[{song['genre']}]`")
            st.markdown(f'<div style="margin-bottom: 10px;"><a href="{yt_url}" target="_blank" class="yt-listen-btn">▶ Listen on YouTube</a></div>', unsafe_allow_html=True)
