
"""Corporate income tax calculations for the Uganda Tax Engine."""

from decimal import Decimal

from src.uganda_tax_engine.core import Tax, TaxContext, TaxResult
from src.uganda_tax_engine.money import Money
from src.uganda_tax_engine.exceptions import InvalidIncomeError


class CorporateTax(Tax):
    """Calculate corporate tax on chargeable income."""

    TAX_RATE = Decimal("0.30")


    def calculate(self, ctx: TaxContext) -> TaxResult:
        """Calculate corporate tax on chargeable income."""

        revenue = ctx.income.amount
        deductions = Decimal(
            str(ctx.metadata.get("allowable_deductions", "0"))
        )

        if revenue < 0 or deductions < 0:
            raise InvalidIncomeError(
                "Revenue and allowable deductions cannot be negative."
            )

        chargeable_income = max(
            revenue - deductions,
            Decimal("0"),
        )

        tax = chargeable_income * self.TAX_RATE

        return TaxResult(
            tax_name="Corporate Income Tax",
            amount=Money(tax),
            taxable_amount=Money(chargeable_income),
            breakdown={
                "revenue": Money(revenue),
                "allowable_deductions": Money(deductions),
                "chargeable_income": Money(chargeable_income),
                "corporate_tax": Money(tax),
            },
            notes=("Calculated using the project's configured corporate tax rate.",),
        )
# python -c "from datetime import date; from src.uganda_tax_engine.core import TaxContext; from src.uganda_tax_engine.money import Money; from src.uganda_tax_engine.corporate_tax import CorporateTax; c = TaxContext(income=Money.from_value('10000000'), effective_date=date(2026, 10, 18), metadata={'allowable_deductions': '4000000'}); print(CorporateTax().calculate(c))"