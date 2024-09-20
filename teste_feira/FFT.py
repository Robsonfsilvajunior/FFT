from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "chave_secreta"  


def utility_processor():
    return dict(enumerate=enumerate)

# Conectar ao banco de dados MongoDB
def conectar_db():
    client = MongoClient("mongodb+srv://Robertin:Teste123456@cluster0.aktpx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client['testefeira']
    return db


@app.rorte('/questionario', methods=['GET', 'POST'])
def questionario():
    if request.method == 'POST':
    
        respostas = {
            'problemas_logicos': int(request.form['problemas_logicos']),
            'criatividade_inovacao': int(request.form['criatividade_inovacao']),
            'trabalho_equipe': int(request.form['trabalho_equipe']),
            'contato_pessoas': int(request.form['contato_pessoas']),
            'ajudar_pessoas': int(request.form['ajudar_pessoas']),
            'dados_analises': int(request.form['dados_analises']),
            'tecnologia_programacao': int(request.form['tecnologia_programacao']),
            'biologia_corpo_humano': int(request.form['biologia_corpo_humano']),
            'impacto_sociedade': int(request.form['impacto_sociedade']),
            'criatividade_diaria': int(request.form['criatividade_diaria']),
            'questoes_praticas': int(request.form['questoes_praticas']),
            'planejamento_organizacao': int(request.form['planejamento_organizacao']),
            'leis_justica': int(request.form['leis_justica']),
            'precisao_detalhes': int(request.form['precisao_detalhes']),
            'interesse_politica': int(request.form['interesse_politica']),
            'facilidade_cientifica': int(request.form['facilidade_cientifica']),
            'trabalho_independente': int(request.form['trabalho_independente']),
            'desafios_intelectuais': int(request.form['desafios_intelectuais']),
            'explorar_culturas': int(request.form['explorar_culturas']),
            'criar_ideias_produtos': int(request.form['criar_ideias_produtos']),
        }

        # Conectar ao banco e armazenar as respostas
        db = conectar_db()
        db.respostas.insert_one(respostas)

        # Chamar função para sugerir faculdades
        faculdades_sugeridas = sugerir_faculdades(respostas)

        flash("Questionário enviado com sucesso!")
        return render_template('resultados.html', faculdades=faculdades_sugeridas)
    
    return render_template('questionario.html')

# Função para sugerir faculdades com base nas respostas
def sugerir_faculdades(respostas):
    faculdades = []

    # Perfis de Lógica, Matemática e Tecnologia
    if respostas['problemas_logicos'] >= 4 or respostas['tecnologia_programacao'] >= 4 or respostas['dados_analises'] >= 4:
        faculdades += ['Engenharia', 'Ciência da Computação', 'Matemática', 'Estatística']

    # Perfis Criativos e Artísticos
    if respostas['criatividade_inovacao'] >= 4 or respostas['criatividade_diaria'] >= 4 or respostas['criar_ideias_produtos'] >= 4:
        faculdades += ['Design Gráfico', 'Artes Visuais', 'Arquitetura']

    # Perfis Humanistas e Sociais
    if respostas['contato_pessoas'] >= 4 or respostas['ajudar_pessoas'] >= 4 or respostas['leis_justica'] >= 4 or respostas['interesse_politica'] >= 4:
        faculdades += ['Direito', 'Ciências Sociais', 'Relações Internacionais', 'Psicologia']

    # Perfis de Saúde e Ciências Biológicas
    if respostas['biologia_corpo_humano'] >= 4 or respostas['impacto_sociedade'] >= 4 or respostas['facilidade_cientifica'] >= 4:
        faculdades += ['Medicina', 'Biomedicina', 'Enfermagem']

    # Perfis Administrativos e de Negócios
    if respostas['planejamento_organizacao'] >= 4 or respostas['trabalho_equipe'] >= 4:
        faculdades += ['Administração', 'Ciências Contábeis', 'Economia']

    # Perfis de Pesquisa e Ciências Exatas
    if respostas['desafios_intelectuais'] >= 4 or respostas['facilidade_cientifica'] >= 4:
        faculdades += ['Física', 'Química', 'Astronomia']

    # Perfis de Comunicação e Mídias
    if respostas['explorar_culturas'] >= 4 or respostas['contato_pessoas'] >= 4:
        faculdades += ['Jornalismo', 'Publicidade e Propaganda', 'Comunicação Social']

    return faculdades

# Rota para página inicial
@app.rorte('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
