from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gpa/', views.gpa_calculator, name='gpa_calculator'),
    path('cgpa/', views.cgpa_calculator, name='cgpa_calculator'),
    path('target-cgpa/', views.target_cgpa, name='target_cgpa'),
    path('grading-system/', views.grading_system, name='grading_system'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Semester management
    path('semester/add/', views.add_semester, name='add_semester'),
    path('semester/<int:pk>/', views.semester_detail, name='semester_detail'),
    path('semester/<int:pk>/edit/', views.edit_semester, name='edit_semester'),
    path('semester/<int:pk>/delete/', views.delete_semester, name='delete_semester'),
    path('semester/<int:pk>/subjects/', views.subject_management, name='subject_management'),
    path('subject/<int:pk>/delete/', views.delete_subject, name='delete_subject'),

    # API
    path('api/grade-lookup/', views.api_grade_lookup, name='api_grade_lookup'),
]
