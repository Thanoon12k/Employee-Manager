from rest_framework import serializers
from .models import User, Questionnaire, Question, FormalBook

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class FormalBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormalBook
        fields = '__all__'
