from typing import Tuple, Dict, Any 
import uuid

from .models import Observation, Action, Reward, State


class CustomerSupportEnv:
    """
    Customer Support OpenEnv Environment
    """

    def __init__(self):
        self._state = None
        self.max_steps = 8

    def reset(self) -> Observation:
        """
        Reset environment and return initial observation
        """

        ticket_id = str(uuid.uuid4())

        customer_message = self._generate_ticket()

        self._state = State(
            ticket_id=ticket_id,
            customer_message=customer_message,
            conversation_history=[],
            classification=None,
            resolved=False,
            step_count=0,
        )

        return self._get_observation()

    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        """
        Take one step in environment
        """

        reward = 0.0
        done = False
        info = {}

        self._state.step_count += 1

        if action.action_type == "classify":
            reward += self._handle_classify(action)

        elif action.action_type == "respond":
            reward += self._handle_respond(action)

        elif action.action_type == "resolve":
            reward += self._handle_resolve(action)
            done = True

        else:
            reward -= 0.1  # penalty for invalid action

        if self._state.step_count >= self.max_steps:
            done = True

        observation = self._get_observation()

        return observation, reward, done, info

    def state(self) -> State:
        """
        Return current state
        """
        return self._state

    def _get_observation(self) -> Observation:
        """
        Build observation from state
        """

        available_actions = ["classify", "respond", "resolve"]

        status = "resolved" if self._state.resolved else "pending"

        return Observation(
            ticket_id=self._state.ticket_id,
            customer_message=self._state.customer_message,
            conversation_history=self._state.conversation_history,
            available_actions=available_actions,
            status=status,
        )

    def _generate_ticket(self) -> str:
        """
        Generate sample customer tickets
        """

        tickets = [
            "My payment failed but money deducted",
            "I want refund for my order",
            "My order is delayed",
            "Unable to login to my account",
            "Cancel my subscription",
        ]

        import random

        return random.choice(tickets)

    def _handle_classify(self, action: Action) -> float:
        """
        Handle classify action
        """

        correct_labels = {
            "payment": "billing",
            "refund": "refund",
            "delayed": "shipping",
            "login": "account",
            "subscription": "subscription",
        }

        message = self._state.customer_message.lower()

        for keyword, label in correct_labels.items():
            if keyword in message:
                if action.content == label:
                    self._state.classification = label
                    return 0.3
                else:
                    return -0.2

        return -0.1

    def _handle_respond(self, action: Action) -> float:
        """
        Handle respond action
        """

        if not self._state.classification:
            return -0.2

        response = action.content or ""

        self._state.conversation_history.append(
            f"Agent: {response}"
        )

        return 0.3

    def _handle_resolve(self, action: Action) -> float:
        """
        Handle resolve action
        """

        if not self._state.classification:
            return -0.3

        self._state.resolved = True
        return 1.0