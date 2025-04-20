from ..utils.constants import (
    BASIC_DEDUCTION,
    EARNED_INCOME_SPECIAL_DEDUCTION,
    CREDIT_CARD_DEDUCTION_RATE,
    CREDIT_CARD_THRESHOLD_RATE
)

def calc_basic_deduction():
    """기본공제 금액을 반환"""
    return BASIC_DEDUCTION

def calc_earned_income_special_deduction(income):
    """근로소득 특별공제 금액을 계산"""
    return income * EARNED_INCOME_SPECIAL_DEDUCTION

def calc_credit_card_deduction(credit_card_usage, income):
    """신용카드 등 사용금액 소득공제를 계산"""
    threshold = income * CREDIT_CARD_THRESHOLD_RATE
    if credit_card_usage <= threshold:
        return 0
    deductible_amount = credit_card_usage - threshold
    return deductible_amount * CREDIT_CARD_DEDUCTION_RATE

def calc_total_deductions(income, credit_card_usage):
    """전체 공제금액을 계산"""
    basic = calc_basic_deduction()
    earned_special = calc_earned_income_special_deduction(income)
    credit_card = calc_credit_card_deduction(credit_card_usage, income)
    total = basic + earned_special + credit_card
    deductions = {
        "기본공제": basic,
        "근로소득 특별공제": earned_special,
        "신용카드 등 소득공제": credit_card
    }
    return total, deductions