from models import Task
from algorithms.dynamic_programming import solve_dp
import random
from algorithms.exhaustive import solve_exhaustive
import pytest

def test_dynamic_programming():
    tasks = [
        Task("T1", "Recursion practice", 10, 60),
        Task("T2", "Sorting practice", 20, 100),
        Task("T3", "Dynamic programming practice", 30, 120)
    ]

    result = solve_dp(tasks, 50)

    # Verify the optimal selection and totals.
    assert result.selected_task_ids == ["T2", "T3"]
    assert result.total_duration == 50
    assert result.total_score == 220
    assert result.unused_time == 0

def test_exhaustive_search():
    tasks = [
        Task("T1", "Recursion practice", 10, 60),
        Task("T2", "Sorting practice", 20, 100),
        Task("T3", "Dynamic programming practice", 30, 120)
    ]

    result = solve_exhaustive(tasks, 50)

    assert result.selected_task_ids == ["T2", "T3"]
    assert result.total_score == 220
    assert result.total_duration == 50
    assert result.unused_time == 0


def test_dp_matches_exhaustive():
    rng = random.Random(42)

    # Compare both algorithms on reproducible random inputs.
    for _ in range(50):
        tasks = [
            Task(
                f"T{i}",
                f"Task {i}",
                rng.randint(1, 30),
                rng.randint(0, 100)
            )
            for i in range(rng.randint(1, 15))
        ]

        budget = rng.randint(0, 100)

        dp_result = solve_dp(tasks, budget)
        exhaustive_result = solve_exhaustive(tasks, budget)

        assert dp_result.total_score == exhaustive_result.total_score
        assert dp_result.total_duration <= budget


# Run boundary cases against both solvers.
@pytest.mark.parametrize("solver", [solve_dp, solve_exhaustive])
@pytest.mark.parametrize("tasks, budget, expected_score", [
    ([], 60, 0),
    ([Task("T1", "Task 1", 10, 60)], 0, 0),
    ([Task("T1", "Task 1", 100, 60)], 50, 0),
    ([Task("T1", "Task 1", 50, 100)], 50, 100),
    ([Task("T1", "Task 1", 10, 0)], 50, 0),
    ([
        Task("T1", "Task 1", 20, 100),
        Task("T2", "Task 2", 30, 100)
    ], 30, 100)
])
def test_boundary_cases(solver, tasks, budget, expected_score):
    result = solver(tasks, budget)

    assert result.total_score == expected_score
    assert 0 <= result.total_duration <= budget
    assert result.unused_time == budget - result.total_duration

    # Verify selected tasks and reported totals.
    task_map = {task.id: task for task in tasks}
    selected_ids = result.selected_task_ids

    assert len(selected_ids) == len(set(selected_ids))
    assert all(task_id in task_map for task_id in selected_ids)

    selected = [task_map[task_id] for task_id in selected_ids]

    assert sum(task.duration for task in selected) == result.total_duration
    assert sum(task.score for task in selected) == result.total_score