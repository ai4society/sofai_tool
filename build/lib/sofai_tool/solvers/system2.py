# solvers/system2.py
from abc import ABC, abstractmethod
from .solver import Solver

class System2Solver(Solver, ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def solve(self, problem, time_limit):
        raise NotImplementedError("Define the 'solve' method for your System-2 Solver.")
    
    @abstractmethod
    def estimate_difficulty(self,problem):
        raise NotImplementedError("Define the 'estimate_difficulty' method for your System-2 Solver.")
    
    @abstractmethod
    def calculate_correctness(self, problem):
        raise NotImplementedError("Define the 'calculate_correctness' method for your System-2 Solver.")
