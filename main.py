import streamlit as st

st.set_page_config(
    page_title="Music Hub",
    page_icon="🎵",
    layout="wide"
)

# 구름 바탕(Gowun Batang) 폰트 & 스타일 적용
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&display=swap');
    
    html, body, [class*="css"], div, span, h1, h2, h3, h4, h5, h6, p, label, input, button {
        font-family: 'Gowun Batang', serif !important;
    }

    h1 { font-size: 40px !important; font-weight: 700; }
    h2 { font-size: 32px !important; font-weight: 700; }
    h3 { font-size: 26px !important; font-weight: 700; }
    p, div { font-size: 20px; }

    /* 메인 카드 스타일 */
    .welcome-card {
        background-color: #F8FAFC;
        border-left: 5px solid #3B82F6;
        padding: 20px;
        border-radius: 8px;
        margin-top: 15px;
        margin-bottom: 25px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 헤더 영역
st.title("🎵 Welcome to Music Hub")
st.write("음악과 감정을 연결하는 나만의 AI 음악 공간에 온 걸 환영해! 💙")

# 안내 카드 영역
st.markdown(
    """
    <div class="welcome-card">
        📌 <b>이용 안내</b><br>
        왼쪽 사이드바 메뉴에서 원하는 기능을 자유롭게 선택해봐!<br>
        AI 가사 감정 분석부터 다양한 음악 추천 기능까지 만날 수 있어 🎧
    </div>
    """,
    unsafe_allow_html=True,
)
