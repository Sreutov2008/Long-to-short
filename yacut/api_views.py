from flask import jsonify, request

from settings import (ERROR_SHORT, MAX_ORIGINAL_SHORT_LENGTH, NO_BODY_REQUEST,
                      SHORT_IS_LONG, SHORT_NOT_FOUND, SHORT_NOT_UNIQUE,
                      URL_IS_REQUIRED)
from yacut import app
from yacut.error_handlers import (CustomAPIException, ErrorOriginalValidation,
                                  ErrorShortValidation, ShortAnFound,
                                  ShortAnUnique)
from yacut.models import URLMap


@app.route('/api/id/', methods=['POST'])
def add_short_url():
    """Создание короткой ссылки."""
    data = request.get_json()
    if not data:
        raise CustomAPIException(
            NO_BODY_REQUEST
        )
    if 'url' not in data:
        raise CustomAPIException(
            URL_IS_REQUIRED
        )
    short = data.get('custom_id')
    try:
        return jsonify(
            URLMap.create(
                original=data['url'],
                short=short,
                validation_required=True,
            ).to_dict()
        ), 201
    except ErrorOriginalValidation:
        raise CustomAPIException(
            SHORT_IS_LONG.format(
                length=MAX_ORIGINAL_SHORT_LENGTH
            )
        )
    except ErrorShortValidation:
        raise CustomAPIException(
            ERROR_SHORT
        )
    except ShortAnUnique:
        raise CustomAPIException(
            SHORT_NOT_UNIQUE.format(
                short=short
            )
        )


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_url(short):
    """Получение оригинальной ссылки."""
    try:
        return jsonify(
            {'url': URLMap.get_original_url(short)}
        ), 200
    except ShortAnFound:
        raise CustomAPIException(
            SHORT_NOT_FOUND, 404
        )
