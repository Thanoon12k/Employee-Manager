from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from .models import User, Questionnaire, Question, FormalBook
from .serializers import UserSerializer, QuestionnaireSerializer, QuestionSerializer, FormalBookSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
import json
from django.views.decorators.csrf import csrf_exempt


class LoginView(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Generate Token Here
            return Response({'status': 'success', 'access': 'YourAccessTokenHere'})
        else:
            return Response({'status': 'fail', 'detail': 'No active account found with the given credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

class QuestionnaireViewSet(viewsets.ModelViewSet):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

class FormalBookViewSet(viewsets.ModelViewSet):
    queryset = FormalBook.objects.all()
    serializer_class = FormalBookSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]