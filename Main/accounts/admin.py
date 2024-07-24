from django.contrib import admin

from accounts.models import Profile



# Now register the new UserAdmin...
admin.site.register(Profile)
