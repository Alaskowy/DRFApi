import os
from django.core.exceptions import ValidationError

VALID_EXTENSIONS = ['.jpg', '.jpeg', '.png']


def validate_file_extension(file):
    extension = os.path.splitext(file.name)[1]
    if extension not in VALID_EXTENSIONS:
        raise ValidationError
    else:
        return file
