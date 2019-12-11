from flask import Flask, escape, request, render_template, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method=='POST':
        value = request.form['value']
        print("The value is:" + str(value))

    return render_template('index.html')
