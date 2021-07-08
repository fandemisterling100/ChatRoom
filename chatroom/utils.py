from django.core.validators import RegexValidator
from django.core import validators


# Validator to avoid spaces and special characters on room names to
# handle TypeErrors in group names
room_name_validator = RegexValidator(regex='^[a-z0-9]+(?:[._-][a-z0-9]+)*$',
                                     message='The room name cannot contain spaces or special characters',
                                     )
