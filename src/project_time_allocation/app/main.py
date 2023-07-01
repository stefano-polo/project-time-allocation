import operator

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from project_time_allocation.app.utils import upload_data
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

st.title("Project Allocation Strategy Optimizer 📈")

uploaded_file = st.file_uploader("Upload Xlsx File for with Inputs", type="xlsx")
if uploaded_file:
    workers_df, project_work_specifics_df, project_returns_df = upload_data(
        uploaded_file
    )
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

    res = Optimizer(linear_coeff, matrix, ineq_vec).run()
    st.subheader("Optimal Allocation Strategy:")
    if not constraint_checker.value(res):
        st.markdown(
            "<span style='color:red'> ** WARNING: the following solution is not optimal: the time constraints is not satisfied!**</span>",
            unsafe_allow_html=True,
        )
    st.markdown(
        "<span style='color:green'> **💰 Potential Earning from this Strategy: {:,}**</span>".format(
            neg_loss.value(res)
        ),
        unsafe_allow_html=True,
    )
    result_map = {projects[key].name: res[projects_map[key]] for key in projects.keys()}
    result_map = dict(
        sorted(result_map.items(), key=operator.itemgetter(1), reverse=True)
    )
    df = pd.DataFrame(result_map.items(), columns=["Project", "Numbers"])
    st.dataframe(df, hide_index=True, width=800)
    fig = px.pie(df, values="Numbers", names="Project")
    st.plotly_chart(fig, theme=None, use_container_width=True)

    st.subheader("Residual Hours")
    busy_hours = constraint.value(res)
    residual_hours_dict = {
        workers_dict[worker_id].name: workers_dict[worker_id].total_available_hour
        - busy_hours[workers_map[worker_id]]
        for worker_id in workers_dict.keys()
    }
    residual_hours_dict = dict(
        sorted(residual_hours_dict.items(), key=operator.itemgetter(1), reverse=True)
    )
    df = pd.DataFrame(
        residual_hours_dict.items(), columns=["Worker Type", "Residual Hours"]
    )
    st.dataframe(df, hide_index=True, width=800)
