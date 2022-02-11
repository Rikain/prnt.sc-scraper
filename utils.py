import string
import random
import os
from time import localtime, asctime

from logger import exception

ALLOWED_CHARACTERS = string.ascii_lowercase + string.digits
CODE_LENGTH = 6


def check_and_create_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
    return


def file_name_for_code(code: str, extension: str = '.png'):
    return f'{code} {asctime(localtime())}{extension}'.replace(':', '-')


@exception()
def add_one_code(code: str, i: int, len_of_last_char: int):
    return code[:i] +\
           ALLOWED_CHARACTERS[ALLOWED_CHARACTERS.index(code[i]) + 1] +\
           ALLOWED_CHARACTERS[0] * len_of_last_char


def get_one_code_higher(code: str):
    if code == ALLOWED_CHARACTERS[-1] * CODE_LENGTH:
        return ALLOWED_CHARACTERS[0] * CODE_LENGTH
    else:
        len_of_last_char = 0
        for i in reversed(range(CODE_LENGTH)):
            if code[i] != ALLOWED_CHARACTERS[-1]:
                try:
                    new_code = add_one_code(code, i, len_of_last_char)
                    return new_code
                except (ValueError, IndexError):
                    return generate_new_code()
            else:
                len_of_last_char += 1
    return generate_new_code()


def generate_new_code():
    return random.choice(string.ascii_lowercase) +\
           ''.join([random.choice(ALLOWED_CHARACTERS) for _ in range(CODE_LENGTH - 1)])


def generate_code():
    first_code = generate_new_code()
    yield first_code
    code = get_one_code_higher(first_code)
    yield code
    while code != first_code:
        code = get_one_code_higher(code)
        yield code
