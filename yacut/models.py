import random
import re
from datetime import datetime

from flask import url_for

from settings import (
    AUTO_SHORT_LENGTH, CHARACTERS, ERROR_SHORT,
    MAX_ORIGINAL_LINK_LENGTH, MAX_SHORT_LENGTH,
    SHORT_IS_LONG, SHORT_NOT_FOUND, SHORT_NOT_UNIQUE,
    SHORT_PATTERN, REDIRECT_TO_ORIGINAL_URL_VIEW,
    MAX_AUTO_ATTEMPT, FAILED_AUTO_GENERATION, ORIGINAL_LINK_IS_LONG
)
from yacut import db
from yacut.error_handlers import (
    ErrorOriginalValidation,
    ErrorShortValidation, ShortAnFound,
    ShortAnUnique, FailedAutoGeneration
)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_ORIGINAL_LINK_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=self.get_absolute_short_url()
        )

    def get_absolute_short_url(self):
        return url_for(
            REDIRECT_TO_ORIGINAL_URL_VIEW,
            short=self.short,
            _external=True
        )

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_original_url(short):
        urlmap = URLMap.get(short)
        if not urlmap:
            raise ShortAnFound(
                SHORT_NOT_FOUND
            )
        return urlmap.original

    @staticmethod
    def create(original, short, validation_required):
        if validation_required and len(original) > MAX_ORIGINAL_LINK_LENGTH:
            raise ErrorOriginalValidation(
                ORIGINAL_LINK_IS_LONG
            )
        if short == '' or short is None:
            short = URLMap.get_unique_short()
        elif validation_required:
            short = URLMap.short_is_valid(short)
        urlmap = URLMap(
            original=original,
            short=short,
        )
        db.session.add(urlmap)
        db.session.commit()
        return urlmap

    @staticmethod
    def short_is_valid(short):
        if len(short) > MAX_SHORT_LENGTH:
            raise ErrorShortValidation(
                SHORT_IS_LONG
            )
        if not re.match(
            pattern=SHORT_PATTERN,
            string=short,
        ):
            raise ErrorShortValidation(
                ERROR_SHORT
            )
        if URLMap.get(short):
            raise ShortAnUnique(
                SHORT_NOT_UNIQUE.format(
                    short=short
                )
            )
        return short

    @staticmethod
    def get_unique_short():
        for attempt in range(MAX_AUTO_ATTEMPT):
            short = ''.join(random.choices(
                CHARACTERS,
                k=AUTO_SHORT_LENGTH
            ))
            if not URLMap.get(short):
                return short
        raise FailedAutoGeneration(
            FAILED_AUTO_GENERATION
        )
