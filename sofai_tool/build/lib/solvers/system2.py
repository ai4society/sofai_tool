# solvers/system2.py

class System2Solver:
    def solve(self, problem):
        raise NotImplementedError("Define the 'solve' method for your System-2 Solver.")
    
    def estimate_difficulty(self,problem):
        raise NotImplementedError("Define the 'estimate_difficulty' method for your System-2 Solver.")
    
    def calculate_correctness(self, problem, solution):
        raise NotImplementedError("Define the 'calculate_correctness' method for your System-2 Solver.")
