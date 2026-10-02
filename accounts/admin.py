from django.contrib import admin
from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'email', 'created_at']
    search_fields = ['user__username', 'full_name', 'email']
    list_filter = ['created_at']
    ordering = ['-created_at']
