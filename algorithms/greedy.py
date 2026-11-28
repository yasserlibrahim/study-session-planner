"""Greedy baseline for the Study Session Planner.

Sorts tasks by score per minute and adds each task that still fits in the
remaining time. Runs in O(n log n) time but does not always find the best
combination of whole tasks.
"""
from fractions import Fraction

from models import SolverResult


def score_per_minute(task):
    """Exact score-to-duration ratio, used as the greedy sort key."""
    return Fraction(task.score, task.duration)


def greedy_select(tasks, capacity):
    """Select tasks greedily by score per minute within the time budget.

    Ties are broken by higher score, then by task ID, so the result is
    always the same for the same input. Selected IDs are listed in the
    order the greedy method picked them.
    """
    if capacity < 0:
        raise ValueError("capacity must be a nonnegative number of minutes")

    # Sort once: O(n log n).
    ordered = sorted(tasks, key=lambda task: (-score_per_minute(task), -task.score, task.id))

    selected_ids = []
    total_duration = 0
    total_score = 0

    # Single pass: O(n). Take each task if it still fits.
    for task in ordered:
        if total_duration + task.duration <= capacity:
            selected_ids.append(task.id)
            total_duration += task.duration
            total_score += task.score

    return SolverResult(
        selected_task_ids=selected_ids,
        total_duration=total_duration,
        total_score=total_score,
        unused_time=capacity - total_duration,
    )
