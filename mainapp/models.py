from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from matplotlib import pyplot as plt
import io
import base64
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

    def save(self, *args, **kwargs):
        if self.pk is None and self.password:  # Check if it's a new user and password is set
            self.set_password(self.password)  # Hash the password
        super().save(*args, **kwargs)

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
    users_submitted = models.ManyToManyField(User, related_name='submitted_reports', blank=True)
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


# Statistics Model for Analyzing User Responses
from django.db import models
from matplotlib import pyplot as plt
import io
import base64

class AnswerStatistics(models.Model):
    question = models.OneToOneField(
        'Question', related_name='statistics', on_delete=models.CASCADE
    )
    option1_percentage = models.FloatField(default=0.0)
    option2_percentage = models.FloatField(default=0.0)
    option3_percentage = models.FloatField(default=0.0)
    option4_percentage = models.FloatField(default=0.0)
    true_percentage = models.FloatField(default=0.0)
    false_percentage = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)

    def calculate_percentages(self):
        total_answers = self.question.answers.count()
        if total_answers > 0:
            if self.question.question_type == 'multiple_choice':
                self.option1_percentage = (
                    self.question.answers.filter(selected_option=self.question.option1).count()
                    / total_answers
                ) * 100
                self.option2_percentage = (
                    self.question.answers.filter(selected_option=self.question.option2).count()
                    / total_answers
                ) * 100
                self.option3_percentage = (
                    self.question.answers.filter(selected_option=self.question.option3).count()
                    / total_answers
                ) * 100
                self.option4_percentage = (
                    self.question.answers.filter(selected_option=self.question.option4).count()
                    / total_answers
                ) * 100
            elif self.question.question_type == 'true_false':
                self.true_percentage = (
                    self.question.answers.filter(true_false_answer=True).count()
                    / total_answers
                ) * 100
                self.false_percentage = (
                    self.question.answers.filter(true_false_answer=False).count()
                    / total_answers
                ) * 100

        self.save()

    def generate_pie_chart(self):
        """Generate a pie chart for the statistics."""
        labels = []
        values = []

        if self.question.question_type == 'multiple_choice':
            labels = [
                self.question.option1, 
                self.question.option2, 
                self.question.option3, 
                self.question.option4
            ]
            values = [
                self.option1_percentage, 
                self.option2_percentage, 
                self.option3_percentage, 
                self.option4_percentage
            ]
        elif self.question.question_type == 'true_false':
            labels = ['True', 'False']
            values = [self.true_percentage, self.false_percentage]

        # Remove zero values and corresponding labels
        filtered_data = [(label, value) for label, value in zip(labels, values) if value > 0]
        if not filtered_data:
            return None  # No data to display
        labels, values = zip(*filtered_data)

        # Create the pie chart
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
        ax.axis('equal')  # Equal aspect ratio to ensure a circular pie chart

        # Save the plot to a base64 string
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close(fig)

        return image_base64
