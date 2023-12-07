import tkinter
import requests
import base64
from flask import Flask, request
from Crypto.Cipher import AES
import base64
import tkinter as tk
from tkinter import messagebox
import json
import os

app = Flask(__name__)
key = b"zBVv#36y-AusKVQ6YnfG_NnZ"
cipher = AES.new(key, AES.MODE_EAX)
nonce = cipher.nonce

game_enc = open("dist/snake", "rb")
game_code = game_enc.read()
ciphertext, tag = cipher.encrypt_and_digest(game_code)
print("Game encriptado!")

with open("snake_enc", "wb") as game_dec:
	game_dec.write(ciphertext)
	print("Game encriptado salvo como \"snake_enc\"")

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

class GameClient(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master.title("Cliente do Jogo")
        self.token = ""

        # Botão para iniciar o jogo
        self.start_button = tk.Button(self, text="Iniciar Jogo", command=self.start_game)
        self.start_button.pack(side="bottom", fill="x")

        # Botão para inserir a chave de licença
        self.license_button = tk.Button(self, text="Autenticar", command=self.insert_auth)
        self.license_button.pack(side="bottom", fill="x")

        # Campo de entrada para a chave de licença
        self.username = tk.Entry(self)
        self.username.pack(side="bottom", fill="x")

        # Campo de entrada para a chave de licença
        self.password = tk.Entry(self)
        self.password.pack(side="bottom", fill="x")

        # Botão para inserir a chave de licença
        self.license_button = tk.Button(self, text="Inserir Licença", command=self.insert_license)
        self.license_button.pack(side="bottom", fill="x")

        # Campo de entrada para a chave de licença
        self.license_entry = tk.Entry(self)
        self.license_entry.pack(side="bottom", fill="x")

    def start_game(self):
        print("Iniciar jogo")
        if self.token == "":
            messagebox.showinfo("Autenticação", f"Usuário não autenticado")
        else:
            print("Usuário ou senha inválidos.")

    def insert_auth(self):
        username = self.username.get()
        password = self.password.get()

        # Envia POST
        send_data = {"username": username, "password": password}
        send_data = json.dumps(send_data)
        print(json.loads(send_data))
        response = requests.post("http://127.0.0.1:5000/api/authenticate", data=send_data)
        if response.status_code == 200:
            token = response.content
            print("Token de autenticação:", token)
            messagebox.showinfo("Autenticação", f"Token de autenticação: {token}")
        elif response.status_code == 401:
            print("Usuário ou senha inválidos.")
        else:
            print("Erro inesperado.")
        print(response)

    def insert_license(self):
        license = self.license_entry.get()
        game_enc = open("snake_enc", "rb")
        game_code = game_enc.read()

        headers = {
            "Authorization": f"Bearer {self.token}",
        }

        # Envia POST
        send_data = {'game': base64.b64encode(game_code)}
        response = requests.post(
            "http://127.0.0.1:5000/api/decrypt", data=send_data, headers=headers
        )
        game_code = base64.urlsafe_b64decode(response.text)

        # Salva arquivo (todo: mudar isso depois para executar diretamente)
        with open("snake_dec", "wb") as game_rcv:
            game_rcv.write(game_code)

        os.system("./snake_dec")

        # Verifica se a chave de ativação está vazia
        if license == "":
            messagebox.showinfo("Erro", "Chave de ativação inválida. Não é possível iniciar o jogo.")

        # Verifica se a chave de ativação é válida
        elif license == "1234567890":
            # Inicia o jogo
            print("Licença válida. Você pode agora iniciar o jogo...")
        else:
            # Mostra que não pode iniciar o jogo
            messagebox.showinfo("Erro", "Chave de ativação inválida. Não é possível iniciar o jogo.")
        print("Licença:", license)

if __name__ == "__main__":
    root = tk.Tk()
    game_client = GameClient(root)
    game_client.pack()
    root.mainloop()

# Lê os bytes criptografados


# game_enc.close()