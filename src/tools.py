import ast
import operator
from datetime import date, datetime

from langchain_core.tools import tool

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

ACADEMIC_EVENTS = {
    "internal assessment 1": "2026-11-10",
    "internal assessment 2": "2026-12-15",
    "semester exams": "2027-01-20",
}


def evaluate(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](evaluate(node.left), evaluate(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](evaluate(node.operand))
    raise ValueError("Unsupported expression")


@tool
def calculator(expression: str) -> str:
    """Calculate a math expression such as attendance or CGPA percentages."""
    try:
        result = evaluate(ast.parse(expression, mode="eval").body)
        return str(result)
    except Exception:
        return "Invalid expression"


@tool
def days_until(target_date: str) -> str:
    """Count the days left until a date written as YYYY-MM-DD."""
    try:
        target = datetime.strptime(target_date, "%Y-%m-%d").date()
    except ValueError:
        return "Invalid date. Use YYYY-MM-DD"
    return str((target - date.today()).days)


@tool
def get_event_date(event_name: str) -> str:
    """Get the date of an academic event such as an exam or assessment."""
    return ACADEMIC_EVENTS.get(event_name.strip().lower(), "Event not found")


TOOLS = [calculator, days_until, get_event_date]


if __name__ == "__main__":
    print(calculator.invoke("(8.5 * 4 + 9 * 3) / 7"))
    print(days_until.invoke("2026-12-01"))
    print(get_event_date.invoke("semester exams "))