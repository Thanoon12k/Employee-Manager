
from django.http import JsonResponse
from mainapp.models import Announcement
from django.core.exceptions import PermissionDenied

def getBoooks(request):
    user = request.user
    if user.is_authenticated:
        announcements = Announcement.objects.filter(users=user)
        return JsonResponse({"announcements": list(announcements.values())}, safe=False)
    return 



# class QueryViewSet(viewsets.ModelViewSet):
#     queryset = Query.objects.all()
#     serializer_class = QuerySerializer

#     @action(detail=True, methods=['post'], url_path='submit-responses')
#     def submit_responses(self, request, pk=None):
#         """
#         Handles bulk submission of responses for a query.
#         """
#         query = self.get_object()  # Get the specific query (form)
#         user = request.user
        
#         responses = request.data.get('responses')  # Expecting bulk responses as a list
#         for response_data in responses:
#             question_id = response_data.get('question')
#             text_answer = response_data.get('text_answer')
#             selected_option = response_data.get('selected_option')
#             true_false_answer = response_data.get('true_false_answer')

#             # Get the corresponding question
#             question = Question.objects.get(id=question_id)

#             # Create the QueryResponse object
#             QueryResponse.objects.create(
#                 query=query,
#                 user=user,
#                 question=question,
#                 text_answer=text_answer,
#                 selected_option=selected_option,
#                 true_false_answer=true_false_answer
#             )

#         return Response({"message": "Responses submitted successfully!"}, status=201)





# class QueryResponseViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet for handling query responses.
#     Provides endpoints to view, create, and manage responses.
#     """
#     queryset = QueryResponse.objects.all()
#     serializer_class = QueryResponseSerializer
#     # authentication_classes = [BasicAuthentication, TokenAuthentication]
#     # permission_classes = [permissions.IsAuthenticated,]

#     def get_queryset(self):
#         """
#         Filter responses based on the authenticated user.
#         """
#         user = self.request.user
#         if user.is_authenticated:
#             return QueryResponse.objects.filter(user=user)  # Fetch only user's responses
#         return QueryResponse.objects.none()  # No responses for unauthenticated users

#     def perform_create(self, serializer):
#         """
#         Automatically associate the authenticated user with the response being created.
#         """
#         user = self.request.user
#         if user.is_authenticated:
#             serializer.save(user=user)  # Save response with the current user
#         else:
#             raise Exception("You must be authenticated to submit a response.")


# class TokenAuthView(APIView):
#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         password = request.data.get('password')

#         # Authenticate the user
#         user = authenticate(username=username, password=password)
#         if user:
#             # Generate a token for the authenticated user
#             token, created = Token.objects.get_or_create(user=user)
#             return Response(
#                 {
#                     "status": "success",
#                     "token": token.key,
#                     "user": {
#                         "username": user.username,
#                         "email": user.email,
#                         "is_manager": user.is_manager,
#                         "is_superuser": user.is_superuser,
#                     },
#                 },
#                 status=status.HTTP_200_OK,
#             )
#         else:
#             return Response(
#                 {"detail": "Invalid credentials"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )


# class UserViewSet(viewsets.ModelViewSet):
    
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]



# @api_view(['POST'])
# def login_view(request):
#     """
#     Custom login view that accepts JSON payload.
#     """
#     permission_classes = [AllowAny]  # Allow unauthenticated access to this endpoint

#     # Extract username and password from request data
#     data = request.data
#     username = data.get('username')
#     password = data.get('password')

#     # Authenticate user
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         # Get or create token for the authenticated user
#         token, _ = Token.objects.get_or_create(user=user)
#         return JsonResponse({"token": token.key, "message": "Login successful."}, status=200)
#     else:
#         return JsonResponse({"error": "Invalid username or password."}, status=400)




# from django.contrib import admin
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from django.conf import settings
# from django.conf.urls.static import static
# # from mainapp.views import login_view

# from .views import *

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('get_user_announcements/', getBoooks, name='get_announcements'),  # Custom endpoint to get announcements
   
# ]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
# # Initialize router
# router = DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'queries', QueryViewSet, basename='query')  # Manage Query APIs
# router.register(r'query-responses', QueryResponseViewSet, basename='queryresponse')  # Manage Responses APIs
# router.register(r'formalbooks', FormalBookViewSet)
    # path('user/',getuserFormalBooks ),
    # path('api/auth/', TokenAuthView.as_view(), name='token-auth'),  # Token authentication endpoint
    # path('admin/', admin.site.urls),
    # path('api/', include(router.urls)),  # Add this to include the router-generated URLs
    # path('api/login/', login_view),  # Custom login endpoint