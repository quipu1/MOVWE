# project_name/validators.py
import re
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
@deconstructible
class AlphanumericUsernameValidator(validators.RegexValidator):
    regex = r'^[\w][\w\d_]{5,150}$'
    message = _(
        'Enter a valid username. This value may contain only English letters, '
        'numbers and underscores.'
    )
    flags = re.ASCII