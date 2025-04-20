from ..utils.constants import TAX_BRACKETS

def get_tax_bracket_info(taxable_income):
    """과세표준 금액에 해당하는 세율을 반환"""
    for start, end, rate in TAX_BRACKETS:
        if start <= taxable_income < end:
            return rate
    return TAX_BRACKETS[-1][2]  # 최고 세율 적용

def calc_tax(taxable_income):
    """과세표준 금액에 대한 세금을 계산"""
    tax_rate = get_tax_bracket_info(taxable_income)
    return taxable_income * tax_rate