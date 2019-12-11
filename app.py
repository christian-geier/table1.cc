from flask import Flask, escape, request, render_template, url_for

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

import pandas as pd
from pandas import read_csv

from io import StringIO

from tableone import TableOne

GROUP_COL = 'group'

DROP_COLS = ['id', 'raw_id', GROUP_COL]


def df_to_table(df):

    df_cols = list(df)

    # this is the list of columns for which Table 1 is generated
    col_list = [df_col for df_col in df_cols if df_col not in DROP_COLS]

    print("These are the selected columns: " + str(col_list))

    my_table = TableOne(df, columns=col_list, groupby=GROUP_COL, pval='True')
    my_table_html = my_table.tabulate(tablefmt="html")

    return my_table_html


app = Flask(__name__)
app.config['SECRET_KEY'] = "very_secret"


class PasteForm(FlaskForm):
    excel_data = TextAreaField(u'Text', id="pastein", widget=TextArea(), validators=[DataRequired()], render_kw={"placeholder": "Paste here"})
    submit = SubmitField('Make Table 1!')

@app.route('/', methods=['GET', 'POST'])
def index():

    my_table_html = None

    if request.method=='POST':
        raw_data = request.form['excel_data']
        raw_string = StringIO(raw_data)
        df = read_csv(raw_string, sep='\t')
        my_table_html = df_to_table(df)

    paste_form = PasteForm()

    return render_template('index.html', form=paste_form, my_table_html=my_table_html)
