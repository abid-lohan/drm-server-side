import base64
import jwt
import flask
import os
from flask import Flask, request
from Crypto.Cipher import AES
from flask import jsonify
from flask_jwt_extended import JWTManager, get_jwt_identity
from dotenv import load_dotenv
from pathlib import Path
from model.Users import Users
from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)

# Setup (TODO: Passar para outro arquivo depois)
app = flask.Flask(__name__)
engine = create_engine('sqlite:///development.db')
session = sessionmaker(bind=engine)()

SECRET_KEY = os.getenv("SECRET_KEY")
AES_KEY = os.getenv("AES_KEY")

print(SECRET_KEY)

key = b"zBVv#36y-AusKVQ6YnfG_NnZ"
cipher = AES.new(key, AES.MODE_EAX)
nonce = cipher.nonce

# game_enc = open("fakegame.exe", "rb")
# game_code = game_enc.read()
# ciphertext, tag = cipher.encrypt_and_digest(game_code)
# print("Game encriptado!")

# TODO: Substituir com a nova função para ver se funciona o encriptar.

# with open("fakegame_enc.exe", "wb") as game_dec:
# 	game_dec.write(ciphertext)
# 	print("Game encriptado salvo como \"fakegame_enc.exe\"")

def game_decrypt(data, key, nonce):
	cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
	plaintext = cipher.decrypt(data)
	return plaintext

@app.route('/api/crypt', methods=['POST'])
def index():
    if request.method == 'POST':
        data = base64.urlsafe_b64decode(request.form.get('game'))
        game_dec = game_decrypt(data, key, nonce)

        return base64.urlsafe_b64encode(game_dec)

    return "Apenas requisições POST são aceitas"


@app.route('/api', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Usuário deve se autenticar."}), 401

    try:
        token_value = token[7:]
        payload = jwt.decode(token_value, SECRET_KEY, algorithms=["HS256"])
        username = payload['username']



        return jsonify({"Success": f"Usuário {username} autenticado."}), 200
    except Exception:
        # O token é inválido
        return jsonify({"error": "Autenticação inválida."}), 401

@app.route("/api/authenticate", methods=["POST"])
def authenticate():
    username = request.json["username"]
    password = request.json["password"]
    user = session.query(Users).filter_by(username=username).first()
    if user is None or user.password != password:
        return jsonify({"error": "Usuário ou senha inválidos."}), 401

    token = jwt.encode({"username": username}, SECRET_KEY, algorithm="HS256")
    return jsonify({"token": token})

if __name__ == '__main__':
    app.run(debug=True)