from django import forms
from .models import GradingSystem, GradeScale, Semester, Subject


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['semester_number', 'academic_year']
        widgets = {
            'semester_number': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'academic_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2023-24'}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_code', 'subject_name', 'credits', 'marks', 'grade', 'grade_point']
        widgets = {
            'subject_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code (optional)'}),
            'subject_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject Name'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'marks': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100, 'step': '0.01'}),
            'grade': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'grade_point': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }

    def clean_marks(self):
        marks = self.cleaned_data.get('marks')
        if marks is not None:
            if marks < 0 or marks > 100:
                raise forms.ValidationError('Marks must be between 0 and 100.')
        return marks

    def clean_credits(self):
        credits = self.cleaned_data.get('credits')
        if credits is not None and credits <= 0:
            raise forms.ValidationError('Credits must be greater than zero.')
        return credits


class GradingSystemForm(forms.ModelForm):
    class Meta:
        model = GradingSystem
        fields = ['name', 'scale_type', 'maximum_grade_point']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'scale_type': forms.Select(attrs={'class': 'form-select'}),
            'maximum_grade_point': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class GradeScaleForm(forms.ModelForm):
    class Meta:
        model = GradeScale
        fields = ['grade', 'minimum_marks', 'maximum_marks', 'grade_point', 'description']
        widgets = {
            'grade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. A+'}),
            'minimum_marks': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'maximum_marks': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'grade_point': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional description'}),
        }


class GPACalculatorForm(forms.Form):
    """Simple form for anonymous GPA calculation."""
    pass


class TargetCGPAForm(forms.Form):
    current_cgpa = forms.DecimalField(
        min_value=0, max_digits=4, decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'})
    )
    completed_credits = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'})
    )
    target_cgpa = forms.DecimalField(
        min_value=0, max_digits=4, decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'})
    )
    future_credits = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'})
    )
    max_gpa = forms.DecimalField(
        min_value=1, max_digits=4, decimal_places=2, initial=10,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '10.00'})
    )
