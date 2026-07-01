from agent.guardrails import GuardRails
from agent.intent import RuleBasedIntentDetector
from agent.retriever import SHLRetriever
from agent.recommender import RecommendationEngine
from agent.comparator import Comparator

guard = GuardRails()
intent_detector = RuleBasedIntentDetector()
retriever = SHLRetriever()
recommender = RecommendationEngine()
comparator = Comparator()


def guardrail_node(state):

    allowed, message = guard.check(state["user_query"])

    if not allowed:
        state["reply"] = message
        state["end_of_conversation"] = True

    return state


def intent_node(state):

    intent = intent_detector.detect(state["user_query"])

    state["intent"] = intent.value

    return state


def clarification_node(state):

    state["reply"] = (
        "Could you please specify the role, experience level, "
        "and whether you need technical, cognitive or personality assessments?"
    )

    state["needs_clarification"] = True

    return state


def retriever_node(state):

    docs = retriever.retrieve(
        state["user_query"],
        top_k=10
    )

    state["retrieved_docs"] = docs

    return state


def recommendation_node(state):

    answer = recommender.recommend(
        state["user_query"],
        state["retrieved_docs"]
    )

    state["reply"] = answer

    return state


def comparison_node(state):

    answer = comparator.compare(
        state["user_query"],
        state["retrieved_docs"]
    )

    state["reply"] = answer

    return state