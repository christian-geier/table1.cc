from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

class PasteForm(FlaskForm):
    excel_data = TextAreaField(u'Text', id="pastein", widget=TextArea(), validators=[DataRequired()], render_kw={"placeholder": "Paste here"})
    submit = SubmitField('Make Table 1!')
