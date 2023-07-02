import pandas as pd
import streamlit as st

st.set_page_config(page_title="Project Allocation Strategy Optimizer", page_icon="📈")

st.title("About 📈")

st.markdown(
    """
Welcome to our web application, a powerful tool designed for efficient project management and optimized project allocation strategies. Our engine leverages the renowned Simplex method, a widely adopted mathematical optimization technique for linear programming problems.

With the Simplex method at its core, our engine excels at identifying the ideal portfolio of projects based on several key factors, such as available resources, project costs, and expected returns. This enables you to make informed decisions and prioritize projects that will yield the best outcomes given your constraints.

Experience the benefits of streamlined project allocation and unleash the full potential of your resources with our web application. Start optimizing your projects today!
""",
    unsafe_allow_html=True,
)

st.markdown(
    """### Usage ⚙️
The web application gets in input just an excel file composed by three sheets:
- **workers**: this sheet must contains the info of the available resources (number, hours and cost per resource per hour); the table should follow this pattern
""",
    unsafe_allow_html=True,
)
worker_sheet = {
    "worker_id": ["SA", "JA"],
    "worker_division": ["Senior Account", "Junior Account"],
    "worker_numbers": [2, 8],
    "number_hour_per_workers_per_year": [160, 1720],
    "costs_per_worker_per_hour": [50, 20],
}
worker_sheet = pd.DataFrame(worker_sheet)
st.dataframe(worker_sheet, hide_index=True)

st.markdown(
    """- **project_returns**: this sheet must contains the returns of each projects; the table should follow this pattern 
""",
    unsafe_allow_html=True,
)
project_return_sheet = {
    "project_id": ["MP", "ITP"],
    "project_name": ["Marketing Project", "IT Project"],
    "project_return": [102, 8800],
}
project_return_sheet = pd.DataFrame(project_return_sheet)
st.dataframe(project_return_sheet, hide_index=True)

st.markdown(
    """- **project_work_specifics**: this sheet links each project with the required resources hours to complete it (be careful to use the same ids used in the previous sheets); the table should follow this pattern
""",
    unsafe_allow_html=True,
)
project_work_specifics = {
    "project_id": ["MP", "MP", "ITP", "ITP"],
    "worker_id": ["SA", "JA", "SA", "JA"],
    "worker_division": [
        "Senior Account",
        "Junior Account",
        "Senior Account",
        "Junior Account",
    ],
    "number_hours": [10, 5, 2, 20],
}
project_work_specifics = pd.DataFrame(project_work_specifics)
st.dataframe(project_work_specifics, hide_index=True)
st.markdown(
    "Once everything is ready, then you just drag your excel file on the app and check the results!"
)

st.markdown(
    """### Code Repository 📂
The code for this web app is available on GitHub. You can find it [here](https://github.com/stefano-polo/project-time-allocation). Feel free to explore the code, contribute, and provide feedback.

### Authors ✍️
- Stefano Polo [![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://www.linkedin.com/in/stefanopolo) [![GitHub](https://img.shields.io/badge/GitHub-Follow-black?logo=github)](https://github.com/stefano-polo)


""",
    unsafe_allow_html=True,
)
