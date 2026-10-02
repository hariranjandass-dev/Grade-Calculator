"""
GradeTrack Calculation Engine
Grading system: Annamalai University (Faculty of Engineering & Technology)
S-10, A-9, B-8, C-7, D-6, E-5, RA-0
"""
from decimal import Decimal, ROUND_HALF_UP


# Annamalai University grading scale
DEFAULT_GRADING_SCALE = [
    {'grade': 'S',  'min': 90, 'max': 100, 'point': 10, 'description': 'Outstanding'},
    {'grade': 'A',  'min': 80, 'max': 89,  'point': 9,  'description': 'Excellent'},
    {'grade': 'B',  'min': 70, 'max': 79,  'point': 8,  'description': 'Very Good'},
    {'grade': 'C',  'min': 60, 'max': 69,  'point': 7,  'description': 'Good'},
    {'grade': 'D',  'min': 55, 'max': 59,  'point': 6,  'description': 'Above Average'},
    {'grade': 'E',  'min': 50, 'max': 54,  'point': 5,  'description': 'Average'},
    {'grade': 'RA', 'min': 0,  'max': 49,  'point': 0,  'description': 'Reappear'},
]


def get_grade_from_marks(marks, grade_scales=None):
    """
    Returns (grade, grade_point) for given marks.
    RA courses are excluded from GPA calculation (grade_point = 0).
    """
    try:
        marks = float(marks)
    except (TypeError, ValueError):
        return 'RA', 0

    if marks < 0 or marks > 100:
        return 'RA', 0

    if grade_scales:
        for scale in grade_scales:
            lo = float(scale.minimum_marks)
            hi = float(scale.maximum_marks)
            if lo <= marks <= hi:
                return scale.grade, float(scale.grade_point)
        return 'RA', 0

    for entry in DEFAULT_GRADING_SCALE:
        if entry['min'] <= marks <= entry['max']:
            return entry['grade'], entry['point']

    return 'RA', 0


def is_ra_grade(grade):
    """RA and W grades are excluded from GPA/CGPA calculation."""
    return grade in ('RA', 'W')


def calculate_gpa(subjects):
    """
    Credit-weighted GPA as per Annamalai University rules.
    RA/W grade courses are NOT counted in GPA calculation.

    GPA = Σ(Ci × GPi) / Σ(Ci)
    where RA/W courses are excluded.
    """
    total_points = Decimal('0')
    total_credits = Decimal('0')

    for subject in subjects:
        if hasattr(subject, 'credits'):
            credits = Decimal(str(subject.credits))
            grade_point = Decimal(str(subject.grade_point))
            grade = subject.grade
        else:
            credits = Decimal(str(subject.get('credits', 0)))
            grade_point = Decimal(str(subject.get('grade_point', 0)))
            grade = subject.get('grade', '')

        if credits <= 0:
            continue

        # Skip RA/W courses — not counted in GPA
        if is_ra_grade(grade):
            continue

        total_points += credits * grade_point
        total_credits += credits

    if total_credits == 0:
        return Decimal('0.00')

    return (total_points / total_credits).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def calculate_cgpa(semesters):
    """
    OGPA/CGPA = Σ(Ci × GPi) / Σ(Ci) across all semesters.
    As per university formula: CGPA = Σ(Credit × GradePoint) / Σ(Credits)
    """
    total_points = Decimal('0')
    total_credits = Decimal('0')

    for sem in semesters:
        if hasattr(sem, 'gpa'):
            gpa = Decimal(str(sem.gpa))
            credits = Decimal(str(sem.total_credits))
        else:
            gpa = Decimal(str(sem.get('gpa', 0)))
            credits = Decimal(str(sem.get('total_credits', 0)))

        if credits <= 0:
            continue

        total_points += gpa * credits
        total_credits += credits

    if total_credits == 0:
        return Decimal('0.00')

    return (total_points / total_credits).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def calculate_percentage(cgpa):
    """
    Annamalai University formula:
    Percentage = (CGPA - 0.25) × 10
    """
    try:
        cgpa = Decimal(str(cgpa))
    except Exception:
        return Decimal('0.00')
    result = (cgpa - Decimal('0.25')) * Decimal('10')
    return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def get_degree_class(cgpa, credits_earned, years_taken, all_first_attempt=False):
    """
    Returns the degree classification as per Annamalai University rules.
    """
    try:
        cgpa = float(cgpa)
    except Exception:
        return 'Not Classified'

    if cgpa >= 8.25 and credits_earned >= 192 and all_first_attempt and years_taken <= 4:
        return 'Honours'
    elif cgpa >= 8.25 and credits_earned >= 172 and all_first_attempt and years_taken <= 4:
        return 'First Class with Distinction'
    elif cgpa >= 6.75 and credits_earned >= 172 and years_taken <= 5:
        return 'First Class'
    elif credits_earned >= 172 and years_taken <= 7:
        return 'Second Class'
    else:
        return 'Not Classified'


def calculate_required_gpa(current_cgpa, completed_credits, target_cgpa, future_credits, max_gpa=10):
    """
    Required GPA = (Target × (Completed + Future) − Current × Completed) / Future
    Max GPA on 10-point scale.
    """
    try:
        current_cgpa = Decimal(str(current_cgpa))
        completed_credits = Decimal(str(completed_credits))
        target_cgpa = Decimal(str(target_cgpa))
        future_credits = Decimal(str(future_credits))
        max_gpa = Decimal(str(max_gpa))
    except Exception:
        return None, False, 'Invalid input values.'

    if future_credits <= 0:
        return None, False, 'Future credits must be greater than zero.'
    if completed_credits < 0:
        return None, False, 'Completed credits cannot be negative.'
    if target_cgpa > max_gpa:
        return None, False, f'Target CGPA cannot exceed {max_gpa}.'
    if current_cgpa >= target_cgpa:
        return Decimal('0.00'), True, 'You have already achieved or exceeded your target CGPA!'

    numerator = (target_cgpa * (completed_credits + future_credits)) - (current_cgpa * completed_credits)
    required_gpa = (numerator / future_credits).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    if required_gpa > max_gpa:
        return required_gpa, False, (
            f'Target CGPA of {target_cgpa} cannot be achieved with {future_credits} credits. '
            f'Required GPA would be {required_gpa}, which exceeds the maximum of {max_gpa}.'
        )

    return required_gpa, True, f'You need a GPA of {required_gpa} in your upcoming semesters.'
