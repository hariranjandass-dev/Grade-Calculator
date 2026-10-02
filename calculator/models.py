from django.db import models
from django.contrib.auth.models import User


class GradingSystem(models.Model):
    SCALE_CHOICES = [
        ('10', '10 Point Scale'),
        ('4', '4 Point Scale'),
        ('custom', 'Custom Scale'),
    ]
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grading_systems')
    name = models.CharField(max_length=100, default='My Grading System')
    scale_type = models.CharField(max_length=10, choices=SCALE_CHOICES, default='10')
    maximum_grade_point = models.DecimalField(max_digits=4, decimal_places=2, default=10.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.student.username})"

    class Meta:
        verbose_name = 'Grading System'
        verbose_name_plural = 'Grading Systems'
        ordering = ['-created_at']


class GradeScale(models.Model):
    grading_system = models.ForeignKey(GradingSystem, on_delete=models.CASCADE, related_name='grade_scales')
    grade = models.CharField(max_length=5)
    minimum_marks = models.DecimalField(max_digits=5, decimal_places=2)
    maximum_marks = models.DecimalField(max_digits=5, decimal_places=2)
    grade_point = models.DecimalField(max_digits=4, decimal_places=2)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.grade} ({self.minimum_marks}-{self.maximum_marks}) = {self.grade_point}"

    class Meta:
        verbose_name = 'Grade Scale'
        verbose_name_plural = 'Grade Scales'
        ordering = ['-minimum_marks']


class Semester(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='semesters')
    semester_number = models.PositiveIntegerField()
    academic_year = models.CharField(max_length=20, blank=True)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    total_credits = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Semester {self.semester_number} - {self.student.username}"

    class Meta:
        verbose_name = 'Semester'
        verbose_name_plural = 'Semesters'
        ordering = ['semester_number']
        unique_together = ['student', 'semester_number']


class Subject(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='subjects')
    subject_code = models.CharField(max_length=20, blank=True)
    subject_name = models.CharField(max_length=200)
    credits = models.PositiveIntegerField()
    marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    grade = models.CharField(max_length=5, blank=True)
    grade_point = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject_name} - Semester {self.semester.semester_number}"

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
        ordering = ['subject_name']
