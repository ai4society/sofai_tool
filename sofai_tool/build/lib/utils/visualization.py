import matplotlib.pyplot as plt
import numpy as np

def plot_solver_activity(log_data):
    # Preparing data
    problem_numbers = {num for sublist in log_data.values() for num, sol in sublist}
    problem_numbers = sorted(problem_numbers)  # Sort problem numbers to maintain order

    # Initialize counts
    total_counts = []
    s1_counts = []
    s2_counts = []

    # Count the occurrences for each system per problem
    for num in problem_numbers:
        total = sum(1 for sublist in log_data.values() for n, sol in sublist if n == num)
        s1_count = sum(1 for n, sol in log_data['System1'] if n == num)
        s2_count = sum(1 for n, sol in log_data['System2'] if n == num)

        total_counts.append(total)
        s1_counts.append(s1_count)
        s2_counts.append(s2_count)

    # Plotting
    bar_width = 0.25
    r1 = np.arange(len(problem_numbers))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]

    plt.bar(r1, total_counts, color='b', width=bar_width, edgecolor='grey', label='Total Problems')
    plt.bar(r2, s1_counts, color='g', width=bar_width, edgecolor='grey', label='S1 Usage')
    plt.bar(r3, s2_counts, color='r', width=bar_width, edgecolor='grey', label='S2 Usage')

    plt.xlabel('Problem Number', fontweight='bold', fontsize=12)
    plt.ylabel('Count', fontweight='bold', fontsize=12)
    plt.xticks([r + bar_width for r in range(len(total_counts))], problem_numbers)

    plt.legend()
    plt.title("Problem Solving Activity")
    plt.savefig("problem_solving_activity.png")
    plt.show()