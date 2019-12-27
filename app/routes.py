from flask import render_template, request, redirect, url_for, flash
from app.forms import CompleteForm

from app import app

from io import StringIO

from pandas import read_csv

from tableone import TableOne

from urllib.parse import urlparse, urlunparse

@app.before_request
def redirect_nonwww():
    """Redirect non-www requests to www."""
    urlparts = urlparse(request.url)
    if urlparts.netloc == 'table1.cc':
        urlparts_list = list(urlparts)
        urlparts_list[1] = 'www.table1.cc'
        return redirect(urlunparse(urlparts_list), code=301)


def df_to_table(df, incl_vars, categorical, nonnormal, groupvar, pval, labels, order, missing):

    df_cols = list(df)

    # this is the list of columns for which Table 1 is generated
    col_list = [df_col for df_col in incl_vars]

    my_table = TableOne(df, columns=col_list, groupby=groupvar,
                        nonnormal=nonnormal, categorical=categorical,
                        pval=pval, missing=missing, label_suffix=True,
                        rename=labels, order=order
                        )

    my_table_html = my_table.to_html(classes=["table", "table-dark", 'table-sm'])

    return my_table_html


@app.route('/', methods=['GET', 'POST'])
def index():

    complete_form = CompleteForm(request.form)
    my_table_html = None
    incl_var_types = request.form.getlist('options-variable_type', None)


    if (request.method == 'POST'):
        if complete_form.paste_data.validate_on_submit():

            flash("Table parsed successfully !", 'success')

            raw_data = request.form['paste_data-excel_data']
            raw_string = StringIO(raw_data)

            frame = read_csv(raw_string, sep='\t')

            rownames = [colname for colname in list(frame)]

            c_varnames = [(k, k) for k in rownames]

            complete_form.options.included_variables.choices = c_varnames

            groupvar_names = ['None'] + rownames
            c_groupvar = [(k, k) for k in groupvar_names]
            complete_form.options.grouping_variable.choices = c_groupvar


            hide_display = True


        if request.form.get('options-submit2') is not None:

            raw_data = request.form['paste_data-excel_data']
            raw_string = StringIO(raw_data)

            frame = read_csv(raw_string, sep='\t')

            groupvar = request.form.get('options-grouping_variable', False)


            groupvar = None if groupvar == 'None' else groupvar

            incl_vars = request.form.getlist('options-included_variables')

            nonnormal = [var for i, var in enumerate(list(frame)) if (incl_var_types[i] == 'nonnormal' and var in incl_vars)]

            categorical = [var for i, var in enumerate(list(frame)) if (incl_var_types[i] == 'cat' and var in incl_vars)]

            print("Categorical: " + str(categorical))
            print("Non-normal: " + str(nonnormal))


            pval = request.form.get('options-pval', False)

            show_missing = request.form.get('options-show_missing', False)

            labels = request.form.getlist('options-custom_labels', False)

            order_switch = request.form.get('options-switch_group_order', False)

            # currently only allows to switch the grouping variable
            order = None if order_switch == False else { groupvar : ["1"]}

            my_table_html = df_to_table(frame, incl_vars, categorical, nonnormal, groupvar, pval, labels, order, missing=show_missing)


        return render_template('table1.html',
            incl_var_types=incl_var_types,
            my_table_html=my_table_html,
            complete_form=complete_form,
            hide_display=True,
            )


    return render_template('index.html', complete_form=complete_form, hide_display=False)



@app.route('/background')
def background():
    return render_template('background.html')


@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')
