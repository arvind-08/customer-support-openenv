from typing import Dict

from .tasks import TASK_REGISTRY


class EnvironmentGrader:
    """
    Main grader for Customer Support Environment
    """

    def __init__(self):
        self.tasks = {
            "easy": TASK_REGISTRY["easy"](),
            "medium": TASK_REGISTRY["medium"](),
            "hard": TASK_REGISTRY["hard"](),
        }

    def grade(self, task_name: str, state) -> float:
        """
        Grade environment state based on task
        """

        if task_name not in self.tasks:
            raise ValueError(f"Unknown task: {task_name}")

        task = self.tasks[task_name]

        score = task.grade(state)

        # Ensure score between 0 and 1
        score = max(0.0, min(1.0, score))

        return score

    def grade_all(self, state) -> Dict[str, float]:
        """
        Grade all tasks
        """

        scores = {}

        for name, task in self.tasks.items():
            score = task.grade(state)
            score = max(0.0, min(1.0, score))
            scores[name] = score

        return scores