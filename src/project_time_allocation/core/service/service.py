from collections import ChainMap
from typing import Dict, List, Union

from project_time_allocation.core.engine.objects import Project, Worker


class ProjectBuildService:
    def build_projects(
        self,
        project_return_dict: Dict[str, Dict[str, Union[str, float]]],
        project_hour_dict: Dict[str, List[Dict]],
        workers_dict: Dict[str, Worker],
    ) -> Dict[str, Project]:
        projects = {}
        for id_project, project_return in project_return_dict.items():
            costs = 0.0
            hour_dict_processed = dict(ChainMap(*project_hour_dict[id_project]))
            for id_worker, worker_info in hour_dict_processed.items():
                costs += worker_info["number_hours"] * workers_dict[id_worker].cost
            projects.update(
                {
                    id_project: Project(
                        project_id=id_project,
                        project_name=project_return["project_name"],
                        return_value=project_return["project_return"],
                        cost_value=costs,
                        workers_id_hours=hour_dict_processed,
                    )
                }
            )
        return projects
