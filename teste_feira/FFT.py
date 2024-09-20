from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Configuração do MongoDB
client = MongoClient("mongodb+srv://Robertin:Teste123456@cluster0.aktpx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['testefeira']
collection = db['respostas']

# Perguntas do questionário
perguntas = [
    {"pergunta": "Eu gosto de resolver problemas lógicos e matemáticos."},  # q1
    {"pergunta": "Prefiro atividades que envolvem criatividade e inovação."},  # q2
    {"pergunta": "Trabalhar em equipe é essencial para mim."},  # q3
    {"pergunta": "Gosto de atividades que envolvem contato direto com outras pessoas."},  # q4
    {"pergunta": "Eu me sinto motivado(a) quando estou ajudando outras pessoas."},  # q5
    {"pergunta": "Prefiro trabalhar com dados e análises do que com criação artística."},  # q6
    {"pergunta": "Tenho interesse por questões relacionadas à tecnologia e programação."},  # q7
    {"pergunta": "Eu gosto de entender como o corpo humano funciona e estudar biologia."},  # q8
    {"pergunta": "Eu me vejo trabalhando em projetos que causam impacto na sociedade."},  # q9
    {"pergunta": "A criatividade é uma parte essencial do meu dia a dia."},  # q10
    {"pergunta": "Prefiro trabalhar com questões práticas e reais em vez de teorias abstratas."},  # q11
    {"pergunta": "Eu gosto de planejar e organizar tarefas ou eventos."},  # q12
    {"pergunta": "Sinto-me atraído(a) por assuntos relacionados a leis e justiça."},  # q13
    {"pergunta": "Prefiro trabalhar em ambientes que exigem precisão e atenção aos detalhes."},  # q14
    {"pergunta": "Eu me interesso por política, história e como a sociedade funciona."},  # q15
    {"pergunta": "Tenho facilidade em aprender e aplicar conhecimentos científicos."},  # q16
    {"pergunta": "Sinto que sou mais produtivo(a) quando trabalho de forma independente."},  # q17
    {"pergunta": "Eu prefiro desafios intelectuais a tarefas físicas."},  # q18
    {"pergunta": "Tenho interesse por explorar novas culturas e línguas."},  # q19
    {"pergunta": "Eu gosto de criar ou desenhar novas ideias, produtos ou espaços."}  # q20
]

# Nichos de faculdades e as perguntas relacionadas
nichos_faculdades = {
    "Tecnologia e Matemática": {
        "perguntas": ['q1', 'q6', 'q7', 'q11', 'q14'],
        "faculdades": ["Engenharia", "Ciência da Computação", "Matemática", "Estatística", "Sistemas de Informação"]
    },
    "Criatividade e Artes": {
        "perguntas": ['q2', 'q10', 'q20'],
        "faculdades": ["Design Gráfico", "Artes Visuais", "Arquitetura", "Moda", "Cinema e Audiovisual", "Publicidade"]
    },
    "Humanas e Sociais": {
        "perguntas": ['q4', 'q5', 'q9', 'q13', 'q15', 'q19'],
        "faculdades": ["Direito", "Ciências Sociais", "Relações Internacionais", "História", "Sociologia", "Psicologia"]
    },
    "Saúde e Biologia": {
        "perguntas": ['q8', 'q9', 'q16'],
        "faculdades": ["Medicina", "Enfermagem", "Nutrição", "Fisioterapia", "Educação Física"]
    },
    "Administração e Negócios": {
        "perguntas": ['q3', 'q12', 'q17'],
        "faculdades": ["Administração", "Ciências Contábeis", "Economia", "Marketing", "Gestão de Projetos"]
    },
    "Engenharia e Construção": {
        "perguntas": ['q1', 'q11', 'q14', 'q16'],
        "faculdades": ["Engenharia Civil", "Engenharia Mecânica", "Engenharia de Produção", "Arquitetura"]
    },
    "Comunicação e Mídias": {
        "perguntas": ['q2', 'q4', 'q9', 'q10', 'q19'],
        "faculdades": ["Jornalismo", "Publicidade", "Comunicação Social", "Relações Públicas"]
    },
    "Pesquisa e Ciências Exatas": {
        "perguntas": ['q1', 'q16', 'q18'],
        "faculdades": ["Física", "Química", "Astronomia", "Geofísica", "Ciências Atuariais"]
    }
}

# Rota principal para exibir o questionário
@app.route('/')
def index():
    return render_template('index.html', perguntas=perguntas)

# Rota para salvar respostas e determinar a área
@app.route('/responder', methods=['POST'])
def responder():
    try:
        # Coletar as respostas do formulário, incluindo o nome do usuário
        respostas = request.form.to_dict(flat=True)
        nome = respostas.pop("nome")  # Remover o nome das respostas

        perfil = determinar_perfil(respostas)

        # Salvar o nome do usuário e o perfil sugerido no MongoDB
        collection.insert_one({"nome": nome, "perfil": perfil})

        return jsonify({"perfil_sugerido": perfil})
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

# Função para determinar o perfil com base nas respostas
def determinar_perfil(respostas):
    perfil_pontuacao = {nicho: 0 for nicho in nichos_faculdades}
    
    # Analisar as respostas e somar as pontuações de cada nicho
    for idx, valor in respostas.items():
        try:
            valor = int(valor)  # Transformar a resposta em inteiro (1-5)
        except ValueError:
            raise ValueError(f"Valor inválido para a pergunta {idx}: {valor}")
        
        for nicho, dados in nichos_faculdades.items():
            if idx in dados["perguntas"]:
                perfil_pontuacao[nicho] += valor

    # Determinar o nicho com maior pontuação
    nicho_sugerido = max(perfil_pontuacao, key=perfil_pontuacao.get)
    faculdades_sugeridas = nichos_faculdades[nicho_sugerido]["faculdades"]
    return {"nicho": nicho_sugerido, "faculdades": faculdades_sugeridas}

if __name__ == '__main__':
    app.run(debug=True)
