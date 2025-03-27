from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(blank=True, null=True)  # Optional email
    birth_date = models.DateField(null=True, blank=True)  # Optional birth date
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='user_images/', blank=True)  # Optional profile image
    is_superuser = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)  # Custom manager flag
    username = models.CharField(max_length=150, unique=True)  # Enforce unique usernames

    def __str__(self):
        return self.username
    
   
    # Override save method to allow simple passwords
    def save(self, *args, **kwargs):
        if self.pk is None and self.password:
            self.set_password(self.password)  # Set password for new users
        super().save(*args, **kwargs)



class FormalBook(models.Model):
    users = models.ManyToManyField(
        User,
        related_name='linked_formal_books',
        blank=True  # Allow optional linking of users
    )
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    file = models.FileField(upload_to='files/')
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title

# Flexible Query Model
class Query(models.Model):
    title = models.CharField(max_length=200)  # Query title (form title)
    description = models.TextField(blank=True)  # Optional description
    users = models.ManyToManyField(
        User, related_name='linked_queries', blank=True
    )
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return self.title


# Question Model for individual questions
class Question(models.Model):
    TEXT = 'text'
    MULTIPLE_CHOICE = 'multiple_choice'
    TRUE_FALSE = 'true_false'

    QUESTION_TYPES = [
        (TEXT, 'Text Answer'),
        (MULTIPLE_CHOICE, 'Multiple Choice'),
        (TRUE_FALSE, 'True/False'),
    ]

    query = models.ForeignKey(
        Query, related_name='questions', on_delete=models.CASCADE
    )
    question_text = models.CharField(max_length=300)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default=TEXT)
    option1 = models.CharField(max_length=200, blank=True, null=True)
    option2 = models.CharField(max_length=200, blank=True, null=True)
    option3 = models.CharField(max_length=200, blank=True, null=True)
    option4 = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.question_text


# Response Model for user answers
class QueryResponse(models.Model):
    query = models.ForeignKey(Query, related_name='responses', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='responses', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='question_responses', on_delete=models.CASCADE)
    text_answer = models.TextField(blank=True, null=True)  # For text-type responses
    selected_option = models.CharField(max_length=200, blank=True, null=True)  # For multiple-choice responses
    true_false_answer = models.BooleanField(blank=True, null=True)  # For true/false responses

    response_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to {self.question.question_text} by {self.user.username}"
