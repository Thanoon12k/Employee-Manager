from django.shortcuts import render
from mainapp.models import Report

import io
import base64
from matplotlib import pyplot as plt

def generate_pie_chart(values, labels):
    """
    Generate pie chart for statistical visualization.

    Args:
        values (list): Numerical values for each slice of the pie.
        labels (list): Labels for each slice of the pie.

    Returns:
        str: Base64-encoded PNG image string for embedding in HTML.
    """
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#99ff99', '#ffcc99', '#ff9999'])
    ax.axis('equal')  # Equal aspect ratio ensures circular pie chart

    # Save chart to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    base64_string = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close(fig)
    return f"data:image/png;base64,{base64_string}"


def report_statistics_view(request):
    # Fetch report ID from query parameters
    selected_report_id = request.GET.get('report_id')
    selected_report = Report.objects.filter(id=selected_report_id).first() if selected_report_id else None
    questions_data = []

    # Check if a report is selected and process its questions
    if selected_report:
        questions = selected_report.linked_questions.filter(question_type__in=["OPTIONS", "T/F"])
        
        for question in questions:
            pie_chart = None
            # Example pie chart generation for OPTIONS and T/F questions
            if question.question_type == "OPTIONS":
                options = question.options_data.split("-") if question.options_data else []
                answers = question.linked_answers.values_list('answer_data', flat=True)
                # Corrected: Use filter instead of count with arguments
                values = [answers.filter(answer_data=option).count() for option in options]
                pie_chart = generate_pie_chart(values, options) if any(values) else None
            elif question.question_type == "T/F":
                answers = question.linked_answers.values_list('answer_data', flat=True)
                # Corrected: Use filter instead of count with arguments
                true_count = answers.filter(answer_data="true").count()
                false_count = answers.filter(answer_data="false").count()
                pie_chart = generate_pie_chart([true_count, false_count], ["True", "False"]) if true_count or false_count else None
            
            questions_data.append({
                'question_text': question.question,
                'pie_chart': pie_chart,
            })

    # print(f"Reports: {Report.objects.all()}")  # Debugging: List all reports
    # print(f"Selected Report: {selected_report}")  # Debugging: Check the selected report
    # print(f"Questions Data: {questions_data}")  # Debugging: Inspect generated question data

    return render(request, 'report_statistics.html', {
        'reports': Report.objects.all(),  # Pass all reports to the template
        'selected_report': selected_report,  # Pass the selected report
        'questions_data': questions_data,  # Pass the processed questions
    })
