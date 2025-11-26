import numpy as np

class SimplexSolver:
    def __init__(self, selected_variables, constraints):
        self.selected_variables = selected_variables
        self.constraints = constraints
        self.tableau = None
        self.initial_tableau = None
        self.tableau_iterations = []
        self.basic_solution_iterations = []
        self.optimal_solution = None
        self.final_basic_solution = None
        self.table_breakdown = None
        self.tol = 1e-9  # numerical tolerance


    def build_tableau(self, upper_bound=20):
        """
        Build tableau for the dual problem (a maximization)
        """
        constraints_list = list(self.constraints.keys())
        RHS = np.array([self.constraints[p] for p in constraints_list], dtype=float)                    # length constraint
        constraints_matrix = self.selected_variables[constraints_list].values.T.astype(float)           # shape (constraint, selected)
        objective_coeff = self.selected_variables["Cost"].values.astype(float)                          # length selected
        n_projects = constraints_matrix.shape[1]

        # upper bounds for projects
        upper_bounds_vector = np.full(n_projects, float(upper_bound), dtype=float)

        # build the tableau
        tableau = np.hstack([constraints_matrix.T, -np.eye(n_projects), np.eye(n_projects), np.zeros((n_projects, 1)), objective_coeff.reshape(-1,1)])

        # Objective row
        obj_row = np.hstack([-RHS, upper_bounds_vector, np.zeros(n_projects, dtype=float), np.array([1.0]), np.array([0.0])])

        tableau = np.vstack([tableau, obj_row.astype(float)])
        self.tableau = tableau
        self.initial_tableau = tableau.copy()
    

    def find_pivot(self):
        # Find pivot column
        last_row = self.tableau[-1,:-1]
        pivot_col_index = np.argmin(last_row)
        pivot_col = self.tableau[:-1, pivot_col_index]
        rhs = self.tableau[:-1, -1]

        ratios = np.full_like(rhs, np.inf, dtype = float)
        positive_mask = pivot_col > self.tol

        if not positive_mask.any():
            raise ValueError("Unbounded LP: no positive entries in pivot column")
        
        ratios[positive_mask] = rhs[positive_mask] / pivot_col[positive_mask]

        pivot_row_index = np.argmin(ratios)
        return pivot_row_index, pivot_col_index


    def pivot(self, pivot_row, pivot_col):
        pivot_element = self.tableau[pivot_row, pivot_col]
        self.tableau[pivot_row] /= pivot_element
        
        for row in range(self.tableau.shape[0]):
            if row != pivot_row:
                self.tableau[row] -= self.tableau[row][pivot_col] * self.tableau[pivot_row]


    def extract_basic_solution(self):
        # Convert everything to Python floats
        row = self.tableau[-1]
        basic_solution = [float(x) for x in row[:-2]]
        basic_solution.append(float(row[-1]))
        self.basic_solution_iterations.append(basic_solution)


    def is_dual_infeasible(self):
        for row in self.tableau[:-1]:  # ignore objective
            rhs = row[-1]
            coefs = row[:-1]
            if rhs < 0 and np.all(coefs <= 0):
                return True
        return False


    def build_table_breakdown(self):
        # Extract the table variables and the costs
        table_variables = self.selected_variables.index.tolist()
        cost_vector = self.selected_variables["Cost"].values.astype(float)
        num_projects = len(cost_vector)
        
        # Get the decision variables x
        x_values = self.final_basic_solution[-1 - num_projects: -1]
        x_values = np.array(x_values)

        # Compute for the cost breakdown per project
        cost_breakdown = x_values * cost_vector

        self.table_breakdown = {
        "Z": float(self.optimal_solution),
        "x_values": x_values.tolist(),
        "project_names": list(self.selected_variables.index),
        "cost_vector": cost_vector.tolist(),
        "cost_breakdown": cost_breakdown.tolist(),
        }

        return self.table_breakdown


    def solve(self, max_iterations = 1000):
        # Check dual feasibility first
        if self.is_dual_infeasible():
            raise ValueError("Initial tableau has negative RHS (dual infeasible)")
        

        iterations = 0
        # Dual simplex iterations
        while np.any(self.tableau[-1,:-1] < 0):
            if iterations >= max_iterations: 
                raise RuntimeError("Maximum iterations reached. Possible cycling.")
                    
            pivot_row, pivot_col = self.find_pivot()
            self.pivot(pivot_row, pivot_col)
            self.tableau_iterations.append(self.tableau.copy())
            self.extract_basic_solution()

            if self.is_dual_infeasible():
                raise ValueError("Dual infeasible solution during iterations.")

            iterations += 1

        self.optimal_solution = self.tableau[-1, -1]
        self.final_basic_solution = self.basic_solution_iterations[-1]
        self.build_table_breakdown()
    

