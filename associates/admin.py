from django.contrib import admin

from .models import User, Associate, UserDepartment

admin.site.register(User)
admin.site.register(UserDepartment)
admin.site.register(Associate)

admin.site.site_title = 'CRM dashboard'
admin.site.site_header = 'Admin dashboard'
