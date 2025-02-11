import random
import time
import pickle
import os
import re
import logging

import ollama  # Assumed to be installed and configured
import sofai_tool as sofai
from sofai_tool.metacognition import metacognition_module as metam
import utilities
from sofai_tool.solvers import system1 as sofai1
from sofai_tool.solvers import system2 as sofai2
from sofai_tool.solvers import Solver

# Folder to store generated problems
if not os.path.exists('gen_data'):
    os.makedirs('gen_data')


# -----------------------------
# Problem Generation Functions
# -----------------------------
def generate_expression(depth: int) -> str:
    """
    Recursively generate a random arithmetic expression using BODMAS operations.
    For depth == 0, return a random integer between 1 and 9.
    For depth > 0, randomly choose an operator and combine two expressions.
    For exponentiation '**', the exponent is generated with depth 0 (to keep it small).
    """
    # Base case: return a number (avoid zero to prevent division by zero)
    if depth == 0:
        return str(random.randint(1, 9))
    
    # Choose an operator randomly
    op = random.choice(["+", "-", "*", "/", "**"])
    
    if op == "**":
        left = generate_expression(depth - 1)
        # For exponentiation, use a small exponent (depth 0)
        right = str(random.randint(2, 3))
    else:
        left = generate_expression(depth - 1)
        right = generate_expression(depth - 1)
    
    # Always wrap the expression in parentheses to enforce explicit grouping.
    return f"({left} {op} {right})"


def generate_bodmas_problems(n_problems: int, depth_list: list) -> list:
    """
    Generate multiple arithmetic (BODMAS) problems.
    
    For each specified depth (complexity level), generate n_problems arithmetic expressions,
    compute their correct answers, and save them as pickle files in the 'gen_data' folder.
    
    Each pickle file stores a tuple:
        (expression (str), correct_answer (float), depth (int))
    
    The file name is in the format:
        gen_data/bodmas_<depth>_<p>_<id>.pickle
    where <p> is a placeholder (kept for similarity with the original code) and <id> is a random identifier.
    
    Returns a list of problem identifiers (file paths without the '.pickle' extension).
    """
    problems = []
    for depth in depth_list:
        for _ in range(n_problems):
            expr = generate_expression(depth)
            try:
                # Safely evaluate the expression.
                # (Since we generate the expression ourselves, eval is acceptable here.)
                correct_answer = eval(expr)
            except Exception as e:
                # In the unlikely event of an error, set answer to None.
                correct_answer = None
                logging.error(f"Error evaluating expression {expr}: {e}")
            
            # Create a unique id for the problem.
            uid = random.randint(0, 100000)
            # We include 'p' (probability) placeholder as in the graph example; here it is fixed to 1.
            problem_filename = f'gen_data/bodmas_{depth}_1_{uid}.pickle'
            with open(problem_filename, 'wb') as f:
                pickle.dump((expr, correct_answer, depth), f)
            # Store the file path without the .pickle extension (to mimic the original code structure)
            problems.append(problem_filename.replace('.pickle', ''))
    return problems


# -----------------------------
# System 1 Solver
# -----------------------------
class CustomSystem1Solver(sofai1.System1Solver):
    def __init__(self):
        super().__init__()

    def process_plan(self, response: str):
        pattern = re.compile(r"(-?\d+(?:\.\d+)?)")
        match = pattern.search(response)
        return float(match.group(1)) if match else None

    def model_res_generator(self, message):
        stream = ollama.chat(model='mistral', messages=message, stream=True)
        return "".join(chunk["message"]["content"] for chunk in stream)

    def simple_prompt_generator(self, expression: str) -> str:
        """
        Generate a prompt instructing the LLM to evaluate the arithmetic expression according to BODMAS rules.
        """
        return f"""
        ### BODMAS Arithmetic Problem ###

        Evaluate the following arithmetic expression strictly following the BODMAS rules (i.e., 
        Brackets, Orders, Division, Multiplication, Addition, Subtraction):

            {expression}

        Please provide the final numerical answer as a single number. For example, if the answer is 42, simply write:

            42

        Your answer:
        """

    def solve(self, problem_id: str):
        with open(problem_id + '.pickle', 'rb') as f:
            expression, correct_answer, depth = pickle.load(f)
        prompt = self.simple_prompt_generator(expression)
        message = [{"role": "user", "content": prompt}]
        start_time = time.time()
        response = self.model_res_generator(message)
        self.running_time = time.time() - start_time
        
        self.solution = self.process_plan(response)
        self.confidence = 1.0
        self.correctness = self.calculate_correctness(problem_id)

        return 1.0, self.solution
        
    def calculate_correctness(self, problem_id: str):
        if self.solution is None:
            return 0.0
        with open(problem_id + '.pickle', 'rb') as f:
            _, correct_answer, _ = pickle.load(f)
        return 1.0 if abs(float(self.solution) - float(correct_answer)) < 1e-6 else 0.0

# -----------------------------
# System 2 Solver
# -----------------------------
class CustomSystem2Solver(sofai2.System2Solver):
    def __init__(self):
        super().__init__()
    
    def solve(self, problem_id: str, time_limit: float):
        with open(problem_id + '.pickle', 'rb') as f:
            expression, correct_answer, depth = pickle.load(f)
        
        start_time = time.time()
        try:
            self.solution = eval(expression)
        except Exception as e:
            logging.error(f"System2 error evaluating {expression}: {e}")
            self.solution = None
        
        self.running_time = time.time() - start_time
        self.confidence = 1.0 if self.solution is not None else 0.0
        
        self.correctness = self.calculate_correctness(problem_id)
        if self.running_time > time_limit:
            self.solution = None
            self.correctness = 0.0
        
        return self.confidence, self.solution  
    
    def calculate_correctness(self, problem_id: str):
        if self.solution is None:
            return 0.0
        with open(problem_id + '.pickle', 'rb') as f:
            _, correct_answer, _ = pickle.load(f)

        return 1.0 if abs(float(self.solution) - float(correct_answer)) < 1e-6 else 0.0
    
    def estimate_difficulty(self, problem_id: str):
        """
        Estimate the difficulty of the problem based on its depth.
        (A deeper expression is assumed to be more difficult.)
        """
        with open(problem_id + '.pickle', 'rb') as f:
            expression, correct_answer, depth = pickle.load(f)
        difficulty = depth * 10  # For example, multiply depth by a constant factor
        return difficulty

# -----------------------------
# Main Planning and Solving
# -----------------------------
def plan_solve(problem_id: str, run_type) -> None:
    """
    Given a problem_id (file path without '.pickle'), instantiate both solvers,
    use metacognition to arbitrate if necessary, solve the problem, and print out the results.
    """
    system1_solver = CustomSystem1Solver()
    system2_solver = CustomSystem2Solver()
    
    context_file = "context.txt"
    thresholds_file = "thresholds.txt"
    experience_file = "math_experience.json"
    new_run = False
    
    # Use metacognition (if available) to decide the final solution.
    # (This call is assumed to integrate both solvers' outputs in some way.)
    metam.metacognition(problem_id, system1_solver, system2_solver, context_file, thresholds_file, experience_file, new_run, run_type)
    


# -----------------------------
# Main Execution
# -----------------------------
if __name__ == "__main__":
    # Generate arithmetic (BODMAS) problems.
    # For example, generate 2 problems for each of the depths: 1, 2, and 3.
    problems = generate_bodmas_problems(
        n_problems=4,         # Number of problems per depth level
        depth_list=[3,2,1]  # Different complexity levels (depth of the expression)
    )
    
    experience_file = "math_experience.json"
    # Solve each generated problem.
    for problem_id in problems:
        try:
            print("="*20)
            plan_solve(problem_id, run_type="s1")
        except SystemExit:
            continue
    for problem_id in problems:
        try:
            print("="*20)
            plan_solve(problem_id, run_type="s2")
        except SystemExit:
            continue
    for problem_id in problems:
        try:
            print("="*20)
            plan_solve(problem_id, run_type="sofai")
        except SystemExit:
            continue
    sofai.utils.visualization.plot_solver_activity(experience_file)