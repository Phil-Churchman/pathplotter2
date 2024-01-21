from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def val_weight(value):
    if value <0 or value >1:
        raise ValidationError(
            _("Weight must be between 0 and 1"),
            code="invalid",
            params={"value": value}
        )
    
def val_duration(value):
    if value <0:
        raise ValidationError(
            _("Duration must be greater than or equal to 0"),
            code="invalid",
            params={"value": value}
        )

def pos_int(value):
    if value < 0:
        raise ValidationError(
            _("Version must be a positive integer"),
            code="invalid",
            params={"value": value}
        )