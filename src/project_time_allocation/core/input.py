from typing import Any, Dict, List, Tuple

import pandas as pd
import pydantic

from project_time_allocation.core.engine.objects import Worker
from project_time_allocation.core.schemas.project import (
    ProjectHourSchema,
    ProjectReturnSchema,
)
from project_time_allocation.core.schemas.worker import WorkerSchema


def validate_project_return_sheet(
    df: pd.DataFrame, index_offset: int = 2
) -> Tuple[Dict[str, Dict[str, Any]], List[Any]]:
    df_dict_rows = df.to_dict(orient="index")
    projects_dict = {}
    bad_data = []
    for index, row in enumerate(df_dict_rows):
        try:
            pd_line_dict = (ProjectReturnSchema.parse_obj(df_dict_rows[row])).dict()
            projects_dict.update(
                {
                    pd_line_dict["project_id"]: {
                        k: pd_line_dict[k]
                        for k in set(list(pd_line_dict.keys())) - set(["project_id"])
                    }
                }
            )
        except pydantic.ValidationError as e:
            # Adds all validation error messages associated with the error
            # and adds them to the dictionary
            row["Errors"] = [error_message["msg"] for error_message in e.errors()]

            row["Error_row_num"] = index + index_offset
            bad_data.append(row)  # appends bad data to a different list of dictionaries
    return (projects_dict, bad_data)


def validate_project_hour_sheet(
    df: pd.DataFrame, index_offset: int = 2
) -> Tuple[Dict[str, List[Dict[str, Dict[str, Any]]]], List[Any]]:
    df_dict_rows = df.to_dict(orient="index")
    projects_hour_dict = {}
    bad_data = []
    for index, row in enumerate(df_dict_rows):
        try:
            pd_line_dict = (ProjectHourSchema.parse_obj(df_dict_rows[row])).dict()
            worker_id_dict = {
                pd_line_dict["worker_id"]: {
                    k: pd_line_dict[k]
                    for k in set(list(pd_line_dict.keys()))
                    - set(["project_id", "worker_id"])
                }
            }
            if pd_line_dict["project_id"] not in projects_hour_dict:
                projects_hour_dict[pd_line_dict["project_id"]] = [worker_id_dict]
            else:
                projects_hour_dict[pd_line_dict["project_id"]].append(worker_id_dict)
        except pydantic.ValidationError as e:
            # Adds all validation error messages associated with the error
            # and adds them to the dictionary
            row["Errors"] = [error_message["msg"] for error_message in e.errors()]

            row["Error_row_num"] = index + index_offset
            bad_data.append(row)  # appends bad data to a different list of dictionaries
    return (projects_hour_dict, bad_data)


def validate_worker_sheet(
    df: pd.DataFrame, index_offset: int = 2
) -> Tuple[Dict[str, Worker], List[Any]]:
    df_dict_rows = df.to_dict(orient="index")
    workers_dict = {}
    bad_data = []
    for index, row in enumerate(df_dict_rows):
        try:
            pd_line_dict = (WorkerSchema.parse_obj(df_dict_rows[row])).dict()
            workers_dict.update(
                {
                    pd_line_dict["worker_id"]: Worker(
                        worker_id=pd_line_dict["worker_id"],
                        worker_division=pd_line_dict["worker_division"],
                        number_workers=pd_line_dict["worker_numbers"],
                        total_hour_per_worker_per_year=pd_line_dict[
                            "number_hour_per_workers_per_year"
                        ],
                        cost_per_worker_per_hour=pd_line_dict[
                            "costs_per_worker_per_hour"
                        ],
                    )
                }
            )
        except pydantic.ValidationError as e:
            # Adds all validation error messages associated with the error
            # and adds them to the dictionary
            row["Errors"] = [error_message["msg"] for error_message in e.errors()]

            row["Error_row_num"] = index + index_offset
            bad_data.append(row)  # appends bad data to a different list of dictionaries
    return (workers_dict, bad_data)
