from django.shortcuts import render
from django.urls import reverse

def list_urls(request):
    urls = [
        {'name': 'Users', 'url': reverse('user-list')},
        {'name': 'Questionnaires', 'url': reverse('questionnaire-list')},
        {'name': 'Questions', 'url': reverse('question-list')},
        {'name': 'Formal Books', 'url': reverse('formalbook-list')},
    ]
    return render(request, 'list_urls.html', {'urls': urls})
