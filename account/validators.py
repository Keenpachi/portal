from django.core.exceptions import ValidationError


def validate_email(value):
    if '.eu' not in value:
        raise ValidationError('mail with eu domain need to by passed')
    else:
        return value