# 3: Create VAT unit tests

from datetime import date
from decimal import Decimal

import pytest

from src.uganda_tax_engine.core import TaxContext
from src.uganda_tax_engine.exceptions import InvalidIncomeError
from src.uganda_tax_engine.money import Money
from src.uganda_tax_engine.vat import VAT


def make_context(sales, supply_type="standard", input_vat="0"):
    return TaxContext(
        income=Money.from_value(sales),
        effective_date=date(2026, 10, 18),
        metadata={
            "supply_type": supply_type,
            "input_vat": input_vat,
        },
    )


def test_standard_rated_vat():
    result = VAT().calculate(make_context("100000"))

    assert result.breakdown["output_vat"].amount == Decimal("18000.00")
    assert result.amount.amount == Decimal("18000.00")


def test_input_vat_deducted_from_output_vat():
    result = VAT().calculate(
        make_context("100000", input_vat="5000")
    )

    assert result.amount.amount == Decimal("13000.00")


def test_zero_rated_supply():
    result = VAT().calculate(
        make_context("100000", supply_type="zero_rated", input_vat="5000")
    )

    assert result.breakdown["output_vat"].amount == Decimal("0.00")
    assert result.amount.amount == Decimal("0.00")


def test_exempt_supply_has_no_deductible_input_vat():
    result = VAT().calculate(
        make_context("100000", supply_type="exempt", input_vat="5000")
    )

    assert result.breakdown["deductible_input_vat"].amount == Decimal("0.00")
    assert result.amount.amount == Decimal("0.00")


def test_input_vat_exceeding_output_vat_creates_credit():
    result = VAT().calculate(
        make_context("10000", input_vat="5000")
    )

    assert result.amount.amount == Decimal("0.00")
    assert result.breakdown["vat_credit"].amount == Decimal("3200.00")


@pytest.mark.parametrize(
    "supply_type",
    ["unknown", "reduced"],
)
def test_invalid_supply_type_raises_error(supply_type):
    with pytest.raises(ValueError, match="supply_type"):
        VAT().calculate(make_context("100000", supply_type=supply_type))


def test_negative_input_vat_raises_error():
    with pytest.raises(InvalidIncomeError):
        VAT().calculate(make_context("100000", input_vat="-100"))
# python -m pytest tests/test_vat.py -v