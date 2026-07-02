from typing import Tuple


class GuardRails:

    def __init__(self):

        self.injection_patterns = [
            "ignore previous instructions",
            "ignore all instructions",
            "forget previous instructions",
            "system prompt",
            "developer message",
            "reveal prompt",
            "jailbreak",
            "bypass",
            "act as"
        ]

        self.off_topic_patterns = [
            "weather",
            "cricket",
            "football",
            "movie",
            "recipe",
            "bitcoin",
            "stock market",
            "travel",
            "hotel",
            "restaurant"
        ]

        self.hr_patterns = [
            "should i hire",
            "should i fire",
            "salary",
            "compensation",
            "promotion",
            "termination",
            "labor law",
            "legal advice"
        ]

    def check(self, query: str) -> Tuple[bool, str]:

        q = query.lower()

        # Prompt Injection
        for pattern in self.injection_patterns:
            if pattern in q:
                return (
                    False,
                    "I can only assist with recommending and comparing SHL assessments."
                )

        # HR / Legal Advice
        for pattern in self.hr_patterns:
            if pattern in q:
                return (
                    False,
                    "I can't provide HR or legal advice. I can help recommend SHL assessments for hiring and talent evaluation."
                )

        # Off-topic
        for pattern in self.off_topic_patterns:
            if pattern in q:
                return (
                    False,
                    "I'm designed to answer questions related to SHL assessments only."
                )

        return True, ""