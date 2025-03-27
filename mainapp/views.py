from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework import permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import User, FormalBook, Query, Question, QueryResponse
from .serializers import QueryResponseSerializer, UserSerializer, FormalBookSerializer, QuerySerializer

class QueryViewSet(viewsets.ModelViewSet):
    queryset = Query.objects.all()
    serializer_class = QuerySerializer

    @action(detail=True, methods=['post'], url_path='submit-responses')
    def submit_responses(self, request, pk=None):
        """
        Handles bulk submission of responses for a query.
        """
        query = self.get_object()  # Get the specific query (form)
        user = request.user
        
        responses = request.data.get('responses')  # Expecting bulk responses as a list
        for response_data in responses:
            question_id = response_data.get('question')
            text_answer = response_data.get('text_answer')
            selected_option = response_data.get('selected_option')
            true_false_answer = response_data.get('true_false_answer')

            # Get the corresponding question
            question = Question.objects.get(id=question_id)

            # Create the QueryResponse object
            QueryResponse.objects.create(
                query=query,
                user=user,
                question=question,
                text_answer=text_answer,
                selected_option=selected_option,
                true_false_answer=true_false_answer
            )

        return Response({"message": "Responses submitted successfully!"}, status=201)




class FormalBookViewSet(viewsets.ModelViewSet):
    queryset= FormalBook.objects.none()
    serializer_class = FormalBookSerializer
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated,]
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return FormalBook.objects.filter(users=user)
        else:
            return FormalBook.objects.none()


class QueryResponseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling query responses.
    Provides endpoints to view, create, and manage responses.
    """
    queryset = QueryResponse.objects.all()
    serializer_class = QueryResponseSerializer
    # authentication_classes = [BasicAuthentication, TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        """
        Filter responses based on the authenticated user.
        """
        user = self.request.user
        if user.is_authenticated:
            return QueryResponse.objects.filter(user=user)  # Fetch only user's responses
        return QueryResponse.objects.none()  # No responses for unauthenticated users

    def perform_create(self, serializer):
        """
        Automatically associate the authenticated user with the response being created.
        """
        user = self.request.user
        if user.is_authenticated:
            serializer.save(user=user)  # Save response with the current user
        else:
            raise Exception("You must be authenticated to submit a response.")


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



@api_view(['POST'])
def login_view(request):
    """
    Custom login view that accepts JSON payload.
    """
    permission_classes = [AllowAny]  # Allow unauthenticated access to this endpoint

    # Extract username and password from request data
    data = request.data
    username = data.get('username')
    password = data.get('password')

    # Authenticate user
    user = authenticate(username=username, password=password)
    if user is not None:
        # Get or create token for the authenticated user
        token, _ = Token.objects.get_or_create(user=user)
        return JsonResponse({"token": token.key, "message": "Login successful."}, status=200)
    else:
        return JsonResponse({"error": "Invalid username or password."}, status=400)

