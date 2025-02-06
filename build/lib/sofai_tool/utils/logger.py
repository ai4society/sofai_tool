import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def log_solution(system_name, problem_id, solution):
    logger.info(f"System {system_name} solved problem {problem_id} with solution: {solution}")

def log_confidence(system_name, problem_id, confidence):
    logger.info(f"System {system_name} confidence for problem {problem_id}: {confidence}")
