from flask import redirect, render_template

from yacut import app
from yacut.forms import URLForm
from yacut.models import URLMap


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
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original
    )
