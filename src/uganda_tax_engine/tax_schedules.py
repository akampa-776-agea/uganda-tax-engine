"""Effective-dated PAYE schedule configuration."""

from dataclasses import dataclass
from datetime import date

from src.uganda_tax_engine.exceptions import NoScheduleForDateError


@dataclass(frozen=True)
class PAYESchedule:
    """Define the validity period and residency type of a PAYE schedule."""

    effective_from: date
    effective_to: date | None
    residency_status: str

    def applies_on(self, calculation_date: date) -> bool:
        """Check whether the schedule applies on the supplied date."""
        return (
            calculation_date >= self.effective_from
            and (
                self.effective_to is None
                or calculation_date <= self.effective_to
            )
        )


# Placeholder dates for this educational project.
# Verify applicable dates and tax rates against official URA guidance.
PAYE_SCHEDULES = (
    PAYESchedule(
        effective_from=date(2026, 7, 1),
        effective_to=None,
        residency_status="resident",
    ),
    PAYESchedule(
        effective_from=date(2026, 7, 1),
        effective_to=None,
        residency_status="nonresident",
    ),
)


def get_paye_schedule(
    calculation_date: date,
    residency_status: str,
) -> PAYESchedule:
    """Return the schedule matching the date and residency status."""
    status = residency_status.strip().lower()

    if status not in {"resident", "nonresident"}:
        raise ValueError(
            "Residency status must be 'resident' or 'nonresident'."
        )

    for schedule in PAYE_SCHEDULES:
        if (
            schedule.residency_status == status
            and schedule.applies_on(calculation_date)
        ):
            return schedule

    raise NoScheduleForDateError(
        f"No PAYE schedule configured for {status!r} "
        f"on {calculation_date.isoformat()}."
    )