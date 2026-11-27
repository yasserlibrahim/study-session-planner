from itertools import combinations
from models import Task, SolverResult


def solve_exhaustive(tasks: list[Task], budget: int) -> SolverResult:
    best_ids = []
    best_score = 0
    best_duration = 0

    # Evaluate every possible subset of tasks.
    for size in range(len(tasks) + 1):
        for subset in combinations(tasks, size):
            duration = sum(task.duration for task in subset)
            score = sum(task.score for task in subset)

            # Keep the best feasible combination.
            if duration <= budget and score > best_score:
                best_ids = [task.id for task in subset]
                best_score = score
                best_duration = duration

    return SolverResult(
        selected_task_ids=best_ids,
        total_duration=best_duration,
        total_score=best_score,
        unused_time=budget - best_duration
    )