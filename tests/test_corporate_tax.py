
from datetime import date
from decimal import Decimal

import pytest

from src.uganda_tax_engine.core import TaxContext
from src.uganda_tax_engine.exceptions import InvalidIncomeError
from src.uganda_tax_engine.money import Money
from src.uganda_tax_engine.corporate_tax import CorporateTax


def make_context(revenue, deductions="0"):
    return TaxContext(
        income=Money.from_value(revenue),
        effective_date=date(2026, 10, 18),
        metadata={"allowable_deductions": deductions},
    )


def test_corporate_tax_calculation():
    result = CorporateTax().calculate(
        make_context("10000000", "4000000")
    )

    assert result.taxable_amount.amount == Decimal("6000000.00")
    assert result.amount.amount == Decimal("1800000.00")


def test_no_deductions():
    result = CorporateTax().calculate(make_context("1000000"))

    assert result.taxable_amount.amount == Decimal("1000000.00")
    assert result.amount.amount == Decimal("300000.00")


def test_deductions_exceed_revenue():
    result = CorporateTax().calculate(
        make_context("1000000", "1500000")
    )

    assert result.taxable_amount.amount == Decimal("0.00")
    assert result.amount.amount == Decimal("0.00")


def test_zero_revenue():
    result = CorporateTax().calculate(make_context("0"))

    assert result.taxable_amount.amount == Decimal("0.00")
    assert result.amount.amount == Decimal("0.00")


@pytest.mark.parametrize(
    "revenue, deductions",
    [
        ("-1000", "0"),
        ("100000", "-5000"),
    ],
)
def test_negative_inputs_raise_error(revenue, deductions):
    with pytest.raises(InvalidIncomeError):
        CorporateTax().calculate(make_context(revenue, deductions))


def test_breakdown_contains_tax_components():
    result = CorporateTax().calculate(
        make_context("5000000", "1000000")
    )

    assert result.breakdown["revenue"].amount == Decimal("5000000.00")
    assert result.breakdown["allowable_deductions"].amount == Decimal("1000000.00")
    assert result.breakdown["chargeable_income"].amount == Decimal("4000000.00")
    assert result.breakdown["corporate_tax"].amount == Decimal("1200000.00")
# python -m pytest tests/test_corporate_tax.py -v

# python -m pytest -v