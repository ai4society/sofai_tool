# solvers/system1.py
from abc import ABC, abstractmethod
from .solver import Solver

class System1Solver(Solver, ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def solve(self, problem):
        raise NotImplementedError("Define the 'solve' method for your System-1 Solver.")
    
    @abstractmethod
    def calculate_correctness(self, problem):
        raise NotImplementedError("Define the 'calculate_correctness' method for your System-1 Solver.")
    

