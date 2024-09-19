from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "chave_secreta"  # Necessária para exibir mensagens flash

# Função para conectar ao banco de dados
def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="testefeira"
    )

# Rota para cadastrar parceiro
@app.route('/cadastrar_parceiro', methods=['GET', 'POST'])
def cadastrar_parceiro():
    if request.method == 'POST':
        parceiro_nome = request.form['parceiro_nome']
        genero = request.form['genero']
        hobbies = request.form['hobbies']
        usuario_nome = request.form['usuario_nome']

        if parceiro_nome and genero and hobbies:
            conn = conectar_db()
            cursor = conn.cursor()
            query = "INSERT INTO Parceiro (nome, genero, hobbies) VALUES (%s, %s, %s)"
            cursor.execute(query, (parceiro_nome, genero, hobbies))
            parceiro_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()

            # Cadastro de usuário associado ao parceiro
            cadastrar_usuario(usuario_nome, parceiro_id, hobbies)
            flash(f"Parceiro cadastrado com sucesso! ID do parceiro: {parceiro_id}")
            return redirect(url_for('buscar_presente', hobbies=hobbies))
        else:
            flash("Por favor, preencha todas as informações do parceiro.")

    return render_template('cadastrar_parceiro.html')

# Função para cadastrar usuário
def cadastrar_usuario(usuario_nome, parceiro_id, hobbies):
    if usuario_nome:
        conn = conectar_db()
        cursor = conn.cursor()
        query = "INSERT INTO Usuario (nome, Parceiro_id) VALUES (%s, %s)"
        cursor.execute(query, (usuario_nome, parceiro_id))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Usuário cadastrado com sucesso!")
    else:
        flash("Por favor, insira o nome do usuário.")

# Rota para buscar presente com base nos hobbies
@app.route('/buscar_presente/<hobbies>')
def buscar_presente(hobbies):
    conn = conectar_db()
    cursor = conn.cursor()

    query = "SELECT categoria, resultados FROM Presente WHERE categoria = %s"
    cursor.execute(query, (hobbies,))
    presentes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('buscar_presente.html', presentes=presentes)

# Rota para cadastrar usuário (inicial)
@app.route('/', methods=['GET', 'POST'])
def cadastrar_usuario_window():
    if request.method == 'POST':
        usuario_nome = request.form['usuario_nome']
        return redirect(url_for('cadastrar_parceiro', usuario_nome=usuario_nome))
    
    return render_template('cadastrar_usuario.html')

if __name__ == '__main__':
    app.run(debug=True)