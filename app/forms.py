from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, RadioField, SelectMultipleField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea, ListWidget, CheckboxInput


class MultiCheckboxField(SelectMultipleField):
	widget			= ListWidget(prefix_label=False)
	option_widget	= CheckboxInput()


class PasteForm(FlaskForm):

    len_val = Length(min=100, max=1000000, message="Data does not meet requirements. Please try again.")

    excel_data = TextAreaField(u'Text', widget=TextArea(), validators=[DataRequired(), len_val], render_kw={"placeholder": "Paste here"})

    grouping_variable = RadioField(choices=[], validators=[DataRequired()])

    included_variables = MultiCheckboxField(choices=[])

    submit = SubmitField('Make Table 1!')
