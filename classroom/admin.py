from django.contrib import admin

from .models import Course, Student, Subject, SubjectGroup, Teacher


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "batch",
        "classroom",
        "division",
    )


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "active",
    )


@admin.register(SubjectGroup)
class SubjectGroupAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "year",
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "dni",
        "gender",
        "date_of_birth",
        "date_of_admission",
        "marital_status",
        "email",
        "phone_number",
        "permission_for_photo",
    )
    search_fields = (
        "first_name",
        "last_name",
        "dni",
    )


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "dni",
        "gender",
        "date_of_birth",
        "date_of_admission",
        "marital_status",
        "email",
        "phone_number",
        "certified",
        "active",
    )
    search_fields = (
        "first_name",
        "last_name",
        "dni",
    )
