import re
import getpass
import os
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


class State(TypedDict):
    """
    represents the state of the essay grading process
    """
    topic: str
    essay: str
    relevance_score: float
    grammar_score: float
    structure_score: float
    depth_score: float
    final_score: float
    
# GRADING FUNCTIONS
def extract_score(content: str) -> float:
    """
    extract the numeric score from the LLM's response
    """
    match = re.search(r'Score:\s*(\d+(\.\d+)?)', content)
    if match:
        return float(match.group(1))
    raise ValueError(f"Could not extract score from: {content}")

def check_relevance(state: State) -> State:
    """
    check the relevance of the essay
    """
    prompt = ChatPromptTemplate.from_template(
        "Analyze the relevance of the following essay to the given topic {topic}. "
        "Provide a relevance score between 0 and 1. "
        "Your response should start with 'Score: ' followed by the numeric score, "
        "then provide your explanation.\n\nEssay: {essay}"
    )
    result = llm.invoke(prompt.format(topic=state["topic"], essay=state["essay"]))
    try:
        state["relevance_score"] = extract_score(result.content)
    except ValueError as e:
        print(f"Error in check_relevance: {e}")
        state["relevance_score"] = 0.0
    return state

def check_grammar(state: State) -> State:
    """
    check the grammar of the essay
    """
    prompt = ChatPromptTemplate.from_template(
        "Analyze the grammar and language usage in the following essay. "
        "Provide a grammar score between 0 and 1. "
        "Your response should start with 'Score: ' followed by the numeric score, "
        "then provide your explanation.\n\nEssay: {essay}"
    )
    result = llm.invoke(prompt.format(topic=state["topic"], essay=state["essay"]))
    try:
        state["grammar_score"] = extract_score(result.content)
    except ValueError as e:
        print(f"Error in check_grammar: {e}")
        state["grammar_score"] = 0.0
    return state

def analyze_structure(state: State) -> State:
    """
    analyze the structure of the essay
    """
    prompt = ChatPromptTemplate.from_template(
        "Analyze the structure of the following essay. "
        "Provide a structure score between 0 and 1. "
        "Your response should start with 'Score: ' followed by the numeric score, "
        "then provide your explanation.\n\nEssay: {essay}"
    )
    result = llm.invoke(prompt.format(topic=state["topic"], essay=state["essay"]))
    try:
        state["structure_score"] = extract_score(result.content)
    except ValueError as e:
        print(f"Error in analyze_structure: {e}")
        state["structure_score"] = 0.0
    return state

def evaluate_depth(state: State) -> State:
    """
    evaluate the depth of analysis in the essay
    """
    prompt = ChatPromptTemplate.from_template(
        "Evaluate the depth of analysis in the following essay. "
        "Provide a depth score between 0 and 1. "
        "Your response should start with 'Score: ' followed by the numeric score, "
        "then provide your explanation.\n\nEssay: {essay}"
    )
    result = llm.invoke(prompt.format(topic=state["topic"], essay=state["essay"]))
    try:
        state["depth_score"] = extract_score(result.content)
    except ValueError as e:
        print(f"Error in evaluate_depth: {e}")
        state["depth_score"] = 0.0
    return state

def calculate_final_score(state: State) -> State:
    """
    calculate the final score based on individual component scores
    """
    state["final_score"] = (
        state["relevance_score"] * 0.3 +
        state["grammar_score"] * 0.2 +
        state["structure_score"] * 0.2 +
        state["depth_score"] * 0.3
    )
    return state


# initialize the StateGraph
workflow = StateGraph(State)

# add nodes to the graph
workflow.add_node("check_relevance", check_relevance)
workflow.add_node("check_grammar", check_grammar)
workflow.add_node("analyze_structure", analyze_structure)
workflow.add_node("evaluate_depth", evaluate_depth)
workflow.add_node("calculate_final_score", calculate_final_score)

# define and add conditional edges
workflow.add_conditional_edges(
    "check_relevance",
    lambda x: "check_grammar" if x["relevance_score"] > 0.5 else "calculate_final_score"
)
workflow.add_conditional_edges(
    "check_grammar",
    lambda x: "analyze_structure" if x["grammar_score"] > 0.6 else "calculate_final_score"
)
workflow.add_conditional_edges(
    "analyze_structure",
    lambda x: "evaluate_depth" if x["structure_score"] > 0.7 else "calculate_final_score"
)
workflow.add_conditional_edges(
    "evaluate_depth",
    lambda x: "calculate_final_score"
)

# set the entry point
workflow.set_entry_point("check_relevance")

# set the exit point
workflow.add_edge("calculate_final_score", END)

# compile the graph
app = workflow.compile()

# ESSAY GRADING FUNCTION
def grade_essay(topic: str, essay: str) -> dict:
    """
    grade the given essay using the defined workflow
    """
    initial_state = State(
        topic=topic,
        essay=essay,
        relevance_score=0.0,
        grammar_score=0.0,
        structure_score=0.0,
        depth_score=0.0,
        final_score=0.0
    )
    result = app.invoke(initial_state)
    return result