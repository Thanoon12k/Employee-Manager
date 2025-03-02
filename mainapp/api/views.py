from rest_framework import viewsets
from ..models import User, Questionnaire, Question, FormalBook
from .serializers import UserSerializer, QuestionnaireSerializer, QuestionSerializer, FormalBookSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class QuestionnaireViewSet(viewsets.ModelViewSet):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class FormalBookViewSet(viewsets.ModelViewSet):
    queryset = FormalBook.objects.all()
    serializer_class = FormalBookSerializer
