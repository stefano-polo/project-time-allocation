import os
from collections import ChainMap
from csv import QUOTE_ALL, Dialect, DictReader
from pathlib import Path
from typing import Dict, Optional

import numpy as np
from project_allocation.core.engine.objects import Project
from project_allocation.core.engine.optimizer import Optimizer
from project_allocation.core.engine.simplex_builder import (
    InequalityMatrixConstraint,
    InequalityVectorConstraint,
    LinearCoefficients,
)
from project_allocation.core.engine.utils import dict_from_lists
from project_allocation.core.input import (
    load_project_hour_file,
    load_project_return_file,
    load_worker_file,
)


def main():
    local_folder_name = "data"
    path = Path(os.path.dirname(__file__)).joinpath(local_folder_name)
    project_return_dict = load_project_return_file("project_return.csv", path)
    project_hour_dict = load_project_hour_file("project_hours.csv", path)
    workers_dict = load_worker_file("workers.csv", path)
    projects = {}
    for id_project in project_return_dict.keys():
        costs = 0.0
        hour_dict_processed = dict(ChainMap(*project_hour_dict[id_project]))
        for id_worker in hour_dict_processed.keys():
            costs += (
                hour_dict_processed[id_worker]["number_hours"]
                * workers_dict[id_worker].cost
            )
        projects.update(
            {
                id_project: Project(
                    project_id=id_project,
                    project_name=project_return_dict[id_project]["project_name"],
                    return_value=project_return_dict[id_project]["project_return"],
                    cost_value=costs,
                    workers_id_hours=hour_dict_processed,
                )
            }
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
    opt = Optimizer(linear_coeff, matrix, ineq_vec)
    res = opt.run()
    print("Optimal Allocation Strategy:")
    for project_id in projects.keys():
        print(projects[project_id].name, ": ", res[projects_map[project_id]])

    print("Total Earning:", -linear_coeff.linear_coefficients @ res, "euros")
    constraint = np.sum(
        matrix.inequality_matrix_constraint @ res
        > ineq_vec.inequality_vector_constraint
    )
    if constraint == 0:
        print("\nTime Constraint Passed!")
    else:
        raise ValueError("Time Constratint is not satisfied")

    print("\nResidual Hours")
    busy_hours = matrix.inequality_matrix_constraint @ res
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
