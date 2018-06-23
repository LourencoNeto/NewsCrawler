from flask import Flask
from flask import render_template  # !Important
import pandas as pd

app = Flask(__name__)


@app.route('/')
def unigrama_dashboard_acuracy():
    return render_template('home.html')


