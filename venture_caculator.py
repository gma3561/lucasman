import streamlit as st

# ─────────────────────────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="벤처투자 소득공제 시뮬레이터",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Streamlit 기본 요소 숨기기
hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 커스텀 CSS 추가
st.markdown("""
<style>
    /* 색상 변수 정의 */
    :root {
        --primary: #4f46e5;
        --primary-light: #e0e7ff;
        --primary-dark: #3730a3;
        --text-primary: #1e293b;
        --text-secondary: #475569;
        --text-light: #64748b;
        --background: #ffffff;
        --background-light: #f8fafc;
        --border: #e2e8f0;
        --border-light: #f1f5f9;
        --positive: #10b981;
        --positive-light: #d1fae5;
        --negative: #ef4444;
        --negative-light: #fee2e2;
    }

    /* 전체 배경색 및 기본 스타일 */
    .stApp {
        background-color: var(--background) !important;
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* 모바일 최적화 */
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.3rem !important;
            margin-top: 0.8rem !important;
            padding: 0 0.5rem !important;
        }
        
        /* 테이블 스크롤 처리 */
        .scrollable-table-container {
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
            margin: 0 -1rem !important;
            padding: 0 1rem !important;
        }
        
        /* 테이블 셀 최적화 */
        .comparison-table td,
        .comparison-table th,
        .deduction-analysis-table td,
        .deduction-analysis-table th {
            padding: 0.7rem 0.5rem !important;
            font-size: 0.85rem !important;
            white-space: nowrap !important;
        }
        
        /* 숫자 표시 최적화 */
        .highlight-number {
            font-size: 0.85rem !important;
            padding: 2px 6px !important;
        }
        
        /* 결과 박스 최적화 */
        .result-box {
            padding: 1rem 0.8rem !important;
            margin: 0.5rem 0 !important;
        }
        
        /* 금액 표시 최적화 */
        .result-box p[style*="font-size:1.7rem"] {
            font-size: 1.3rem !important;
        }
        
        /* 설명 텍스트 최적화 */
        .result-box p[style*="font-size:0.8rem"] {
            font-size: 0.75rem !important;
        }
        
        /* 탭 내용 최적화 */
        [data-testid="stTabs"] {
            margin: 0 -1rem !important;
        }
        
        [data-testid="stTabContent"] {
            padding: 0 0.5rem !important;
        }

        /* 투자 효율성 평가 섹션 모바일 최적화 */
        .highlight-box div {
            text-align: center !important;
            padding: 0.8rem !important;
        }

        .highlight-box div[style*="margin-bottom:2rem"] {
            background-color: var(--background-light) !important;
            border-radius: 8px !important;
            margin: 0.8rem auto !important;
            max-width: 90% !important;
            padding: 1rem !important;
        }

        /* 금액 표시 스타일 */
        .highlight-box div[style*="color:var(--text-primary)"] {
            font-size: 1.3rem !important;
            margin: 0.5rem 0 !important;
        }

        /* 설명 텍스트 스타일 */
        .highlight-box div[style*="color:var(--text-secondary)"] {
            font-size: 0.9rem !important;
            margin: 0.3rem 0 !important;
        }

        /* 섹션 제목 스타일 */
        .highlight-box h3[style*="font-weight:700"] {
            font-size: 1.2rem !important;
            margin: 1rem 0 1.5rem 0 !important;
        }

        /* 결과값 강조 스타일 */
        .highlight-box div[style*="color:var(--positive)"] {
            font-size: 1.4rem !important;
            margin: 0.5rem 0 !important;
        }
    }
    
    /* Streamlit 기본 요소 오버라이드 */
    .st-emotion-cache-eczf16, .st-emotion-cache-16txtl3, .st-emotion-cache-1v0mbdj, 
    .st-emotion-cache-1wrcr25, .st-emotion-cache-6qob1r, .st-emotion-cache-1cypcdb, 
    .st-emotion-cache-18ni7ap, .st-emotion-cache-ue6h4q, .st-emotion-cache-z5fcl4 {
        background-color: var(--background) !important;
    }
    
    /* 메인 헤더 */
    .main-header {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 1.5rem 0 1rem 0;
        color: var(--primary-dark);
        padding: 0.5rem 0;
        border-bottom: 2px solid var(--primary-light);
        text-align: center;
    }
    
    /* 섹션 헤더 */
    .section-header {
        color: var(--text-primary);
        font-size: 1.5rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--border);
        background-color: var(--background);
    }
    
    /* 서브 헤더 */
    .result-subheader {
        color: var(--primary-dark);
        font-size: 1.3rem;
        font-weight: 700;
        margin: 1.5rem 0;
        padding: 0.8rem 1.2rem;
        background-color: var(--primary-light);
        border-radius: 8px;
        display: block;
    }
    
    /* 결과 박스 */
    .result-box {
        background-color: var(--background);
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid var(--border);
        margin: 1.8rem 0;
        box-shadow: 0 6px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease-in-out;
    }
    .result-box:hover {
        box-shadow: 0 12px 20px -3px rgba(0, 0, 0, 0.1), 0 8px 12px -4px rgba(0, 0, 0, 0.05);
        transform: translateY(-3px);
        border-color: var(--primary-light);
    }
    
    /* 하이라이트 박스 */
    .highlight-box {
        background-color: var(--background) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05) !important;
    }
    
    .highlight-box div[style*="margin-bottom:2rem"] {
        transition: all 0.2s ease-in-out !important;
    }
    
    .highlight-box div[style*="margin-bottom:2rem"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* 비교 테이블 */
    .comparison-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin: 1.5rem 0;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
    }
    .comparison-table th {
        background-color: var(--primary-light);
        padding: 1rem 1.2rem;
        text-align: center;
        border-bottom: 1px solid var(--border);
        color: var(--primary-dark);
        font-weight: 700;
        font-size: 1.05rem;
    }
    .comparison-table td {
        padding: 1.2rem;
        text-align: right;
        border-bottom: 1px solid var(--border-light);
        color: var(--text-primary);
        background-color: var(--background);
        font-size: 1.05rem;
    }
    .comparison-table tr:last-child td {
        border-bottom: none;
    }
    .comparison-table td:first-child {
        text-align: left;
        font-weight: 600;
        color: var(--text-primary);
        background-color: var(--background-light);
    }
    
    /* 강조 숫자 */
    .highlight-number {
        color: var(--primary-dark);
        font-weight: 700;
        font-size: 1.15rem;
    }
    .decrease-number {
        color: var(--negative);
        background-color: var(--negative-light);
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
    }
    .increase-number {
        color: var(--positive);
        background-color: var(--positive-light);
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
    }
    
    /* 최종 수익 표시 */
    .total-profit {
        font-size: 1.5rem;
        color: var(--primary-dark);
        font-weight: 700;
        text-align: center;
        padding: 2rem;
        background-color: var(--primary-light);
        border-radius: 12px;
        margin: 2rem 0;
        box-shadow: 0 4px 10px -2px rgba(0, 0, 0, 0.1);
    }
    
    /* 버튼 스타일 */
    .stButton>button {
        width: 100%;
        margin: 0.5rem 0;
        background-color: var(--primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
    }
    .stButton>button:hover {
        background-color: var(--primary-dark) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* 사이드바 스타일링 */
    .css-1d391kg, .st-emotion-cache-1cypcdb {
        background-color: var(--background) !important;
        padding: 2rem 1.5rem;
        border-right: 1px solid var(--border);
    }
    
    /* 번호 입력 스타일 개선 */
    .stNumberInput > div {
        width: 100% !important;
    }
    .stNumberInput input {
        border-radius: 8px !important;
        width: 100% !important;
        padding: 0.75rem 1rem !important;
        text-align: right !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        color: var(--primary-dark) !important;
        background-color: var(--background) !important;
        border: 1px solid var(--primary) !important;
        transition: all 0.2s ease !important;
    }
    
    .stNumberInput input:focus {
        box-shadow: 0 0 0 2px var(--primary-light) !important;
        border-color: var(--primary) !important;
    }
    
    /* 입력 그룹 여백 및 스타일 */
    .input-group {
        background-color: var(--background);
        padding: 1.2rem;
        border-radius: 8px;
        margin: 1.2rem 0;
        border: 1px solid var(--border);
    }
    
    /* 입력 필드 간격 조정 */
    .st-emotion-cache-1gulkj5 {
        margin-bottom: 1rem !important;
    }
    
    /* 입력 라벨 스타일 */
    .input-label {
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.6rem;
    }
    
    /* 필수 입력 표시 */
    .required-field {
        color: var(--negative);
        font-weight: 600;
        background-color: var(--negative-light);
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.8rem;
    }
    
    /* 결과 제목과 아이템 스타일 */
    .result-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary-dark);
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 3px solid var(--primary-light);
    }
    
    .result-item {
        font-weight: 600;
        color: var(--text-secondary);
        margin: 0.8rem 0 0.3rem 0;
    }
    
    .result-number {
        font-weight: 600;
        font-size: 1.1rem;
        color: var(--primary-dark);
        margin: 0.2rem 0 1rem 0;
        padding-left: 1rem;
    }
    
    /* 확장 패널 스타일 개선 */
    .streamlit-expanderHeader {
        background-color: var(--primary-light) !important;
        color: var(--primary-dark) !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.8rem 1rem !important;
        margin-bottom: 0.5rem !important;
        transition: all 0.2s ease !important;
    }
    .streamlit-expanderHeader:hover {
        background-color: var(--primary-light) !important;
        transform: translateY(-1px);
    }
    
    /* 확장 패널 내용 */
    .streamlit-expanderContent {
        background-color: var(--background) !important;
        border: 1px solid var(--border-light) !important;
        border-top: none !important;
        padding: 1.2rem !important;
        border-radius: 0 0 8px 8px !important;
        margin-bottom: 1rem !important;
    }
    
    /* 소득공제 항목 제목 */
    .deduction-item-title {
        font-weight: 600;
        color: var(--primary-dark);
        margin-bottom: 0.8rem;
        font-size: 1rem;
    }
    
    /* 금액 표시 스타일 */
    .money-amount {
        font-weight: 700;
        color: var(--primary-dark);
    }
    
    /* 모바일 대응 */
    @media (max-width: 768px) {
        .result-box {
            padding: 1rem;
        }
        .comparison-table td, .comparison-table th {
            padding: 0.6rem;
            font-size: 0.9rem;
        }
    }

    /* 추가 스타일 */
    /* 라벨 스타일 개선 */
    .stNumberInput label {
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        font-size: 0.95rem !important;
    }
    
    /* 공제 항목 헤더 */
    .deduction-header {
        color: var(--primary-dark);
        font-weight: 700;
        font-size: 1.15rem;
        margin: 0.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--primary-light);
        text-align: center;
    }
    
    /* 입력 값 효과 */
    .stNumberInput input:not(:placeholder-shown) {
        background-color: var(--background-light) !important;
        border-color: var(--primary) !important;
    }

    /* 사이드바 헤더 개선 */
    .sidebar-header {
        color: var(--primary-dark);
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--primary-light);
    }

    /* 공제 항목 타이틀 통일 */
    .deduction-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--primary-dark);
        margin: 0.7rem 0;
        padding-bottom: 0.3rem;
    }

    /* 탭 버튼 가시성 개선 */
    .st-cc {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    
    /* 선택된 탭 더 분명하게 */
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: var(--primary-light) !important;
        color: var(--primary-dark) !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        padding: 5px 20px !important;
    }
    
    /* 선택되지 않은 탭도 더 뚜렷하게 */
    button[data-baseweb="tab"][aria-selected="false"] {
        color: var(--text-secondary) !important;
        font-weight: 600 !important;
        padding: 5px 20px !important;
    }
    
    /* 탭 컨테이너 스타일링 */
    [data-testid="stTabs"] {
        background-color: var(--background) !important;
        border-radius: 8px !important;
        padding: 5px !important;
        border: 1px solid var(--border-light) !important;
        margin-bottom: 1rem !important;
        width: 100% !important;
    }
    
    /* 숫자 입력 필드 플러스/마이너스 버튼만 제거 */
    .stNumberInput [data-testid="stNumberInputPlus"],
    .stNumberInput [data-testid="stNumberInputMinus"] {
        display: none !important;
    }
    
    /* 결과 안내 메시지 */
    .result-notification {
        background-color: var(--primary-light);
        color: var(--primary-dark);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 600;
        border: 1px solid var(--primary);
        font-size: 1.1rem;
    }

    /* 불필요한 공백 제거 및 레이아웃 최적화 */
    .main .block-container {
        padding: 0 !important;
        max-width: 1200px !important;
    }

    .element-container {
        margin-bottom: 0 !important;
    }

    /* 탭 컨텐츠 영역 */
    [data-testid="stTabContent"] {
        padding: 0 !important;
    }

    /* 숫자 셀 영역 확보 */
    .comparison-table td {
        padding: 1rem 1.5rem !important;
        white-space: nowrap !important; /* 줄바꿈 방지 */
        min-width: 80px !important;
    }

    .comparison-table th {
        padding: 1rem 1.5rem !important;
        white-space: nowrap !important;
        min-width: 80px !important;
    }

    /* 숫자 표시 공간 확보 */
    .highlight-number {
        white-space: nowrap !important;
        display: inline-block !important;
        min-width: fit-content !important;
    }

    /* 결과 박스 중 상단 여백 불필요한 것 제거 */
    .result-box:first-child {
        margin-top: 0.5rem !important;
    }

    /* 레이아웃 전체 최적화 - 불필요한 공간 제거 */
    .main .block-container {
        padding: 0 !important;
        max-width: 1200px !important;
    }

    .element-container {
        margin-bottom: 0 !important;
    }

    /* 결과 박스 여백 최적화 */
    .result-box {
        margin: 0.8rem 0;
        padding: 1.5rem;
    }

    /* 테이블 최적화 - 숫자가 잘 보이도록 */
    .comparison-table {
        table-layout: fixed;
        width: 100%;
    }
    
    .comparison-table th,
    .comparison-table td {
        white-space: nowrap;
        overflow: visible;
        padding: 0.8rem;
    }
    
    /* 테이블 셀 너비 조정 */
    .comparison-table th:first-child,
    .comparison-table td:first-child {
        width: 20%;
    }
    
    .comparison-table th:not(:first-child),
    .comparison-table td:not(:first-child) {
        width: 25%;
        text-align: right;
    }

    /* 탭 컨테이너 최적화 */
    [data-testid="stTabs"] {
        margin: 0 !important;
    }
    
    [data-testid="stTabContent"] {
        padding: 0 !important;
    }

    /* 불필요한 여백 제거 */
    .stTabs [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }

    /* 숫자 셀 항상 보이게 */
    .highlight-number {
        white-space: nowrap !important;
        min-width: fit-content !important;
    }

    /* 테이블 레이아웃이 깨지지 않도록 스크롤 허용 */
    .scrollable-table-container {
        overflow-x: auto;
        padding-bottom: 0.5rem;
    }

    /* 테이블 스타일 - 소득공제 항목 분석용 */
    .deduction-analysis-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin: 0.5rem 0;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        table-layout: fixed;
    }
    
    .deduction-analysis-table th,
    .deduction-analysis-table td {
        padding: 1rem;
        border-bottom: 1px solid var(--border-light);
        font-size: 1rem;
        line-height: 1.5;
        white-space: nowrap;
        overflow: visible;
    }
    
    .deduction-analysis-table th {
        background-color: var(--primary-light);
        color: var(--primary-dark);
        font-weight: 700;
    }
    
    .deduction-analysis-table th:first-child,
    .deduction-analysis-table td:first-child {
        width: 50%;
        text-align: left;
        padding-left: 1.5rem;
    }
    
    .deduction-analysis-table th:not(:first-child),
    .deduction-analysis-table td:not(:first-child) {
        width: 25%;
        text-align: right;
        padding-right: 1.5rem;
    }
    
    .deduction-analysis-table td:first-child {
        background-color: var(--background-light);
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .deduction-analysis-table td:nth-child(2) {
        color: var(--primary-dark);
        font-weight: 600;
    }
    
    .deduction-analysis-table td:nth-child(3) {
        color: var(--text-secondary);
    }
    
    .deduction-analysis-table tr:last-child td {
        border-bottom: none;
        background-color: var(--primary-light);
        color: var(--primary-dark) !important;
        font-weight: 700;
    }

    /* 테이블 내용 정렬을 위한 추가 스타일 제거 */
    .deduction-analysis-table tr {
        display: table-row;
    }
    
    .deduction-analysis-table th,
    .deduction-analysis-table td {
        display: table-cell;
    }

    /* 입력 스타일 개선 */
    .input-container {
        display: flex;
        align-items: center;
        margin-bottom: 0.8rem;
        border: 1px solid var(--primary);
        border-radius: 8px;
        overflow: hidden;
        background-color: var(--background);
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    }
    
    .input-container input {
        flex: 1;
        border: none !important;
        padding: 1rem !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        text-align: right !important;
        outline: none !important;
        box-shadow: none !important;
        color: var(--primary-dark) !important;
    }
    
    .input-container button {
        background-color: var(--primary) !important;
        color: white !important;
        border: none !important;
        padding: 1rem 1.5rem !important;
        font-weight: 600 !important;
        min-width: 100px !important;
        cursor: pointer !important;
        transition: background-color 0.2s ease !important;
        font-size: 1.1rem !important;
    }
    
    .input-container button:hover {
        background-color: var(--primary-dark) !important;
    }

    /* 금액 단위 강조 */
    .currency-unit {
        font-weight: 600;
        color: var(--primary);
        padding-left: 0.5rem;
    }

    /* 계산 버튼 스타일 */
    .calculate-button {
        background-color: var(--primary) !important;
        color: white !important;
        padding: 1rem 2rem !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: none !important;
        cursor: pointer !important;
        width: 100% !important;
        margin-top: 1.5rem !important;
        margin-bottom: 2rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1) !important;
    }
    
    .calculate-button:hover {
        background-color: var(--primary-dark) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* 결과 섹션 스타일 */
    .results-container {
        background-color: var(--background-light);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 2rem;
        border: 1px solid var(--primary-light);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    .results-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--primary-dark);
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid var(--primary);
    }
    
    .result-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.8rem 0;
        border-bottom: 1px solid rgba(0, 0, 0, 0.08);
    }
    
    .result-label {
        font-weight: 600;
        font-size: 1.05rem;
        color: var(--text-primary);
    }
    
    .result-value {
        font-weight: 700;
        font-size: 1.1rem;
        color: var(--primary);
        text-align: right;
    }
    
    .result-highlight {
        background-color: var(--primary-light);
        color: var(--primary-dark);
        padding: 1rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.15rem;
        margin: 1.5rem 0;
        text-align: center;
    }

    /* 계산 버튼 스타일 추가 - 버튼 클릭 이벤트 밖으로 이동 */
    .stButton button[data-testid="stButtonPrimary"] {
        height: 3.5rem !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15) !important;
        transition: all 0.2s ease !important;
    }
    .stButton button[data-testid="stButtonPrimary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2) !important;
    }

    /* 입력 필드 스타일 개선 */
    .stTextInput label {
        color: #000000 !important; /* 라벨 텍스트 색상 검정색으로 변경 */
        font-weight: 500 !important;
    }
    
    .stTextInput input {
        background-color: #ffffff !important; /* 입력 필드 배경색 흰색으로 설정 */
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1.1rem !important;
        color: var(--text-primary) !important;
    }
    
    .stTextInput input:focus {
        box-shadow: 0 0 0 2px var(--primary-light) !important;
        border-color: var(--primary) !important;
    }

    /* 테이블 헤더 */
    .deduction-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin: 1rem 0;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .deduction-table th {
        background-color: var(--primary-light);
        color: var(--primary-dark);
        font-weight: 600;
        padding: 12px 16px;
        text-align: left;
        border-bottom: 1px solid var(--border);
        white-space: nowrap;
    }
    
    .deduction-table td {
        padding: 12px 16px;
        border-bottom: 1px solid var(--border-light);
        background-color: var(--background);
        font-size: 1rem;
        line-height: 1.5;
    }
    
    .deduction-table tr:last-child td {
        border-bottom: none;
    }
    
    .deduction-table td:first-child {
        background-color: var(--background-light);
        font-weight: 500;
        color: var(--text-primary);
        width: 40%;
    }
    
    .deduction-table td:nth-child(2) {
        text-align: right;
        width: 35%;
        font-family: monospace;
        font-weight: 600;
        color: var(--primary-dark);
    }
    
    .deduction-table td:nth-child(3) {
        text-align: right;
        width: 25%;
        font-family: monospace;
        font-weight: 600;
        color: var(--text-secondary);
    }
    
    .deduction-table th:nth-child(2),
    .deduction-table th:nth-child(3) {
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
# 2️⃣ 근로소득공제 계산
# ─────────────────────────────────────────────────────────
def calc_earned_income_ded(salary):
    if salary <= 5_000_000:
        return int(salary * 0.7)
    elif salary <= 15_000_000:
        return int(3_500_000 + (salary - 5_000_000) * 0.4)
    elif salary <= 45_000_000:
        return int(7_500_000 + (salary - 15_000_000) * 0.15)
    elif salary <= 100_000_000:
        return int(12_000_000 + (salary - 45_000_000) * 0.05)
    else:
        return int(14_750_000 + (salary - 100_000_000) * 0.02)

# ─────────────────────────────────────────────────────────
# 3️⃣ 벤처투자 소득공제 계산
# ─────────────────────────────────────────────────────────
BRACKETS = [(30_000_000,1.0),(50_000_000,0.7),(float("inf"),0.3)]
def calc_venture(a):
    r, d, lo = a, 0, 0
    for up, rate in BRACKETS:
        s = min(r, up - lo)
        if s <= 0:
            break
        d += s * rate
        r -= s
        lo = up
    return int(d)

# ─────────────────────────────────────────────────────────
# 4️⃣ 누진세율 산출함수
# ─────────────────────────────────────────────────────────
TAX_TABLE = [
    (14_000_000, 0.06, 0),
    (50_000_000, 0.15, 1_400_000),
    (88_000_000, 0.24, 7_640_000),
    (150_000_000, 0.35, 19_640_000),
    (300_000_000, 0.38, 25_640_000),
    (500_000_000, 0.40, 47_640_000),
    (1_000_000_000, 0.42, 83_640_000),
    (float("inf"), 0.45, 183_640_000),
]

# 세율 구간 정보 함수
def get_tax_bracket_info(taxable_income):
    tax_bracket_desc = ""
    tax_bracket_rate = 0.0
    
    for i, (limit, rate, _) in enumerate(TAX_TABLE):
        if taxable_income <= limit:
            tax_bracket_rate = rate * 100
            if i == 0:
                tax_bracket_desc = f"1,400만원 이하 (6%)"
            elif i == 1:
                tax_bracket_desc = f"1,400만원 초과 5,000만원 이하 (15%)"
            elif i == 2:
                tax_bracket_desc = f"5,000만원 초과 8,800만원 이하 (24%)"
            elif i == 3:
                tax_bracket_desc = f"8,800만원 초과 1억5,000만원 이하 (35%)"
            elif i == 4:
                tax_bracket_desc = f"1억5,000만원 초과 3억원 이하 (38%)"
            elif i == 5:
                tax_bracket_desc = f"3억원 초과 5억원 이하 (40%)"
            elif i == 6:
                tax_bracket_desc = f"5억원 초과 10억원 이하 (42%)"
            else:
                tax_bracket_desc = f"10억원 초과 (45%)"
            break
    
    return tax_bracket_desc, tax_bracket_rate

def calc_tax(base):
    for up, rate, dec in TAX_TABLE:
        if base <= up:
            return max(0, int(base * rate - dec))
    return 0

# 세션 상태 초기화
if 'show_result' not in st.session_state:
    st.session_state.show_result = False
if 'current_salary' not in st.session_state:
    st.session_state.current_salary = 0
if 'credit_card' not in st.session_state:
    st.session_state.credit_card = 0
if 'dependent_count' not in st.session_state:
    st.session_state.dependent_count = 0
if 'elderly_count' not in st.session_state:
    st.session_state.elderly_count = 0

# 메인 헤더
st.markdown('<p class="main-header">벤처투자 소득공제 시뮬레이터</p>', unsafe_allow_html=True)

# 사이드바에 입력 섹션
with st.sidebar:
    st.markdown("""
    <h2 class="sidebar-header">
        💰 소득 정보 입력
    </h2>
    """, unsafe_allow_html=True)
    
    # 총급여액 입력
    st.markdown("""
    <div class="input-group">
        <p class="deduction-title">📌 총급여액 <span class="required-field">필수</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    # 총급여액 입력 필드
    salary = st.text_input(
        "금액을 입력하세요",
        value=format(st.session_state.current_salary, ',d') if st.session_state.current_salary > 0 else "",
        key="salary_input",
        label_visibility="collapsed"
    )
    
    try:
        st.session_state.current_salary = int(salary.replace(',', '')) if salary.replace(',', '').isdigit() else 0
    except:
        st.session_state.current_salary = 0
    
    # 현재 총급여액 표시
    if st.session_state.current_salary > 0:
        st.markdown(f"""
            <div style="background-color:var(--primary-light); padding:1rem; border-radius:8px; margin:1rem 0; text-align:center;">
                <p style="color:var(--text-secondary); margin:0; font-size:0.9rem;">현재 총급여액</p>
                <p style="color:var(--primary-dark); font-size:1.4rem; font-weight:700; margin:0.3rem 0 0 0;">
                    {st.session_state.current_salary:,}원
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 연간 신용카드 예상 사용 금액 입력
    st.markdown("""
    <div class="input-group">
        <p class="deduction-title">💳 연간 신용카드 예상 사용 금액</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 신용카드 사용액 입력 필드
    credit_card = st.text_input(
        "금액을 입력하세요",
        value=format(st.session_state.credit_card, ',d') if st.session_state.credit_card > 0 else "",
        key="credit_card_input",
        label_visibility="collapsed"
    )
    
    try:
        st.session_state.credit_card = int(credit_card.replace(',', '')) if credit_card.replace(',', '').isdigit() else 0
    except:
        st.session_state.credit_card = 0
    
    # 현재 연간 신용카드 사용액 표시
    if st.session_state.credit_card > 0:
        st.markdown(f"""
            <div style="background-color:var(--primary-light); padding:1rem; border-radius:8px; margin:1rem 0; text-align:center;">
                <p style="color:var(--text-secondary); margin:0; font-size:0.9rem;">연간 신용카드 사용액</p>
                <p style="color:var(--primary-dark); font-size:1.4rem; font-weight:700; margin:0.3rem 0 0 0;">
                    {st.session_state.credit_card:,}원
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 추가 소득공제 항목 (expander로 숨김)
    with st.expander("👨‍👩‍👧‍👦 추가 소득공제 항목"):
        # 부양가족 수 입력
        st.markdown("""
        <div style="margin-bottom: 0.5rem;">
            <div style="color: var(--text-secondary); font-size: 0.9rem;">
                부양가족 수를 입력하세요 (기본공제 1인당 150만원)
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        dependent_count = st.text_input(
            "부양가족 수",
            value=str(st.session_state.dependent_count) if st.session_state.dependent_count > 0 else "",
            key="dependent_count",
            label_visibility="collapsed"
        )
        
        try:
            st.session_state.dependent_count = int(dependent_count) if dependent_count.isdigit() else 0
        except:
            st.session_state.dependent_count = 0
        
        # 경로우대 대상자 수 입력
        st.markdown("""
        <div style="margin: 1rem 0 0.5rem 0;">
            <div style="color: var(--text-secondary); font-size: 0.9rem;">
                경로우대 대상자 수를 입력하세요 (추가공제 1인당 100만원)
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        elderly_count = st.text_input(
            "경로우대 대상자 수",
            value=str(st.session_state.elderly_count) if st.session_state.elderly_count > 0 else "",
            key="elderly_count",
            label_visibility="collapsed"
        )
        
        try:
            st.session_state.elderly_count = int(elderly_count) if elderly_count.isdigit() else 0
        except:
            st.session_state.elderly_count = 0
    
    # 벤처투자 관련 입력 (고정값)
    invest_amt = 30_000_000  # 3천만원 고정
    cash_back_amt = 25_000_000  # 2천5백만원 고정

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # 계산하기 버튼
    if st.button("계산하기", key="calculate_button", use_container_width=True, type="primary"):
        st.session_state.show_result = True

# 메인 영역에 설명 표시
if not st.session_state.show_result:
    # 소개 카드 레이아웃
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="result-box">
            <div style="text-align:center; margin-bottom:1rem;">
                <span style="font-size:2.5rem;">💸</span>
            </div>
            <h3 style="text-align:center; color:var(--primary-dark); margin-bottom:1rem;">세금 절약 계산</h3>
            <p style="text-align:center; color:var(--text-secondary); margin-bottom:1rem;">
                벤처기업 투자로 얼마나 세금을 절약할 수 있는지 계산해보세요.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="result-box">
            <div style="text-align:center; margin-bottom:1rem;">
                <span style="font-size:2.5rem;">📊</span>
            </div>
            <h3 style="text-align:center; color:var(--primary-dark); margin-bottom:1rem;">세율 구간 분석</h3>
            <p style="text-align:center; color:var(--text-secondary); margin-bottom:1rem;">
                소득공제 전후의 세율 구간 변화와 한계세율 효과를 확인하세요.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="result-box">
            <div style="text-align:center; margin-bottom:1rem;">
                <span style="font-size:2.5rem;">💰</span>
            </div>
            <h3 style="text-align:center; color:var(--primary-dark); margin-bottom:1rem;">투자 수익성 분석</h3>
            <p style="text-align:center; color:var(--text-secondary); margin-bottom:1rem;">
                현금 리턴과 세금 절감을 통한 최종 수익률을 확인하세요.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # 사용 방법 안내
    st.markdown("""
    <div class="result-box">
        <h3 class="result-title">📋 사용 방법</h3>
        <ol style="color:var(--text-secondary); padding-left:1.5rem; line-height:1.6;">
            <li><strong>소득 정보 입력:</strong> 왼쪽 사이드바에서 총급여액, 소득공제 항목, 세액공제, 세액감면 정보를 입력하세요.</li>
            <li><strong>계산하기 버튼 클릭:</strong> 모든 정보 입력 후 하단의 계산하기 버튼을 클릭하면 결과가 표시됩니다.</li>
            <li><strong>결과 확인:</strong> 계산 완료 후 결과가 화면에 표시됩니다.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # 벤처투자 설명
    st.markdown("""
    <div class="result-box">
        <h3 class="result-title">💡 벤처투자 세제혜택 안내</h3>
        <p style="color:var(--text-secondary); margin-bottom:1rem;">
            벤처기업에 투자하면 투자금액에 대해 소득공제를 받을 수 있습니다. 소득공제율은 다음과 같습니다:
        </p>
        <table class="comparison-table">
            <tr>
                <th>투자 금액</th>
                <th>소득공제율</th>
            </tr>
            <tr>
                <td>3천만원 이하</td>
                <td>100%</td>
            </tr>
            <tr>
                <td>3천만원 초과 ~ 5천만원 이하</td>
                <td>70%</td>
            </tr>
            <tr>
                <td>5천만원 초과</td>
                <td>30%</td>
            </tr>
        </table>
        <p style="color:var(--text-secondary); margin-top:1rem; font-size:0.9rem;">
            * 본 시뮬레이터는 정확한 세금 계산을 보장하지 않으며 참고용으로만 사용하세요.
        </p>
    </div>
    """, unsafe_allow_html=True)

# 결과 표시
if st.session_state.show_result and st.session_state.current_salary > 0:
    calculate_and_show_results()

# 사이드바에 추가 공제 항목 입력 섹션
st.sidebar.markdown("""
<div class="input-group">
    <p class="deduction-title">👨‍👩‍👧‍👦 추가 소득공제 항목</p>
</div>
""", unsafe_allow_html=True)

# 부양가족 수 입력
def on_dependent_change():
    try:
        cleaned_text = st.session_state.dependent_text.replace(',', '')
        if cleaned_text:
            if cleaned_text.isdigit():
                st.session_state.dependent_count = int(cleaned_text)
                if st.session_state.current_salary > 0:
                    st.session_state.show_result = True
    except ValueError:
        pass

if 'dependent_count' not in st.session_state:
    st.session_state.dependent_count = 0

st.sidebar.markdown("""
<div style="margin-bottom: 0.5rem;">
    <div style="color: var(--text-secondary); font-size: 0.9rem;">
        부양가족 수를 입력하세요 (기본공제 1인당 150만원)
    </div>
</div>
""", unsafe_allow_html=True)

dependent_text = st.sidebar.text_input(
    "부양가족 수",
    value=str(st.session_state.dependent_count) if st.session_state.dependent_count > 0 else "",
    key="dependent_text",
    on_change=on_dependent_change,
    help="부양가족 수를 입력하세요 (예: 2)"
)

# 경로우대 대상자 수 입력
def on_elderly_change():
    try:
        cleaned_text = st.session_state.elderly_text.replace(',', '')
        if cleaned_text:
            if cleaned_text.isdigit():
                st.session_state.elderly_count = int(cleaned_text)
                if st.session_state.current_salary > 0:
                    st.session_state.show_result = True
    except ValueError:
        pass

if 'elderly_count' not in st.session_state:
    st.session_state.elderly_count = 0

st.sidebar.markdown("""
<div style="margin-bottom: 0.5rem;">
    <div style="color: var(--text-secondary); font-size: 0.9rem;">
        경로우대 대상자 수를 입력하세요 (추가공제 1인당 100만원)
    </div>
</div>
""", unsafe_allow_html=True)

elderly_text = st.sidebar.text_input(
    "경로우대 대상자 수",
    value=str(st.session_state.elderly_count) if st.session_state.elderly_count > 0 else "",
    key="elderly_text",
    on_change=on_elderly_change,
    help="만 70세 이상 경로우대 대상자 수를 입력하세요 (예: 1)"
)