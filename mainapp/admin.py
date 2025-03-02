from django.contrib import admin
from .models import User, Questionnaire, Question, FormalBook  # Ensure this User is your custom User model
from django import forms
from django.contrib.auth.models import Group

# Unregister the Group model
admin.site.unregister(Group)

class UserAdminForm(forms.ModelForm):
     class Meta:
        model = User
        fields = '__all__'
        exclude = ('groups', 'user_permissions','is_active','is_staff','first_name','last_name','last_login','password')  # 🚀 Hides these fields in the form


class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ('username', 'phone','is_superuser',  'is_manager')
    search_fields = ('username',  )

class QuestionnaireAdminForm(forms.ModelForm):
    class Meta:
        
        model = Questionnaire
        fields = '__all__'
        exclude = ('user',)

class QuestionnaireAdmin(admin.ModelAdmin):
    form = QuestionnaireAdminForm
    list_display = ('title', 'description', 'pub_date', 'user')
    search_fields = ('title', 'description')

class QuestionAdminForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    list_display = ('question_text',  'correct_option')
    search_fields = ('question_text', 'inquery__title')

class FormalBookAdminForm(forms.ModelForm):
    class Meta:
        model = FormalBook
        fields = '__all__'
        exclude = ('user',)

class FormalBookAdmin(admin.ModelAdmin):
    form = FormalBookAdminForm
    list_display = ('title', 'description', 'pub_date')
    search_fields = ('title', 'description', 'user__username')

admin.site.register(User, UserAdmin)  # Ensure this User is your custom User model
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(FormalBook, FormalBookAdmin)
