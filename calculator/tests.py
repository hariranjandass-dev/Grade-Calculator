"""
GradeTrack Unit Tests — Annamalai University grading scale
S=10(90-100), A=9(80-89), B=8(70-79), C=7(60-69), D=6(55-59), E=5(50-54), RA=0(below 50)
"""
from decimal import Decimal
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .calculations import (
    get_grade_from_marks, calculate_gpa, calculate_cgpa,
    calculate_required_gpa, calculate_percentage, get_degree_class, is_ra_grade,
)
from .models import Semester, Subject


# ─── Grade Conversion ─────────────────────────────────────────────────────────

class GradeConversionTest(TestCase):

    def test_grade_S(self):
        grade, point = get_grade_from_marks(95)
        self.assertEqual(grade, 'S'); self.assertEqual(point, 10)

    def test_grade_S_boundary(self):
        grade, point = get_grade_from_marks(90)
        self.assertEqual(grade, 'S')

    def test_grade_A(self):
        grade, point = get_grade_from_marks(85)
        self.assertEqual(grade, 'A'); self.assertEqual(point, 9)

    def test_grade_A_boundary(self):
        grade, point = get_grade_from_marks(80)
        self.assertEqual(grade, 'A')

    def test_grade_B(self):
        grade, point = get_grade_from_marks(75)
        self.assertEqual(grade, 'B'); self.assertEqual(point, 8)

    def test_grade_C(self):
        grade, point = get_grade_from_marks(65)
        self.assertEqual(grade, 'C'); self.assertEqual(point, 7)

    def test_grade_D(self):
        grade, point = get_grade_from_marks(57)
        self.assertEqual(grade, 'D'); self.assertEqual(point, 6)

    def test_grade_D_boundary_low(self):
        grade, point = get_grade_from_marks(55)
        self.assertEqual(grade, 'D')

    def test_grade_E(self):
        grade, point = get_grade_from_marks(52)
        self.assertEqual(grade, 'E'); self.assertEqual(point, 5)

    def test_grade_E_boundary_low(self):
        grade, point = get_grade_from_marks(50)
        self.assertEqual(grade, 'E')

    def test_grade_RA(self):
        grade, point = get_grade_from_marks(49)
        self.assertEqual(grade, 'RA'); self.assertEqual(point, 0)

    def test_grade_RA_zero(self):
        grade, point = get_grade_from_marks(0)
        self.assertEqual(grade, 'RA')

    def test_invalid_negative(self):
        grade, point = get_grade_from_marks(-5)
        self.assertEqual(grade, 'RA')

    def test_invalid_over_100(self):
        grade, point = get_grade_from_marks(105)
        self.assertEqual(grade, 'RA')

    def test_is_ra_grade(self):
        self.assertTrue(is_ra_grade('RA'))
        self.assertTrue(is_ra_grade('W'))
        self.assertFalse(is_ra_grade('S'))
        self.assertFalse(is_ra_grade('A'))


# ─── GPA Calculation ─────────────────────────────────────────────────────────

class GPACalculationTest(TestCase):

    def test_single_subject(self):
        subjects = [{'credits': 4, 'grade_point': 10, 'grade': 'S'}]
        self.assertEqual(calculate_gpa(subjects), Decimal('10.00'))

    def test_multiple_subjects(self):
        # Your marksheet Semester 1 example
        subjects = [
            {'credits': 4, 'grade_point': 8, 'grade': 'B'},  # Maths
            {'credits': 4, 'grade_point': 9, 'grade': 'A'},  # Physics
            {'credits': 4, 'grade_point': 8, 'grade': 'B'},  # Chemistry
            {'credits': 3, 'grade_point': 8, 'grade': 'B'},  # Programming
            {'credits': 1, 'grade_point': 8, 'grade': 'B'},  # Heritage
            {'credits': 1.5, 'grade_point': 8, 'grade': 'B'},  # Comm Lab
            {'credits': 1.5, 'grade_point': 9, 'grade': 'A'},  # Workshop
            {'credits': 1.5, 'grade_point': 9, 'grade': 'A'},  # Electrical Lab
        ]
        result = calculate_gpa(subjects)
        self.assertIsInstance(result, Decimal)
        self.assertGreater(result, Decimal('7.0'))

    def test_ra_grade_excluded(self):
        # RA course must NOT count in GPA
        subjects = [
            {'credits': 4, 'grade_point': 10, 'grade': 'S'},
            {'credits': 4, 'grade_point': 0,  'grade': 'RA'},  # excluded
        ]
        # Only the S grade counts: 40/4 = 10.00
        result = calculate_gpa(subjects)
        self.assertEqual(result, Decimal('10.00'))

    def test_all_ra_grades(self):
        subjects = [{'credits': 4, 'grade_point': 0, 'grade': 'RA'}]
        self.assertEqual(calculate_gpa(subjects), Decimal('0.00'))

    def test_zero_credits(self):
        subjects = [{'credits': 0, 'grade_point': 10, 'grade': 'S'}]
        self.assertEqual(calculate_gpa(subjects), Decimal('0.00'))

    def test_empty(self):
        self.assertEqual(calculate_gpa([]), Decimal('0.00'))


# ─── CGPA Calculation ─────────────────────────────────────────────────────────

class CGPACalculationTest(TestCase):

    def test_single_semester(self):
        sems = [{'gpa': 8.5, 'total_credits': 21}]
        self.assertEqual(calculate_cgpa(sems), Decimal('8.50'))

    def test_multiple_semesters(self):
        sems = [
            {'gpa': 8.0, 'total_credits': 21},
            {'gpa': 8.5, 'total_credits': 21},
            {'gpa': 9.0, 'total_credits': 21},
        ]
        result = calculate_cgpa(sems)
        self.assertEqual(result, Decimal('8.50'))

    def test_different_credits(self):
        sems = [
            {'gpa': 10.0, 'total_credits': 1},
            {'gpa': 0.0,  'total_credits': 9},
        ]
        self.assertEqual(calculate_cgpa(sems), Decimal('1.00'))

    def test_empty(self):
        self.assertEqual(calculate_cgpa([]), Decimal('0.00'))


# ─── Percentage Calculation ───────────────────────────────────────────────────

class PercentageTest(TestCase):

    def test_percentage_formula(self):
        # (8.50 - 0.25) * 10 = 82.50
        self.assertEqual(calculate_percentage(8.50), Decimal('82.50'))

    def test_percentage_honours(self):
        # (8.25 - 0.25) * 10 = 80.00
        self.assertEqual(calculate_percentage(8.25), Decimal('80.00'))

    def test_percentage_first_class(self):
        # (6.75 - 0.25) * 10 = 65.00
        self.assertEqual(calculate_percentage(6.75), Decimal('65.00'))


# ─── Target CGPA ─────────────────────────────────────────────────────────────

class TargetCGPATest(TestCase):

    def test_achievable(self):
        gpa, ok, msg = calculate_required_gpa(7.5, 80, 8.25, 21)
        self.assertTrue(ok)
        self.assertLessEqual(gpa, Decimal('10'))

    def test_impossible(self):
        gpa, ok, msg = calculate_required_gpa(5.0, 180, 9.5, 21)
        self.assertFalse(ok)

    def test_already_above_target(self):
        gpa, ok, msg = calculate_required_gpa(8.5, 100, 8.25, 21)
        self.assertTrue(ok)
        self.assertEqual(gpa, Decimal('0.00'))

    def test_zero_future_credits(self):
        gpa, ok, msg = calculate_required_gpa(7.5, 80, 8.5, 0)
        self.assertFalse(ok)
        self.assertIsNone(gpa)

    def test_target_exceeds_max(self):
        gpa, ok, msg = calculate_required_gpa(5.0, 100, 11.0, 21)
        self.assertFalse(ok)


# ─── Authentication & Security ────────────────────────────────────────────────

class AuthTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass123')

    def test_register_page(self):
        self.assertEqual(self.client.get(reverse('register')).status_code, 200)

    def test_login_success(self):
        resp = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass123'})
        self.assertRedirects(resp, reverse('dashboard'))

    def test_logout(self):
        self.client.login(username='testuser', password='testpass123')
        resp = self.client.get(reverse('logout'))
        self.assertRedirects(resp, reverse('home'))

    def test_dashboard_requires_login(self):
        resp = self.client.get(reverse('dashboard'))
        self.assertRedirects(resp, '/login/?next=/dashboard/')


class DataIsolationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_a = User.objects.create_user('user_a', password='pass123')
        self.user_b = User.objects.create_user('user_b', password='pass123')
        self.sem = Semester.objects.create(
            student=self.user_a, semester_number=1, gpa=8.5, total_credits=21
        )

    def test_user_b_cannot_view_user_a_semester(self):
        self.client.login(username='user_b', password='pass123')
        resp = self.client.get(reverse('semester_detail', args=[self.sem.pk]))
        self.assertEqual(resp.status_code, 404)

    def test_user_b_cannot_delete_user_a_semester(self):
        self.client.login(username='user_b', password='pass123')
        self.client.post(reverse('delete_semester', args=[self.sem.pk]))
        self.assertTrue(Semester.objects.filter(pk=self.sem.pk).exists())


class PublicCalculatorTest(TestCase):
    def test_gpa_page(self):
        self.assertEqual(self.client.get(reverse('gpa_calculator')).status_code, 200)

    def test_cgpa_page(self):
        self.assertEqual(self.client.get(reverse('cgpa_calculator')).status_code, 200)

    def test_target_page(self):
        self.assertEqual(self.client.get(reverse('target_cgpa')).status_code, 200)

    def test_gpa_post(self):
        resp = self.client.post(reverse('gpa_calculator'), {
            'subject_name[]': ['Mathematics I', 'Physics'],
            'credits[]': ['4', '4'],
            'marks[]': ['75', '85'],
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '8.')  # B=8, A=9, avg should be 8.5
