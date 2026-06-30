from django.contrib import admin

# Register your models here.

from .models import User, Agent, Lead, UserProfile, Category # then, they will show up in the admin interface

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Agent)
admin.site.register(Lead)
admin.site.register(Category)

