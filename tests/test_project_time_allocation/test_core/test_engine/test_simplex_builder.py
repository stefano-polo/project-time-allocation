import numpy as np
from pytest import fixture

from project_time_allocation.core.engine.objects import Project, Worker
from project_time_allocation.core.engine.simplex_builder import (
    InequalityMatrixConstraint,
    InequalityVectorConstraint,
    LinearCoefficients,
)

STRATEGY = np.array([10, 20])


@fixture(name="project_alpha", scope="module")
def fixture_project_alpha():
    return Project(
        project_id="123",
        project_name="alpha",
        return_value=100,
        cost_value=20,
        workers_id_hours={"001": {"number_hours": 3}, "002": {"number_hours": 5}},
    )


@fixture(name="project_beta", scope="module")
def fixture_project_beta():
    return Project(
        project_id="456",
        project_name="beta",
        return_value=1000,
        cost_value=300,
        workers_id_hours={"001": {"number_hours": 13}, "003": {"number_hours": 25}},
    )


@fixture(name="senior", scope="module")
def fixture_senior_worker():
    return Worker(
        worker_id="001",
        worker_division="senior",
        number_workers=1,
        total_hour_per_worker_per_year=20,
        cost_per_worker_per_hour=10,
    )


@fixture(name="junior", scope="module")
def fixture_junior_worker():
    return Worker(
        worker_id="002",
        worker_division="junior",
        number_workers=3,
        total_hour_per_worker_per_year=10,
        cost_per_worker_per_hour=4,
    )


@fixture(name="creative", scope="module")
def fixture_creative_worker():
    return Worker(
        worker_id="003",
        worker_division="creative",
        number_workers=2,
        total_hour_per_worker_per_year=5,
        cost_per_worker_per_hour=7,
    )


@fixture(name="projects", scope="module")
def fixture_projects(project_alpha, project_beta):
    return {
        project_alpha.project_id: project_alpha,
        project_beta.project_id: project_beta,
    }


@fixture(name="workers", scope="module")
def fixture_workers(senior, junior, creative):
    return {
        senior.worker_id: senior,
        junior.worker_id: junior,
        creative.worker_id: creative,
    }


@fixture(name="map_prj_id_index", scope="module")
def fixture_map_prj_id_index(project_alpha, project_beta):
    return {project_alpha.project_id: 0, project_beta.project_id: 1}


@fixture(name="map_wrk_id_index", scope="module")
def fixture_map_wrk_id_index(senior, junior, creative):
    return {senior.worker_id: 0, junior.worker_id: 1, creative.worker_id: 2}


def test_linear_coeff(projects, map_prj_id_index):
    lin_coeff = LinearCoefficients(projects=projects, map_id_index=map_prj_id_index)
    assert np.sum(lin_coeff.value == -np.array([80, 700])) == 2


def test_ineq_matrix(projects, map_prj_id_index, map_wrk_id_index):
    ineq_matrix = InequalityMatrixConstraint(
        projects=projects,
        map_project_id_index=map_prj_id_index,
        map_worker_id_index=map_wrk_id_index,
    )
    assert (
        np.sum(ineq_matrix.value == np.array([[3, 13], [5, 0], [0, 25]]))
        == ineq_matrix.value.shape[0] * ineq_matrix.value.shape[1]
    )


def test_ineq_constraint_vector(workers, map_wrk_id_index):
    ineq_vec = InequalityVectorConstraint(
        workers=workers, map_worker_id_index=map_wrk_id_index
    )
    assert np.sum(ineq_vec.value == np.array([20, 30, 10])) == 3
