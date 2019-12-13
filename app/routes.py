from flask import render_template, request
from app.forms import PasteForm

from app import app

from io import StringIO

from pandas import read_csv

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


@app.route('/', methods=['GET', 'POST'])
def index():

    my_table_html = None
    rownames = None

    paste_form = PasteForm()

    print(paste_form.errors)

    if paste_form.validate_on_submit() & (request.method=='POST'):
        raw_data = request.form['excel_data']
        raw_string = StringIO(raw_data)
        df = read_csv(raw_string, sep='\t')
        my_table_html = df_to_table(df)

        if rownames == None:

            rownames = list(df)

    return render_template('index.html',
        form=paste_form, rownames=rownames, my_table_html=my_table_html,
        )
