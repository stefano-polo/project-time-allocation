from typing import Dict

import numpy as np

from project_time_allocation.core.engine.objects import Project, Worker


class LinearCoefficients:
    def __init__(
        self, projects: Dict[str, Project], map_id_index: Dict[str, int]
    ) -> None:
        self._linear_coefficients = np.zeros(len(projects))
        for project_id in projects.keys():
            index = map_id_index[project_id]
            self._linear_coefficients[index] = -(
                projects[project_id].return_value - projects[project_id].cost
            )

    @property
    def value(self) -> np.ndarray:
        return self._linear_coefficients


class InequalityMatrixConstraint:
    def __init__(
        self,
        projects: Dict[str, Project],
        map_project_id_index: Dict[str, int],
        map_worker_id_index: Dict[str, int],
    ) -> None:
        self._inequality_matrix_constraint = np.zeros(
            (len(map_worker_id_index), len(map_project_id_index))
        )
        for project_id in projects.keys():
            columns_index = map_project_id_index[project_id]
            for worker_id in projects[project_id].worker_id_hours.keys():
                row_index = map_worker_id_index[worker_id]
                self._inequality_matrix_constraint[row_index, columns_index] = projects[
                    project_id
                ].worker_id_hours[worker_id]["number_hours"]

    @property
    def value(self) -> np.ndarray:
        return self._inequality_matrix_constraint


class InequalityVectorConstraint:
    def __init__(
        self,
        workers: Dict[str, Worker],
        map_worker_id_index: Dict[str, int],
    ) -> None:
        self._inequality_vector_constraint = np.zeros(len(map_worker_id_index))
        for worker_id in workers.keys():
            index = map_worker_id_index[worker_id]
            self._inequality_vector_constraint[index] = workers[
                worker_id
            ].total_available_hour

    @property
    def value(self) -> np.ndarray:
        return self._inequality_vector_constraint
