from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/perfil")
def perfil():
    return render_template("perfil.html")

print ("Servidor iniciado em http://127.0.0.1:5000/")


if __name__ == "__main__":
    app.run(debug=True)

