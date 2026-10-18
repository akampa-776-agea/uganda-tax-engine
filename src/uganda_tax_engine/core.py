# 7 - Define the tax engine's core abstractions

# three essential components to be implemented:
# 1 TaxContext - carries the inputs a tax calculation needs.
# 2 TaxResult - stores the result and a calculation breakdown.
# 3 Tax - an abstract base class requiring every tax module to implement calculate().


"""Core abstractions shared by Uganda Tax Engine modules."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal

from src.uganda_tax_engine.money import Money


@dataclass(frozen=True)
class TaxContext:
    """Provide common inputs and configuration for a tax calculation."""

    income: Money
    effective_date: date
    residency_status: str = "resident"
    allowances: Money = field(default_factory=lambda: Money(Decimal("0")))
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class TaxResult:
    """Represent a tax calculation result and its explanation."""

    tax_name: str
    amount: Money
    taxable_amount: Money
    breakdown: dict[str, Money] = field(default_factory=dict)
    notes: tuple[str, ...] = ()


class Tax(ABC):
    """Abstract base class for individual tax calculation modules."""

    @abstractmethod
    def calculate(self, ctx: TaxContext) -> TaxResult:
        """Calculate tax using the supplied context."""
        raise NotImplementedError
# python -c "from src.uganda_tax_engine.core import Tax, TaxContext, TaxResult; print('Core imports successful'); print('Tax is abstract:', hasattr(Tax.calculate, '__isabstractmethod__'))"
# Tax is abstract: True confirms that Tax requires subclasses to implement calculate().
