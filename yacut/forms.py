from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import (InputRequired, Length, Optional, Regexp,
                                ValidationError)

from settings import (CUSTOM_URL_COMMENT, ERROR_SHORT,
                      MAX_ORIGINAL_SHORT_LENGTH, MAX_SHORT_LENGTH,
                      ORIGINAL_URL_COMMENT, SHORT_NOT_UNIQUE, SHORT_PATTERN,
                      SUBMIT_COMMENT, URL_IS_REQUIRED)
from yacut.models import URLMap


class URLForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_URL_COMMENT,
        validators=[
            Length(
                max=MAX_ORIGINAL_SHORT_LENGTH
            ),
            InputRequired(
                message=URL_IS_REQUIRED
            )
        ]
    )
    custom_id = URLField(
        CUSTOM_URL_COMMENT,
        validators=[
            Length(
                max=MAX_SHORT_LENGTH,
                message=ERROR_SHORT
            ),
            Optional(),
            Regexp(
                regex=SHORT_PATTERN,
                message=ERROR_SHORT
            )
        ]
    )
    submit = SubmitField(
        SUBMIT_COMMENT
    )

    def validate_custom_id(self, field):
        if URLMap.get(field.data):
            raise ValidationError(
                SHORT_NOT_UNIQUE
            )
