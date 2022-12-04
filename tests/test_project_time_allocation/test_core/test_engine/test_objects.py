from project_time_allocation.core.engine.objects import Project, Worker


def test_project():

    proj = Project(
        project_id="11",
        project_name="project",
        return_value=1230.2,
        cost_value=100,
        workers_id_hours={"123": 10, "124": 20},
    )
    assert proj.cost == 100
    assert proj.name == "project"
    assert proj.project_id == "11"
    assert proj.worker_id_hours == {"123": 10, "124": 20}
    assert proj.return_value == 1230.2


def test_worker():
    worker = Worker(
        worker_id="123",
        worker_division="Senior",
        number_workers=10,
        total_hour_per_worker_per_year=120,
        cost_per_worker_per_hour=11,
    )
    assert worker.worker_id == "123"
    assert worker.name == "Senior"
    assert worker.number_workers == 10
    assert worker.total_available_hour == 1200
    assert worker.cost == 11
