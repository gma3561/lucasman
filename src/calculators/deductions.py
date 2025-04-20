BASIC_DEDUCTION = 1500000
EARNED_INCOME_SPECIAL_DEDUCTION = 0.02
CREDIT_CARD_DEDUCTION_RATE = 0.15
CREDIT_CARD_THRESHOLD_RATE = 0.25

def calc_basic_deduction():
    return BASIC_DEDUCTION

def calc_earned_income_special_deduction(income):
    return income * EARNED_INCOME_SPECIAL_DEDUCTION

def calc_credit_card_deduction(credit_card_usage, income):
    threshold = income * CREDIT_CARD_THRESHOLD_RATE
    if credit_card_usage <= threshold:
        return 0
    deductible_amount = credit_card_usage - threshold
    return deductible_amount * CREDIT_CARD_DEDUCTION_RATE

def calc_total_deductions(income, credit_card_usage):
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