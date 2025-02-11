import matplotlib.pyplot as plt
import json
import numpy as np

def plot_solver_activity(file_name):
    # Load data
    with open("db/" +file_name, 'r') as f:
        log_data = json.load(f)

    # Extract cases
    case_data = log_data.get("cases", {})

    # Prepare lists
    case_numbers = []
    solving_times = []
    systems = []

    for case_number, case_info in case_data.items():
        if not case_number.isdigit():
            continue
        case_numbers.append(int(case_number))
        solving_times.append(case_info['solving_time'])
        systems.append(case_info['system'])

    # Convert to NumPy arrays
    case_numbers = np.array(case_numbers)
    solving_times = np.array(solving_times)
    systems = np.array(systems)

    # Ensure we have data
    if len(case_numbers) == 0:
        print("No valid case data found!")
        return

    # Create a scatter plot for System 1 and System 2
    plt.figure(figsize=(8, 6))

    # Mask for filtering system types
    system1_mask = (systems == 1)
    system2_mask = (systems == 2)

    # Scatter plot with different colors for systems
    plt.scatter(case_numbers[system1_mask], solving_times[system1_mask], color='g', label='System 1')
    plt.scatter(case_numbers[system2_mask], solving_times[system2_mask], color='r', label='System 2')

    # Labels and title
    plt.xlabel('Case Number', fontweight='bold', fontsize=12)
    plt.ylabel('Solving Time', fontweight='bold', fontsize=12)
    plt.title('Solving Time per Case')
    plt.legend()
    
    # Save and show the plot
    plt.savefig("solving_time_per_case.png")
    plt.show()