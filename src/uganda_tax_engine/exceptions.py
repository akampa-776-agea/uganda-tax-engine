# 6 - Create the custom exception hierarchy
# These exceptions will help the tax engine report invalid income,
# missing tax schedules, and other tax-related errors explicitly instead of failing silently.

"""Custom exceptions for the Uganda Tax Engine."""


class TaxError(Exception):
    """Base exception for tax engine errors."""


class InvalidIncomeError(TaxError):
    """Raised when income or another monetary input is invalid."""


class NoScheduleForDateError(TaxError):
    """Raised when no applicable tax schedule exists for a given date."""
# python -c "from src.uganda_tax_engine.exceptions import TaxError, InvalidIncomeError, NoScheduleForDateError; print(issubclass(InvalidIncomeError, TaxError)); print(issubclass(NoScheduleForDateError, TaxError))"
# True, True - confirms that both specific exceptions inherit from TaxError, giving us a consistent exception hierarchy.
