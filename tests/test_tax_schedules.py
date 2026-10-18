
from datetime import date

import pytest

from src.uganda_tax_engine.exceptions import NoScheduleForDateError
from src.uganda_tax_engine.tax_schedules import (
    PAYESchedule,
    get_paye_schedule,
)


def test_schedule_applies_on_start_date():
    schedule = PAYESchedule(
        effective_from=date(2026, 7, 1),
        effective_to=date(2026, 12, 31),
        residency_status="resident",
    )

    assert schedule.applies_on(date(2026, 7, 1))


def test_schedule_applies_on_end_date():
    schedule = PAYESchedule(
        effective_from=date(2026, 7, 1),
        effective_to=date(2026, 12, 31),
        residency_status="resident",
    )

    assert schedule.applies_on(date(2026, 12, 31))


def test_schedule_rejects_date_after_end_date():
    schedule = PAYESchedule(
        effective_from=date(2026, 7, 1),
        effective_to=date(2026, 12, 31),
        residency_status="resident",
    )

    assert not schedule.applies_on(date(2027, 1, 1))


def test_open_ended_schedule_applies_to_future_date():
    schedule = PAYESchedule(
        effective_from=date(2026, 7, 1),
        effective_to=None,
        residency_status="resident",
    )

    assert schedule.applies_on(date(2030, 1, 1))


def test_unknown_date_has_no_matching_schedule():
    with pytest.raises(NoScheduleForDateError):
        get_paye_schedule(
            calculation_date=date(2026, 6, 30),
            residency_status="resident",
        )
# These tests use a temporary, illustrative end date solely to test the date-handling logic. They do not assert that 31 December 2026 is an official Uganda PAYE schedule end date.