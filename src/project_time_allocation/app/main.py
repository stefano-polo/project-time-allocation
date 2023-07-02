import operator

import pandas as pd
import plotly.express as px
import streamlit as st

from project_time_allocation.app.utils import run_engine, upload_data


def main():
    st.title("Project Allocation Strategy Optimizer 📈")
    st.write("\n\n")

    uploaded_file = st.file_uploader("📝 Upload Xlsx File for with Inputs", type="xlsx")
    if uploaded_file:
        workers_df, project_work_specifics_df, project_returns_df = upload_data(
            uploaded_file
        )

        (
            res,
            constraint,
            constraint_checker,
            neg_loss,
            projects,
            projects_map,
            workers_dict,
            workers_map,
        ) = run_engine(project_returns_df, project_work_specifics_df, workers_df)
        st.subheader("⭐ Optimal Allocation Strategy:")
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
        result_map = {
            projects[key].name: res[projects_map[key]] for key in projects.keys()
        }
        result_map = dict(
            sorted(result_map.items(), key=operator.itemgetter(1), reverse=True)
        )
        df = pd.DataFrame(result_map.items(), columns=["Project", "Numbers"])
        st.dataframe(df, hide_index=True, width=800)
        fig = px.pie(df, values="Numbers", names="Project")
        st.plotly_chart(fig, theme=None, use_container_width=True)

        st.subheader("🕒 Residual Hours")
        busy_hours = constraint.value(res)
        residual_hours_dict = {
            workers_dict[worker_id].name: workers_dict[worker_id].total_available_hour
            - busy_hours[workers_map[worker_id]]
            for worker_id in workers_dict.keys()
        }
        residual_hours_dict = dict(
            sorted(
                residual_hours_dict.items(), key=operator.itemgetter(1), reverse=True
            )
        )
        df = pd.DataFrame(
            residual_hours_dict.items(), columns=["Worker Type", "Residual Hours"]
        )
        st.dataframe(df, hide_index=True, width=800)

        st.subheader("🛠️ Projects' Specific")
        i = 0
        for key in projects.keys():
            project_i = projects[key]
            with st.expander("**" + project_i.name + "**"):
                st.markdown("- **Return**: {:,}".format(project_i.return_value))
                st.markdown("- **Total Cost**: {:,}".format(project_i.cost))
                string = """- **Required Resources:**"""
                for worker_id in project_i.worker_id_hours.keys():
                    worker = project_i.worker_id_hours[worker_id]
                    substring = "\n    - {}: {} hours".format(
                        worker["worker_division"], worker["number_hours"]
                    )
                    string += substring
                st.markdown(string)

        st.subheader("👷🏻 Available Resources")
        i = 0
        for worker_id in workers_dict.keys():
            worker = workers_dict[worker_id]
            with st.expander("**" + worker.name + "**"):
                st.markdown("- **Resource number**: {:,}".format(worker.number_workers))
                st.markdown(
                    "- **Available hours per resource**: {:,}".format(
                        worker.total_available_hour / worker.number_workers
                    )
                )
                st.markdown(
                    "- **Cost per hour per resource**: {:,}".format(worker.cost)
                )
