from flask import render_template, request, redirect, url_for, flash
from app.forms import CompleteForm

from app import app

from io import StringIO

from pandas import read_csv

from tableone import TableOne


DROP_COLS = ['id', 'raw_id']


def df_to_table(df, incl_vars, groupvar, pval, missing=False):

    df_cols = list(df)

    # this is the list of columns for which Table 1 is generated
    col_list = [df_col for df_col in incl_vars if df_col not in DROP_COLS]

    my_table = TableOne(df, columns=col_list, groupby=groupvar, pval=pval, missing=missing)
    my_table_html = my_table.to_html(classes=["table", "table-dark", 'table-sm'])

    return my_table_html


@app.route('/', methods=['GET', 'POST'])
def index():

    complete_form = CompleteForm(request.form)
    hide_display = False
    my_table_html = None

    if (request.method == 'POST'):
        if complete_form.paste_data.validate_on_submit():

            flash("Table parsed successfully !", 'success')

            raw_data = request.form['paste_data-excel_data']
            raw_string = StringIO(raw_data)

            frame = read_csv(raw_string, sep='\t')

            rownames = list(frame)

            c_groupvar = [(k, k) for k in rownames]
            c_vartypes = [(k, 'continuous') for k in rownames]

            complete_form.options.grouping_variable.choices = c_groupvar
            complete_form.options.included_variables.choices = c_groupvar

            hide_display = True


        if request.form.get('options-submit2') is not None:

            raw_data = request.form['paste_data-excel_data']
            raw_string = StringIO(raw_data)

            frame = read_csv(raw_string, sep='\t')

            groupvar = request.form['options-grouping_variable']

            incl_vars = request.form.getlist('options-included_variables')

            pval = request.form.get('options-pval', False)

            my_table_html = df_to_table(frame, incl_vars, groupvar, pval)


        return render_template('table1.html',
            my_table_html=my_table_html,
            complete_form=complete_form,
            hide_display=True
            )


    return render_template('index.html', complete_form=complete_form, hide_display=False)



@app.route('/background')
def background():
    return render_template('background.html')


@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')
