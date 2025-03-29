from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator


# Custom User Model
class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='user_images/', blank=True)
   
    is_superuser = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)


    def __str__(self):
        return self.username
    
# Announcement Model
class Announcement(models.Model):
    users = models.ManyToManyField(User, related_name='linked_announcements', blank=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='images/')
    file = models.FileField(upload_to='files/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])], blank=True,null=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return self.title


# Report Model
class Report(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(User, related_name='linked_reports', blank=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return self.title


# Question Model
class Question(models.Model):
    TEXT = 'text'
    MULTIPLE_CHOICE = 'multiple_choice'
    TRUE_FALSE = 'true_false'

    QUESTION_TYPES = [
        (TEXT, 'Text Answer'),
        (MULTIPLE_CHOICE, 'Multiple Choice'),
        (TRUE_FALSE, 'True/False'),
    ]

    report = models.ForeignKey(Report, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=300)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default=TEXT)
    option1 = models.CharField(max_length=200, blank=True, null=True)
    option2 = models.CharField(max_length=200, blank=True, null=True)
    option3 = models.CharField(max_length=200, blank=True, null=True)
    option4 = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.question_text


# Answer Model
class Answer(models.Model):
    report = models.ForeignKey(Report, related_name='answers', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text_answer = models.TextField(blank=True, null=True)
    selected_option = models.CharField(max_length=200, blank=True, null=True)
    true_false_answer = models.BooleanField(blank=True, null=True)
    response_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to {self.question.question_text} by {self.user.username}"
