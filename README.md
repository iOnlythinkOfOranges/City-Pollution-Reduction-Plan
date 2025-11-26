# 🌆 City-Pollution-Reduction 

## 📝 About the project
This is a simplex minimizer program. It loads the mitigation projects and pollutants CSV files, then optimizes the cost and number of project units based on the selected projects. It follows this algorithm:
* Get objective function and constraint matrix
* Transpose the matrix
* Set up the initial tableau
* Form the dual problem
* Solve using the standard simplex method
* Get the optimal solution from the bottom row of the final simplex tableau

### 🏗️ Built with 
* [![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
* [![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white)](https://numpy.org/)
* [![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
* [![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)


## 🎟️ Prerequisite
No prerequisite for using the webapp.

**To run locally**
1. Download zip
2. Extract
3. Change directory to the project folder
4. Install dependencies
   ```bash
   pip install -r requirements.txt
5. Run Streamlit
   ```bash
   streamlit run main.py

## ❓ How to use
* Click this [link](https://www.youtube.com/watch?v=zpCLWA9l0LA)
* Select projects
* Set max iterations and upper bound limit
* Click solve
* Scroll down to see the result and iterations
* Select iteration 


## ⚙️ Functionalities 
* Dark mode
* Search and sort function for projects
* Downloadable tables
* Control over max iterations and the upper bound limit
* Detailed view of tables
