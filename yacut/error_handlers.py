from flask import jsonify, render_template

from yacut import app, db


class ShortAnUnique(Exception):
    """Ошибка проверки на уникальность: короткая ссылка уже существует."""
    pass


class ErrorShortValidation(Exception):
    """Ошибка валидации: недопустимая короткая ссылка."""
    pass


class ErrorOriginalValidation(Exception):
    """Ошибка валидации: превышен размер оригинальной ссылки."""
    pass


class ShortAnFound(Exception):
    """Указанный ссылка не найдена."""
    pass


class CustomAPIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(CustomAPIException)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
