import os
import re
import string

CHARACTERS = string.ascii_letters + string.digits

AUTO_SHORT_LENGTH = 6
MAX_SHORT_LENGTH = 16
MAX_ORIGINAL_SHORT_LENGTH = 256

SHORT_PATTERN = '^[' + re.escape(CHARACTERS) + ']+$'

NO_BODY_REQUEST = 'Отсутствует тело запроса'
ERROR_SHORT = 'Указано недопустимое имя для короткой ссылки'
URL_IS_REQUIRED = '\"url\" является обязательным полем!'
SHORT_NOT_UNIQUE = 'Предложенный вариант короткой ссылки уже существует.'
SHORT_IS_LONG = (
    'Размер короткой ссылки превышен. '
    'Максимум {length} символов.'
)
SHORT_NOT_FOUND = 'Указанный id не найден'
ORIGINAL_URL_COMMENT = 'Добавьте исходную ссылку'
CUSTOM_URL_COMMENT = 'Добавьте свой вариант короткой ссылки'
SUBMIT_COMMENT = 'Создать'


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
