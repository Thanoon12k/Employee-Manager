from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from .models import User, Questionnaire, Question, FormalBook

# Unregister the Group model (optional cleanup)
admin.site.unregister(Group)

# User admin customization
class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'phone', 'email', 'image', 'password', 'birth_date', 'address', 'is_superuser', 'is_manager')

    def __init__(self, *args, **kwargs):
        super(UserAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['password'].disabled = True  # Prevent password editing on update

class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ('username', 'phone', 'is_superuser', 'is_manager')
    search_fields = ('username',)

# Questionnaire admin customization
class QuestionnaireAdminForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = '__all__'
        exclude = ('user',)

class QuestionnaireAdmin(admin.ModelAdmin):
    form = QuestionnaireAdminForm
    list_display = ('title', 'description', 'pub_date', 'user')
    search_fields = ('title', 'description')

# Question admin customization
class QuestionAdminForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    list_display = ('question_text', 'user_choice')
    search_fields = ('question_text', 'inquery__title')

# FormalBook admin customization
class FormalBookAdminForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Display users as checkboxes
        required=False
    )

    class Meta:
        model = FormalBook
        fields = '__all__'

class FormalBookAdmin(admin.ModelAdmin):
    form = FormalBookAdminForm
    list_display = ('title', 'description', 'pub_date', 'linked_users')
    search_fields = ('title', 'description', 'users__username')
    filter_horizontal = ('users',)  # Enable horizontal filter for ManyToMany field

    def linked_users(self, obj):
        return ", ".join([user.username for user in obj.users.all()])
    linked_users.short_description = 'Linked Users'

# Register models
admin.site.register(User, UserAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(FormalBook, FormalBookAdmin)
