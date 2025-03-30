from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from .models import *

# ---------------------------------
# Custom User Admin
# ---------------------------------
class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username', 'phone', 'email', 'image', 'password', 
            'birth_date', 'address', 'is_superuser', 'is_manager'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['password'].disabled = True  # Prevent editing the password for existing users


class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ('username', 'phone', 'email', 'is_superuser', 'is_manager')
    search_fields = ('username', 'phone', 'email')
    list_filter = ('is_superuser', 'is_manager')  # Filters for user roles


# ---------------------------------
# Custom Announcement Admin
# ---------------------------------
class AnnouncementAdminForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
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
    list_filter = ('pub_date',)  # Filters announcements by publication date

    def linked_users(self, obj):
        return ", ".join([user.username for user in obj.users.all()])
    linked_users.short_description = 'Linked Users'


# ---------------------------------
# Inline admin for managing Questions within a Report
# ---------------------------------
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1  # Number of empty fields to display for adding new questions


# ---------------------------------
# Custom Report Admin
# ---------------------------------
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title','num_questions', 'number_of_users_submitted')
    search_fields = ('title', 'description', 'users__username')
    readonly_fields=('pub_date','users_submitted')
    filter_horizontal = ('users',)
    inlines = [QuestionInline]
    list_filter = ( 'users','title')  # Filters reports by publication date and associated users
    def num_questions(self, obj):
        return obj.linked_questions.count()
    num_questions.short_description = 'Number of Questions'
    def number_of_users_submitted(self, obj):
        return obj.users_submitted.count()
    number_of_users_submitted.short_description = 'Number of Users Submitted'
    


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('report', 'question', 'is_statistic', 'number_of_users_submitted')
    list_filter = ('report', )  # Filters questions by type and associated report

    def number_of_users_submitted(self, obj):
        return obj.report.users_submitted.count()
    number_of_users_submitted.short_description = 'Number of Users Submitted'
    search_fields = ('question',)
    readonly_fields = ('is_statistic',)  # Prevents editing the report field in the admin interface
    radio_fields = {'question_type': admin.HORIZONTAL}  # Displays question types as radio buttons
    


# ---------------------------------
# Custom Answer Admin
# ---------------------------------
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('report', 'user', 'get_question_type', 'question', 'answer_data',)
    list_filter = ('report', 'user')  # Filters by date, report, question, and user
    # search_fields = ('report__title', 'question__question', 'user__username')

    def get_question_type(self, obj):
        return obj.question.question_type
    get_question_type.short_description = 'Question Type'


# ---------------------------------
# Register Models in Admin
# ---------------------------------
admin.site.register(User, UserAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)

# Unregister the default Group model (if unused)
admin.site.unregister(Group)
