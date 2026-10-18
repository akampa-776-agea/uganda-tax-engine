# Uganda Tax Engine

## Project Overview

The Uganda Tax Engine is an object-oriented Python mini-project designed to demonstrate the calculation of selected taxes and payroll deductions using configurable tax schedules and decimal-based monetary arithmetic.

## Features

- PAYE calculations for resident and nonresident taxpayers.
- Payroll calculations covering employee NSSF, employer NSSF, PAYE, Local Service Tax, and net pay.
- VAT calculations for standard-rated, zero-rated, and exempt supplies.
- Corporate income tax calculations using revenue and allowable deductions.
- Immutable `Money` value objects using Python's `Decimal`.
- Effective-dated PAYE schedules and custom exceptions.
- Unit testing with `pytest` and property-based testing with `Hypothesis`.

## Project Structure

- `src/uganda_tax_engine/` — tax engine implementation.
- `tests/` — unit and property-based tests.
- `requirements.txt` — Python dependencies.
- `notebooks/` — location for the final executable notebook.

## Installation

Create and activate a virtual environment, then install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Running Tests

Run the complete test suite:

```bash
python -m pytest -v
```

The current test run completed successfully with 51 passing tests.

## Important Disclaimer

This is an educational software project, not an official tax filing tool. Tax rates, effective dates, deductions, and simplified calculation assumptions must be verified against applicable Uganda Revenue Authority guidance before practical use.
