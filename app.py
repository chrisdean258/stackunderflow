from flask import *
from blockchain import blockchain
import os

app=Flask(__name__)

bc = blockchain()


@app.route("/")
def index():
    return "Welcome to Stackunderflow"

@app.route("/ledger")
def ledger():
    global bc
    bc.update_ledger()
    root_dir = os.getcwd()
    print(root_dir)
    return send_from_directory(root_dir, "ledger.json")

@app.route("/newpost", methods = ['POST'])
def newpost():
    global bc
    print(request.form)
    required_fields = [ "sender", "message", "tags" ]
    for field in required_fields:
        if field not in request.form:
            return ("not implemented", 400)

    bc.add_post(request.form["sender"], request.form["message"], request.form["tags"])
    print(bc.blocks)

    return "Not implemented"

@app.route("/respond", methods = ['POST'])
def respond():
    return "Not implemented"
