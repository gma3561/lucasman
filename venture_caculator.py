import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정을 스크립트 최상단에 배치
try:
    st.set_page_config(
        page_title="벤처투자 소득공제 시뮬레이터",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except Exception as e:
    pass

# 스타일 설정
st.markdown("""
<style>
    /* 기본 요소 숨기기 */
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    
    /* 에러 메시지 숨기기 */
    .stException, .stAlert {display: none !important;}
    div[data-testid="stStatusWidget"] {display: none !important;}
    .element-container iframe {display: none !important;}
    
    /* 레이아웃 최적화 */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1200px;
    }
    
    .stApp > header {
        background-color: transparent;
    }
    
    .stApp {
        margin-top: -2rem;
    }
    
    /* 사이드바 최적화 */
    [data-testid="stSidebar"][aria-expanded="true"] {
        padding: 2rem 1rem;
    }
    
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        padding-top: 0;
    }
    
    /* 모바일 최적화 */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem 0.5rem;
        }
        
        [data-testid="stSidebar"][aria-expanded="true"] {
            padding: 1rem 0.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# 기존 CSS 스타일 유지
st.markdown("""
<style>
    /* 기존 CSS 스타일 내용 */
    /* ... existing code ... */
</style>
""", unsafe_allow_html=True)

# 페이지 로딩 상태 관리
if 'loaded' not in st.session_state:
    st.session_state.loaded = True
    st.session_state.show_result = False
    st.session_state.current_salary = 0
    st.session_state.credit_card = 0
    st.session_state.dependent_count = 0
    st.session_state.elderly_count = 0

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

# 초기 화면 표시
if not st.session_state.show_result:
    st.markdown('<p class="main-header">벤처투자 소득공제 시뮬레이터</p>', unsafe_allow_html=True)
    
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

# ─────────────────────────────────────────────────────────
# 1️⃣ 입력 섹션
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <h2 class="sidebar-header">
        💰 소득 정보 입력
    </h2>
    """, unsafe_allow_html=True)
    
    # 세션 상태 초기화
    if 'current_salary' not in st.session_state:
        st.session_state.current_salary = 0
        
    # 총급여액 입력
    st.markdown("""
    <div class="input-group">
        <p class="deduction-title">📌 총급여액 <span class="required-field">필수</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    # 총급여액 입력 - 자동 업데이트 방식
    def on_salary_change():
        try:
            # 콤마 제거 후 숫자로 변환
            cleaned_text = st.session_state.salary_text.replace(',', '')
            if cleaned_text:  # 빈 문자열이 아닌 경우에만 처리
                if cleaned_text.isdigit():
                    st.session_state.current_salary = int(cleaned_text)
                    st.session_state.show_result = True  # 입력값이 변경되면 결과 자동 업데이트
                else:
                    st.markdown("""
                        <div style="padding: 0.5rem; color: var(--text-secondary); font-size: 0.9rem;">
                            숫자만 입력해주세요
                        </div>
                    """, unsafe_allow_html=True)
        except ValueError:
            pass  # 에러 메시지 대신 무시
    
    # 입력 필드 스타일 적용 (총급여액)
    st.markdown("""
        <div style="margin-bottom: 0.5rem;">
            <div style="color: var(--text-secondary); font-size: 0.9rem;">
                숫자만 입력하세요 (예: 50000000)
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    salary_text = st.text_input(
        "금액을 입력하세요",
        value=format(st.session_state.current_salary, ',d') if st.session_state.current_salary > 0 else "",
        key="salary_text",
        on_change=on_salary_change,
        help="총급여액을 숫자로만 입력해주세요 (예: 50000000)"
    )
    
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
    
    # 신용카드 입력 - 자동 업데이트 방식
    def on_credit_card_change():
        try:
            # 콤마 제거 후 숫자로 변환
            cleaned_text = st.session_state.credit_card_text.replace(',', '')
            if cleaned_text:  # 빈 문자열이 아닌 경우에만 처리
                if cleaned_text.isdigit():
                    st.session_state.credit_card = int(cleaned_text)
                    if st.session_state.current_salary > 0:
                        st.session_state.show_result = True  # 입력값이 변경되면 결과 자동 업데이트
                else:
                    st.markdown("""
                        <div style="padding: 0.5rem; color: var(--text-secondary); font-size: 0.9rem;">
                            숫자만 입력해주세요
                        </div>
                    """, unsafe_allow_html=True)
        except ValueError:
            pass  # 에러 메시지 대신 무시
    
    # 세션 상태 초기화
    if 'credit_card' not in st.session_state:
        st.session_state.credit_card = 0
    
    # 입력 필드 스타일 적용 (신용카드)
    st.markdown("""
        <div style="margin-bottom: 0.5rem;">
            <div style="color: var(--text-secondary); font-size: 0.9rem;">
                숫자만 입력하세요 (예: 30000000)
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    credit_card_text = st.text_input(
        "금액을 입력하세요",
        value=format(st.session_state.credit_card, ',d') if st.session_state.credit_card > 0 else "",
        key="credit_card_text",
        on_change=on_credit_card_change,
        help="연간 신용카드 사용금액을 숫자로만 입력해주세요 (예: 30000000)"
    )
    
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
    
    # 벤처투자 관련 입력 (고정값)
    invest_amt = 30_000_000  # 3천만원 고정
    cash_back_amt = 25_000_000  # 2천5백만원 고정

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # 계산하기 버튼
    if st.button("계산하기", key="calculate_button", use_container_width=True, 
                type="primary"):
        st.session_state.show_result = True

# 자동 계산 함수 - 기본 공제, 국민연금, 4대보험 등 계산
def calculate_default_deductions(salary):
    # 1. 기본공제 (본인 공제)
    personal_deduction = 1_500_000
    
    # 2. 부양가족 공제
    dependent_deduction = st.session_state.dependent_count * 1_500_000
    
    # 3. 경로우대 추가공제
    elderly_deduction = st.session_state.elderly_count * 1_000_000
    
    # 4. 국민연금 (총급여의 4.5%)
    national_pension = int(salary * 0.045)
    
    # 5. 건강보험 (총급여의 3.545%)
    health_insurance = int(salary * 0.03545)
    
    # 6. 고용보험 (총급여의 0.8%)
    employment_insurance = int(salary * 0.008)
    
    # 7. 장기요양보험 (건강보험의 12.81%)
    long_term_care = int(health_insurance * 0.1281)
    
    # 총 4대보험료
    insurance_total = national_pension + health_insurance + employment_insurance + long_term_care
    
    return {
        'personal': personal_deduction,
        'dependent': dependent_deduction,
        'elderly': elderly_deduction,
        'national_pension': national_pension,
        'health_insurance': health_insurance,
        'employment_insurance': employment_insurance,
        'long_term_care': long_term_care,
        'insurance_total': insurance_total
    }

# 신용카드 공제 계산 함수 수정
def calculate_credit_card_deduction(salary, credit_card_spending):
    # 총급여의 25% 계산
    min_spending = salary * 0.25
    
    # 신용카드 사용액이 최소 사용액보다 적으면 공제 없음
    if credit_card_spending <= min_spending:
        return 0
    
    # 초과분에 대해 15% 공제율 적용
    deductible_amount = credit_card_spending - min_spending
    deduction = int(deductible_amount * 0.15)
    
    # 공제 한도 계산 (총급여 구간별)
    if salary <= 70_000_000:
        max_deduction = min(3_000_000, salary * 0.20)  # 총급여의 20% 한도
    elif salary <= 120_000_000:
        max_deduction = min(2_500_000, salary * 0.20)
    else:
        max_deduction = min(2_000_000, salary * 0.20)
    
    # 최종 공제액 (한도 적용)
    final_deduction = min(deduction, max_deduction)
    return final_deduction

def calculate_and_show_results():
    # 근로소득공제 계산
    earned_income_ded = calc_earned_income_ded(st.session_state.current_salary)
    
    # 자동 계산 항목 (기본 공제, 국민연금, 4대보험 등)
    auto_deductions = calculate_default_deductions(st.session_state.current_salary)
    
    # 신용카드 공제 계산
    credit_card_ded = calculate_credit_card_deduction(st.session_state.current_salary, st.session_state.credit_card)
    
    # 기본 공제 합계 계산 (벤처투자 공제 제외)
    base_deductions = sum([
        earned_income_ded,  # 근로소득공제
        auto_deductions['personal'],  # 기본공제 (본인)
        auto_deductions['dependent'],  # 부양가족 공제
        auto_deductions['elderly'],  # 경로우대 공제
        auto_deductions['insurance_total'],  # 4대보험
        credit_card_ded  # 신용카드 공제
    ])

    # 벤처투자 소득공제 계산
    venture_ded = calc_venture(invest_amt)
    
    # 벤처투자 공제 전 과세표준 (다른 모든 공제 적용 후)
    pre_venture_taxable = max(0, st.session_state.current_salary - base_deductions)
    
    # 벤처투자 공제 후 과세표준
    post_venture_taxable = max(0, pre_venture_taxable - venture_ded)
    
    # 세율 구간 정보 가져오기 (벤처투자 전후)
    pre_bracket_desc, pre_bracket_rate = get_tax_bracket_info(pre_venture_taxable)
    post_bracket_desc, post_bracket_rate = get_tax_bracket_info(post_venture_taxable)

    # 세금 계산 (벤처투자 전후)
    tax_pre_raw = calc_tax(pre_venture_taxable)
    tax_post_raw = calc_tax(post_venture_taxable)

    # ────────── ① 산출세액 ──────────
    tax_pre_raw  = calc_tax(pre_venture_taxable)
    tax_post_raw = calc_tax(post_venture_taxable)

    # ────────── ② 세액감면·세액공제 차감 ──────────
    # 세액공제 및 감면 항목은 제거하고 자동 계산으로 변경
    # 근로소득세액공제 (근로소득세액 × 55%, 상한 있음)
    if tax_pre_raw <= 1_300_000:
        tax_credit = int(tax_pre_raw * 0.55)
    else:
        tax_credit = int(1_300_000 * 0.55 + (tax_pre_raw - 1_300_000) * 0.30)
        
    # 최대 공제한도 설정
    if st.session_state.current_salary <= 33_000_000:
        tax_credit = min(tax_credit, 740_000)
    elif st.session_state.current_salary <= 70_000_000:
        tax_credit = min(tax_credit, 740_000 - ((st.session_state.current_salary - 33_000_000) * 0.008))
    else:
        tax_credit = min(tax_credit, 660_000)
        
    tax_reduction = 0  # 세액감면 항목은 제거
    
    tax_pre_after  = max(0, tax_pre_raw  - tax_reduction - tax_credit)
    tax_post_after = max(0, tax_post_raw - tax_reduction - tax_credit)

    # ────────── ③ 지방소득세 (10%) ──────────
    local_pre  = int(tax_pre_after  * 0.10)
    local_post = int(tax_post_after * 0.10)

    total_tax_pre  = tax_pre_after  + local_pre
    total_tax_post = tax_post_after + local_post

    refund = total_tax_pre - total_tax_post        # 절세·환급액
    
    # 절세 효과 상세 분석
    income_tax_saved = tax_pre_after - tax_post_after
    local_tax_saved = local_pre - local_post
    
    # 한계세율에 따른 최대 절세 금액 계산
    theoretical_max_saving = venture_ded * (pre_bracket_rate / 100)

    # 비즈니스 모델: 투자비용, 세금 절감, 수익률 계산 수정
    net_cost = invest_amt - cash_back_amt  # 실제 투자비용 (500만원)
    tax_benefit = refund  # 세금 절감 효과
    roi = (tax_benefit / net_cost) if net_cost > 0 else 0  # 실제 투자비용 대비 세금 절감 효과의 수익률

    # ─── 결과 레이아웃 ───────────────────────────
    st.empty()  # 기존 내용 지우기
    
    st.markdown('<p class="main-header">💰 벤처투자 소득공제 시뮬레이션 결과</p>', unsafe_allow_html=True)
    
    # 상단 요약 정보 카드 (3단 레이아웃)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="result-box" style="text-align:center;">
            <p style="color:var(--text-secondary); margin:0; font-size:0.9rem;">실제 투자 비용</p>
            <p style="color:var(--primary-dark); font-size:1.7rem; font-weight:700; margin:0.5rem 0; height:45px;">
                {net_cost:,}원
            </p>
            <p style="color:var(--text-light); margin:0.5rem 0 0 0; font-size:0.8rem; height:35px;">
                투자금액 - 현금리턴
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="result-box" style="text-align:center;">
            <p style="color:var(--text-secondary); margin:0; font-size:0.9rem;">총 절세 효과</p>
            <p style="color:var(--positive); font-size:1.7rem; font-weight:700; margin:0.5rem 0; height:45px;">
                +{refund:,}원
            </p>
            <p style="color:var(--text-light); margin:0.5rem 0 0 0; font-size:0.8rem; height:35px;">
                소득공제를 통한 절세 효과
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        roi_percent = roi * 100
        net_profit = -net_cost + tax_benefit
        st.markdown(f"""
        <div class="result-box" style="text-align:center;">
            <p style="color:var(--text-secondary); margin:0; font-size:0.9rem;">투자 수익률</p>
            <p style="color:var(--positive); font-size:1.7rem; font-weight:700; margin:0.5rem 0; height:45px;">
                {roi_percent:.1f}%
            </p>
            <p style="color:var(--text-light); margin:0.5rem 0 0 0; font-size:0.8rem; height:35px;">
                실 순수익: {net_profit:,}원
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # 탭으로 구분된 상세 정보
    tab1, tab2, tab3 = st.tabs(["💡 세율 구간 분석", "📊 공제 항목 상세", "💰 투자 효율성 평가"])
    
    with tab1:
        st.markdown('<p class="result-subheader">�� 벤처투자 소득공제 전후 세율 구간 분석</p>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="scrollable-table-container">
        <table class="comparison-table">
            <tr>
                <th>구분</th>
                <th>과세표준</th>
                <th>세율 구간</th>
                <th>한계세율</th>
            </tr>
            <tr>
                <td>벤처투자 공제 전</td>
                <td>{pre_venture_taxable:,}원</td>
                <td>{pre_bracket_desc}</td>
                <td>{pre_bracket_rate:.1f}%</td>
            </tr>
            <tr>
                <td>벤처투자 공제 후</td>
                <td>{post_venture_taxable:,}원</td>
                <td>{post_bracket_desc}</td>
                <td>{post_bracket_rate:.1f}%</td>
            </tr>
        </table>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<p class="result-subheader">💡 벤처투자 전후 세금 비교</p>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="scrollable-table-container">
        <table class="comparison-table">
            <tr>
                <th>구분</th>
                <th>벤처투자 전</th>
                <th>벤처투자 후</th>
                <th>차액</th>
            </tr>
            <tr>
                <td>과세표준</td>
                <td>{pre_venture_taxable:,}원</td>
                <td>{post_venture_taxable:,}원</td>
                <td class="highlight-number decrease-number">▼ {pre_venture_taxable - post_venture_taxable:,}원</td>
            </tr>
            <tr>
                <td>산출세액</td>
                <td>{tax_pre_raw:,}원</td>
                <td>{tax_post_raw:,}원</td>
                <td class="highlight-number decrease-number">▼ {tax_pre_raw - tax_post_raw:,}원</td>
            </tr>
            <tr>
                <td>결정세액</td>
                <td>{tax_pre_after:,}원</td>
                <td>{tax_post_after:,}원</td>
                <td class="highlight-number decrease-number">▼ {tax_pre_after - tax_post_after:,}원</td>
            </tr>
            <tr>
                <td>지방소득세</td>
                <td>{local_pre:,}원</td>
                <td>{local_post:,}원</td>
                <td class="highlight-number decrease-number">▼ {local_pre - local_post:,}원</td>
            </tr>
            <tr>
                <td>부담세액</td>
                <td>{total_tax_pre:,}원</td>
                <td>{total_tax_post:,}원</td>
                <td class="highlight-number decrease-number">▼ {total_tax_pre - total_tax_post:,}원</td>
            </tr>
        </table>
        </div>
        
        <div class="highlight-box" style="margin-top:1rem;">
            <p style="font-weight:600; margin-bottom:0.5rem; color:var(--primary-dark);">세율 구간 변동 효과</p>
            <p style="color:var(--text-secondary); line-height:1.6; margin:0;">
                벤처기업 투자로 인한 소득공제({venture_ded:,}원)를 통해 과세표준이 <strong>{pre_venture_taxable:,}원</strong>에서 <strong>{post_venture_taxable:,}원</strong>으로 감소했습니다.
                이로 인해 한계세율이 <strong>{pre_bracket_rate:.1f}%</strong>에서 <strong>{post_bracket_rate:.1f}%</strong>로 변동되었습니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        # 소득공제 항목 시각화 - 카드 스타일로 변경
        st.markdown('<p class="result-subheader">📝 자동 계산된 공제 항목</p>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="highlight-box" style="margin-top:1.5rem; padding:1.5rem; background-color:var(--background); border:1px solid var(--border); border-radius:12px;">
            <h4 style="color:var(--primary-dark); font-size:1.2rem; font-weight:600; margin:0 0 1.5rem 0; text-align:left;">
                📊 공제 항목 분석
            </h4>
            <div style="display: grid; grid-template-columns: repeat(1, 1fr); gap: 1rem;">
        """, unsafe_allow_html=True)
        
        # 각 공제 항목을 카드로 표시
        for item, amount in deduction_items.items():
            if total_ded > 0:
                percentage = (amount / total_ded) * 100
                st.markdown(f"""
                <div style="background-color:var(--background-light); padding:1.2rem; border-radius:8px; border:1px solid var(--border);">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div style="flex:1;">
                            <p style="color:var(--text-primary); font-weight:600; font-size:1.1rem; margin:0 0 0.5rem 0;">
                                {item}
                            </p>
                            <p style="color:var(--primary-dark); font-weight:700; font-size:1.2rem; margin:0;">
                                {amount:,}원
                            </p>
                        </div>
                        <div style="background-color:var(--primary-light); color:var(--primary-dark); padding:0.5rem 1rem; border-radius:6px; font-weight:600;">
                            {percentage:.1f}%
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # 총 공제금액을 강조하여 표시
        st.markdown(f"""
            </div>
            <div style="margin-top:1.5rem; background-color:var(--primary-light); padding:1.5rem; border-radius:8px; text-align:center;">
                <p style="color:var(--primary-dark); font-size:1.1rem; font-weight:600; margin:0 0 0.5rem 0;">
                    총 공제금액
                </p>
                <p style="color:var(--primary-dark); font-size:1.6rem; font-weight:700; margin:0;">
                    {total_ded:,}원
                </p>
            </div>
            <p style="color:var(--text-secondary); font-size:0.9rem; margin:1rem 0 0 0; text-align:left;">
                * 각 항목별 공제금액과 전체 공제금액 대비 비율을 나타냅니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        # 투자 적합성 평가만 표시
        roi_percent = roi * 100
        net_profit = -net_cost + tax_benefit  # 실 순수익 계산 (실제투자비용의 마이너스 + 세금절감액)

        # 각 항목을 개별 div로 분리하여 표시
        st.markdown("""
        <div class="highlight-box" style="margin-top:1rem; padding: 2rem; text-align:center;">
            <h3 style="font-weight:700; margin-bottom:2rem; color:var(--primary-dark); font-size:1.4rem;">
                투자 효율성 평가
            </h3>
        """, unsafe_allow_html=True)

        # 투자 금액과 현금 리턴
        st.markdown(f"""
        <div style="margin-bottom:2rem;">
            <div style="color:var(--text-secondary); font-size:1.1rem; margin-bottom:0.5rem;">투자 금액</div>
            <div style="color:var(--text-primary); font-size:1.5rem; font-weight:700;">{invest_amt:,}원</div>
            <div style="color:var(--text-secondary); font-size:0.9rem; margin-top:0.3rem;">현금 리턴: {cash_back_amt:,}원</div>
        </div>
        """, unsafe_allow_html=True)

        # 실제 투자 비용
        st.markdown(f"""
        <div style="margin-bottom:2rem;">
            <div style="color:var(--text-secondary); font-size:1.1rem; margin-bottom:0.5rem;">실제 투자 비용</div>
            <div style="color:var(--text-primary); font-size:1.5rem; font-weight:700;">{net_cost:,}원</div>
            <div style="color:var(--text-secondary); font-size:0.9rem; margin-top:0.3rem;">투자금액 - 현금리턴</div>
        </div>
        """, unsafe_allow_html=True)

        # 세금 절감액
        st.markdown(f"""
        <div style="margin-bottom:2rem;">
            <div style="color:var(--text-secondary); font-size:1.1rem; margin-bottom:0.5rem;">세금 절감액</div>
            <div style="color:var(--primary-dark); font-size:1.5rem; font-weight:700;">+ {tax_benefit:,}원</div>
            <div style="color:var(--text-secondary); font-size:0.9rem; margin-top:0.3rem;">소득공제를 통한 절세 효과</div>
        </div>
        """, unsafe_allow_html=True)

        # 투자 수익률
        st.markdown(f"""
        <div style="margin-bottom:2rem;">
            <div style="color:var(--text-secondary); font-size:1.1rem; margin-bottom:0.5rem;">투자 수익률</div>
            <div style="color:var(--positive); font-size:1.8rem; font-weight:700;">{roi_percent:.1f}%</div>
            <div style="color:var(--text-secondary); font-size:0.9rem; margin-top:0.3rem;">실 순수익: {net_profit:,}원</div>
        </div>
        """, unsafe_allow_html=True)

        # 실 순수익
        st.markdown(f"""
        <div style="margin-bottom:1rem;">
            <div style="color:var(--text-secondary); font-size:1.1rem; margin-bottom:0.5rem;">실 순수익</div>
            <div style="color:var(--positive); font-size:1.8rem; font-weight:700;">{net_profit:,}원</div>
            <div style="color:var(--text-secondary); font-size:0.9rem; margin-top:0.3rem;">현금리턴 - 투자금액 + 세금절감액</div>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 재계산 버튼
    st.button("다시 계산하기", on_click=lambda: setattr(st.session_state, 'show_result', False))

# 결과가 계산된 상태라면 결과를 표시 (메인 화면 버튼 클릭으로만 결과 표시)
if st.session_state.show_result and st.session_state.current_salary > 0:
    calculate_and_show_results()
else:
    # 초기 설명 화면 표시
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