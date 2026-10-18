# We'll test three properties:
# 1. Non-negative tax: tax should never be negative.
# 2. Monotonicity: increasing taxable income should not decrease tax.
# 3. Tax does not exceed income: for the configured PAYE schedule, tax should not exceed taxable income.


from datetime import date
from decimal import Decimal

from hypothesis import given, settings
from hypothesis import strategies as st

from src.uganda_tax_engine.core import TaxContext
from src.uganda_tax_engine.money import Money
from src.uganda_tax_engine.paye import PAYE


@settings(max_examples=200)
@given(income=st.integers(min_value=0, max_value=100_000_000))
def test_paye_tax_is_non_negative(income):
    context = TaxContext(
        income=Money.from_value(income),
        effective_date=date(2026, 10, 18),
    )

    result = PAYE().calculate(context)

    assert result.amount.amount >= Decimal("0")


@settings(max_examples=200)
@given(
    lower_income=st.integers(min_value=0, max_value=99_999_999),
    increment=st.integers(min_value=1, max_value=100_000_000),
)
def test_paye_tax_is_monotonic(lower_income, increment):
    higher_income = lower_income + increment

    lower_context = TaxContext(
        income=Money.from_value(lower_income),
        effective_date=date(2026, 10, 18),
    )
    higher_context = TaxContext(
        income=Money.from_value(higher_income),
        effective_date=date(2026, 10, 18),
    )

    lower_tax = PAYE().calculate(lower_context).amount.amount
    higher_tax = PAYE().calculate(higher_context).amount.amount

    assert higher_tax >= lower_tax


@settings(max_examples=200)
@given(income=st.integers(min_value=0, max_value=100_000_000))
def test_paye_tax_never_exceeds_income(income):
    context = TaxContext(
        income=Money.from_value(income),
        effective_date=date(2026, 10, 18),
    )

    result = PAYE().calculate(context)

    assert result.amount.amount <= result.taxable_amount.amount
#python -m pytest tests/test_properties.py -v
# python -m pytest -v