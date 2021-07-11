""" Validator to avoid spaces and special characters on room names to
    handle TypeErrors in group names
"""

from django.core.validators import RegexValidator


room_name_validator = RegexValidator(regex='^[A-Za-z_-][A-Za-z0-9_-]*$',
                                     message='The room name cannot contain spaces or special characters',
                                     )
