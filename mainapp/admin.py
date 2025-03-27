from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from .models import User, FormalBook, Query

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

admin.site.register(User, UserAdmin)

admin.site.register(FormalBook, FormalBookAdmin)


from .models import Query, Question, QueryResponse

# Inline admin for managing questions within a Query
class QuestionInline(admin.TabularInline):  # or use admin.StackedInline
    model = Question
    extra = 1  # Number of empty fields to display for adding new questions

# Admin for Query
class QueryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'pub_date')  # Display fields in the query list
    search_fields = ('title', 'description')  # Add search functionality
    inlines = [QuestionInline]  # Allow managing questions directly within the Query admin
    filter_horizontal = ('users',)  # Horizontal filter for ManyToManyField

# Admin for Questions
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'question_type', 'query')  # Fields to display
    list_filter = ('question_type',)  # Filter by question type
    search_fields = ('question_text',)  # Enable search by question text

# Admin for QueryResponse
class QueryResponseAdmin(admin.ModelAdmin):
    list_display = ('query', 'question', 'user', 'response_date')  # Display fields
    list_filter = ('response_date',)  # Filter responses by date
    search_fields = ('query__title', 'question__question_text', 'user__username')  # Enable search

# Register models in admin
admin.site.register(Query, QueryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QueryResponse, QueryResponseAdmin)

