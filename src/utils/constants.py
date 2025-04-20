PAGE_CONFIG = {
    "page_title": "벤처투자 소득공제 시뮬레이터",
    "page_icon": "💰",
    "layout": "wide",
    "initial_sidebar_state": "collapsed"
}

TAX_BRACKETS = [
    (0, 12000000, 0.06),
    (12000000, 46000000, 0.15),
    (46000000, 88000000, 0.24),
    (88000000, 150000000, 0.35),
    (150000000, 300000000, 0.38),
    (300000000, 500000000, 0.40),
    (500000000, float("inf"), 0.42)
]

BASIC_DEDUCTION = 1500000
EARNED_INCOME_SPECIAL_DEDUCTION = 0.02
CREDIT_CARD_DEDUCTION_RATE = 0.15
CREDIT_CARD_THRESHOLD_RATE = 0.25