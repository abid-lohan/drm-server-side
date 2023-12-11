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
import json
import time

dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)

app = flask.Flask(__name__)
engine = create_engine('sqlite:///development.db')
session = sessionmaker(bind=engine)()

SECRET_KEY = os.getenv("SECRET_KEY")
AES_KEY = os.getenv("AES_KEY")

key = b"zBVv#36y-AusKVQ6YnfG_NnZ"
cipher = AES.new(key, AES.MODE_EAX)
nonce = cipher.nonce

def game_decrypt(data, key, nonce):
	cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
	plaintext = cipher.decrypt(data)
	return plaintext

@app.route('/api/crypt', methods=['POST'])
def crypt():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Usuário deve se autenticar."}), 401
    try:
        token_value = token[7:]
        payload = jwt.decode(token_value, SECRET_KEY, algorithms=["HS256"])
        # username = payload['username']

        start_time = time.time()

        game_enc = open("../game/dist/snake.exe", "rb")
        game_code = game_enc.read()
        ciphertext, tag = cipher.encrypt_and_digest(game_code)

        with open("snake_enc.exe", "wb") as game_dec:
            game_dec.write(ciphertext)
            print("Game encriptado salvo como \"snake_enc.exe\"")

        end_time = time.time()

        crypt_time = end_time - start_time

        print(f"Tempo Criptografando: {crypt_time}")

        return jsonify({"Success": "Jogo disponível para download."}), 200
    except Exception:
        return jsonify({"Error": "Erro Inesperado."}), 500

@app.route('/api/decrypt', methods=['POST'])
def decrypt():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"Error": "Usuário deve se autenticar."}), 401
    try:
        token_value = token[7:]
        payload = jwt.decode(token_value, SECRET_KEY, algorithms=["HS256"])
        # username = payload['username']
        data = base64.urlsafe_b64decode(request.form.get('game'))

        start_time = time.time()

        game_dec = game_decrypt(data, key, nonce)

        end_time = time.time()

        decrypt_time = end_time - start_time

        print(f"Tempo Descriptografando: {decrypt_time}")

        return base64.urlsafe_b64encode(game_dec)
    except Exception:
        # O token é inválido
        return jsonify({"Error": "Autenticação inválida."}), 401

@app.route("/api/authenticate", methods=["POST"])
def authenticate():
    data = request.data
    json_data = json.loads(data)
    username = json_data["username"]
    password = json_data["password"]
    user = session.query(Users).filter_by(username=username).first()
    if user is None or user.password != password:
        return jsonify({"Error": "Usuário ou senha inválidos."}), 401

    token = jwt.encode({"username": username}, SECRET_KEY, algorithm="HS256")
    return jsonify({"token": token})

if __name__ == '__main__':
    app.run(debug=True)