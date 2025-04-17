
import json
from django.http import JsonResponse
from mainapp.models import Announcement, Answer, Question, Report, User,Complaint
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
    # user=GetUserFromToken(request)
    user=request.user
    if user is None or user.is_anonymous:
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
    if user is None or user.is_anonymous:
        return JsonResponse({"error": "Invalid token"}, status=401)
    
    if user.is_manager or user.is_superuser:
        users = User.objects.all()
        users_data = list(users.values('id', 'username', 'email', 'birth_date', 'address', 'phone', 'image'))
        for user_data in users_data:
            if user_data['image']:
                user_data['image'] = request.build_absolute_uri('/media/' + user_data['image'])
        return JsonResponse({"users": users_data}, safe=False)
    return JsonResponse({"error": "You are not manager"}, status=403)            

def get_user_reports(request):
    user=request.user
    if user is None or user.is_anonymous:
        return JsonResponse({"error": "Invalid token"}, status=401)
    reports = user.linked_reports.all()
    reports_data = []
    for report in reports:
        questions = report.linked_questions.all()
        questions_data = list(questions.values('id', 'question', 'question_type', 'options_data', 'is_statistic'))
        reports_data.append({
            "id": report.id,
            "title": report.title,
            "description": report.description,
            "pub_date": report.pub_date,
            "questions": questions_data
        })
    return JsonResponse({"reports": reports_data}, safe=False, json_dumps_params={'ensure_ascii': False})

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
        report_title = data.get("report_title")
        answers = data.get("answers", [])

        if not report_title or not answers:
            return JsonResponse({"error": "Invalid data"}, status=400)

        try:
            report = Report.objects.get(title=report_title)
        except Report.DoesNotExist:
            return JsonResponse({"error": f"Report with title '{report_title}' does not exist"}, status=400)

        # Check if the user has already submitted the report
        if report.users_submitted.filter(id=user.id).exists():
            return JsonResponse({
                "error": f"User '{user.username}' has already submitted answers for the report"
            }, status=208)

        for answer in answers:
            question_title = answer.get("question_title")
            answer_data = answer.get("answer_data")

            if not question_title or answer_data is None:
                return JsonResponse({"error": "Invalid answer data"}, status=400)

            try:
                question = report.linked_questions.get(question=question_title)
            except Question.DoesNotExist:
                return JsonResponse({
                    "error": f"Question with title '{question_title}' does not exist in the report"
                }, status=400)

            Answer.objects.create(
                report=report,
                user=user,
                question=question,
                answer_data=answer_data,
            )

        report.users_submitted.add(user)
        report.save()

        return JsonResponse({"message": "Answers submitted successfully"}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def getComplaintsList(request):
    user = request.user
    if user is None or user.is_anonymous:
        return JsonResponse({"error": "Invalid token"}, status=401)
    
    complaints = Complaint.objects.all()
    complaints_data = list(complaints.values('id', 'text', 'complainant', 'respondent', 'created_at', 'is_resolved'))
    return JsonResponse({"complaints": complaints_data}, safe=False)


def addComplaint(request):
    user = request.user
    if user is None or user.is_anonymous:
        return JsonResponse({"error": "Invalid token"}, status=401)

    try:
        data = json.loads(request.body)
        text = data.get("text")
        respondent_id = data.get("respondent")
    
        if not text or not respondent_id:
            return JsonResponse({"error": "Invalid data"}, status=400)
        
        respondent = User.objects.get(id=respondent_id)
    
        complaint = Complaint.objects.create(
            text=text,
            complainant=user,
            respondent=respondent,
            is_resolved=False
        )
        return JsonResponse({"message": "Complaint added successfully"}, status=201)
    except User.DoesNotExist:
        return JsonResponse({"error": "Respondent user not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
