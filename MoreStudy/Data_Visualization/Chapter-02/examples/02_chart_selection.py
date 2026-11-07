# Choose a chart from the question rather than from appearance.
questions = {
    "Branch totals?": "Bar chart",
    "Visits changing over time?": "Line chart",
    "How are daily counts distributed?": "Histogram",
    "Visits related to new members?": "Scatter plot",
}
for question, chart in questions.items():
    print(f"{question} -> {chart}")
