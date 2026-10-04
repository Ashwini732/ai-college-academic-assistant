import json
from datetime import date, timedelta
from typing import TypedDict

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START, StateGraph

from src.chains import ACADEMIC_PROMPT, SUMMARY_PROMPT
from src.planner import build_plan, format_plan, update_details
from src.rag import format_docs, llm, retriever
from src.tools import ACADEMIC_EVENTS, calculator, days_until, get_event_date

NOT_AVAILABLE = "I'm sorry, but that information is not available in the uploaded college documents or website."
ASK_DETAILS = (
    "Please tell me your subjects, daily study hours and an exam date at least 2 days away. "
    "Example: Make a study plan for Algorithms and Databases, 3 hours a day, exam on 2026-11-20."
)
CATEGORIES = {"academic", "summary", "study_plan", "modify_plan", "calculation", "deadline"}

PLAN = {}

CLASSIFY_PROMPT = ChatPromptTemplate.from_template(
    """Classify the question into exactly one word:
academic - rules, syllabus, exams, attendance, placements or other college information
summary - asks to summarize a topic or document
study_plan - asks to create a new study plan or schedule
modify_plan - asks to change, update or adjust an existing study plan
calculation - asks for a math or percentage calculation
deadline - asks for days left or the date of an exam
Question: {question}
Reply with only the one word."""
)

EXTRACT_PROMPT = ChatPromptTemplate.from_template(
    """Extract study plan details from the request. Today is {today}.
Return only JSON with the keys subjects (list of strings), hours_per_day (number) and exam_date (YYYY-MM-DD).
Use null for any value that is missing.
Request: {question}"""
)

MODIFY_PROMPT = ChatPromptTemplate.from_template(
    """Today is {today}. The student has this study plan: {plan}
Extract the requested change. Return only JSON with the keys hours_per_day (number), exam_date (YYYY-MM-DD), add_subjects (list), remove_subjects (list) and weights (object mapping a subject name to a number, where 2 means double time and 0.5 means half time).
Use null for anything not mentioned.
Request: {question}"""
)

EXPRESSION_PROMPT = ChatPromptTemplate.from_template(
    """Convert the question into one Python math expression using only numbers and + - * / **.
Reply with only the expression.
Question: {question}"""
)

EVENT_PROMPT = ChatPromptTemplate.from_template(
    """Which one of these events does the question ask about: {events}?
Reply with only the exact event name, or none.
Question: {question}"""
)

REVIEW_PROMPT = ChatPromptTemplate.from_template(
    """Context:
{context}

Answer:
{answer}

Is every statement in the answer supported by the context, or does the answer say the information is not available?
Reply with only yes or no."""
)


class State(TypedDict):
    question: str
    category: str
    context: str
    answer: str
    review: str


def run(prompt, **values):
    return (prompt | llm | StrOutputParser()).invoke(values).strip()


def parse_json(raw):
    return json.loads(raw[raw.find("{"): raw.rfind("}") + 1])


def analyze(state):
    label = run(CLASSIFY_PROMPT, question=state["question"]).lower()
    if label not in CATEGORIES:
        label = "academic"
    return {"category": label}


def retrieve(state):
    return {"context": format_docs(retriever.invoke(state["question"]))}


def generate(state):
    if state["category"] == "summary":
        answer = run(SUMMARY_PROMPT, context=state["context"], topic=state["question"])
    else:
        answer = run(ACADEMIC_PROMPT, context=state["context"], question=state["question"])
    return {"answer": answer}


def review_answer(state):
    verdict = run(REVIEW_PROMPT, context=state["context"], answer=state["answer"]).lower()
    return {"review": "ok" if verdict.startswith("yes") else "retry"}


def fallback(state):
    return {"answer": NOT_AVAILABLE}


def study_plan(state):
    raw = run(EXTRACT_PROMPT, question=state["question"], today=date.today().isoformat())
    try:
        details = parse_json(raw)
        subjects = details["subjects"]
        hours = float(details["hours_per_day"])
        plan = build_plan(subjects, hours, details["exam_date"])
    except Exception:
        return {"answer": ASK_DETAILS}
    PLAN.clear()
    PLAN.update(
        {
            "subjects": subjects,
            "hours_per_day": hours,
            "exam_date": details["exam_date"],
            "weights": {subject: 1 for subject in subjects},
        }
    )
    return {"answer": format_plan(plan)}


def modify_plan(state):
    if not PLAN:
        return {"answer": "Please create a study plan first. " + ASK_DETAILS}
    raw = run(MODIFY_PROMPT, question=state["question"], today=date.today().isoformat(), plan=json.dumps(PLAN))
    try:
        updated = update_details(PLAN, parse_json(raw))
        plan = build_plan(updated["subjects"], updated["hours_per_day"], updated["exam_date"], updated["weights"])
    except Exception:
        return {
            "answer": "I could not apply that change. Try: give more time to Algorithms, "
            "change study hours to 4 per day, or remove Databases."
        }
    PLAN.clear()
    PLAN.update(updated)
    return {"answer": format_plan(plan)}


def calculate(state):
    expression = run(EXPRESSION_PROMPT, question=state["question"])
    return {"answer": f"{expression} = {calculator.invoke(expression)}"}


def deadline(state):
    event = run(EVENT_PROMPT, question=state["question"], events=", ".join(ACADEMIC_EVENTS)).lower()
    event_date = get_event_date.invoke(event)
    if event_date == "Event not found":
        return {"answer": NOT_AVAILABLE}
    return {"answer": f"{event} is on {event_date}, which is {days_until.invoke(event_date)} days from today."}


def route(state):
    return {
        "academic": "retrieve",
        "summary": "retrieve",
        "study_plan": "study_plan",
        "modify_plan": "modify_plan",
        "calculation": "calculate",
        "deadline": "deadline",
    }[state["category"]]


def after_review(state):
    return END if state["review"] == "ok" else "fallback"


builder = StateGraph(State)
builder.add_node("analyze", analyze)
builder.add_node("retrieve", retrieve)
builder.add_node("generate", generate)
builder.add_node("review_answer", review_answer)
builder.add_node("fallback", fallback)
builder.add_node("study_plan", study_plan)
builder.add_node("modify_plan", modify_plan)
builder.add_node("calculate", calculate)
builder.add_node("deadline", deadline)
builder.add_edge(START, "analyze")
builder.add_conditional_edges(
    "analyze", route, ["retrieve", "study_plan", "modify_plan", "calculate", "deadline"]
)
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", "review_answer")
builder.add_conditional_edges("review_answer", after_review, [END, "fallback"])
builder.add_edge("fallback", END)
builder.add_edge("study_plan", END)
builder.add_edge("modify_plan", END)
builder.add_edge("calculate", END)
builder.add_edge("deadline", END)

app = builder.compile()


def ask(question):
    return app.invoke({"question": question})["answer"]


if __name__ == "__main__":
    exam = (date.today() + timedelta(days=6)).isoformat()
    questions = [
        "What is the minimum attendance requirement?",
        "Summarize the internship guidelines",
        "What is 8.5 * 4 + 9 * 3 divided by 7?",
        "How many days are left for semester exams?",
        f"Make a study plan for Algorithms and Databases, 3 hours a day, exam on {exam}",
        "Give more time to Algorithms",
        "Change study hours to 4 per day",
        "What is the policy for hostel fee refunds?",
    ]
    for question in questions:
        print(f"Q: {question}\n{ask(question)}\n{'=' * 60}")