import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from .models import GradingSystem, GradeScale, Semester, Subject
from .forms import SemesterForm, SubjectForm, GradingSystemForm, GradeScaleForm, TargetCGPAForm
from .calculations import (
    get_grade_from_marks, calculate_gpa, calculate_cgpa,
    calculate_required_gpa, calculate_percentage, get_degree_class,
    DEFAULT_GRADING_SCALE, is_ra_grade,
)


def home(request):
    return render(request, 'home.html')


# ─── GPA Calculator ───────────────────────────────────────────────────────────

def gpa_calculator(request):
    result = None
    subjects = []
    error = None
    grade_scales_data = DEFAULT_GRADING_SCALE

    if request.user.is_authenticated:
        gs = GradingSystem.objects.filter(student=request.user, is_active=True).first()
        if gs:
            grade_scales_data = [
                {'grade': s.grade, 'min': float(s.minimum_marks),
                 'max': float(s.maximum_marks), 'point': float(s.grade_point),
                 'description': s.description}
                for s in gs.grade_scales.all()
            ]

    if request.method == 'POST':
        names = request.POST.getlist('subject_name[]')
        credits_list = request.POST.getlist('credits[]')
        marks_list = request.POST.getlist('marks[]')

        if not names or all(n.strip() == '' for n in names):
            error = 'Please add at least one subject.'
        else:
            grade_scales_qs = None
            if request.user.is_authenticated:
                gs = GradingSystem.objects.filter(student=request.user, is_active=True).first()
                if gs:
                    grade_scales_qs = gs.grade_scales.all()

            for name, credit, marks in zip(names, credits_list, marks_list):
                if not name.strip():
                    continue
                try:
                    credits = int(credit)
                    marks_val = float(marks)
                except (ValueError, TypeError):
                    error = 'Please enter valid numeric values for credits and marks.'
                    break
                if credits <= 0:
                    error = 'Credits must be greater than zero.'
                    break
                if marks_val < 0 or marks_val > 100:
                    error = 'Marks must be between 0 and 100.'
                    break

                grade, grade_point = get_grade_from_marks(marks_val, grade_scales_qs)
                subjects.append({
                    'name': name,
                    'credits': credits,
                    'marks': marks_val,
                    'grade': grade,
                    'grade_point': grade_point,
                    'is_ra': is_ra_grade(grade),
                })

            if not error and subjects:
                result = float(calculate_gpa(subjects))

    return render(request, 'calculator/gpa.html', {
        'result': result,
        'subjects': subjects,
        'error': error,
        'grade_scales_json': json.dumps(grade_scales_data),
    })


# ─── CGPA Calculator ─────────────────────────────────────────────────────────

def cgpa_calculator(request):
    result = None
    percentage = None
    semesters = []
    error = None

    if request.method == 'POST':
        gpas = request.POST.getlist('gpa[]')
        credits_list = request.POST.getlist('credits[]')

        if not gpas:
            error = 'Please add at least one semester.'
        else:
            for gpa_val, credits_val in zip(gpas, credits_list):
                try:
                    gpa = float(gpa_val)
                    credits = int(credits_val)
                except (ValueError, TypeError):
                    error = 'Please enter valid values.'
                    break
                if credits <= 0:
                    error = 'Credits must be greater than zero.'
                    break
                semesters.append({'gpa': gpa, 'total_credits': credits})

            if not error and semesters:
                result = float(calculate_cgpa(semesters))
                percentage = float(calculate_percentage(result))

    return render(request, 'calculator/cgpa.html', {
        'result': result,
        'percentage': percentage,
        'semesters': semesters,
        'error': error,
    })


# ─── Target CGPA ─────────────────────────────────────────────────────────────

def target_cgpa(request):
    form = TargetCGPAForm(request.POST or None)
    result = None
    achievable = None
    message = ''
    percentage = None

    if request.method == 'POST' and form.is_valid():
        max_gpa = form.cleaned_data.get('max_gpa') or 10
        required_gpa, achievable, message = calculate_required_gpa(
            current_cgpa=form.cleaned_data['current_cgpa'],
            completed_credits=form.cleaned_data['completed_credits'],
            target_cgpa=form.cleaned_data['target_cgpa'],
            future_credits=form.cleaned_data['future_credits'],
            max_gpa=max_gpa,
        )
        result = required_gpa
        if achievable and result is not None:
            target = form.cleaned_data['target_cgpa']
            percentage = float(calculate_percentage(target))

    return render(request, 'calculator/target_cgpa.html', {
        'form': form,
        'result': result,
        'achievable': achievable,
        'message': message,
        'percentage': percentage,
    })


# ─── Dashboard ───────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    semesters = Semester.objects.filter(student=request.user).order_by('semester_number')
    cgpa = float(calculate_cgpa(semesters)) if semesters else 0
    total_credits = sum(s.total_credits for s in semesters)
    percentage = float(calculate_percentage(cgpa)) if cgpa else 0

    # Degree class
    degree_class = get_degree_class(cgpa, total_credits, years_taken=4)

    chart_labels = [f'S{s.semester_number}' for s in semesters]
    chart_gpas = [float(s.gpa) for s in semesters]

    # Cumulative CGPA per semester
    cumulative_cgpa = []
    running = []
    for sem in semesters:
        running.append(sem)
        cumulative_cgpa.append(float(calculate_cgpa(running)))

    return render(request, 'dashboard/dashboard.html', {
        'semesters': semesters,
        'cgpa': round(cgpa, 2),
        'total_credits': total_credits,
        'percentage': round(percentage, 2),
        'degree_class': degree_class,
        'chart_labels': json.dumps(chart_labels),
        'chart_gpas': json.dumps(chart_gpas),
        'cumulative_cgpa': json.dumps(cumulative_cgpa),
    })


# ─── Semester Management ─────────────────────────────────────────────────────

@login_required
def add_semester(request):
    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            semester = form.save(commit=False)
            semester.student = request.user
            if Semester.objects.filter(student=request.user, semester_number=semester.semester_number).exists():
                messages.error(request, f'Semester {semester.semester_number} already exists.')
            else:
                semester.save()
                messages.success(request, f'Semester {semester.semester_number} added.')
                return redirect('subject_management', pk=semester.pk)
    else:
        form = SemesterForm()
    return render(request, 'calculator/semester_form.html', {'form': form, 'action': 'Add'})


@login_required
def semester_detail(request, pk):
    semester = get_object_or_404(Semester, pk=pk, student=request.user)
    subjects = semester.subjects.all()
    percentage = float(calculate_percentage(semester.gpa))
    return render(request, 'calculator/semester_detail.html', {
        'semester': semester,
        'subjects': subjects,
        'percentage': round(percentage, 2),
    })


@login_required
def edit_semester(request, pk):
    semester = get_object_or_404(Semester, pk=pk, student=request.user)
    if request.method == 'POST':
        form = SemesterForm(request.POST, instance=semester)
        if form.is_valid():
            form.save()
            messages.success(request, 'Semester updated.')
            return redirect('semester_detail', pk=semester.pk)
    else:
        form = SemesterForm(instance=semester)
    return render(request, 'calculator/semester_form.html', {'form': form, 'action': 'Edit', 'semester': semester})


@login_required
def delete_semester(request, pk):
    semester = get_object_or_404(Semester, pk=pk, student=request.user)
    if request.method == 'POST':
        num = semester.semester_number
        semester.delete()
        messages.success(request, f'Semester {num} deleted.')
        return redirect('dashboard')
    return render(request, 'calculator/confirm_delete.html', {'object': f'Semester {semester.semester_number}', 'type': ''})


# ─── Subject Management ──────────────────────────────────────────────────────

@login_required
def subject_management(request, pk):
    semester = get_object_or_404(Semester, pk=pk, student=request.user)

    grade_scales_qs = None
    gs = GradingSystem.objects.filter(student=request.user, is_active=True).first()
    if gs:
        grade_scales_qs = gs.grade_scales.all()

    if request.method == 'POST':
        names = request.POST.getlist('subject_name[]')
        codes = request.POST.getlist('subject_code[]')
        credits_list = request.POST.getlist('credits[]')
        marks_list = request.POST.getlist('marks[]')

        if not names or all(n.strip() == '' for n in names):
            messages.error(request, 'Please add at least one subject.')
        else:
            semester.subjects.all().delete()
            subjects_to_create = []
            error = None

            for name, code, credit, marks in zip(names, codes, credits_list, marks_list):
                if not name.strip():
                    continue
                try:
                    credits = int(credit)
                    marks_val = float(marks)
                except (ValueError, TypeError):
                    error = 'Invalid numeric values.'
                    break
                if credits <= 0:
                    error = 'Credits must be greater than zero.'
                    break
                if marks_val < 0 or marks_val > 100:
                    error = 'Marks must be between 0 and 100.'
                    break

                grade, grade_point = get_grade_from_marks(marks_val, grade_scales_qs)
                subjects_to_create.append(Subject(
                    semester=semester,
                    subject_name=name.strip(),
                    subject_code=code.strip(),
                    credits=credits,
                    marks=marks_val,
                    grade=grade,
                    grade_point=grade_point,
                ))

            if error:
                messages.error(request, error)
            elif subjects_to_create:
                Subject.objects.bulk_create(subjects_to_create)
                all_subjects = semester.subjects.all()
                semester.gpa = calculate_gpa(all_subjects)
                semester.total_credits = sum(s.credits for s in all_subjects)
                semester.save()
                messages.success(request, f'Subjects saved. Semester GPA: {semester.gpa}')
                return redirect('semester_detail', pk=semester.pk)

    subjects = semester.subjects.all()
    grade_scales_data = DEFAULT_GRADING_SCALE
    if grade_scales_qs:
        grade_scales_data = [
            {'grade': s.grade, 'min': float(s.minimum_marks),
             'max': float(s.maximum_marks), 'point': float(s.grade_point),
             'description': s.description}
            for s in grade_scales_qs
        ]

    return render(request, 'calculator/subject_form.html', {
        'semester': semester,
        'subjects': subjects,
        'grade_scales_json': json.dumps(grade_scales_data),
    })


@login_required
def delete_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk, semester__student=request.user)
    semester = subject.semester
    subject.delete()
    all_subjects = semester.subjects.all()
    semester.gpa = calculate_gpa(all_subjects) if all_subjects else 0
    semester.total_credits = sum(s.credits for s in all_subjects)
    semester.save()
    messages.success(request, 'Subject deleted.')
    return redirect('subject_management', pk=semester.pk)


# ─── Grading System ──────────────────────────────────────────────────────────

@login_required
def grading_system(request):
    gs = GradingSystem.objects.filter(student=request.user, is_active=True).first()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'reset':
            if gs:
                gs.grade_scales.all().delete()
            else:
                gs = GradingSystem.objects.create(
                    student=request.user,
                    name='Annamalai University 10-Point Scale',
                    scale_type='10',
                    maximum_grade_point=10.00,
                )
            for entry in DEFAULT_GRADING_SCALE:
                GradeScale.objects.create(
                    grading_system=gs,
                    grade=entry['grade'],
                    minimum_marks=entry['min'],
                    maximum_marks=entry['max'],
                    grade_point=entry['point'],
                    description=entry.get('description', ''),
                )
            messages.success(request, 'Grading system reset to default.')
            return redirect('grading_system')

        if action == 'save':
            grades = request.POST.getlist('grade[]')
            mins = request.POST.getlist('min_marks[]')
            maxs = request.POST.getlist('max_marks[]')
            points = request.POST.getlist('grade_point[]')
            descs = request.POST.getlist('description[]')
            sys_name = request.POST.get('system_name', 'My Grading System')
            max_gp = request.POST.get('maximum_grade_point', 10)

            if not gs:
                gs = GradingSystem.objects.create(
                    student=request.user, name=sys_name,
                    scale_type='custom', maximum_grade_point=max_gp,
                )
            else:
                gs.name = sys_name
                gs.maximum_grade_point = max_gp
                gs.save()
                gs.grade_scales.all().delete()

            for grade, mn, mx, pt, desc in zip(grades, mins, maxs, points, descs):
                if not grade.strip():
                    continue
                try:
                    GradeScale.objects.create(
                        grading_system=gs,
                        grade=grade.strip(),
                        minimum_marks=float(mn),
                        maximum_marks=float(mx),
                        grade_point=float(pt),
                        description=desc.strip(),
                    )
                except (ValueError, TypeError):
                    messages.error(request, 'Invalid values in grading scale.')
                    break
            else:
                messages.success(request, 'Grading system saved.')
            return redirect('grading_system')

    grade_scales = gs.grade_scales.all() if gs else []
    return render(request, 'calculator/grading_system.html', {
        'grading_system': gs,
        'grade_scales': grade_scales,
        'default_scale': DEFAULT_GRADING_SCALE,
    })


# ─── API ─────────────────────────────────────────────────────────────────────

def api_grade_lookup(request):
    try:
        marks = float(request.GET.get('marks', -1))
    except ValueError:
        return JsonResponse({'error': 'Invalid marks'}, status=400)

    grade_scales_qs = None
    if request.user.is_authenticated:
        gs = GradingSystem.objects.filter(student=request.user, is_active=True).first()
        if gs:
            grade_scales_qs = gs.grade_scales.all()

    grade, grade_point = get_grade_from_marks(marks, grade_scales_qs)
    percentage = float(calculate_percentage(grade_point)) if not is_ra_grade(grade) else 0
    return JsonResponse({'grade': grade, 'grade_point': grade_point, 'is_ra': is_ra_grade(grade)})
