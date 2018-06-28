from flask import Flask
from flask import render_template  # !Important
import pandas as pd

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/unigrama/')
def unigrama_dashboard_acuracy():
    test_dataset = pd.read_excel("pandas_simple.xlsx")
    daily_data = pd.read_excel("Dados_Diarios.xlsx")
    
    graphics_data = []
    label = []
    for i in range(len(daily_data)):
        if daily_data["Tipo"][i] == "Unigrama":
            graphics_data.append(daily_data["Acurácia"][i])
            label.append(daily_data["Dia"][i])
    
    vocabulary_data = pd.read_excel("Analise_Vocabulario.xlsx")
    vocabulary_label = []
    vocabulary_metrics = []
    for i in range(len(vocabulary_data)):
        if vocabulary_data["Tipo"][i] == "Unigrama":
            vocabulary_label.append(vocabulary_data["Tamanho Vocabulário"][i])
            vocabulary_metrics.append(vocabulary_data["Acurácia"][i])
    return render_template('unigrama.html', metrica = "Acurácia", test_set = test_dataset, test_size = len(test_dataset), dados = graphics_data, legenda = label, dados_vocabulario = vocabulary_metrics, vocabulario_legenda = vocabulary_label)

@app.route('/unigrama/<metrics>')
def unigrama_dashboard(metrics):
    test_dataset = pd.read_excel("pandas_simple.xlsx")
    daily_data = pd.read_excel("Dados_Diarios.xlsx")
    vocabulary_data = pd.read_excel("Analise_Vocabulario.xlsx")
    vocabulary_label = []
    vocabulary_metrics = []
    graphics_data = []
    label = []
    
    if metrics in ["Índice Cohen-Kappa", "Análise Temporal"]:
        for i in range(len(daily_data)):
            if daily_data["Tipo"][i] == "Unigrama":
                graphics_data.append(daily_data[metrics][i])
                label.append(daily_data["Dia"][i])
                
        for i in range(len(vocabulary_data)):
            if vocabulary_data["Tipo"][i] == "Unigrama":
                vocabulary_label.append(vocabulary_data["Tamanho Vocabulário"][i])
                vocabulary_metrics.append(vocabulary_data[metrics][i])
        return render_template('unigrama.html', metrica = metrics, test_set = test_dataset, test_size = len(test_dataset), dados = graphics_data, legenda = label, dados_vocabulario = vocabulary_metrics, vocabulario_legenda = vocabulary_label)

@app.route('/bigrama/')
def bigrama_dashboard_acuracy():
    test_dataset = pd.read_excel("pandas_simple.xlsx")
    daily_data = pd.read_excel("Dados_Diarios.xlsx")
    
    graphics_data = []
    label = []
    for i in range(len(daily_data)):
        if daily_data["Tipo"][i] == "Bigrama":
            graphics_data.append(daily_data["Acurácia"][i])
            label.append(daily_data["Dia"][i])
    
    vocabulary_data = pd.read_excel("Analise_Vocabulario.xlsx")
    vocabulary_label = []
    vocabulary_metrics = []
    for i in range(len(vocabulary_data)):
        if vocabulary_data["Tipo"][i] == "Bigrama":
            vocabulary_label.append(vocabulary_data["Tamanho Vocabulário"][i])
            vocabulary_metrics.append(vocabulary_data["Acurácia"][i])
    
    return render_template('bigrama.html', metrica = "Acurácia", test_set = test_dataset, test_size = len(test_dataset), dados = graphics_data, legenda = label, dados_vocabulario = vocabulary_metrics, vocabulario_legenda = vocabulary_label)


@app.route('/bigrama/<metrics>')
def bigrama_dashboard(metrics):
    test_dataset = pd.read_excel("pandas_simple.xlsx")
    daily_data = pd.read_excel("Dados_Diarios.xlsx")
    vocabulary_data = pd.read_excel("Analise_Vocabulario.xlsx")
    vocabulary_label = []
    vocabulary_metrics = []
    graphics_data = []
    label = []
    if metrics in ["Índice Cohen-Kappa", "Análise Temporal"]:
        for i in range(len(daily_data)):
            if daily_data["Tipo"][i] == "Bigrama":
                graphics_data.append(daily_data[metrics][i])
                label.append(daily_data["Dia"][i])
        for i in range(len(vocabulary_data)):
            if vocabulary_data["Tipo"][i] == "Bigrama":
                vocabulary_label.append(vocabulary_data["Tamanho Vocabulário"][i])
                vocabulary_metrics.append(vocabulary_data[metrics][i])
        return render_template('bigrama.html', metrica = metrics, test_set = test_dataset, test_size = len(test_dataset), dados = graphics_data, legenda = label, dados_vocabulario = vocabulary_metrics, vocabulario_legenda = vocabulary_label)
    

"""
@app.route('/trigrama/')
def trigrama_dashboard_acuracy():
    test_dataset = pd.read_excel("pandas_simple.xlsx")
    daily_data = pd.read_excel("Dados_Diarios.xlsx")
    
    graphics_data = []
    label = []
    for i in range(len(daily_data)):
        if daily_data["Tipo"][i] == "Unigrama":
            graphics_data.append(daily_data["Acurácia"][i])
            label.append(daily_data["Dia"][i])
    return render_template('trigrama.html', metrica = "Acurácia", test_set = test_dataset, test_size = len(test_dataset), dados = graphics_data, legenda = label)

@app.route('/trigrama/<metrics>')
def trigrama_dashboard(metrics):
    test_dataset = pd.read_excel("pandas_simple.xlsx")
    daily_data = pd.read_excel("Dados_Diarios.xlsx")
    graphics_data = []
    label = []
    
    if metrics in ["Índice Cohen-Kappa", "Análise Temporal"]:
        for i in range(len(daily_data)):
            if daily_data["Tipo"][i] == "Unigrama":
                graphics_data.append(daily_data[metrics][i])
                label.append(daily_data["Dia"][i])
        return render_template('trigrama.html', metrica = metrics, test_set = test_dataset, test_size = len(test_dataset), dados = graphics_data, legenda = label)
"""