from django.shortcuts import render
from mainapp.models import Report

def report_statistics_view(request):
    reports = Report.objects.all()  # Fetch all reports
    selected_report_id = request.GET.get('report_id')  # Get selected report ID from query params
    selected_report = None
    questions_data = []

    if selected_report_id:
        try:
            selected_report = Report.objects.get(id=selected_report_id)
            print(f"Selected Report: {selected_report}")  # Debugging line to check the selected report
            questions = selected_report.linked_questions.all()

            for question in questions:
                if question.question_type in ['multiple_choice', 'true_false']:
                    pie_chart = None
                    statistics = getattr(question, 'statistics', None)
                    if statistics and hasattr(statistics, 'generate_pie_chart'):
                        pie_chart = statistics.generate_pie_chart()
                    questions_data.append({
                        'question_text': question.question_text,
                        'pie_chart': pie_chart,
                    })
        except Report.DoesNotExist:
            selected_report = None

    return render(request, 'report_statistics.html', {
        'reports': reports,
        'selected_report': selected_report,
        'questions_data': questions_data,
    })
