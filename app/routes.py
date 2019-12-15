from flask import render_template, request
from app.forms import PasteForm

from app import app

from io import StringIO

from pandas import read_csv

from tableone import TableOne


DROP_COLS = ['id', 'raw_id']


def df_to_table(df, incl_vars, groupvar):

    df_cols = list(df)

    # this is the list of columns for which Table 1 is generated
    col_list = [df_col for df_col in incl_vars if df_col not in DROP_COLS]

    my_table = TableOne(df, columns=col_list, groupby=groupvar)
    my_table_html = my_table.tabulate(tablefmt="html")

    return my_table_html


@app.route('/', methods=['GET', 'POST'])
def index():

    paste_form = PasteForm()


    if request.method=='POST':
        raw_data = request.form['excel_data']
        raw_string = StringIO(raw_data)
        df = read_csv(raw_string, sep='\t')

        rownames = list(df)

        c_groupvar = [(k, k) for k in rownames]

        paste_form.grouping_variable.choices = c_groupvar

        paste_form.included_variables.choices = c_groupvar


    if paste_form.validate_on_submit():
        groupvar = request.form['grouping_variable']

        incl_vars = request.form.getlist('included_variables')

        my_table_html = df_to_table(df, incl_vars, groupvar)

        return render_template('index.html',
            form=paste_form, my_table_html=my_table_html,
            )


    return render_template('index.html',
        form=paste_form,
        )
