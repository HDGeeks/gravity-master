from django.contrib import admin
from .models import Role,ExtendedUser
# Register your models here.


class ExtendedUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email','role')
    list_filter = ('email_verified', 'role')
    search_fields = ('username', 'email', 'phone', 'middle_name')

class RoleAdmin(admin.ModelAdmin):
    list_display = ('id','role')
    list_filter = ('id','role')
    search_fields = ('id','role')

admin.site.register(Role,RoleAdmin)
admin.site.register(ExtendedUser, ExtendedUserAdmin)