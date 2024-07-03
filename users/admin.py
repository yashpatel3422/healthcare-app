from django.contrib import admin
from .models import CustomUser, PatientProfile, DoctorProfile
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

# Register the CustomUser model with the CustomUserAdmin configuration
admin.site.register(CustomUser, CustomUserAdmin)

# Register the PatientProfile and DoctorProfile models as they are
admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)
