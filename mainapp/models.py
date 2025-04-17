from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from matplotlib import pyplot as plt


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
    title = models.CharField(max_length=200,unique=True)
    description = models.CharField(max_length=500,blank=True,null=True)
    users = models.ManyToManyField(User, related_name='linked_reports', blank=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    users_submitted = models.ManyToManyField(User, related_name='submitted_reports', blank=True)
    def __str__(self):
        return self.title



QUESTION_TYPES = [
        ("TEXT", 'Text Answer'),
        ("multiple_choice", 'Multiple Choice'),
        ("T/F", 'True/False'),
    ]
class Question(models.Model):
    question = models.CharField(max_length=300)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default="TEXT")
    
    report = models.ForeignKey(Report, related_name='linked_questions', on_delete=models.CASCADE)
    options_data= models.CharField(max_length=300,blank=True,null=True)
    is_statistic=models.BooleanField(default=False)
# when the question type is options the options_data field will store the options in this kind "opt1-opt2-opt3-opt4 ....."
#   the question is_statistic if it was from type options or t/f only
    def __str__(self):
        return self.question
    
    
    def save(self, *args, **kwargs):
        if self.question_type == 'multiple_choice' or self.question_type == 'T/F':
            self.is_statistic = True
        else:
            self.is_statistic = False
        # Save the question to the database
        super().save(*args, **kwargs)

# Answer Model
class Answer(models.Model):
    report = models.ForeignKey(Report, related_name='linked_answers', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='linked_answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='linked_answers', on_delete=models.CASCADE)
    answer_data =  models.CharField(max_length=300)
    response_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer_data




class Complaint(models.Model):
    complainant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints_made')
    respondent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints_received')
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField('Date Published', auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text
