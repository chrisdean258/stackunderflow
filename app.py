from flask import *
import hashlib
import os

app=Flask(__name__)

def hash(string):
    return hashlib.sha256(string).hexdigest()


@app.route("/")
def index():
    return "Welcome to Stackunderflow"

@app.route("/ledger")
def ledger():
    root_dir = os.getcwd()
    print(root_dir)
    return send_from_directory(root_dir, "ledger.json")
