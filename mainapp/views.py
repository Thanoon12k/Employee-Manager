
import json
from django.http import JsonResponse
from mainapp.models import Announcement, Answer, Question, Report, User
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt


def GetUserFromToken(request):
    token_key = request.headers.get('Authorization', '').split('Token ')[-1]
    token = Token.objects.filter(key=token_key).first()
    if token is None:
        return None
    return token.user

def getAnnouncement(request):
    user=GetUserFromToken(request)
    if user is None:
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
    user=GetUserFromToken(request)
    if user is None:
        return JsonResponse({"error": "Invalid token"}, status=401)
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
    user=GetUserFromToken(request)
    if user is None:
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
    user = GetUserFromToken(request)
    if user is None:
        return JsonResponse({"error": "Invalid token"}, status=401)
    try:
        data = json.loads(request.body)
        report_id = data.get("report_id")
        answers = data.get("answers", [])

        if not report_id or not answers:
            return JsonResponse({"error": "Invalid data"}, status=400)

        report = Report.objects.get(id=report_id)

        # Check if the user has already submitted the report
        if report.users_submitted.filter(id=user.id).exists():
            return JsonResponse({
                "already exist": f"User '{user.username}' has already submitted answers for the report"
            }, status=208 )

        for answer in answers:
            question_id = answer.get("question_id")
            text_answer = answer.get("text_answer")
            selected_option = answer.get("selected_option")
            true_false_answer = answer.get("true_false_answer")

            if not question_id:
                continue

            try:
                question = report.questions.get(id=question_id)
            except Question.DoesNotExist:
                return JsonResponse({
                    "error": f"Question with ID {question_id} does not exist in the report"
                }, status=400)

            Answer.objects.create(
                report=report,
                user=user,
                question=question,
                text_answer=text_answer,
                selected_option=selected_option,
                true_false_answer=true_false_answer,
            )

        report.users_submitted.add(user)
        report.save()

        return JsonResponse({"message": "Answers submitted successfully"}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
