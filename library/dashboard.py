"""Moving the template code to a separate file.

Mixing Python code with HTML is ugly. Templates usually live in their own
location. By default, flask will look up for templates in a 'templates'
directory living in the same path as the application.

"""

from flask import Flask
from flask import render_template  # !Important
import pandas as pd

app = Flask(__name__)



@app.route('/')
def unigrama_dashboard_acuracy():
    
    return render_template('teste_2.html')

@app.route('/bigrama/')
def bigrama_dashboard_acuracy():
    test_dataset = pd.read_excel("pandas_simple.xlsx")
    return render_template('bigrama.html', metrica = "Acurácia", test_set = test_dataset, test_size = len(test_dataset))

@app.route('/bigrama/<metrics>')
def bigrama_dashboard(metrics):
    test_dataset = pd.read_excel("pandas_simple.xlsx")
    if metrics in ["Índice Cohen-Kappa", "Matriz de Confusão", "Análise Temporal"]:
        return render_template('bigrama.html', metrica = metrics, test_set = test_dataset, test_size = len(test_dataset))
        
@app.route('/trigrama/')
def trigrama_dashboard_acuracy():
    test_dataset = pd.read_excel("pandas_simple.xlsx")
    return render_template('trigrama.html', metrica = "Acurácia", test_set = test_dataset, test_size = len(test_dataset))

@app.route('/trigrama/<metrics>')
def trigrama_dashboard(metrics):
    test_dataset = pd.read_excel("pandas_simple.xlsx")
    if metrics in ["Índice Cohen-Kappa", "Matriz de Confusão", "Análise Temporal"]:
        return render_template('trigrama.html', metrica = metrics, test_set = test_dataset, test_size = len(test_dataset))