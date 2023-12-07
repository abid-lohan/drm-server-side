import requests
import base64
from flask import Flask, request
from Crypto.Cipher import AES
import base64

app = Flask(__name__)
key = b"zBVv#36y-AusKVQ6YnfG_NnZ"
cipher = AES.new(key, AES.MODE_EAX)
nonce = cipher.nonce

game_enc = open("fakegame.exe", "rb")
game_code = game_enc.read()
ciphertext, tag = cipher.encrypt_and_digest(game_code)
print("Game encriptado!")

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
    
if __name__ == '__main__':
    app.run(debug=True)

# Lê os bytes criptografados
game_enc = open("fakegame_enc.exe", "rb")
game_code = game_enc.read()

# Envia POST
send_data = {'game': base64.b64encode(game_code)}
response = requests.post("http://127.0.0.1:5000", data=send_data)
game_code = base64.urlsafe_b64decode(response.text)

# Salva arquivo (todo: mudar isso depois para executar diretamente)
with open("test.exe", "wb") as game_rcv:
	game_rcv.write(game_code)

game_enc.close()