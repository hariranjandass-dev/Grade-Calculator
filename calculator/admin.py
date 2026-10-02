from django.contrib import admin
from .models import GradingSystem, GradeScale, Semester, Subject


class GradeScaleInline(admin.TabularInline):
    model = GradeScale
    extra = 0


@admin.register(GradingSystem)
class GradingSystemAdmin(admin.ModelAdmin):
    list_display = ['name', 'student', 'scale_type', 'maximum_grade_point', 'is_active', 'created_at']
    search_fields = ['name', 'student__username']
    list_filter = ['scale_type', 'is_active', 'created_at']
    ordering = ['-created_at']
    inlines = [GradeScaleInline]


@admin.register(GradeScale)
class GradeScaleAdmin(admin.ModelAdmin):
    list_display = ['grading_system', 'grade', 'minimum_marks', 'maximum_marks', 'grade_point']
    search_fields = ['grade', 'grading_system__name']
    list_filter = ['grading_system']
    ordering = ['-minimum_marks']


class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 0


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['student', 'semester_number', 'academic_year', 'gpa', 'total_credits', 'created_at']
    search_fields = ['student__username', 'academic_year']
    list_filter = ['semester_number', 'created_at']
    ordering = ['student', 'semester_number']
    inlines = [SubjectInline]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['subject_name', 'subject_code', 'semester', 'credits', 'marks', 'grade', 'grade_point']
    search_fields = ['subject_name', 'subject_code', 'semester__student__username']
    list_filter = ['grade', 'credits']
    ordering = ['semester', 'subject_name']
