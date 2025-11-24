# City-Pollution-Reduction

## About the project 📝
This is a simplex minimizer program. It loads the mitigation projects and pollutants CSV files. It solves for the optimal cost and number of project units based on the selected projects. It follows this algorithm:
* Set up the initial tableau
* Transpose
* Form the dual problem
* Solve using the standard simplex method
* Get the optimal solution from the bottom row of the final simplex tableau

### Built with 🏗️
* [![Python][Python.org]][https://www.python.org/]
* [![NumPy][NumPy.org]][https://numpy.org/]
* [![Pandas][Pandas.pydata.org]][https://pandas.pydata.org/]
* [![Streamlit][Streamlit.io]][https://streamlit.io/]
  
## Prerequisites 🎟️
This program has no prerequisites, as it is a web app.

## How to use ❓
* Click this link
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
