from flask import Flask, request
import flask
from flask_sqlalchemy import SQLAlchemy
from Crypto.Cipher import AES
import base64
import jwt
from flask import jsonify

from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)

exemplo = os.getenv('exemplo')

app = Flask(__name__)
key = b"zBVv#36y-AusKVQ6YnfG_NnZ"
cipher = AES.new(key, AES.MODE_EAX)
nonce = cipher.nonce

game_enc = open("fakegame.exe", "rb")
game_code = game_enc.read()
ciphertext, tag = cipher.encrypt_and_digest(game_code)
print("Game encriptado!")

# TODO: Substituir com a nova função para ver se funciona o encriptar.

with open("fakegame_enc.exe", "wb") as game_dec:
	game_dec.write(ciphertext)
	print("Game encriptado salvo como \"fakegame_enc.exe\"")

def game_decrypt(data, key, nonce):
	cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
	plaintext = cipher.decrypt(data)
	return plaintext

@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        data = base64.urlsafe_b64decode(request.form.get('game'))
        game_dec = game_decrypt(data, key, nonce)

        return base64.urlsafe_b64encode(game_dec)

    return "Apenas requisições POST são aceitas"

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db" # TODO: Padronizar para virar variável de ambiente.
db = SQLAlchemy(app)

# TODO: Ainda tentando fazer funcionar a autenticação.

@app.route("/api/authenticate", methods=["POST"])
def authenticate():
    username = request.json["username"]
    password = request.json["password"]

    user = Users.query.filter_by(username=username).first()
    if user is None or user.password != password:
        return jsonify({"error": "Usuário ou senha inválidos."}), 401

    token = jwt.encode({"username": username}, app.config["SECRET_KEY"], algorithm="HS256")
    return jsonify({"token": token})

if __name__ == '__main__':
    app.run(debug=True)