from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_marshmallow import Marshmallow


app = Flask(__name__)
db = SQLAlchemy()
ma = Marshmallow()

mysql = MySQL(app)

class livros(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(30), nullable=False)
    autor = db.Column(db.String(30), nullable=False)
    editora = db.Column(db.String(15), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)

    def __init__(self, nome, autor, editora, preco, categoria) -> None:
        self.nome = nome
        self.autor = autor
        self.editora = editora
        self.preco = preco
        self.categoria = categoria

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/livros'
db.init_app(app)
with app.app_context():
    db.create_all()

# @app.route('/livros', methods['GET'])
# def mostra_livros():
#     db.session.update()

@app.route('/livros/adicionar', methods=['POST'])
def adicionar_livro():
    _json = request.json
    nome = _json['nome']
    autor = _json['autor']
    editora = _json['editora']
    preco = _json['preco']
    categoria = _json['categoria']
    novo_livro = livros(nome,autor,editora,preco,categoria)
    db.session.add(novo_livro)
    db.session.commit()
    return jsonify({'Message': 'Livro Cadastrado Com Sucesso'})


if __name__ == '__main__':
    app.run(debug=True)