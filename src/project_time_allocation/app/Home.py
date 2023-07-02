import streamlit as st

from project_time_allocation.app.main import main

st.set_page_config(page_title="Project Allocation Strategy Optimizer", page_icon="📈")

if __name__ == "__main__":
    main()
