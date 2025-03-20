from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from .models import User, Questionnaire, Question, FormalBook
from .serializers import UserSerializer, QuestionnaireSerializer, QuestionSerializer, FormalBookSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

class TokenAuthView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user:
            # Generate a token for the authenticated user
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "status": "success",
                    "token": token.key,
                    "user": {
                        "username": user.username,
                        "email": user.email,
                        "is_manager": user.is_manager,
                        "is_superuser": user.is_superuser,
                    },
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class UserViewSet(viewsets.ModelViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class QuestionnaireViewSet(viewsets.ModelViewSet):
    queryset = Questionnaire.objects.none()
    serializer_class = QuestionnaireSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Show only questionnaires belonging to the authenticated user
            return Questionnaire.objects.filter(user=user)
        else:
            return Questionnaire.objects.none()


class QuestionViewSet(viewsets.ModelViewSet):
    queryset= Question.objects.none()
    serializer_class = QuestionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Show only questions related to the user's questionnaires
            return Question.objects.filter(inquery__user=user)
        else:
            return Question.objects.none()


class FormalBookViewSet(viewsets.ModelViewSet):
    queryset= FormalBook.objects.none()
    serializer_class = FormalBookSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Show only formal books linked to the authenticated user
            return FormalBook.objects.filter(users=user)
        else:
            return FormalBook.objects.none()
