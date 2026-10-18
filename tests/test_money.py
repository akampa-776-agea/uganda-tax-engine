#This will help verify the monetary calculations independently of PAYE, VAT, and corporate tax.

from decimal import Decimal, ROUND_HALF_UP

import pytest

from src.uganda_tax_engine.money import Money


def test_money_addition():
    result = Money.from_value("1000.50") + Money.from_value("200.25")
    assert result.amount == Decimal("1200.75")


def test_money_multiplication():
    result = Money.from_value("1000") * 5
    assert result.amount == Decimal("5000.00")


def test_money_less_than():
    assert Money.from_value("100") < Money.from_value("200")


def test_money_equality():
    assert Money.from_value("100.00") == Money.from_value("100")


def test_money_rounds_half_up():
    result = Money.from_value("10.125")
    expected = Decimal("10.13")
    assert result.amount == expected


def test_money_rejects_float():
    with pytest.raises(TypeError):
        Money.from_value(10.25)


def test_money_rejects_boolean():
    with pytest.raises(TypeError):
        Money.from_value(True)


def test_money_is_immutable():
    money = Money.from_value("100")

    with pytest.raises(AttributeError):
        money.amount = Decimal("200.00")


def test_money_repr():
    assert repr(Money.from_value("1000")) == "Money(UGX 1000.00)"
