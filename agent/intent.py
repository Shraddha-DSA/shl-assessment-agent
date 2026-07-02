from abc import ABC, abstractmethod
from enum import Enum


class Intent(Enum):
    CLARIFY = "clarify"
    RECOMMEND = "recommend"
    COMPARE = "compare"
    REFUSE = "refuse"


# Base class
class BaseIntentDetector(ABC):

    @abstractmethod
    def detect(self, query: str) -> Intent:
        pass


# Rule-based implementation
class RuleBasedIntentDetector(BaseIntentDetector):

    def detect(self, query: str) -> Intent:

        query = query.lower()

        # Prompt injection
        if any(word in query for word in [
            "ignore previous",
            "forget instructions",
            "system prompt"
        ]):
            return Intent.REFUSE

        # Comparison
        if any(word in query for word in [
            "compare",
            "difference",
            "vs",
            "versus"
        ]):
            return Intent.COMPARE

        # Too little information
        if len(query.split()) < 4:
            return Intent.CLARIFY

        return Intent.RECOMMEND