import os
import random
import time
import urllib.parse
import streamlit as st
from google import genai

st.set_page_config(page_title="AI Playlist", page_icon="🎧", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&display=swap');

.stApp {
    background-color: #0e0e10;
    color: #e0e0e0;
}

html, body, [class*="css"], div, span, h1, h2, h3, p, label, button {
    font-family: 'Gowun Batang', serif !important;
}

h1 { color: #ffffff !important; }

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
}
.yt-listen-btn:hover {
    border-color: #c0c0c0;
    background-color: #27272a;
}
</style>
""", unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

st.markdown("<h1>🎧 My Own Playlist 🖤</h1>", unsafe_allow_html=True)
st.caption("당신의 무드와 순간에 맞춘 커스텀 플레이리스트 💙")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    mood_score = st.slider("Feeling (1: Down ~ 100: Up)", 1, 100, 50)
    weather_score = st.slider("Weather (1: Dark ~ 100: Sunny)", 1, 100, 50)
    playlist_length = st.slider("Length (minute)", 15, 180, 60, step=15)

with col2:
    situation = st.radio("Situation", ["선택 안 함", "📖 Study / Work", "🏋️ Exercise / Walk", "☕ Break / Healing", "🌙 Sleep / Meditation", "🚗 Drive"])
    selected_genres = st.multiselect("Genre", ["K-Pop", "Pop", "Lofi / Jazz", "Indie / Acoustic", "Hip-Hop / R&B", "EDM / Dance", "Classic / Instrumental", "Rock / Metal"])

st.markdown("---")

if st.button("✨ Make Playlist", type="primary", use_container_width=True):
    situation_str = situation if situation != "선택 안 함" else "특별한 제한 없음"
    genres_str = ", ".join(selected_genres) if selected_genres else "전 장르 자유"

    st.subheader("🎵 Playlist")

    if client:
        with st.spinner("Analyzing your vibe... 💙"):
            prompt = (
                f"다음 조건에 어울리는 음악 플레이리스트를 5곡 이상 리스트 형태로 추천해줘.\n"
                f"- 기분: {mood_score}/100, 날씨: {weather_score}/100\n"
                f"- 길이: {playlist_length}분, 상황: {situation_str}, 장르: {genres_str}\n"
                f"출력 형식 예시:\n1. **곡명** - 아티스트 (추천 이유)"
            )
            
            try:
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=prompt
                )
                st.success("Build Complete 🖤")
                
                for line in response.text.split("\n"):
                    line_str = line.strip()
                    if line_str and line_str[0].isdigit() and "." in line_str[:3]:
                        st.markdown(line_str, unsafe_allow_html=True)
                        parts = line_str.split("-")
                        if len(parts) >= 2:
                            song = parts[0].replace("*", "").split(".")[1].strip()
                            artist = parts[1].split("(")[0].replace("*", "").strip()
                            q = urllib.parse.quote(f"{artist} {song}")
                            url = f"https://www.youtube.com/results?search_query={q}"
                            st.markdown(f'<div style="margin-bottom: 10px;"><a href="{url}" target="_blank" class="yt-listen-btn">▶ Listen on YouTube</a></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(line_str)
            except Exception as e:
                st.error(f"오류가 발생했어요: {e}")
    else:
        st.info("💡 API 키가 없어 알고리즘으로 추천해줄게!")
        songs_db = [
            {"title": "Ditto", "artist": "NewJeans", "genre": "K-Pop"},
            {"title": "Night Dancer", "artist": "Imase", "genre": "Pop"},
            {"title": "Event Horizon", "artist": "Younha", "genre": "K-Pop"},
            {"title": "Lofi Rain Beats", "artist": "Chillhop", "genre": "Lofi / Jazz"}
        ]
        for i, s in enumerate(random.sample(songs_db, 3), 1):
            q = urllib.parse.quote(f"{s['artist']} {s['title']}")
            url = f"https://www.youtube.com/results?search_query={q}"
            st.markdown(f"**{i}. {s['title']}** - {s['artist']} `[{s['genre']}]`")
            st.markdown(f'<div style="margin-bottom: 10px;"><a href="{url}" target="_blank" class="yt-listen-btn">▶ Listen on YouTube</a></div>', unsafe_allow_html=True)
