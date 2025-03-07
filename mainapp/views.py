from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from .models import User, Questionnaire, Question, FormalBook
from .serializers import UserSerializer, QuestionnaireSerializer, QuestionSerializer, FormalBookSerializer

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
