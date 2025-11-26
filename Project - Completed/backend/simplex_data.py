"""
Mitigation Projects Data

Contains the complete pollutant reductions per project unit data.
Complete Pollutant Reductions per Project Unit data
"""

import pandas as pd
import os

class problem_data:
    def __init__(self, csv_file="projects.csv", constraints_file="constraints.csv"):
        # Load decision variables from CSV
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"CSV file not found: {csv_file}")
        
        df = pd.read_csv(csv_file)
        
        # Remove 'Select' column if it exists (not needed for backend)
        # Streamlit creates the CSV with 'Select' column. 
        # I decided to keep the CSV as is and filter out the select column
        if "Select" in df.columns:
            df = df.drop(columns=["Select"])
        
        # Set "Mitigation Project" as index
        if "Mitigation Project" in df.columns:
            df.set_index("Mitigation Project", inplace=True)
        else:
            raise ValueError("CSV file must contain 'Mitigation Project' column")
        
        self.decision_variables_df = df

        # Load constraints from CSV
        if os.path.exists(constraints_file):
            constraints_df = pd.read_csv(constraints_file)
            # Assume format: first column = name, second column = target value
            if len(constraints_df.columns) >= 2:
                self.constraints = dict(zip(constraints_df.iloc[:, 0], constraints_df.iloc[:, 1]))
            else:
                raise ValueError(f"Constraints CSV must have at least 2 columns: {constraints_file}")
        else:
            # Set to 0 as default constraints if file doesn't exist
            pollutant_columns = [col for col in df.columns if col != "Cost"]
            self.constraints = {col: 0 for col in pollutant_columns}


    def get_decision_variables_df(self):
        return self.decision_variables_df
    
    def get_constraints(self):
        return self.constraints
    

