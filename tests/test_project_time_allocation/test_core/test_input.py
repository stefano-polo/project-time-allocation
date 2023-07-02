import pandas as pd
import pytest

from project_time_allocation.core.input import (
    validate_project_hour_sheet,
    validate_project_return_sheet,
    validate_worker_sheet,
)


@pytest.fixture()
def worker_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "worker_id": ["SA", "JA"],
            "worker_division": ["Senior Account", "Junior Account"],
            "worker_numbers": [2, 8],
            "number_hour_per_workers_per_year": [160, 1720],
            "costs_per_worker_per_hour": [50, 20],
        }
    )


@pytest.fixture()
def projects_return_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "project_id": ["MP", "ITP"],
            "project_name": ["Marketing Project", "IT Project"],
            "project_return": [102, 8800],
        }
    )


@pytest.fixture()
def projects_hours_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "project_id": ["MP", "MP", "ITP", "ITP"],
            "worker_id": ["SA", "JA", "SA", "JA"],
            "worker_division": [
                "Senior Account",
                "Junior Account",
                "Senior Account",
                "Junior Account",
            ],
            "number_hours": [10, 5, 2, 20],
        }
    )


def test_validate_worker_sheet(worker_df: pd.DataFrame):
    validated_values, anomaly_lines = validate_worker_sheet(worker_df)
    assert anomaly_lines == []
    assert validated_values["SA"].name == "Senior Account"
    assert validated_values["SA"].cost == 50
    assert validated_values["SA"].number_workers == 2
    assert validated_values["SA"].total_available_hour == 2 * 160


def test_validate_projects_return(projects_return_df: pd.DataFrame):
    _, anomaly_lines = validate_project_return_sheet(projects_return_df)
    assert anomaly_lines == []


def test_validate_project_hour_sheet(projects_hours_df: pd.DataFrame):
    _, anomaly_lines = validate_project_hour_sheet(projects_hours_df)
    assert anomaly_lines == []
