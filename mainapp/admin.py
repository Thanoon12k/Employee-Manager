from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from .models import User, Announcement, Report, Question, Answer, AnswerStatistics

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
    list_display = ('title', 'description', 'pub_date')
    search_fields = ('title', 'description', 'users__username')
    filter_horizontal = ('users',)
    inlines = [QuestionInline]
    list_filter = ('pub_date', 'users')  # Filters reports by publication date and associated users


# ---------------------------------
# Custom Question Admin
# ---------------------------------
class AnswerStatisticsInline(admin.StackedInline):
    model = AnswerStatistics
    readonly_fields = (
        'option1_percentage', 'option2_percentage', 'option3_percentage',
        'option4_percentage', 'true_percentage', 'false_percentage',
        'last_updated', 'pie_chart_preview'
    )
    can_delete = False
    extra = 0

    def pie_chart_preview(self, obj):
        """Display a pie chart for each question's statistics."""
        if obj and obj.question.question_type in ['multiple_choice', 'true_false']:
            image_base64 = obj.generate_pie_chart()
            return mark_safe(f'<img src="data:image/png;base64,{image_base64}" style="width: 100%; max-height: 400px;" />')
        return "No data to display"
    pie_chart_preview.short_description = "Answer Statistics Pie Chart"


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'question_type', 'report')
    list_filter = ('question_type', 'report')  # Filters questions by type and associated report
    search_fields = ('question_text',)


# ---------------------------------
# Custom Answer Admin
# ---------------------------------
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('report', 'question', 'user', 'response_date')
    list_filter = ('response_date', 'report', 'question', 'user')  # Filters by date, report, question, and user
    search_fields = ('report__title', 'question__question_text', 'user__username')


# ---------------------------------
# Custom AnswerStatistics Admin
# ---------------------------------
class AnswerStatisticsAdmin(admin.ModelAdmin):
    list_display = ('question', 'last_updated')
    readonly_fields = (
        'option1_percentage', 'option2_percentage', 'option3_percentage',
        'option4_percentage', 'true_percentage', 'false_percentage',
        'last_updated', 'pie_chart_preview'
    )
    list_filter = ('last_updated', 'question')  # Filters by question and last updated timestamp

    def pie_chart_preview(self, obj):
        """Render the pie chart as an image in the admin panel."""
        pie_chart = obj.generate_pie_chart()
        if pie_chart:
            return mark_safe(f'<img src="data:image/png;base64,{pie_chart}" style="width: 400px; height: auto;" />')
        return "No data to display"
    pie_chart_preview.short_description = "Pie Chart"


# ---------------------------------
# Register Models in Admin
# ---------------------------------
admin.site.register(User, UserAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(AnswerStatistics, AnswerStatisticsAdmin)

# Unregister the default Group model (if unused)
admin.site.unregister(Group)
