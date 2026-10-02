from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GradingSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='My Grading System', max_length=100)),
                ('scale_type', models.CharField(
                    choices=[('10', '10 Point Scale'), ('4', '4 Point Scale'), ('custom', 'Custom Scale')],
                    default='10', max_length=10,
                )),
                ('maximum_grade_point', models.DecimalField(decimal_places=2, default=10.0, max_digits=4)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='grading_systems',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={'verbose_name': 'Grading System', 'verbose_name_plural': 'Grading Systems', 'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester_number', models.PositiveIntegerField()),
                ('academic_year', models.CharField(blank=True, max_length=20)),
                ('gpa', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('total_credits', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='semesters',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'verbose_name': 'Semester',
                'verbose_name_plural': 'Semesters',
                'ordering': ['semester_number'],
                'unique_together': {('student', 'semester_number')},
            },
        ),
        migrations.CreateModel(
            name='GradeScale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(max_length=5)),
                ('minimum_marks', models.DecimalField(decimal_places=2, max_digits=5)),
                ('maximum_marks', models.DecimalField(decimal_places=2, max_digits=5)),
                ('grade_point', models.DecimalField(decimal_places=2, max_digits=4)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('grading_system', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='grade_scales',
                    to='calculator.gradingsystem',
                )),
            ],
            options={'verbose_name': 'Grade Scale', 'verbose_name_plural': 'Grade Scales', 'ordering': ['-minimum_marks']},
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_code', models.CharField(blank=True, max_length=20)),
                ('subject_name', models.CharField(max_length=200)),
                ('credits', models.PositiveIntegerField()),
                ('marks', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('grade', models.CharField(blank=True, max_length=5)),
                ('grade_point', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('semester', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='subjects',
                    to='calculator.semester',
                )),
            ],
            options={'verbose_name': 'Subject', 'verbose_name_plural': 'Subjects', 'ordering': ['subject_name']},
        ),
    ]
