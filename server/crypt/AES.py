from Crypto.Cipher import AES
from Crypto.Util import Counter

def encrypt_file(file_path: str, key: bytes):
    """
    Encripta um arquivo usando AES no modo EAX.

    Args:
        file_path (str): Caminho do arquivo a ser encriptado.
        key (bytes): Chave de encriptação AES (32 bytes).

    Returns:
        tuple: (ciphertext, nonce, tag)
    """

    # TODO: Esse counter a IA que gerou. O quê é isso?
    counter = Counter.new(128)
    cipher = AES.new(key, AES.MODE_EAX, counter=counter)
    nonce = cipher.nonce

    with open(file_path, "rb") as f:
        data = f.read()

    ciphertext, tag = cipher.encrypt_and_digest(data)

    return ciphertext, nonce, tag