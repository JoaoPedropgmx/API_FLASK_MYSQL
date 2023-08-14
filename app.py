from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_marshmallow import Marshmallow


app = Flask(__name__)
db = SQLAlchemy()
ma = Marshmallow()

mysql = MySQL(app)

class Livros(db.Model):
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


class livroSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nome', 'autor', 'editora', 'preco', 'categoria')


livro_Schema = livroSchema()
livros_Schema = livroSchema(many=True)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/livros'
app.config['JSON_SORT_KEYS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/livros', methods=['GET'])
def mostra_livros():
    livros = []
    data = Livros.query.all()
    livros = livros_Schema.dump(data)
    return jsonify(livros)


@app.route('/livros', methods=['POST'])
def adicionar_livro():
    _json = request.json
    nome = _json['nome']
    autor = _json['autor']
    editora = _json['editora']
    preco = _json['preco']
    categoria = _json['categoria']
    novo_livro = Livros(nome=nome,autor=autor,editora=editora,preco=preco,categoria=categoria)
    db.session.add(novo_livro)
    db.session.commit()
    return jsonify({'Message': 'Livro Cadastrado Com Sucesso'})


@app.route('/livros/<id>', methods=['GET'])
def mostra_livro_porid(id):
    if str.isdigit(id) == False:
        return jsonify({'message': 'O id do livro não pode ser uma string'})
    data = []
    livro = Livros.query.get(id)
    if not livro:
        return jsonify({'message': 'Livro Não encontrado'})
    data = livro_Schema.dump(livro)
    return jsonify(data)

@app.route('/livros/<id>', methods=['DELETE'])
def deleta_livro_porid(id):
    if str.isdigit(id) == False:
        return jsonify({'message': 'O id do livro não pode ser uma string'})
    livro = Livros.query.get(id)
    if not livro:
        return jsonify({'message': 'Livro Não encontrado'})
    db.session.delete(livro)
    db.session.commit()
    return jsonify({'message': 'Livro deletado com sucesso'})


if __name__ == '__main__':
    app.run(debug=True)