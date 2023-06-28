import os
from pathlib import Path

import numpy as np

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
    load_project_hour_file,
    load_project_return_file,
    load_worker_file,
)
from project_time_allocation.core.service.service import ProjectBuildService


def main():
    local_folder_name = "data"
    path = Path(os.path.dirname(__file__)).joinpath(local_folder_name)
    project_return_dict = load_project_return_file("project_return.csv", path)
    project_hour_dict = load_project_hour_file("project_hours.csv", path)
    workers_dict = load_worker_file("workers.csv", path)
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

    res = Optimizer(linear_coeff, matrix, ineq_vec).run()
    print("Optimal Allocation Strategy:")
    for project_id in projects.keys():
        print(projects[project_id].name, ": ", res[projects_map[project_id]])

    print("Total Earning:", neg_loss.value(res), "euros")
    if constraint_checker.value(res):
        print("\nTime Constraint Passed!")
    else:
        raise ValueError("Time Constratint is not satisfied")

    print("\nResidual Hours")
    busy_hours = constraint.value(res)
    for worker_id in workers_dict:
        print(
            workers_dict[worker_id].name,
            ":",
            workers_dict[worker_id].total_available_hour
            - busy_hours[workers_map[worker_id]],
            " hours",
        )


if __name__ == "__main__":
    main()
