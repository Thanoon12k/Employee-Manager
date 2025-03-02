from django.contrib import admin
from django.contrib.auth.models import User, Group

# Unregister the User and Group models
admin.site.unregister(User)
admin.site.unregister(Group)
