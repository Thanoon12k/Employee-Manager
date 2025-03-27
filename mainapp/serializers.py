from rest_framework import serializers
from .models import Question, User, FormalBook,Query,QueryResponse



class FormalBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormalBook
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'option1', 'option2', 'option3', 'option4']


class QuerySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)  # Nested questions

    class Meta:
        model = Query
        fields = ['id', 'title', 'description', 'questions']




class QueryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryResponse
        fields = ['id', 'query', 'text_answer', 'selected_option', 'true_false_answer', 'response_date', 'user']
        read_only_fields = ['user', 'response_date']  # Prevent user and response_date modification


