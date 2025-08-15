from flask import Flask, render_template, request
from flask_socketio import SocketIO 
import sqlite3

app = Flask(__name__)
socketio = SocketIO(app)
app.config['banco_dados'] = 'models/teste.db'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fazer_pedido', methods=['POST', 'GET'])
def fazer_pedido():
    if request.method == 'POST':
        nome_prato = request.form.get('nome_prato')
        descricao = request.form.get('descricao')
        mesa = request.form.get('mesa')

        try:
            conexao = sqlite3.connect(app.config['banco_dados'])
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO tb_pratos (nome_prato, descricao, mesa) VALUES (?, ?, ?)", (nome_prato, descricao, mesa))
            conexao.commit()
            conexao.close()

            socketio.emit('atualizar_lista')
        except Exception as e:
            return render_template('erro.html', erro=f"Erro ao cadastrar: {str(e)}")

    return render_template('index.html')

@app.route('/ver_pedidos', methods=['GET'])
def ver_pedidos():
    try:
        conexao = sqlite3.connect(app.config['banco_dados'])
        conexao.row_factory = sqlite3.Row  
        cursor = conexao.cursor()
        
        cursor.execute("SELECT * FROM tb_pratos ORDER BY mesa ASC ")
        pedidos = cursor.fetchall()
        conexao.close()

        return render_template('ver_pedidos.html', pedidos=pedidos)
    except Exception as e:
        return render_template('erro.html', erro=f"Erro ao carregar pedidos: {str(e)}")

@app.route('/mesas', methods=['GET'])
def mesas():
    try:
        conexao = sqlite3.connect(app.config['banco_dados'])
        conexao.row_factory = sqlite3.Row  
        cursor = conexao.cursor()
        
        cursor.execute("SELECT * FROM tb_mesa")
        pedidos = cursor.fetchall()
        conexao.close()
    except Exception as e:
        return render_template('mesas.html', mesas=mesas)
    
    
app.run("127.0.0.1", port=80, debug=True)
