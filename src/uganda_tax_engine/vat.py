# Create the VAT module
# We'll implement VAT calculations for standard-rated, zero-rated, and exempt supplies, including output VAT, input VAT, and net VAT payable.
# imports and VAT class


"""VAT calculations for the Uganda Tax Engine."""

from decimal import Decimal

from src.uganda_tax_engine.core import Tax, TaxContext, TaxResult
from src.uganda_tax_engine.money import Money
from src.uganda_tax_engine.exceptions import InvalidIncomeError


class VAT(Tax):
    """Calculate VAT for standard-rated, zero-rated, and exempt supplies."""

    STANDARD_RATE = Decimal("0.18")
    ZERO_RATE = Decimal("0.00")

#VAT inherits from the abstract Tax class.
# The standard VAT rate is configured as 18%.
# Zero-rated supplies use a 0% output VAT rate.
# Exempt supplies will be handled separately because their input VAT treatment differs.

# 2: Implement calculate()

    def calculate(self, ctx: TaxContext) -> TaxResult:
        """Calculate output VAT and net VAT payable."""

        supply_type = str( ctx.metadata.get("supply_type", "standard") ).strip().lower()

        if supply_type not in {"standard", "zero_rated", "exempt"}:
            raise ValueError( "supply_type must be 'standard', 'zero_rated', or 'exempt'." )

        sales = ctx.income.amount
        input_vat = Decimal( str(ctx.metadata.get("input_vat", "0")) )

        if sales < 0 or input_vat < 0:
            raise InvalidIncomeError(   "Sales and input VAT cannot be negative." )

        if supply_type == "standard":
            output_vat = sales * self.STANDARD_RATE
        else:
            output_vat = Decimal("0")

        if supply_type == "exempt":
            deductible_input_vat = Decimal("0")
        else:
            deductible_input_vat = input_vat

        net_vat = output_vat - deductible_input_vat

        return TaxResult(
            tax_name="VAT",
            amount=Money(max(net_vat, Decimal("0"))),
            taxable_amount=Money(  sales if supply_type == "standard" else Decimal("0")),
            breakdown={
                "output_vat": Money(output_vat),
                "input_vat": Money(input_vat),
                "deductible_input_vat": Money(deductible_input_vat),
                "net_vat_payable": Money(max(net_vat, Decimal("0"))),
                "vat_credit": Money(max(-net_vat, Decimal("0"))),
            },
            notes=(f"Supply type: {supply_type}.",),
        )

# ctx.income represents sales while ctx.metadata carries supply_type and input_vat.
# For example, supply_type="standard" applies 18% output VAT.
# python -c "from src.uganda_tax_engine.vat import VAT; print('VAT module imported successfully')"