import re

EMAIL_REGEX_PATTERN = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')


def is_email_valid(email):
    return bool(EMAIL_REGEX_PATTERN.match(email))
