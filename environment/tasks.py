from typing import Dict, Any


class BaseTask:
    """
    Base task class
    """

    def __init__(self):
        self.score = 0.0

    def grade(self, state) -> float:
        raise NotImplementedError


class EasyTask(BaseTask):
    """
    Easy Task: Classify customer issue
    """

    def grade(self, state) -> float:

        if not state.classification:
            return 0.0

        message = state.customer_message.lower()

        correct_labels = {
            "payment": "billing",
            "refund": "refund",
            "delayed": "shipping",
            "login": "account",
            "subscription": "subscription",
        }

        for keyword, label in correct_labels.items():
            if keyword in message:
                if state.classification == label:
                    return 1.0

        return 0.0


class MediumTask(BaseTask):
    """
    Medium Task: Classify + Respond
    """

    def grade(self, state) -> float:

        score = 0.0

        # classification score
        if state.classification:
            score += 0.5

        # response score
        if len(state.conversation_history) > 0:
            score += 0.5

        return score


class HardTask(BaseTask):
    """
    Hard Task: Full resolution workflow
    """

    def grade(self, state) -> float:

        score = 0.0

        # classification
        if state.classification:
            score += 0.3

        # response
        if len(state.conversation_history) > 0:
            score += 0.3

        # resolution
        if state.resolved:
            score += 0.4

        return score


TASK_REGISTRY = {
    "easy": EasyTask,
    "medium": MediumTask,
    "hard": HardTask,
}