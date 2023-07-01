from typing import Tuple

import pandas as pd
import streamlit as st


def upload_data(uploaded_file: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    xls = pd.ExcelFile(uploaded_file)
    workers_df = pd.read_excel(xls, "workers")
    project_work_specifics_df = pd.read_excel(xls, "project_work_specifics")
    project_returns_df = pd.read_excel(xls, "project_returns")
    return workers_df, project_work_specifics_df, project_returns_df
