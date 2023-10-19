from flask import abort, redirect, render_template
from http import HTTPStatus
from yacut import app
from yacut.forms import URLForm
from yacut.models import URLMap
from yacut.error_handlers import ShortAnFound


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """View-функция главной страницы."""
    form = URLForm()
    if not form.validate_on_submit():
        return render_template(
            'index.html',
            form=form
        )
    short = form.custom_id.data
    return render_template(
        'index.html',
        form=form,
        short_link=URLMap.create(
            original=form.original_link.data,
            short=short,
            validation_required=False,
        ).get_absolute_short_url()
    )


@app.route('/<string:short>', methods=['GET'])
def short_url_view(short):
    """Переадресация."""
    try:
        return redirect(
            URLMap.get_original_url(short),
            code=HTTPStatus.FOUND
        )
    except ShortAnFound:
        abort(404)
