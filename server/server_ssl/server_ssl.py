# TODO: Auto-gerado. Nem testei ainda.

import flask
from flask_sslify import SSLify

app = flask.Flask(__name__)
app.config["SSL_CERTFILE"] = "cert.pem"
app.config["SSL_KEYFILE"] = "key.pem"

SSLify(app)

@app.route("/")
def index():
    return "Hello, world!"

if __name__ == "__main__":
    app.run(debug=True)