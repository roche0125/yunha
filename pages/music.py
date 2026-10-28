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
        filter: drop-shadow(0 0 12px rgba(255, 255, 255, 0.95)) drop-shadow(0 0 25px rgba(255, 255, 255, 0.
