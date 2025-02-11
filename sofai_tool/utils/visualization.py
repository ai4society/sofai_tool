import matplotlib.pyplot as plt
import json
import numpy as np

def plot_solver_activity(file_name):
    # Load data
    with open("db/" + file_name, 'r') as f:
        log_data = json.load(f)

    # Extract cases
    case_data = log_data.get("cases", {})

    # Dictionary to store solving times per problem
    problem_times = {}

    for case_info in case_data.values():
        problem_name = case_info['name']
        solving_time = case_info['solving_time']
        system = case_info['system']

        if problem_name not in problem_times:
            problem_times[problem_name] = {'s1': None, 's2': None, 'sofai': None}

        if system == 1:
            problem_times[problem_name]['s1'] = solving_time
        elif system == 2:
            problem_times[problem_name]['s2'] = solving_time
        elif system == -1:
            problem_times[problem_name]['sofai'] = solving_time

    # Assign a unique index to each problem
    unique_problems = list(problem_times.keys())
    x_values = np.arange(1, len(unique_problems) + 1)

    # Extract solving times
    s1_times = [problem_times[p].get('s1', None) for p in unique_problems]
    s2_times = [problem_times[p].get('s2', None) for p in unique_problems]
    sofai_times = [problem_times[p].get('sofai', None) for p in unique_problems]

    # Convert None values to NaN for plotting
    s1_times = np.array([t if t is not None else np.nan for t in s1_times])
    s2_times = np.array([t if t is not None else np.nan for t in s2_times])
    sofai_times = np.array([t if t is not None else np.nan for t in sofai_times])

    # Ensure we have data
    if len(unique_problems) == 0:
        print("No valid problem data found!")
        return

    # Create the scatter plot
    plt.figure(figsize=(10, 8))

    # Scatter plot with different markers and transparency for clarity
    plt.scatter(x_values, s1_times, color='blue', marker='o', s=80, alpha=0.7, edgecolors='black', label='S1')
    plt.scatter(x_values, s2_times, color='orange', marker='s', s=80, alpha=0.7, edgecolors='black', label='S2')
    plt.scatter(x_values, sofai_times, color='purple', marker='^', s=80, alpha=0.7, edgecolors='black', label='SOFAI')

    # Labels and title
    plt.xlabel('Problem Index', fontweight='bold', fontsize=12)
    plt.ylabel('Solving Time', fontweight='bold', fontsize=12)
    plt.title('Solving Time per Unique Problem')
    plt.legend()

    # Save and show the plot
    plt.savefig(file_name.replace("_experience.json", "") + "_solver_activity.png")
    plt.show()