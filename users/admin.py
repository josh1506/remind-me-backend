from django.contrib import admin
from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'joined_date']
    exclude = ('joined_date',)
    list_filter = ['auth_provider', 'is_verified', 'is_staff',
                   'is_active', 'is_superuser', 'joined_date']
    search_fields = ['username', 'email',
                     'first_name', 'last_name']
