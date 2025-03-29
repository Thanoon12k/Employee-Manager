
import json
from django.http import JsonResponse
from mainapp.models import Announcement, User
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt

def getBoooks(request):
    user = request.user
    if user.is_authenticated:
        announcements = Announcement.objects.filter(users=user)
        announcements_data = list(announcements.values())
        for announcement in announcements_data:
            if announcement['image']:
                announcement['image'] = request.build_absolute_uri('/media/' + announcement['image'])
            if announcement['file']:
                announcement['file'] = request.build_absolute_uri('/media/' + announcement['file'])
        return JsonResponse({"announcements": announcements_data}, safe=False)
    return JsonResponse({"error": "User not authenticated"}, status=401)


def get_users_list(request):
    user=request.user
    if user.is_authenticated:
        if user.is_manager or user.is_superuser:
            users = User.objects.all()
            users_data = list(users.values('id', 'username', 'email', 'birth_date', 'address', 'phone', 'image'))
            for user_data in users_data:
                if user_data['image']:
                    user_data['image'] = request.build_absolute_uri('/media/' + user_data['image'])
            return JsonResponse({"users": users_data}, safe=False)
        return JsonResponse({"error": "You are not manager"}, status=403)            
    return JsonResponse({"error": "User not authenticated"}, status=401)

def get_user_reports(request):
    user = request.user
    if user.is_authenticated:
        reports = user.linked_reports.all()
        reports_data = []
        for report in reports:
            questions = report.questions.all()
            questions_data = list(questions.values('id', 'question_text', 'question_type', 'option1', 'option2', 'option3', 'option4'))
            reports_data.append({
                "id": report.id,
                "title": report.title,
                "description": report.description,
                "pub_date": report.pub_date,
                "questions": questions_data
            })
        return JsonResponse({"reports": reports_data}, safe=False)
    return JsonResponse({"error": "User not authenticated"}, status=401)


@csrf_exempt
def authenticate_user_and_get_token(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        token,_=Token.objects.get_or_create(user=user)
        return JsonResponse({"token":token.key}, status=200)
    return JsonResponse({"error": "Invalid credentials "}, status=401)
  