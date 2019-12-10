from flask import Flask, escape, request, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
