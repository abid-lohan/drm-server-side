import base64

from Crypto.Cipher import AES

def game_decrypt(data, key, nonce):
	cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
	plaintext = cipher.decrypt(data)
	return plaintext

key = b"zBVv#36y-AusKVQ6YnfG_NnZ"
cipher = AES.new(key, AES.MODE_EAX)
nonce = cipher.nonce
game_enc = open("snake_enc", "rb")
game_code = game_enc.read()

# Envia POST
send_data = {'game': base64.b64encode(game_code)}

game_dec = game_decrypt(base64.b64encode(game_code), key, nonce)

# Salva arquivo (todo: mudar isso depois para executar diretamente)
with open("snake_dec", "wb") as game_rcv:
    game_rcv.write(game_code)