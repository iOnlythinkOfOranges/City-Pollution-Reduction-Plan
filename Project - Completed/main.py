import streamlit as st
from backend.simplex_data import problem_data
import pandas as pd

st.set_page_config(
    page_title="Simplex Minimizer",
    page_icon="🗃️",
    layout="wide"
)

col1, col2 = st.columns([10,1])

with col1:
    st.title("🌆 City Pollution Reduction Optimization")

with col2:
    st.link_button("Info", "https://github.com/iOnlythinkOfOranges/City-Pollution-Reduction", type="primary", icon="❔", help="Click to see info and Github Repository.")

with st.container(border=True):
    st.subheader("🌳 Mitigation Projects Database")
    # Load data
    # Error handling
    data = problem_data()
    try:
        df_original = data.get_decision_variables_df()
    except (FileNotFoundError) as e:
        error_msg = str(e)
        st.toast(f"❌ :red[**{error_msg}**]")


    # Initialize selection state
    if "selected_projects" not in st.session_state:
        st.session_state.selected_projects = []
    if "table_selection" not in st.session_state:
        st.session_state.table_selection = [False] * len(df_original)



    # Search Projects 
    search_query = st.text_input("Search Projects", placeholder="Type to search...", key="project_search")

    # Filter dataframe based on search query
    if search_query:
        mask = df_original.index.str.contains(search_query, case=False, na=False)
        df_filtered = df_original[mask]
    else:
        df_filtered = df_original


    # Build a table with checkbox 
    if len(df_filtered) == 0:
        st.info("No projects found matching your search.")
        df = pd.DataFrame()
    else:
        df = df_filtered.copy()

        # Get selection state for filtered projects
        filtered_selection = [st.session_state.table_selection[df_original.index.get_loc(idx)] 
                                for idx in df_filtered.index]
        
        # The first column = selection state
        df.insert(0, "Select", filtered_selection)

        edited_df = st.data_editor(
            df,
            column_config={
                "Select": st.column_config.CheckboxColumn(
                    "Select",
                    help="Tick to include project",
                    width="small",
                )
            },
            hide_index=False,
            use_container_width=True
        )

        # Update selections in session state
        new_selection_mask = edited_df["Select"].tolist()
        
        # Update the full selection state based on filtered results
        for i, idx in enumerate(df_filtered.index):
            original_idx = df_original.index.get_loc(idx)
            st.session_state.table_selection[original_idx] = new_selection_mask[i]


    # Get selected projects from the full original dataframe
    selected_projects = [idx for idx in df_original.index 
                        if st.session_state.table_selection[df_original.index.get_loc(idx)]]
    st.session_state.selected_projects = selected_projects


    # Buttons
    row1col1, row1col2= st.columns([1,1], gap="small")

    with row1col1:
        upper_bound = st.number_input(
            "Upper Bound Limit",
            min_value=0,
            value=20,
            step=1,
        )

    with row1col2:
        max_iter = st.number_input(
            "Max Iterations",
            min_value=0,
            value=1000,
            step=1,
        )

    row2col1, row2col2, row2col3 = st.columns([1,1,1],gap="small")
    # Select all button
    with row2col1:
        if st.button("Select All", use_container_width=True):
            st.session_state.table_selection = [True] * len(df_original)
            st.session_state.selected_projects = df_original.index.tolist()

    # Clear selection button
    with row2col2:
        if st.button("Clear", use_container_width=True):
            st.session_state.table_selection = [False] * len(df_original)
            st.session_state.selected_projects = []

    # Solver button logic
    with row2col3:
        if st.button("Solve LP", use_container_width=True):
            selected_df = df_original.loc[st.session_state.selected_projects]

            from backend.simplex_solver import SimplexSolver

            # Error handling catch missing csv, infeasibility, unboundedness, max iter
            try:
                solver = SimplexSolver(selected_df, data.get_constraints())
                solver.build_tableau(upper_bound)
                solver.solve(max_iter)

                st.session_state["solver"] = solver
                st.toast("✅ :green[**LP Solved! Scroll down to see Results and Iterations.**]")

            except (ValueError, RuntimeError) as e:
                st.session_state["solver"] = solver # Store solver instance to show iterations afterwards.
                error_msg = str(e)

                if "Unbounded" in error_msg:
                    st.toast("❗ :red[**Unbounded LP detected.**]")
                elif "Infeasible" in error_msg:
                    st.toast("❌ :red[**Infeasible LP.**]")
                elif "Maximum" in error_msg:
                    st.toast("❌ :red[**Maximum iterations reached.**]")
                else:
                    st.toast(f"⚠️ :red[**An unexpected error occurred: {error_msg}**]")



with st.container(border=True):
    # Final Basic Solution 
    st.title("🗒️ Results")

    if "solver" not in st.session_state:
        st.info("Solve LP to see the final solution.")
    else:
        solver = st.session_state["solver"]
        
        if solver.table_breakdown is None:
            st.info("No solution available yet.")
        else:
            breakdown = solver.table_breakdown
            
            # Filter to show only projects with non-zero values
            included_projects = []
            for i, x_val in enumerate(breakdown["x_values"]):
                if abs(x_val) > 1e-6:  # Non-zero threshold
                    included_projects.append({
                        "Project": breakdown["project_names"][i],
                        "Number of Project Units": round(x_val, 4),
                        # "Cost": round(breakdown["cost_vector"][i], 2), # Optional
                        "Cost($)": round(breakdown["cost_breakdown"][i], 2)
                    })
            
            if len(included_projects) == 0:
                st.info("No projects included in the solution.")
            else:
                # Display objective value
                st.write(f"**💰 Optimized Cost($):** {round(breakdown['Z'], 4)}")
                
                # Display solution table
                df_solution = pd.DataFrame(included_projects)
                st.dataframe(df_solution, use_container_width=True, hide_index=True)




with st.container(border=True):
    st.title("🔁 Iterations")
    # Check if solver exists 
    if "solver" not in st.session_state:
        st.error("No LP solution found. Please scroll up and click **Solve LP**.")
        st.stop()

    solver = st.session_state["solver"]

    # Check iteration counts 
    num_iters = len(solver.tableau_iterations)

    if num_iters == 0:
        st.warning("The simplex solver finished without any pivot iterations.")
        st.info("This usually means the initial tableau was already optimal.")
        st.stop()

    st.write(f"### Total Iterations: {num_iters}")


    # Choose iteration number 
    iter_num = st.number_input(
        "Select iteration number:",
        min_value=0,
        max_value=num_iters,
        value=0,
        step=1,
    )

    # Display Tableau 
    st.subheader("📋 Tableau")

    if (iter_num == 0): tableau = solver.initial_tableau
    else: tableau = solver.tableau_iterations[iter_num - 1]

    # Label columns for the tableau
    num_s = len(solver.constraints) + len(solver.selected_variables)       # Number of s variables (dual variables)
    num_x = len(solver.selected_variables)                                 # Number of slack 

    # Label for tableau iterations
    col_names = (
        [f"S{i+1}" for i in range(num_s)] +
        [f"X{i+1}" for i in range(num_x)] +
        ["Z"] +
        ["RHS"]
    )

    df_tableau = pd.DataFrame(
        tableau,
        columns=col_names,
        dtype=float
    )


    st.dataframe(df_tableau, use_container_width=True)


with st.container(border=True):
    # Display Basic Solution 
    st.subheader("🟰 Basic Solution")

    # Get the basic solution for the selected iteration
    basic_solution = solver.basic_solution_iterations[iter_num - 1]

    # Extract project information
    project_names = solver.selected_variables.index.tolist()
    cost_vector = solver.selected_variables["Cost"].values
    num_projects = len(project_names)

    # Extract project decision variables (x) from basic solution
    # located at positions [-1-num_projects : -1]
    x_values = basic_solution[-1 - num_projects: -1]
    objective_value = basic_solution[-1]

    # Calculate cost breakdown per project
    cost_breakdown = [x * cost for x, cost in zip(x_values, cost_vector)]
    total_cost = sum(cost_breakdown)

    # Create dataframe for basic solution 
    solution_data = {
        "Project": project_names,
        "Number of Project Units": [round(x, 4) for x in x_values],
        # "Cost": [round(cost, 2) for cost in cost_vector], # Optional
        "Cost($)": [round(cb, 2) for cb in cost_breakdown]
    }

    df_solution = pd.DataFrame(solution_data)

    # Display cost
    st.write(f"**💰 Cost:** {round(objective_value, 4)}")


    # Display solution table
    st.dataframe(df_solution, use_container_width=True, hide_index=True)

