import requests

# TODO: Finalizar o login.

def authenticate(username, password):
    url = "https://example.com/api/authenticate"
    data = {"username": username, "password": password}
    response = requests.post(url, data=data, verify=True)
    if response.status_code == 200:
        return response.json()["token"]
    else:
        return None

token = authenticate("username", "password")
if token is not None:
    print("Usuário autenticado com sucesso.")
else:
    print("Falha na autenticação.")