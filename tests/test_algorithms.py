from models import Task
from algorithms.dynamic_programming import solve_dp
import random
from algorithms.exhaustive import solve_exhaustive


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