from models import Task, SolverResult


def build_dp_table(tasks: list[Task], budget: int) -> list[list[int]]:
    n = len(tasks)

    # Initialize the DP table.
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    # Calculate the maximum score for each time capacity.
    for i in range(1, n + 1):
        task = tasks[i - 1]

        for t in range(budget + 1):
            if task.duration <= t:
                include = task.score + dp[i - 1][t - task.duration]
                exclude = dp[i - 1][t]

                dp[i][t] = max(include, exclude)
            else:
                dp[i][t] = dp[i - 1][t]

    return dp


def solve_dp(tasks: list[Task], budget: int) -> SolverResult:
    n = len(tasks)
    dp = build_dp_table(tasks, budget)

    selected_task_ids = []
    total_duration = 0
    remaining = budget

    # Reconstruct the selected tasks from the DP table.
    for i in range(n, 0, -1):
        if dp[i][remaining] != dp[i - 1][remaining]:
            task = tasks[i - 1]
            selected_task_ids.append(task.id)
            total_duration += task.duration
            remaining -= task.duration

    selected_task_ids.reverse()

    return SolverResult(
        selected_task_ids=selected_task_ids,
        total_duration=total_duration,
        total_score=dp[n][budget],
        unused_time=budget - total_duration
    )