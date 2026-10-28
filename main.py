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

    /* 사이드바 접기/펼치기 버튼은 남겨두고, 깨지는 텍스트만 투명하게 숨기기 */
    [data-testid="stSidebarCollapseButton"] button {
        font-size: 0px !important;
        color: transparent !important;
    }
    [data-testid="stSidebarCollapseButton"] button svg {
        font-size: 16px !important;
        color: #e0e0e0 !important; /* 버튼 아이콘 색상 */
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
        border-left: 5px solid #c0c0c0;
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

    /* 🎵 중앙 하단 음표 박스 스타일 */
    .dancing-box {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 15px;
        margin-top: 40px;
        padding: 20px;
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

    /* 💃 우측 하단 리얼한 인체 라인 & 드레스 흩날림 애니메이션 🤍 */
    .dancer-container {
        position: fixed;
        bottom: 20px;
        right: 30px;
        width: 150px;
        height: 180px;
        z-index: 999;
        pointer-events: none;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .dancer-glow {
        position: absolute;
        width: 130px;
        height: 130px;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.28) 0%, rgba(255, 255, 255, 0.06) 45%, rgba(0, 0, 0, 0) 75%);
        border-radius: 50%;
        animation: glowPulse 2s infinite alternate ease-in-out;
    }

    .realistic-dancer-svg {
        width: 120px;
        height: 160px;
        position: relative;
        z-index: 2;
        filter: drop-shadow(0 0 12px rgba(255, 255, 255, 0.95)) drop-shadow(0 0 25px rgba(255, 255, 255, 0.45));
        animation: bodySway 2.5s infinite alternate ease-in-out;
    }

    /* 우아한 몸통 실루엣 */
    .body-shape {
        fill: #ffffff;
        transform-origin: 60px 50px;
    }

    /* 흩날리는 풍성한 드레스 스커트 */
    .flowing-dress {
        fill: rgba(255, 255, 255, 0.9);
        transform-origin: 60px 65px;
        animation: dressWave 1.6s infinite alternate ease-in-out;
    }

    /* 우아한 팔 움직임 */
    .arm-left {
        fill: none;
        stroke: #ffffff;
        stroke-width: 4;
        stroke-linecap: round;
        stroke-linejoin: round;
        transform-origin: 55px 35px;
        animation: armLeftMotion 2s infinite alternate ease-in-out;
    }

    .arm-right {
        fill: none;
        stroke: #ffffff;
        stroke-width: 4;
        stroke-linecap: round;
        stroke-linejoin: round;
        transform-origin: 65px 35px;
        animation: armRightMotion 2s infinite alternate ease-in-out;
    }

    /* 다리 움직임 */
    .leg-left {
        fill: none;
        stroke: #ffffff;
        stroke-width: 3.5;
        stroke-linecap: round;
        transform-origin: 55px 95px;
        animation: legLeftMotion 1.8s infinite alternate ease-in-out;
    }

    .leg-right {
        fill: none;
        stroke: #ffffff;
        stroke-width: 3.5;
        stroke-linecap: round;
        transform-origin: 65px 95px;
        animation: legRightMotion 1.8s infinite alternate ease-in-out;
    }

    @keyframes bodySway {
        0% { transform: translateY(0px) rotate(-4deg) scale(0.98); }
        50% { transform: translateY(-8px) rotate(4deg) scale(1.02); }
        100% { transform: translateY(-3px) rotate(6deg) scale(1); }
    }

    @keyframes dressWave {
        0% { transform: rotate(-6deg) skewX(-12deg) scaleX(0.95); }
        50% { transform: rotate(8deg) skewX(15deg) scaleX(1.12); }
        100% { transform: rotate(-4deg) skewX(-8deg) scaleX(1.02); }
    }

    @keyframes armLeftMotion {
        0% { transform: rotate(0deg); }
        50% { transform: rotate(-25deg) translateY(-3px); }
        100% { transform: rotate(15deg); }
    }

    @keyframes armRightMotion {
        0% { transform: rotate(0deg); }
        50% { transform: rotate(30deg) translateY(-3px); }
        100% { transform: rotate(-15deg); }
    }

    @keyframes legLeftMotion {
        0% { transform: rotate(0deg); }
        50% { transform: rotate(12deg); }
        100% { transform: rotate(-8deg); }
    }

    @keyframes legRightMotion {
        0% { transform: rotate(0deg); }
        50% { transform: rotate(-15deg); }
        100% { transform: rotate(10deg); }
    }

    @keyframes glowPulse {
        0% { opacity: 0.5; transform: scale(0.95); }
        100% { opacity: 1; transform: scale(1.25); }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 헤더 영역
st.title("🖤 Welcome to Music Hub")
st.write("Deep & Chill Music Bar 🍸")

st.markdown("<hr>", unsafe_allow_html=True)

# 안내 카드 영역
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
    unsafe_allow_html=True
)

# 하단 중앙 음표 애니메이션 박스
st.markdown(
    """
    <div class="dancing-box">
        <span class="dancing-note">🎵</span>
        <span class="dancing-note">🖤</span>
        <span class="dancing-note">🎶</span>
        <span class="dancing-note">🍸</span>
        <span class="dancing-note">💿</span>
    </div>
    """,
    unsafe_allow_html=True
)

# 우측 하단 리얼한 인체 곡선 & 드레스 실루엣 춤추는 애니메이션 (변수로 분리하여 따옴표 꼬임 원천 차단)
dancer_html = """
<div class="dancer-container">
    <div class="dancer-glow"></div>
    <svg class="realistic-dancer-svg" viewBox="0 0 120 160">
        <path class="body-shape" d="M57 15 C53 15 50 18 50 22 C50 26 53 29 57 29 C61 29 64 26 64 22 C64 18 61 15 57 15 Z" />
        <path d="M55 29 L55 35 L61 35 L61 29 Z" fill="#ffffff" />
        <path class="body-shape" d="M48 37 C45 37 42 42 45 48 C48 54 53 58 58 63 C63 58 68 54 71 48 C74 42 71 37 68 37 C64 37 61 44 58 44 C55 44 52 37 48 37 Z" />
        <path class="arm-left" d="M46 41 C36 46 28 38 22 30" />
        <path class="arm-right" d="M70 41 C82 38 92 48 98 56" />
        <path class="flowing-dress" d="M50 62 C35 72 18 95 12 122 C32 128 55 125 72 115 C88 122 102 125 110 120 C102 92 82 72 68 62 C63 60 55 60 50 62 Z" />
        <path class="leg-left" d="M48 115 L40 152" />
        <path class="leg-right" d="M74 112 L84 148" />
    </svg>
</div>
"""
st.markdown(dancer_html, unsafe_allow_html=True)
