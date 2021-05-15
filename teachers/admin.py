from django.contrib import admin

from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "dni",
        "date_of_birth",
        "date_of_admission",
        "marital_status",
        "email",
        "phone_number",
        "certified",
    )
    search_fields = (
        "first_name",
        "last_name",
        "dni",
    )
