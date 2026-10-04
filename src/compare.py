from datetime import date, timedelta

from graph import ask
from rag import llm

EXAM = (date.today() + timedelta(days=10)).isoformat()

QUESTIONS = [
    ("Direct", "What is the minimum attendance requirement?"),
    ("Direct", "What are the criteria for promotion to higher semesters?"),
    ("Direct", "How many total credits are required for the B.Tech degree?"),
    ("Direct", "What happens if a student gets an F grade in a course?"),
    ("Direct", "What are the rules regarding Continuous Internal Evaluation (CIE)?"),
    ("Direct", "What are the rules for Additional Mathematics?"),
    ("RAG", "Summarize the 8th semester internship guidelines"),
    ("RAG", "How is the 8th semester internship evaluated?"),
    ("RAG", "What companies visit for placements?"),
    ("RAG", "What are the highest and average salary packages offered during placements?"),
    ("RAG", "Which major recruiters offer placement opportunities for engineering students?"),
    ("Tool", "What is (8.5 * 4 + 9 * 3) / 7?"),
    ("Tool", "What percentage is 42 out of 56 classes attended?"),
    ("Tool", "How many days are left for semester exams?"),
    ("Study plan", f"Make a study plan for Algorithms and Databases, 3 hours a day, exam on {EXAM}"),
    ("Study plan", f"Make a study plan for Operating Systems and Networks, 2 hours a day, exam on {EXAM}"),
    ("Unknown", "What is the policy for hostel fee refunds?"),
    ("Unknown", "Can students apply for campus space missions?"),
    ("Unknown", "What is the capital of France?"),
    ("Multi-step", "Summarize the attendance rules and tell me what percentage 30 out of 40 classes is"),
]


def basic_llm(question):
    return llm.invoke(question).content.strip()


def clean(text):
    return text.replace("\n", " ").replace("|", "/")


if __name__ == "__main__":
    rows = ["| Type | Question | Basic LLM | RAG |", "|---|---|---|---|"]
    for kind, question in QUESTIONS:
        print(f"Running: {question}")
        rows.append(f"| {kind} | {clean(question)} | {clean(basic_llm(question))} | {clean(ask(question))} |")
    table = "\n".join(rows)
    print(table)
    with open("comparison_results.md", "w", encoding="utf-8") as file:
        file.write(table)