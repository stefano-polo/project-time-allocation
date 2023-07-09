# Project Allocation Strategy Optimizer 📈
[![python](https://img.shields.io/badge/Python-3.8-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
![Tests](https://github.com/stefano-polo/project_allocation_strategy/actions/workflows/python-tests.yml/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.22.0-FF4B4B.svg?style=flat&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repo aims to provide a tool for efficient project management and optimized project allocation strategies. 

The engine leverages the renowned Simplex method, a widely adopted mathematical optimization technique for linear programming problems.

With the Simplex method at its core, the tool will identify the ideal portfolio of projects based on several key factors, such as available resources, project costs, and expected returns. This will enable the user to make informed decisions and prioritize projects that will yield the best outcomes given your constraints.

## Installation ⚙️

This project uses the package manager poetry. To install poetry then run
```
pip install poetry 
```
After installing poetry then you must config the following flag
```
poetry config virtualenvs.in-project true
```
To intall the dependendencies then run the command
```
poetry install
```
To activate the virtual environment then run 
```
poetry shell
```

## Usage 🚀
To run the web app on your local machine, use the following command:
```
streamlit run src/project_time_allocation/app/Home.py
```
This will start the app using Streamlit. You can then access the web app through your browser.


## License 📄
This project is licensed under the MIT License.

## Authors ✍️
This project is developed and maintained by:
- [Stefano Polo](https://github.com/stefano-polo)