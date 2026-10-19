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
            왼쪽 사이드바 메뉴에서 감정 선율에 맞는 기능을 선택해 보세요.<br>
            가사 감정 분석부터 뮤직 바의 큐레이션 플레이리스트까지 🎧
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
