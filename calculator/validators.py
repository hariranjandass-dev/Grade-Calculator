from django.core.exceptions import ValidationError


def validate_marks(value):
    if value is not None:
        if float(value) < 0 or float(value) > 100:
            raise ValidationError('Marks must be between 0 and 100.')


def validate_credits(value):
    if int(value) <= 0:
        raise ValidationError('Credits must be greater than zero.')


def validate_gpa(value, max_gpa=10):
    if float(value) < 0 or float(value) > max_gpa:
        raise ValidationError(f'GPA must be between 0 and {max_gpa}.')
