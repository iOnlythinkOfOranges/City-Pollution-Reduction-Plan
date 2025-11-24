# City-Pollution-Reduction

## About the project
This is a simplex minimizer program. It loads the mitigation projects and pollutants CSV files. It solves for the optimal cost and number of project units by following this algorithm:
* Set up the initial tableau
* Tranpose
* Form the dual problem
* Solve using the standard simplex method
* Get the optimal solution from the bottom row of the final simplex tableau
