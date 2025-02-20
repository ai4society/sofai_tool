[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
![Python Version](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Last commit](https://img.shields.io/github/last-commit/ai4society/sofai_tool?color=orange)
![Open PRs](https://img.shields.io/github/issues-pr/ai4society/sofai_tool?color=blue)
![Issues](https://img.shields.io/github/issues/ai4society/sofai_tool?color=red)
![Repo Size](https://img.shields.io/github/repo-size/ai4society/sofai_tool?color=purple)
[![GitHub stars](https://img.shields.io/github/stars/ai4society/sofai_tool.svg?style=social)](https://github.com/ai4society/sofai_tool/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/ai4society/sofai_tool.svg?style=social)](https://github.com/ai4society/sofai_tool/network/members)

# SOFAI Tool (AAAI 2025)

SOFAI Tool is a neurosymbolic system designed to integrate fast experience-based decision-making (System 1) with logical, deliberative processing (System 2) through a metacognition module. This package enables developers and researchers to easily instantiate, configure, and extend System 1 and System 2 solvers, log system activities, and visualize solver performance across a batch of problems.

## Features

- **Flexible Solver Architecture**: Define custom System 1 and System 2 solvers with problem-solving methods.
- **Metacognition Module**: A metacognition module that chooses between System 1 and System 2 based on set constraints.
- **Logging and Visualization**: Log solutions, confidence levels, and visualize the activities of System 1 and System 2 across multiple problems.

![SOFAI Tool](assets/dev-pov.png)

## Installation

Follow the steps below to install the SOFAI Tool locally:

1. **Create a Conda environment** (Python >=3.10 recommended):
   ```bash
   conda create --name sofai_env python=3.10 -y
   conda activate sofai_env
   ```

2. **Clone the repository**:
   ```bash
   git clone https://github.com/ai4society/sofai_tool.git
   cd sofai_tool
   ```

3. **Install dependencies**:
   ```bash
   pip install .
   ```

4. **Verify installation**:
   ```bash
   python -c "import sofai; print('SOFAI Tool installed successfully!')"
   ```

### Optional: Installing in Development Mode
If you want to modify the package and test changes, install it in **editable mode**:
   ```bash
   pip install -e .
   ```

## Directory Structure

```
sofai_tool/
├── sofai_tool/                # Core SOFAI tool package
│   ├── metacognition/         # Contains metacognition module
│   │   ├── metacognition_module.py
│   │   ├── mos.py             # Model of Self
│   │   ├── temp_thresholds.py # Temporary thresholds for decision-making
│   │   └── utilities.py       # Metacognition-related utilities
│   ├── solvers/               # Contains solver implementations
│   │   ├── solver.py          # Generic solver base class
│   │   ├── system1.py         # System 1 solver base class
│   │   └── system2.py         # System 2 solver base class
│   ├── utils/                 # Utility functions
│   │   ├── logger.py          # Logging functions
│   │   └── visualization.py   # Visualization functions
├── sofai_instances/           # Predefined SOFAI instances for specific tasks
│   ├── math-sofai/            # SOFAI instance for mathematical problems
│   └── plan-sofai/            # SOFAI instance for planning problems
└── README.md                  # Project documentation
```

## Usage

The following examples demonstrate how to use the SOFAI Tool by importing the package as `sofai`.

```python
import sofai_tool as sofai
```

### 1. Importing Required Modules

```python
import random
import time
import pickle
import os
import logging
import sofai_tool as sofai
from sofai_tool.metacognition import metacognition_module as metam
from sofai_tool.solvers import system1 as sofai1
from sofai_tool.solvers import system2 as sofai2
from sofai_tool.solvers import Solver
```

- `sofai_tool`: Core SOFAI framework.
- `metacognition_module`: Handles solver selection logic.
- `system1` & `system2`: Provide base classes for implementing solvers.

### 2. Problem Generation

```python
def generate_problems(n_problems: int, complexity_list: list) -> list:
    pass  # Modify to generate problems
```

- This function is a placeholder for generating a batch of problems.
- `n_problems`: Number of problems to generate.
- `complexity_list`: Specifies the complexity levels.

### 3. Implementing System 1 Solver

```python
class CustomSystem1Solver(sofai1.System1Solver):
    def __init__(self):
        super().__init__()

    def solve(self, problem):
        pass

    def calculate_correctness(self, problem):
        """
        Evaluate correctness by comparing with the expected solution.
        Modify this function based on the expected output format.
        """
        pass  # Modify with actual correctness computation
```

### 4. Implementing System 2 Solver

```python
class CustomSystem2Solver(sofai2.System2Solver):
    def __init__(self):
        super().__init__()

    def solve(self, problem, time_limit: float):
        pass

    def calculate_correctness(self, problem):
        pass  # Modify to compute correctness
    
    def estimate_difficulty(self, problem):
        pass  # Modify to estimate difficulty
```

### 5. Using Metacognition

```python
def plan_solve(problem, run_type) -> None:
    """
    Given a problem instance, instantiate both solvers, use metacognition to arbitrate if necessary,
    solve the problem, and print out the results.
    """
    system1_solver = CustomSystem1Solver()
    system2_solver = CustomSystem2Solver()
    
    context_file = "<name of context file>"
    thresholds_file = "<name of thresholds file>"
    experience_file = "<name of experience file>"
    new_run = False
    
    # Use metacognition to decide the final solution.
    metam.metacognition(
        problem, system1_solver, system2_solver, 
        context_file, thresholds_file, experience_file, new_run, run_type
    )
```

### 6. Running SOFAI Tool on the Problems

```python
if __name__ == "__main__":
    # Generate a batch of problems with different complexity levels.
    problems = generate_problems(
        n_problems=5,         # Number of problems to generate
        complexity_list=["easy", "medium", "hard"]  # Generic complexity levels
    )

    experience_file = "<name of experience file>"

    solving_modes = ["s1", "s2", "sofai"]  # Different execution modes

    for mode in solving_modes:
        print(f"Running experiments with mode: {mode.upper()}")
        for problem in problems:
            try:
                print("="*20)
                plan_solve(problem, run_type=mode)
            except SystemExit:
                continue

    # Visualize solver performance
    sofai.utils.visualization.plot_solver_activity(experience_file)
```

## Example Instances using SOFAI Tool

SOFAI Tool provides a modular setup that enables users to adapt this system to build neurosymbolic architectures for problems of their choice. By implementing custom System 1 and System 2 solvers, you can model various types of decision-making systems. 

| Instance Name          | Notebook/Source | Paper |
|------------------------|----------------|--------|
| **Math-SOFAI (HelloWorld!)** | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)]() | - |
| **Plan-SOFAI** | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1uHqCns7ztxLEMFL4PWSWMlpkrqywtnVu?usp=sharing) | [![Paper](https://img.shields.io/badge/Paper-PDF-blue?logo=adobeacrobatreader)](https://openreview.net/pdf?id=ORAhay0H4x) |
| **Grid-SOFAI** | [![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/aloreggia/sofai) | [![Paper](https://img.shields.io/badge/Paper-PDF-blue?logo=adobeacrobatreader)](https://ceur-ws.org/Vol-3212/paper12.pdf) |
| **CSP-SOFAI (v1)** | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/your_notebook_link_here) | [![Paper](https://img.shields.io/badge/Paper-PDF-blue?logo=adobeacrobatreader)](https://arxiv.org/pdf/2412.01752) |
| **CSP-SOFAI (v2)** | [![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/khvedant02/CSP-SOFAI-Instance) | [![Paper](https://img.shields.io/badge/Paper-PDF-blue?logo=adobeacrobatreader)](https://arxiv.org/pdf/2412.01752) |

##  Contributing to the Lab
We encourage contributions and feedback.

## Citation for the Lab

If you wish to cite the lab titled "Harnessing Large Language Models for Planning: A Lab on Strategies for Success and Mitigation of Pitfalls" in your work, please cite it as follows:

Pallagani, V., Loreggia, A., Fabiano, F., Srivastava, B., Rossi, F., & Horesh, L. (2025, February). SOFAI Lab: A Hands-On Guide to Building Neurosymbolic Systems with Metacognitive Control. In AAAI Conference on Artificial Intelligence. 

```
@inproceedings{pallagani2025sofailab,
  title={SOFAI Lab: A Hands-On Guide to Building Neurosymbolic Systems with Metacognitive Control},
  author={Pallagani, Vishal and Loreggia, Andrea and Fabiano, Francesco and Srivastava, Biplav and Rossi, Francesca and Horesh, Lior},
  booktitle={AAAI Conference on Artificial Intelligence},
  year={2025}
}
```

## License

This project is licensed under the MIT License.
