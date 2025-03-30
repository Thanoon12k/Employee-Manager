
import json
from django.http import JsonResponse
from mainapp.models import Announcement, Answer, User
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt

def getAnnouncement(request):
    user=request.user
    token_key = request.headers.get('Authorization', '').split('Token ')[-1]
    print(f"Token Key: {token_key}")  # Log the token key
    try:
        token = Token.objects.get(key=token_key)
        user = token.user
    except Token.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, status=401)
    announcements = Announcement.objects.filter(users=user)
    announcements_data = list(announcements.values())
    for announcement in announcements_data:
        if announcement['image']:
            announcement['image'] = request.build_absolute_uri('/media/' + announcement['image'])
        if announcement['file']:
            announcement['file'] = request.build_absolute_uri('/media/' + announcement['file'])
    return JsonResponse({"announcements": announcements_data}, safe=False)
    


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
    token_key = request.headers.get('Authorization', '').split('Token ')[-1]
    try:
        token = Token.objects.get(key=token_key)
        user = token.user
    except Token.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, status=401)
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
    


@csrf_exempt
def authenticate_user_and_get_token(request):
    data = json.loads(request.body)
    print(f"Request Data: {data}")  # Log the request body
    username = data.get('username')
    password = data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "birth_date": user.birth_date,
            "address": user.address,
            "phone": user.phone,
            "image": request.build_absolute_uri(user.image.url) if user.image else None,
            "token": token.key
        }
        return JsonResponse(user_data, status=200)
    return JsonResponse({"error": "Invalid credentials "}, status=401)


@csrf_exempt
def submit_report(request):
    user=request.user
    if request.method == "POST":
        token_key = request.headers.get('Authorization', '').split('Token ')[-1]
        print(f"Token Key: {token_key}")  # Log the token key
    try:
        token = Token.objects.get(key=token_key)
        user = token.user
    except Token.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, status=401)
    try:
        data = json.loads(request.body)
        report_id = data.get("report_id")
        answers = data.get("answers", [])

        if not report_id or not answers:
            return JsonResponse({"error": "Invalid data"}, status=400)

        for answer in answers:
            question_id = answer.get("question_id")
            text_answer = answer.get("text_answer")
            selected_option = answer.get("selected_option")
            true_false_answer = answer.get("true_false_answer")

            if not question_id:
                continue

            Answer.objects.create(
                report_id=report_id,
                user=user,
                question_id=question_id,
                text_answer=text_answer,
                selected_option=selected_option,
                true_false_answer=true_false_answer,
            )

        return JsonResponse({"message": "Answers submitted successfully"}, status=201)
    except Exception as e:
        return JsonResponse({"error in submitting report": str(e)}, status=500)
