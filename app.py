from flask import Flask, escape, request, render_template, url_for

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

app = Flask(__name__)
app.config['SECRET_KEY'] = "very_secret"


class PasteForm(FlaskForm):
    excel_data = TextAreaField(u'Text', id="pastein", widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Load Data Set')

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method=='POST':
        body = request.form['excel_data']
        print("The value is:" + str(body))


    paste_form = PasteForm()
    return render_template('index.html', form=paste_form)
