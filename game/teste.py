import base64

from Crypto.Cipher import AES

def game_decrypt(data, key, nonce):
	cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
	plaintext = cipher.decrypt(data)
	return plaintext

key = b"zBVv#36y-AusKVQ6YnfG_NnZ"
cipher = AES.new(key, AES.MODE_EAX)
nonce = cipher.nonce

game_enc = open("fakegame.exe", "rb")
game_code = game_enc.read()
ciphertext, tag = cipher.encrypt_and_digest(game_code)

send_data = {'game': base64.b64encode(game_code)}
response = requests.post("http://127.0.0.1:5000", data=send_data)
game_code = base64.urlsafe_b64decode(response.text)

data = base64.urlsafe_b64decode(request.form.get('game'))
game_dec = game_decrypt(data, key, nonce)
return base64.urlsafe_b64encode(game_dec)


game_enc = open("fakegame.exe", "rb")
game_code = game_enc.read()

# Envia POST
send_data = {'game': base64.b64encode(game_code)}

game_dec = game_decrypt(base64.urlsafe_b64decode(base64.b64encode(game_code)), key, nonce)

# Salva arquivo
with open("fakegame.exe", "wb") as game_rcv:
    game_rcv.write(game_code)