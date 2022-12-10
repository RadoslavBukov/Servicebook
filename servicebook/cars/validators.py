from datetime import date
from django.core import exceptions
from django.core.exceptions import ValidationError


def validate_date_is_not_in_past(filled_date):
    if filled_date < date.today():
        raise ValidationError("The date cannot be in the past!")


def validate_string_min_2_symbols(value):
    MIN_SYMBOLS = 2
    if len(value) < MIN_SYMBOLS:
        raise exceptions.ValidationError("The username must be a minimum of 2 chars")


def validate_year_between_1970_and_2022(value):
    MIN_YEAR = 1970
    MAX_YEAR = 2022
    if value < MIN_YEAR or value > MAX_YEAR:
        raise exceptions.ValidationError("Year must be between 1970 and 2022")