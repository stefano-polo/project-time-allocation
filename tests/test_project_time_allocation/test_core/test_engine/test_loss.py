import numpy as np
from pytest import fixture

from project_time_allocation.core.engine.loss import (
    ConstraintChecker,
    ConstraintValues,
    NegLossFunction,
)
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


def test_negative_loss(projects, map_prj_id_index):
    lin_coeff = LinearCoefficients(projects=projects, map_id_index=map_prj_id_index)
    loss = NegLossFunction(lin_coeff=lin_coeff)
    assert loss.value(strategy=STRATEGY) == 10 * (100 - 20) + 20 * (1000 - 300)


def test_contraint_values(projects, map_prj_id_index, map_wrk_id_index):
    ineq_matrix = InequalityMatrixConstraint(
        projects=projects,
        map_project_id_index=map_prj_id_index,
        map_worker_id_index=map_wrk_id_index,
    )
    constraint_f = ConstraintValues(constr_matrix=ineq_matrix)
    assert np.sum(constraint_f.value(STRATEGY) == np.array([290, 50, 500])) == 3


def test_constraint_checker(projects, workers, map_prj_id_index, map_wrk_id_index):
    ineq_matrix = InequalityMatrixConstraint(
        projects=projects,
        map_project_id_index=map_prj_id_index,
        map_worker_id_index=map_wrk_id_index,
    )
    constraint_f = ConstraintValues(constr_matrix=ineq_matrix)
    ineq_vec = InequalityVectorConstraint(
        workers=workers, map_worker_id_index=map_wrk_id_index
    )
    cons_checker = ConstraintChecker(constr_value=constraint_f, constr_target=ineq_vec)
    assert cons_checker.value(STRATEGY) == False
    assert cons_checker.value(np.array([0.0, 0.0])) == True
    assert cons_checker.value(np.array([1.0, 0.0])) == True
