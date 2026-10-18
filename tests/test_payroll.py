
from datetime import date
from decimal import Decimal

import pytest

from src.uganda_tax_engine.money import Money
from src.uganda_tax_engine.payroll import Payroll


def test_payroll_calculates_employee_and_employer_nssf():
    result = Payroll().calculate(
        Money.from_value("1000000"),
        date(2026, 10, 18),
    )

    assert result.employee_nssf.amount == Decimal("50000.00")
    assert result.employer_nssf.amount == Decimal("100000.00")


def test_payroll_net_pay_reconciles():
    result = Payroll().calculate(
        Money.from_value("1000000"),
        date(2026, 10, 18),
    )

    expected = (
        result.gross_pay.amount
        - result.employee_nssf.amount
        - result.paye.amount
        - result.local_service_tax.amount
    )

    assert result.net_pay.amount == expected


def test_payroll_applies_configured_local_service_tax():
    result = Payroll().calculate(
        Money.from_value("1000000"),
        date(2026, 10, 18),
        local_service_tax=Money.from_value("5000"),
    )

    assert result.local_service_tax.amount == Decimal("5000.00")
    assert result.net_pay.amount == Decimal("756750.00")


def test_negative_gross_pay_raises_error():
    with pytest.raises(ValueError, match="Gross pay"):
        Payroll().calculate(
            Money.from_value("-1000"),
            date(2026, 10, 18),
        )


def test_negative_local_service_tax_raises_error():
    with pytest.raises(ValueError, match="Local Service Tax"):
        Payroll().calculate(
            Money.from_value("1000000"),
            date(2026, 10, 18),
            local_service_tax=Money.from_value("-100"),
        )
