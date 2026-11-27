from models import Task
from algorithms.dynamic_programming import solve_dp


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