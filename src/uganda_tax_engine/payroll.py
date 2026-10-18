# to connect the tax calculations into a payroll pipeline:
# 1. Calculate employee NSSF contribution at the configured 5%.
# 2. Calculate employer NSSF contribution at the configured 10%.
# 3. Calculate PAYE.
# 4. Apply configurable Local Service Tax (LST).
# 5 Calculate net pay and produce an itemized payroll breakdown.


"""Payroll calculations for the Uganda Tax Engine."""

from dataclasses import dataclass
from decimal import Decimal

from src.uganda_tax_engine.core import TaxContext
from src.uganda_tax_engine.money import Money
from src.uganda_tax_engine.paye import PAYE


@dataclass(frozen=True)
class PayrollResult:
    """Store an employee's payroll calculation results."""

    gross_pay: Money
    employee_nssf: Money
    employer_nssf: Money
    paye: Money
    local_service_tax: Money
    net_pay: Money


class Payroll:
    """Calculate payroll deductions and employee net pay."""

    EMPLOYEE_NSSF_RATE = Decimal("0.05")
    EMPLOYER_NSSF_RATE = Decimal("0.10")

    def __init__(self, paye_calculator: PAYE | None = None):
        self.paye_calculator = paye_calculator or PAYE()

# PayrollResult stores the payroll outputs in one structured object.
# Employee NSSF is configured at 5%.
# Employer NSSF is configured at 10%.
# The payroll class reuses your existing PAYE calculator instead of duplicating tax logic.
# python -c "from src.uganda_tax_engine.payroll import Payroll, PayrollResult; print('Payroll module imported successfully')"


    def calculate(
        self,
        gross_pay: Money,
        effective_date,
        residency_status: str = "resident",
        local_service_tax: Money | None = None,
    ) -> PayrollResult:
        """Calculate payroll deductions and employee net pay."""

        if gross_pay.amount < 0:
            raise ValueError("Gross pay cannot be negative.")

        lst = local_service_tax or Money.from_value("0")

        if lst.amount < 0:
            raise ValueError("Local Service Tax cannot be negative.")

        employee_nssf = gross_pay * self.EMPLOYEE_NSSF_RATE
        employer_nssf = gross_pay * self.EMPLOYER_NSSF_RATE

        context = TaxContext(
            income=gross_pay,
            effective_date=effective_date,
            residency_status=residency_status,
        )

        paye_result = self.paye_calculator.calculate(context)
        paye_amount = paye_result.amount

        net_pay = (
            gross_pay.amount
            - employee_nssf.amount
            - paye_amount.amount
            - lst.amount
        )

        return PayrollResult(
            gross_pay=gross_pay,
            employee_nssf=employee_nssf,
            employer_nssf=employer_nssf,
            paye=paye_amount,
            local_service_tax=lst,
            net_pay=Money(max(net_pay, Decimal("0"))),
        )
# calculation works as :
# Employee NSSF is deducted from gross pay.
# Employer NSSF is reported separately; it is not deducted from the employee's net pay.
# PAYE is calculated using your existing PAYE class.
# Local Service Tax is passed in as a configurable amount.
# Net pay is calculated after employee deductions.
#the current max(..., 0) prevents negative net pay from appearing, rather than reporting a shortfall.
# python -c "from datetime import date; from src.uganda_tax_engine.payroll import Payroll; from src.uganda_tax_engine.money import Money; r = Payroll().calculate(Money.from_value('1000000'), date(2026, 10, 18)); print(r)"