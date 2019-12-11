from flask import Flask, escape, request, render_template, url_for

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

import pandas as pd
from pandas import read_csv

from io import StringIO

from tableone import TableOne

app = Flask(__name__)
app.config['SECRET_KEY'] = "very_secret"


class PasteForm(FlaskForm):
    excel_data = TextAreaField(u'Text', id="pastein", widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Load Data Set')

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method=='POST':
        raw_data = request.form['excel_data']
        raw_string = StringIO(raw_data)
        df = read_csv(raw_string, sep='\t')
        my_table = TableOne(df, groupby='gender', pval='True')
        my_table_html = my_table.tabulate(tablefmt="html")
        return my_table_html

    paste_form = PasteForm()
    return render_template('index.html', form=paste_form)
