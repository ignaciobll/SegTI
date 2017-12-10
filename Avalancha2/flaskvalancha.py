from flask import Flask
from xtea import *

app = Flask(__name__)


@app.route('/encrypt/<cipher_name>/<key>/<text>')
def encrypt(cipher_name, key, text):
    x = new(key, mode=MODE_OFB, IV="12345678")

    c = x.encrypt(text)

    return c


app.run()
