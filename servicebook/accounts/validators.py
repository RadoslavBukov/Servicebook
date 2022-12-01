from datetime import date

from django.core.exceptions import ValidationError

from servicebook.core.utils import megabytes_to_bytes


def validate_file_less_than_5mb(fileobj):
    filesize = fileobj.file.size
    megabyte_limit = 5.0
    if filesize > megabytes_to_bytes(megabyte_limit):
        raise ValidationError(f'Max file size is {megabyte_limit}MB')


def validate_date_is_not_in_future(filled_date):
    if filled_date > date.today():
        raise ValidationError("The date cannot be in the future!")
