from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, RadioField, SelectMultipleField, SelectField, FormField, BooleanField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea, ListWidget, CheckboxInput


class MultiCheckboxField(SelectMultipleField):
    widget			= ListWidget(prefix_label=False)
    option_widget	= CheckboxInput()


class PasteForm(FlaskForm):

    len_val = Length(min=100, max=1000000, message="Data does not meet requirements. Please try again.")
    excel_data = TextAreaField(u'Text', widget=TextArea(), validators=[DataRequired(), len_val], render_kw={"placeholder": "Step 0. Copy the raw spreadsheet data from Excel/Google Sheets/etc. and paste it into this field!"})

    submit1 = SubmitField('I pasted the spreadsheet data!')


class SetOptionsForm(FlaskForm):

    grouping_variable = SelectField(choices=[], validators=[DataRequired()])
    included_variables = MultiCheckboxField(choices=[], validators=[DataRequired()])
    variable_type = SelectField(choices=[('cont', 'continuous'), ('cat', 'categorical')], validators = [DataRequired()])

    submit2 = SubmitField('Make Table 1!')

    pval = BooleanField('calculate p-Value')

class CompleteForm(FlaskForm):
    paste_data = FormField(PasteForm)
    options = FormField(SetOptionsForm)
