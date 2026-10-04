from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from rag import format_docs, llm, retriever

ACADEMIC_PROMPT = ChatPromptTemplate.from_template(
    """You are an AI-based College Academic Assistant.
Answer clearly and concisely using ONLY the context below.
Use bullet points or numbered lists where helpful.
Do not mention file names, page numbers or chunk numbers.
If the information is not in the context, say: "I'm sorry, but that information is not available in the uploaded college documents or website."

Context:
{context}

Question:
{question}

Answer:"""
)

SUMMARY_PROMPT = ChatPromptTemplate.from_template(
    """You are an AI-based College Academic Assistant.
Summarize the topic below using ONLY the context.
Give a short overview of 2 to 3 sentences, then 5 to 7 key points as bullets.
If the context has nothing on the topic, say: "I'm sorry, but that information is not available in the uploaded college documents or website."

Context:
{context}

Topic:
{topic}

Summary:"""
)

STUDY_PLAN_PROMPT = ChatPromptTemplate.from_template(
    """You are an AI-based College Academic Assistant.
Create a day-by-day study plan.
Subjects: {subjects}
Study hours available per day: {hours_per_day}
Days left until the exam: {days_left}

Rules:
1. Split the hours across subjects and give harder or larger subjects more time.
2. Use topics from the syllabus context when they are available.
3. Add one revision day at the end.
4. Present the plan as a table with the columns Day, Subject and Topics.

Syllabus context:
{context}

Study plan:"""
)


def build_chain(prompt):
    return prompt | llm | StrOutputParser()


def academic_answer(question):
    context = format_docs(retriever.invoke(question))
    return build_chain(ACADEMIC_PROMPT).invoke({"context": context, "question": question})


def summarize(topic):
    context = format_docs(retriever.invoke(topic))
    return build_chain(SUMMARY_PROMPT).invoke({"context": context, "topic": topic})


def study_plan(subjects, hours_per_day, days_left):
    context = format_docs(retriever.invoke(f"syllabus topics {subjects}"))
    return build_chain(STUDY_PLAN_PROMPT).invoke(
        {
            "context": context,
            "subjects": subjects,
            "hours_per_day": hours_per_day,
            "days_left": days_left,
        }
    )


if __name__ == "__main__":
    print(academic_answer("What is the minimum attendance requirement?"))
    print("=" * 60)
    print(summarize("internship guidelines for the 8th semester"))
    print("=" * 60)
    print(study_plan("Algorithms, Databases", 3, 10))