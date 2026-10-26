import streamlit as st

st.set_page_config(
    page_title="Music Bar",
    page_icon="🖤",
    layout="wide"
)

# 구름 바탕(Gowun Batang) 폰트 & 블랙&실버 다크 테마 스타일 적용
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&display=swap');

    /* 1. 사이드바 여닫기 버튼 깨짐 현상 완벽 차단 */
    [data-testid="stSidebarCollapseButton"] {
        color: transparent !important;
    }
    [data-testid="stSidebarCollapseButton"] button span {
        font-family: 'Material Symbols Outlined', 'Material Icons' !important;
        font-size: 0px !important;
    }
   
    /* 전체 배경 다크 모드 설정 */
    .stApp {
        background-color: #0e0e10;
        color: #e0e0e0;
    }

    /* 폰트 적용 (구름 바탕 유지) */
    html, body, [class*="css"], div, span, h1, h2, h3, h4, h5, h6, p, label, input, button {
        font-family: 'Gowun Batang', serif !important;
        color: #e0e0e0;
    }

    /* 제목 및 헤더 스타일 */
    h1 {
        font-size: 42px !important;
        font-weight: 700;
        color: #ffffff !important;
        letter-spacing: -1px;
    }
    h2 { font-size: 32px !important; font-weight: 700; color: #d1d5db !important; }
    h3 { font-size: 26px !important; font-weight: 700; color: #9ca3af !important; }
    p, div { font-size: 19px; color: #c4c4c4; }

    /* 메인 카드 스타일 (블랙 & 실버 감성) */
    .welcome-card {
        background: linear-gradient(145deg, #18181b, #121214);
        border: 1px solid #3f3f46;
        border-left: 5px solid #c0c0c0; /* 실버 포인트 line */
        padding: 24px;
        border-radius: 12px;
        margin-top: 20px;
        margin-bottom: 30px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.6), 0 0 10px rgba(192, 192, 192, 0.08);
    }

    .card-title {
        font-size: 22px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .card-text {
        font-size: 18px;
        color: #a1a1aa;
        line-height: 1.6;
    }

    /* 🕺 춤추는 애니메이션 박스 스타일 (상대 위치 설정) */
    .dancing-box {
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 15px;
        margin-top: 40px;
        padding: 30px 20px;
        background: linear-gradient(145deg, #141416, #0e0e10);
        border: 1px solid #27272a;
        border-radius: 16px;
        box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.8);
    }

    .dancing-note {
        font-size: 24px;
        animation: danceBeat 1s infinite alternate ease-in-out;
    }

    .dancing-note:nth-child(1) { animation-delay: 0.1s; }
    .dancing-note:nth-child(2) { animation-delay: 0.3s; }
    .dancing-note:nth-child(3) { animation-delay: 0.5s; }
    .dancing-note:nth-child(4) { animation-delay: 0.2s; }

    @keyframes danceBeat {
        0% { transform: translateY(0px) scale(0.9); opacity: 0.5; }
        100% { transform: translateY(-10px) scale(1.1); opacity: 1; }
    }

    /* 💃 애니메이션 박스의 우측 하단 구석에 배치된 하얀 춤추는 사람 */
    .box-corner-dancer {
        position: absolute;
        bottom: 8px;
        right: 16px;
        font-size: 22px;
        color: #ffffff;
        animation: dancePerson 0.8s infinite alternate ease-in-out;
        filter: drop-shadow(0 0 8px rgba(255, 255, 255, 0.7));
    }

    @keyframes dancePerson {
        0% { transform: translateY(0px) rotate(-8deg) scale(0.95); }
        100% { transform: translateY(-8px) rotate(8deg) scale(1.1); }
    }

    /* 구분선 스타일 */
    hr {
        border-color: #27272a !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 헤더 영역
st.title("🖤 Welcome to Music Hub")
st.write("Deep & Chill Music Bar 🍸")

st.markdown("<hr>", unsafe_allow_html=True)

# 안내 카드 영역 (실버 & 매트 블랙 스타일)
st.markdown(
    """
    <div class="welcome-card">
        <div class="card-title">
            <span>💿</span> Guideline
        </div>
        <div class="card-text">
            사이드바에서 원하는 모드를 선택하세요.<br>
            가사 감정 분석부터 커스텀 플레이리스트 큐레이션까지 🎧
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# 🕺 박스 내부 우측 하단 구석에 하얀색 춤추는 사람이 들어간 애니메이션 🖤
st.markdown(
    """
    <div class="dancing-box">
        <span class="dancing-note">🎵</span>
        <span class="dancing-note">🖤</span>
        <span class="dancing-note">🎶</span>
        <span class="dancing-note">🍸</span>
        <span class="box-corner-dancer">🕺</span>
    </div>
    """,
    unsafe_allow_html=True,
)
