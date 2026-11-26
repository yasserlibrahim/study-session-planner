from dataclasses import dataclass


# Represents a study task with its duration and priority score.
@dataclass
class Task:
    id: str
    name: str
    duration: int
    score: int


# Stores the results returned by each optimization algorithm.
@dataclass
class SolverResult:
    selected_task_ids: list[str]
    total_duration: int
    total_score: int
    unused_time: int