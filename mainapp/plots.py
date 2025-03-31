from django.shortcuts import render
from mainapp.models import Report
from arabic_reshaper import reshape
from bidi.algorithm import get_display
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np
import matplotlib

# Use a non-interactive backend for Matplotlib
matplotlib.use('Agg')
from arabic_reshaper import reshape
from bidi.algorithm import get_display
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np
import matplotlib

# Use a non-interactive backend for Matplotlib
matplotlib.use('Agg')

def autopct_func(pct):
    return f'{pct:.1f}%' if pct > 0 else ''  # Hide if 0%

def generate_pie_chart(values, labels):
    # Reshape and apply Bidi algorithm for Arabic labels
    labels = [get_display(reshape(label)) for label in labels]

    # Create the figure
    fig, ax = plt.subplots(figsize=(6, 6))  # Larger size for better visibility

    # Generate the pie chart without labels
    wedges, texts, autotexts = ax.pie(
        values,
        labels=None,  # Remove labels from slices
        startangle=90,
        autopct=autopct_func,  # Use custom function to hide 0%
        colors=['#66b3ff', '#99ff99', '#ffcc99', '#ff9999'],
        pctdistance=0.8  
    )
    ax.axis('equal')  # Ensure the pie chart is circular

    # Create a legend table below the pie chart
    ax.legend(wedges, labels, loc='upper center', bbox_to_anchor=(0.5, -0.05),
              fancybox=True, shadow=True, ncol=2)  # Adjust position & columns

    # Save the plot to a buffer
    buffer = BytesIO()
    plt.tight_layout()  # Ensure everything fits properly
    plt.savefig(buffer, format='png', dpi=300)  # High DPI ensures clear text
    buffer.seek(0)

    # Encode the image as a base64 string
    base64_string = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close(fig)

    return f"data:image/png;base64,{base64_string}"

def report_statistics_view(request):
    # Fetch report ID from query parameters
    selected_report_id = request.GET.get('report_id')
    selected_report = Report.objects.filter(id=selected_report_id).first() if selected_report_id else None
    questions_data = []

    # Check if a report is selected and process its questions
    if selected_report:
        questions = selected_report.linked_questions.filter(question_type__in=["multiple_choice", "T/F"])
        
        for question in questions:
            pie_chart = None
            # Example pie chart generation for OPTIONS and T/F questions
            if question.question_type == "multiple_choice":
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

  
    return render(request, 'report_statistics.html', {
        'reports': Report.objects.all(),  # Pass all reports to the template
        'selected_report': selected_report,  # Pass the selected report
        'questions_data': questions_data,  # Pass the processed questions
    })
