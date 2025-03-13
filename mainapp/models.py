from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(blank=True, null=True)  # Make email optional
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='user_images/', blank=True)
    is_superuser = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    username = models.CharField(max_length=150, unique=True)  # Make username unique

    def __str__(self):
        return self.username
    
    # 🔹 FIX CONFLICTS: Add `related_name` to avoid clashes with Django's default `auth.User`
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True
    )

    # Override the save method to allow simple passwords
    def save(self, *args, **kwargs):
        if self.pk is None and self.password:
            self.set_password(self.password)
        super().save(*args, **kwargs)

class Questionnaire(models.Model):
    user = models.ForeignKey(User, related_name='questionnaires', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.title
    

class Question(models.Model):
    inquery = models.ForeignKey(Questionnaire, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    OPTION_CHOICES = [
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
        ('option3', 'Option 3'),
    ]
    user_choice = models.CharField(max_length=7, choices=OPTION_CHOICES, default='option1')
    def __str__(self):
        return self.question_text

class FormalBook(models.Model):
    user = models.ForeignKey(User, related_name='formal_books', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    file = models.FileField(upload_to='files/')
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.title