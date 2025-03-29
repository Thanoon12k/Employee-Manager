from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from .models import User, Announcement, Report, Question, Answer


# Custom User Admin
class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'phone', 'email', 'image', 'password', 'birth_date', 'address', 'is_superuser', 'is_manager')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['password'].disabled = True  # Prevent password editing on update


class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ('username', 'phone', 'is_superuser', 'is_manager')
    search_fields = ('username',)


# Custom Announcement Admin
class AnnouncementAdminForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Display users as checkboxes
        required=False
    )

    class Meta:
        model = Announcement
        fields = '__all__'


class AnnouncementAdmin(admin.ModelAdmin):
    form = AnnouncementAdminForm
    list_display = ('title', 'description', 'pub_date', 'linked_users')
    search_fields = ('title', 'description', 'users__username')
    filter_horizontal = ('users',)

    def linked_users(self, obj):
        return ", ".join([user.username for user in obj.users.all()])
    linked_users.short_description = 'Linked Users'


# Inline admin for managing questions within a Report
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1  # Number of empty fields to display for adding new questions


# Custom Report Admin
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'pub_date')
    search_fields = ('title', 'description')
    inlines = [QuestionInline]
    filter_horizontal = ('users',)


# Custom Question Admin
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'question_type', 'report')
    list_filter = ('question_type',)
    search_fields = ('question_text',)


# Custom Answer Admin
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('report', 'question', 'user', 'response_date')
    list_filter = ('response_date',)
    search_fields = ('report__title', 'question__question_text', 'user__username')


# Registering models with the admin site
admin.site.register(User, UserAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)

# Unregister the default Group model
admin.site.unregister(Group)
