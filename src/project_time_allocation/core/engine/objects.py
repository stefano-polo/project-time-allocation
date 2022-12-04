""" Object classes"""
from typing import Dict


class Project:
    def __init__(
        self,
        project_id: str,
        project_name: str,
        return_value: float,
        cost_value: float,
        workers_id_hours: Dict[str, int],
    ) -> None:
        self._project_id = project_id
        self._project_name = project_name
        self._return_value = return_value
        self._cost = cost_value
        self._workers_id_hours = workers_id_hours

    @property
    def project_id(self) -> str:
        return self._project_id

    @property
    def name(self) -> str:
        return self._project_name

    @property
    def return_value(self) -> float:
        return self._return_value

    @property
    def cost(self) -> float:
        return self._cost

    @property
    def worker_id_hours(self) -> Dict[str, int]:
        return self._workers_id_hours


class Worker:
    def __init__(
        self,
        worker_id: str,
        worker_division: str,
        number_workers: int,
        total_hour_per_worker_per_year: int,
        cost_per_worker_per_hour: float,
    ) -> None:
        self._worker_id = worker_id
        self._worker_division = worker_division
        self._n_workers = number_workers
        self._total_hour_per_worker_per_year = total_hour_per_worker_per_year
        self._cost_per_worker_per_hour = cost_per_worker_per_hour
        self._total_available_hour = (
            self._total_hour_per_worker_per_year * self._n_workers
        )

    @property
    def worker_id(self) -> str:
        return self._worker_id

    @property
    def name(self) -> str:
        return self._worker_division

    @property
    def number_workers(self) -> float:
        return self._n_workers

    @property
    def total_available_hour(self) -> float:
        return self._total_available_hour

    @property
    def cost(self) -> float:
        return self._cost_per_worker_per_hour
