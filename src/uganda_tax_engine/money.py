#this application implements
# 1. Decimal instead of floating-point arithmetic.
# 2. Explicit rounding using ROUND_HALF_UP.
# 3. Immutable monetary amounts.
# 4. Required operator overloading: __add__, __mul__, __lt__, and __repr__.
# 5. Rejection of floats to prevent accidental precision errors.

"""Money value object for Ugandan shilling calculations."""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


CENT = Decimal("0.01")
ZERO = Decimal("0.00")


def to_decimal(value: Decimal | int | str) -> Decimal:
    """Convert supported numeric input to Decimal without using float."""
    if isinstance(value, bool) or isinstance(value, float):
        raise TypeError("Money values must not use float or bool.")

    try:
        return Decimal(value).quantize(CENT, rounding=ROUND_HALF_UP)
    except Exception as exc:
        raise ValueError(f"Invalid monetary amount: {value!r}") from exc


@dataclass(frozen=True, eq=False)
class Money:
    """Represent an immutable monetary amount denominated in UGX."""

    amount: Decimal

    def __post_init__(self) -> None:
        """Validate and round the amount to two decimal places."""
        object.__setattr__(self, "amount", to_decimal(self.amount))

    @classmethod
    def from_value(cls, value: Decimal | int | str) -> "Money":
        """Construct Money from a Decimal, integer, or decimal string."""
        return cls(to_decimal(value))

    def __add__(self, other: object) -> "Money":
        """Add two UGX monetary amounts."""
        if not isinstance(other, Money):
            return NotImplemented
        return Money(self.amount + other.amount)

    def __mul__(self, multiplier: Decimal | int) -> "Money":
        """Multiply an amount by a supported numeric multiplier."""
        if isinstance(multiplier, bool) or isinstance(multiplier, float):
            raise TypeError("Multiplier must not be float or bool.")
        factor = Decimal(multiplier)
        return Money(self.amount * factor)

    def __lt__(self, other: object) -> bool:
        """Compare this amount with another UGX amount."""
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount < other.amount

    def __eq__(self, other: object) -> bool:
        """Check monetary equality."""
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount

    def __repr__(self) -> str:
        """Return an unambiguous representation of the UGX amount."""
        return f"Money(UGX {self.amount:.2f})"
# python -c "from src.uganda_tax_engine.money import Money; print(Money.from_value('1000.50') + Money.from_value('200.25')); print(Money.from_value('1000') * 5); print(Money.from_value('100') < Money.from_value('200'))"
# this confirms, addition, multiplication and comparison