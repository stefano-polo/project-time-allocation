from typing import Tuple

import numpy as np
import pandas as pd

from project_time_allocation.core.engine.loss import (
    ConstraintChecker,
    ConstraintValues,
    NegLossFunction,
)
from project_time_allocation.core.engine.optimizer import Optimizer
from project_time_allocation.core.engine.simplex_builder import (
    InequalityMatrixConstraint,
    InequalityVectorConstraint,
    LinearCoefficients,
)
from project_time_allocation.core.engine.utils import dict_from_lists
from project_time_allocation.core.input import (
    validate_project_hour_sheet,
    validate_project_return_sheet,
    validate_worker_sheet,
)
from project_time_allocation.core.service.service import ProjectBuildService


def upload_data(uploaded_file: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    xls = pd.ExcelFile(uploaded_file)
    workers_df = pd.read_excel(xls, "workers")
    project_work_specifics_df = pd.read_excel(xls, "project_work_specifics")
    project_returns_df = pd.read_excel(xls, "project_returns")
    return workers_df, project_work_specifics_df, project_returns_df


def run_engine(
    project_returns_df: pd.DataFrame,
    project_work_specifics_df: pd.DataFrame,
    workers_df: pd.DataFrame,
) -> Tuple:
    project_return_dict, bad_lines = validate_project_return_sheet(project_returns_df)
    project_hour_dict, bad_lines = validate_project_hour_sheet(
        project_work_specifics_df
    )
    workers_dict, bad_lines = validate_worker_sheet(workers_df)

    projects = ProjectBuildService().build_projects(
        project_return_dict=project_return_dict,
        project_hour_dict=project_hour_dict,
        workers_dict=workers_dict,
    )
    workers_map = dict_from_lists(
        list_values=np.arange(0, len(workers_dict), 1),
        list_keys=list(workers_dict.keys()),
    )
    projects_map = dict_from_lists(
        list_values=np.arange(0, len(projects), 1), list_keys=list(projects.keys())
    )
    linear_coeff = LinearCoefficients(projects=projects, map_id_index=projects_map)
    matrix = InequalityMatrixConstraint(
        projects=projects,
        map_project_id_index=projects_map,
        map_worker_id_index=workers_map,
    )
    ineq_vec = InequalityVectorConstraint(
        workers=workers_dict, map_worker_id_index=workers_map
    )
    neg_loss = NegLossFunction(lin_coeff=linear_coeff)
    constraint = ConstraintValues(constr_matrix=matrix)
    constraint_checker = ConstraintChecker(
        constr_value=constraint, constr_target=ineq_vec
    )

    result = Optimizer(linear_coeff, matrix, ineq_vec).run()

    return (
        result,
        constraint,
        constraint_checker,
        neg_loss,
        projects,
        projects_map,
        workers_dict,
        workers_map,
    )
