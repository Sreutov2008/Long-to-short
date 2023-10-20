import os
import re
import string

CHARACTERS = string.ascii_letters + string.digits

AUTO_SHORT_LENGTH = 6
MAX_SHORT_LENGTH = 16
MAX_ORIGINAL_LINK_LENGTH = 2048
MAX_AUTO_ATTEMPT = 10

SHORT_PATTERN = '^[' + re.escape(CHARACTERS) + ']+$'
REDIRECT_TO_ORIGINAL_URL_VIEW = 'redirect_to_original_url'
NO_BODY_REQUEST = 'Отсутствует тело запроса'
ERROR_SHORT = 'Указано недопустимое имя для короткой ссылки'
URL_IS_REQUIRED = '"url" является обязательным полем!'
SHORT_NOT_UNIQUE = 'Предложенный вариант короткой ссылки уже существует.'
SHORT_IS_LONG = (
    'Размер короткой ссылки превышен. '
    f'Максимум {MAX_SHORT_LENGTH} символов.'
)
SHORT_NOT_FOUND = 'Указанный id не найден'
ORIGINAL_URL_COMMENT = 'Добавьте исходную ссылку'
CUSTOM_URL_COMMENT = 'Добавьте свой вариант короткой ссылки'
FAILED_AUTO_GENERATION = (
    'Ошибка автоматической генерации короткой ссылки'
    'Попробуйте еще раз'
)
SUBMIT_COMMENT = 'Создать'


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
