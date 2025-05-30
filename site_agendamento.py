
from flask import Flask, render_template_string, request, redirect, url_for
from datetime import datetime, timedelta, date

app = Flask(__name__)

# Dados simulados na memória
agendamentos = []
senha_manicure = "unhas123"

# Horário de atendimento: 07:00 às 20:00 (de hora em hora)
horarios_disponiveis = [(datetime(2025, 1, 1, 7) + timedelta(hours=i)).strftime('%H:%M') for i in range(14)]

template = """
<!doctype html>
<html lang='pt-br'>
<head>
  <meta charset='UTF-8'>
  <title>Agenda da Manicure</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-image: url('https://i.imgur.com/yxPYCrx.jpg');
      background-size: cover;
      background-repeat: no-repeat;
      background-attachment: fixed;
      padding: 20px;
      color: #fff;
    }
    h1, h2 {
      background-color: rgba(0, 0, 0, 0.5);
      padding: 10px;
      border-radius: 8px;
    }
    form {
      background-color: rgba(0, 0, 0, 0.6);
      padding: 15px;
      margin-bottom: 20px;
      border-radius: 8px;
    }
    input, select, button {
      margin: 5px;
      padding: 8px;
      border-radius: 5px;
      border: none;
    }
    ul {
      background-color: rgba(255, 255, 255, 0.2);
      padding: 10px;
      border-radius: 8px;
      list-style-type: none;
    }
    li {
      margin-bottom: 5px;
    }
    button {
      background-color: #ff69b4;
      color: white;
      font-weight: bold;
      cursor: pointer;
    }
    button:hover {
      background-color: #e754a3;
    }
  </style>
</head>
<body>
  <h1>Agendamento de Horários</h1>
  <p>Funcionamento: Terça a Domingo, 07:00 às 20:00</p>

  <form method='POST' action='/agendar'>
    Nome: <input name='nome' required>
    Data: <input type='date' name='data' min='{{ data_hoje }}' required>
    Horário:
    <select name='hora'>
      {% for hora in horas %}
        <option value='{{ hora }}'>{{ hora }}</option>
      {% endfor %}
    </select>
    <button type='submit'>Agendar</button>
  </form>

  <h2>Horários Agendados</h2>
  <ul>
  {% for ag in agendamentos %}
    <li>{{ ag['data'] }} - {{ ag['hora'] }}</li>
  {% endfor %}
  </ul>

  <h2>Cancelar Agendamento (Somente Manicure)</h2>
  <form method='POST' action='/deletar'>
    Data: <input name='data' required>
    Hora: <input name='hora' required>
    Senha: <input type='password' name='senha' required>
    <button type='submit'>Deletar</button>
  </form>

  <h2>Agenda Completa (Somente Manicure)</h2>
  <form method='POST' action='/veragenda'>
    Senha: <input type='password' name='senha' required>
    <button type='submit'>Ver Agenda Completa</button>
  </form>
</body>
</html>
"""

agenda_template = """
<h2>Agenda Completa</h2>
<ul>
{% for ag in agendamentos %}
  <li>{{ ag['data'] }} - {{ ag['hora'] }} | Cliente: {{ ag['nome'] }}</li>
{% endfor %}
</ul>
<a href='/'>Voltar</a>
"""

@app.route("/")
def index():
    return render_template_string(template, 
        agendamentos=agendamentos, 
        horas=horarios_disponiveis,
        data_hoje=date.today().isoformat())

@app.route("/agendar", methods=["POST"])
def agendar():
    nome = request.form['nome']
    data = request.form['data']
    hora = request.form['hora']

    if data < date.today().isoformat():
        return "<h3>Não é possível agendar para datas passadas!</h3><a href='/'>Voltar</a>"

    for ag in agendamentos:
        if ag['data'] == data and ag['hora'] == hora:
            return "<h3>Horário já agendado!</h3><a href='/'>Voltar</a>"

    agendamentos.append({"nome": nome, "data": data, "hora": hora})
    return redirect(url_for('index'))

@app.route("/deletar", methods=["POST"])
def deletar():
    data = request.form['data']
    hora = request.form['hora']
    senha = request.form['senha']

    if senha != senha_manicure:
        return "<h3>Senha incorreta!</h3><a href='/'>Voltar</a>"

    global agendamentos
    agendamentos = [ag for ag in agendamentos if not (ag['data'] == data and ag['hora'] == hora)]
    return redirect(url_for('index'))

@app.route("/veragenda", methods=["POST"])
def ver_agenda():
    senha = request.form['senha']
    if senha != senha_manicure:
        return "<h3>Senha incorreta!</h3><a href='/'>Voltar</a>"
    return render_template_string(agenda_template, agendamentos=agendamentos)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

