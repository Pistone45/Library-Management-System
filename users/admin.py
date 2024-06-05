from django.contrib import admin
from django.contrib.auth.models import User as AuthUser
# Register your models here.


from users.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserInline(admin.StackedInline):
    model = User
    can_delete = False
    verbose_name_plural = 'user'


# New User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserInline, )


# Re-register UserAdmin
admin.site.unregister(AuthUser)
admin.site.register(AuthUser, UserAdmin)
