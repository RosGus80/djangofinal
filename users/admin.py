from django.contrib import admin

from users.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name')
    search_fields = ('email', 'phone_number')
    list_filter = ('is_verified', )

