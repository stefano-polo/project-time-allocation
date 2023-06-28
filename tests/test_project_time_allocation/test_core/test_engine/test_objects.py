from pytest import fixture

from project_time_allocation.core.engine.objects import Project, Worker


@fixture(name="project_alpha", scope="module")
def fixture_project_alpha():
    return Project(
        project_id="123",
        project_name="alpha",
        return_value=100,
        cost_value=20,
        workers_id_hours={"001": {"number_hours": 3}, "002": {"number_hours": 5}},
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


def test_project(project_alpha):
    assert project_alpha.cost == 20
    assert project_alpha.name == "alpha"
    assert project_alpha.project_id == "123"
    assert project_alpha.worker_id_hours == {
        "001": {"number_hours": 3},
        "002": {"number_hours": 5},
    }
    assert project_alpha.return_value == 100


def test_worker(junior):
    assert junior.worker_id == "002"
    assert junior.name == "junior"
    assert junior.number_workers == 3
    assert junior.total_available_hour == 30
    assert junior.cost == 4
