from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, RadioField, SelectField, SelectMultipleField, FormField, BooleanField
from wtforms.validators import DataRequired, Length, Optional
from wtforms.widgets import TextArea, ListWidget, CheckboxInput


class MultiCheckboxField(SelectMultipleField):
    widget            = ListWidget(prefix_label=False)
    option_widget    = CheckboxInput()


class PasteForm(FlaskForm):

    len_val = Length(min=100, max=1000000, message="Data does not meet requirements. Please try again.")
    excel_data = TextAreaField(u'Text', widget=TextArea(), validators=[DataRequired(), len_val], render_kw={"placeholder": "Step 0: Copy the raw spreadsheet data from Excel/Google Sheets/etc. and paste it into this field!"})

    submit1 = SubmitField('I pasted the spreadsheet data!')


class SetOptionsForm(FlaskForm):

    grouping_variable = SelectField(choices=[], validators=[DataRequired()])
    switch_group_order = BooleanField('switch group order', validators=[Optional()])

    included_variables = MultiCheckboxField(choices=[], validators=[DataRequired()])
    variable_type = SelectField(choices=[('cat', 'categorical'), ('cont', 'continuous'), ('nonnormal', 'non-normal')])

    submit2 = SubmitField('Make Table 1!')

    pval = BooleanField('calculate p-values', validators=[Optional()])
    show_missing = BooleanField('show missing values')

    def validate(self):
        if not super(SetOptionsForm, self).validate():
            return False
        if self.pval.data and self.grouping_variable.data == "None":
            msg = "If \'calculate p-values\' is selected, a grouping variable is required !"
            self.pval.errors.append(msg)
            self.grouping_variable.errors.append(msg)
            return False
        return True

class CompleteForm(FlaskForm):
    paste_data = FormField(PasteForm)
    options = FormField(SetOptionsForm)
