# PAYE is implemented as a separate class that inherits from Tax

"""Pay As You Earn (PAYE) tax calculation module."""

from decimal import Decimal

from src.uganda_tax_engine.core import Tax, TaxContext, TaxResult
from src.uganda_tax_engine.money import Money
from src.uganda_tax_engine.exceptions import InvalidIncomeError
# 3: Connecting  the schedule to PAYE
from src.uganda_tax_engine.tax_schedules import get_paye_schedule
from src.uganda_tax_engine.exceptions import (
    InvalidIncomeError,
    NoScheduleForDateError,
)

class PAYE(Tax):
    """Calculate monthly PAYE using the project's resident tax bands."""

    def calculate(self, ctx: TaxContext) -> TaxResult:
        income = ctx.income.amount - ctx.allowances.amount

        if income < Decimal("0"):
            raise InvalidIncomeError("Taxable income cannot be negative.")

        # if ctx.residency_status.lower() != "resident":
        #     raise NotImplementedError("Nonresident PAYE schedule will be implemented separately.")

        # if income <= Decimal("335000"):
        #     tax = Decimal("0")
        # elif income <= Decimal("410000"):
        #     tax = (income - Decimal("335000")) * Decimal("0.20")
        # elif income <= Decimal("485000"):
        #     tax = ( Decimal("15000") + (income - Decimal("410000")) * Decimal("0.25"))
        # elif income <= Decimal("10000000"):
        #     tax = (Decimal("33750") + (income - Decimal("485000")) * Decimal("0.30"))
        # else:
        #     tax = ( Decimal("2888250")  + (income - Decimal("10000000")) * Decimal("0.10"))
        schedule = get_paye_schedule(
            ctx.effective_date,
            ctx.residency_status,
        )

        status = schedule.residency_status
        #status = ctx.residency_status.strip().lower()

        #if status not in {"resident", "nonresident"}:
            #raise ValueError("Residency status must be 'resident' or 'nonresident'.")

        if status == "nonresident":
            if income <= Decimal("335000"):
                tax = income * Decimal("0.10")
            elif income <= Decimal("410000"):
                tax = ( Decimal("33500") + (income - Decimal("335000")) * Decimal("0.20"))
            elif income <= Decimal("10000000"):
                tax = ( Decimal("48500") + (income - Decimal("410000")) * Decimal("0.30"))
            else:
                tax = ( Decimal("48500") + (income - Decimal("410000")) * Decimal("0.30") + (income - Decimal("10000000")) * Decimal("0.10"))

        else:
            if income <= Decimal("335000"):
                tax = Decimal("0")
            elif income <= Decimal("410000"):
                tax = (income - Decimal("335000")) * Decimal("0.20")
            elif income <= Decimal("485000"):
                tax = (Decimal("15000") + (income - Decimal("410000")) * Decimal("0.25"))
            elif income <= Decimal("10000000"):
                tax = ( Decimal("33750")  + (income - Decimal("485000")) * Decimal("0.30") )
            else:
                tax = ( Decimal("33750") + (income - Decimal("485000")) * Decimal("0.30") + (income - Decimal("10000000")) * Decimal("0.10") )
        

        # return TaxResult( tax_name="PAYE", amount=Money(tax), taxable_amount=Money(income),breakdown={"PAYE": Money(tax)}, notes=(
        #         "Calculated using the resident PAYE bands specified in the project brief.",),)
        
        return TaxResult(
            tax_name="PAYE",
            amount=Money(tax),
            taxable_amount=Money(income),
            breakdown={"PAYE": Money(tax)},
            notes=(
                f"Calculated using the {status} PAYE schedule "
                f"effective from {schedule.effective_from.isoformat()}",
            ),
        )

# python -c "from src.uganda_tax_engine.paye import PAYE; print('PAYE module imports successfully')"
# test the PAYE calculations at the tax-band boundaries before adding more features.

# results 
# The eight resident PAYE boundary tests pass.
# Negative taxable income raises the expected exception.
# Nonresident PAYE is calculated separately from resident PAYE.
# 