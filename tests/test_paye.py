# automated PAYE tests

from datetime import date

import pytest

from src.uganda_tax_engine.core import TaxContext
from src.uganda_tax_engine.money import Money
from src.uganda_tax_engine.paye import PAYE
# Test invalid income and residency handling
from src.uganda_tax_engine.exceptions import InvalidIncomeError

# 6: Test schedule validity dates
from src.uganda_tax_engine.exceptions import NoScheduleForDateError
from decimal import Decimal

@pytest.mark.parametrize(
    "income, expected_tax",
    [
        (335000, "0.00"),
        (335001, "0.20"),
        (410000, "15000.00"),
        (410001, "15000.25"),
        (485000, "33750.00"),
        (485001, "33750.30"),
        (10000000, "2888250.00"),
        (10000001, "2888250.40"), # attracts both:30% on income above UGX 485,000; andan additional 10% on income above UGX 10 million. https://ura.go.ug/en/changes-to-paye-return-form-following-the-income-tax-amendment-act-2026/
    ],
)
def test_paye_tax_band_boundaries(income, expected_tax):
    context = TaxContext( income=Money.from_value(income), effective_date=date(2026, 10, 18), )

    result = PAYE().calculate(context)

    assert result.amount.amount == Money.from_value(expected_tax).amount
    assert result.taxable_amount.amount == Money.from_value(income).amount
# python -m pytest tests/test_paye.py -v

# Test invalid income and residency handling

def test_negative_taxable_income_raises_error():
    context = TaxContext(income=Money.from_value(100000), allowances=Money.from_value(150000), effective_date=date(2026, 10, 18),)

    with pytest.raises(InvalidIncomeError):
        PAYE().calculate(context)


# def test_nonresident_schedule_is_not_silently_applied():
#     context = TaxContext( income=Money.from_value(1000000),  effective_date=date(2026, 10, 18), residency_status="nonresident",)

#     with pytest.raises(NotImplementedError):
#         PAYE().calculate(context)

def test_nonresident_paye_uses_nonresident_rates():
    context = TaxContext(
        income=Money.from_value(335000),
        effective_date=date(2026, 10, 18),
        residency_status="nonresident",
    )

    result = PAYE().calculate(context)

    assert result.amount.amount == Money.from_value(33500).amount




        
# python -m pytest tests/test_paye.py -v
# Results
# 1. All eight resident PAYE tax-band boundary calculations.
# 2. Negative taxable income raises InvalidIncomeError.
# 3. Nonresident income is not silently processed using the resident schedule.


# Add a test for invalid residency status
# erify that the module rejects unsupported residency labels such as "visitor", rather than silently applying a tax schedule.


def test_invalid_residency_status_raises_error():
    context = TaxContext(
        income=Money.from_value(500000),
        effective_date=date(2026, 10, 18),
        residency_status="visitor",
    )

    with pytest.raises(ValueError, match="Residency status"):
        PAYE().calculate(context)
# python -m pytest tests/test_paye.py -v
# results
# 1. All 8 resident PAYE boundary cases.
# 2. Negative taxable income raises InvalidIncomeError.
# 3. Nonresident PAYE uses its configured schedule.
# 4. Invalid residency status raises an error.

def test_paye_rejects_date_before_schedule():
    context = TaxContext(
        income=Money.from_value(500000),
        effective_date=date(2026, 6, 30),
        residency_status="resident",
    )

    with pytest.raises(NoScheduleForDateError):
        PAYE().calculate(context)
# python -m pytest tests/test_paye.py -v

# 7: Add two more schedule tests

def test_paye_accepts_schedule_start_date():
    context = TaxContext(
        income=Money.from_value(500000),
        effective_date=date(2026, 7, 1),
        residency_status="resident",
    )

    result = PAYE().calculate(context)

    assert result.amount.amount == Decimal("38250.00")


def test_paye_rejects_unknown_residency_status():
    context = TaxContext(
        income=Money.from_value(500000),
        effective_date=date(2026, 10, 18),
        residency_status="visitor",
    )

    with pytest.raises(ValueError, match="Residency status"):
        PAYE().calculate(context)
