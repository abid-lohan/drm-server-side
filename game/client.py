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
import time

app = Flask(__name__)

class GameClient(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master.title("Cliente do Jogo")
        self.token = ""

        # Botão para iniciar o jogo
        self.start_button = tk.Button(self, text="Iniciar Jogo", command=self.start_game)
        self.start_button.pack(side="bottom", fill="x")

        # Botão para inserir a chave de licença
        self.license_button = tk.Button(self, text="Baixar Jogo", command=self.download_game)
        self.license_button.pack(side="bottom", fill="x")


        # Botão para inserir a chave de licença
        self.license_button = tk.Button(self, text="Autenticar", command=self.insert_auth)
        self.license_button.pack(side="bottom", fill="x")

        # Campo de entrada para a chave de licença
        self.username = tk.Entry(self)
        self.username.pack(side="bottom", fill="x")

        # Campo de entrada para a chave de licença
        self.password = tk.Entry(self)
        self.password.pack(side="bottom", fill="x")
        

    def start_game(self):
        if self.token == "":
            messagebox.showerror("Autenticação", f"Usuário não autenticado")
            return
        
        print("Iniciar jogo")
        game_enc = open("../server/snake_enc.exe", "rb")
        game_code = game_enc.read()

        send_data = {'game': base64.b64encode(game_code)}

        print("inserindo autenticacao")
        print(self.token)
        headers = {
            "Authorization": f"Bearer {self.token}",
        }

        start_time = time.time()
        
        response = requests.post("http://127.0.0.1:5000/api/decrypt", data=send_data, headers=headers)
        game_code = base64.urlsafe_b64decode(response.text)

        with open("snake_dec.exe", "wb") as game_rcv:
            game_rcv.write(game_code)

        game_enc.close()

        end_time = time.time()

        latency = end_time - start_time

        print(f"Latência: {latency}")

        os.system("snake_dec.exe")
        

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
            json_data = json.loads(token)
            self.token = json_data['token']
        elif response.status_code == 401:
            print("Usuário ou senha inválidos.")
            messagebox.showerror("Autenticação", "Usuário ou senha inválidos.")
        else:
            print("Erro inesperado.")
            messagebox.showerror("Autenticação", "Erro Inesperado.")
        print(response)

    def download_game(self):
        if self.token == "":
            messagebox.showerror("Autenticação", f"Usuário não autenticado")
            return

        headers = {
            "Authorization": f"Bearer {self.token}",
        }

        response = requests.post("http://127.0.0.1:5000/api/crypt", data=None, headers=headers)
        messagebox.showinfo("Download Completo", f"Download do jogo completo.")

        

if __name__ == "__main__":
    root = tk.Tk()
    game_client = GameClient(root)
    game_client.pack()
    root.mainloop()

# Lê os bytes criptografados


# game_enc.close()