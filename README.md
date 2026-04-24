# Installation and setup requirements

## Dependencies
This project has the following two dependencies (required for testing):
- `pytest`
- `pytest-cov`

Please create a fresh python virtual environment (e.g., by running `python3 -m venv .venv`) and install these two packages with `pip` (`pip install pytest pytest-cov`).

If you have an existing virtual environment that has these dependecies installed, it should be fine to use it as well.

## Running tests
To execute full test suite, run `python3 -m pytest` from inside the `tests/` directory

## Reproducing coverage report
- To obtain a plain text coverage report in your terminal, run `python3 -m pytest tests --cov=src --cov-branch --cov-report=term-missing` from inside the root (`hw3`) directory
- To obtain a user-friendly html coverage report (this is the format I included in the report), run `python3 -m pytest tests --cov=src --cov-branch --cov-report=html` from inside the root (`hw3`) directory
    - To view the generated report, navigate to the `htmlcov` directory created by pytest and open the `index.html` file in your browser