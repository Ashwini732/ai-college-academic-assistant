from datetime import date, datetime, timedelta


def parse_date(value):
    return datetime.strptime(value, "%Y-%m-%d").date()


def build_plan(subjects, hours_per_day, exam_date, weights=None):
    days_left = (parse_date(exam_date) - date.today()).days
    if days_left < 2:
        raise ValueError("Exam date must be at least 2 days away")
    weights = weights or {subject: 1 for subject in subjects}
    total_weight = sum(weights[subject] for subject in subjects)
    plan = []
    for offset in range(days_left - 1):
        day = date.today() + timedelta(days=offset)
        for subject in subjects:
            hours = round(hours_per_day * weights[subject] / total_weight, 1)
            plan.append({"date": day.isoformat(), "subject": subject, "hours": hours})
    revision_day = parse_date(exam_date) - timedelta(days=1)
    plan.append({"date": revision_day.isoformat(), "subject": "Revision of all subjects", "hours": hours_per_day})
    return plan


def format_plan(plan):
    lines = ["| Date | Subject | Hours |", "|---|---|---|"]
    for row in plan:
        lines.append(f"| {row['date']} | {row['subject']} | {row['hours']} |")
    return "\n".join(lines)


def update_details(details, changes):
    updated = dict(details)
    if changes.get("hours_per_day"):
        updated["hours_per_day"] = float(changes["hours_per_day"])
    if changes.get("exam_date"):
        updated["exam_date"] = changes["exam_date"]
    subjects = list(updated["subjects"])
    for subject in changes.get("add_subjects") or []:
        if subject.lower() not in {s.lower() for s in subjects}:
            subjects.append(subject)
    removed = {s.lower() for s in changes.get("remove_subjects") or []}
    subjects = [s for s in subjects if s.lower() not in removed]
    weights = {s: updated["weights"].get(s, 1) for s in subjects}
    for name, weight in (changes.get("weights") or {}).items():
        for subject in subjects:
            if subject.lower() == name.lower():
                weights[subject] = float(weight)
    updated["subjects"] = subjects
    updated["weights"] = weights
    return updated


if __name__ == "__main__":
    exam = (date.today() + timedelta(days=7)).isoformat()
    print(format_plan(build_plan(["Algorithms", "Databases"], 4, exam, {"Algorithms": 2, "Databases": 1})))