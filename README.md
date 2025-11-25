# City-Pollution-Reduction 🌆

## About the project 📝
This is a simplex minimizer program. It loads the mitigation projects and pollutants CSV files, then solves for the optimal cost and number of project units based on the selected projects. It follows this algorithm:
* Set up the initial tableau
* Transpose
* Form the dual problem
* Solve using the standard simplex method
* Get the optimal solution from the bottom row of the final simplex tableau

### Built with 🏗️
* [![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
* [![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white)](https://numpy.org/)
* [![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
* [![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)


## Prerequisites 🎟️
This program has no prerequisites, as it is a web app.


## How to use ❓
* Click this [link](https://www.youtube.com/watch?v=zpCLWA9l0LA)
* Select projects
* Set max iterations and upper bound limit
* Click solve
* Scroll down to see the result and iterations
* Select or input a number to see the tableau and basic solution of that iteration


## Functionalities ⚙️
* Dark mode
* Table of selectable projects
* The user can set max iterations and upper bound limit
* Shows the result table, tableau, and basic solution for every iteration
