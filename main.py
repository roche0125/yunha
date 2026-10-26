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

    /* 💃 우측 하단 몽환적으로 춤추는 드레스 실루엣 애니메이션 🤍 */
    .dancer-container {
        position: fixed;
        bottom: 25px;
        right: 35px;
        width: 130px;
        height: 160px;
        z-index: 999;
        pointer-events: none;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .dancer-glow {
        position: absolute;
        width: 110px;
        height: 110px;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.05) 45%, rgba(0, 0, 0, 0) 70%);
        border-radius: 50%;
        animation: glowPulse 2s infinite alternate ease-in-out;
    }

    .silhouette-svg {
        width: 100px;
        height: 140px;
        position: relative;
        z-index: 2;
        filter: drop-shadow(0 0 12px rgba(255, 255, 255, 0.95)) drop-shadow(0 0 25px rgba(255, 255, 255, 0.4));
        animation: bodyTurn 3s infinite alternate ease-in-out;
    }

    /* 드레스 스커트 흩날림 애니메이션 */
    .dress-skirt {
        fill: rgba(255, 255, 255, 0.85);
        transform-origin: 50px 55px;
        animation: skirtWave 1.8s infinite alternate ease-in-out;
    }

    /* 왼팔 움직임 */
    .left-arm {
        stroke: #ffffff;
        stroke-width: 3.5;
        stroke-linecap: round;
        transform-origin: 45px 30px;
        animation: armLeftMove 2.2s infinite alternate ease-in-out;
    }

    /* 오른팔 움직임 */
    .right-arm {
        stroke: #ffffff;
        stroke-width: 3.5;
        stroke-linecap: round;
        transform-origin: 55px 30px;
        animation: armRightMove 2.2s infinite alternate ease-in-out;
    }

    /* 다리 동작 */
    .leg-left {
        stroke: #ffffff;
        stroke-width: 3;
        stroke-linecap: round;
        transform-origin: 46px 85px;
        animation: legLeftMove 2s infinite alternate ease-in-out;
    }

    .leg-right {
        stroke: #ffffff;
        stroke-width: 3;
        stroke-linecap: round;
        transform-origin: 54px 85px;
        animation: legRightMove 2s infinite alternate ease-in-out;
    }

    @keyframes bodyTurn {
        0% { transform: translateY(0px) rotate(-6deg); }
        50% { transform: translateY(-8px) rotate(4deg) scale(1.03); }
        100% { transform: translateY(-2px) rotate(8deg); }
    }

    @keyframes skirtWave {
        0% { transform: rotate(-8deg) skewX(-10deg) scaleX(0.95); }
        50% { transform: rotate(10deg) skewX(12deg) scaleX(1.1); }
        100% { transform: rotate(-5deg) skewX(-6deg) scaleX(1.02); }
    }

    @keyframes armLeftMove {
        0% { transform: rotate(0deg); }
        50% { transform: rotate(-35deg) translateY(-5px); }
        100% { transform: rotate(15deg); }
    }

    @keyframes armRightMove {
        0% { transform: rotate(0deg); }
        50% { transform: rotate(40deg) translateY(-4px); }
        100% { transform: rotate(-20deg); }
    }

    @keyframes legLeftMove {
        0% { transform: rotate(0deg); }
        50% { transform: rotate(15deg); }
        100% { transform: rotate(-10deg); }
    }

    @keyframes legRightMove {
        0% { transform: rotate(0deg); }
        50% { transform: rotate(-20deg); }
        100% { transform: rotate(12deg); }
    }

    @keyframes glowPulse {
        0% { opacity: 0.4; transform: scale(0.9); }
        100% { opacity: 0.9; transform: scale(1.2); }
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

# 🎵 하단 중앙 음표 애니메이션 박스
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
    unsafe_allow_html=True,
)

# 💃 우측 하단 몽환적 드레스 실루엣 춤추는 애니메이션 (팔/다리/드레스 유기적 움직임)
st.markdown(
    """
    <div class="dancer-container">
        <div class="dancer-glow"></div>
        <svg class="silhouette-svg" viewBox="0 0 100 140">
            <!-- 머리 -->
            <circle cx="50" cy="20" r="7" fill="#ffffff" />
            <!-- 상체 -->
            <path d="M46 27 C46 27, 50 25, 54 27 C55 35, 53 45, 50 55 C47 45, 45 35, 46 27 Z" fill="#ffffff" />
            <!-- 왼팔 -->
            <path class="left-arm" d="M45 28 C35 32, 25 25, 18 18" fill="none" />
            <!-- 오른팔 -->
            <path class="right-arm" d="M55 28 C68 25, 78 35, 85 45" fill="none" />
            <!-- 흩날리는 드레스 스커트 -->
            <path class="dress-skirt" d="M50 50 C40 60, 20 85, 15 105 C35 110, 65 110, 85 100 C80 80, 60 60, 50 50 Z" />
            <!-- 왼다리 -->
            <path class="leg-left" d="M44 95 L38 130" fill="none" />
            <!-- 오른다리 -->
            <path class="leg-right" d="M56 95 L65 128" fill="none" />
        </svg>
    </div>
    """,
    unsafe_allow_html=True,
)
