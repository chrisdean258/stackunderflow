from flask import *
from blockchain import blockchain
import os

app=Flask(__name__)

bc = blockchain("http://stackunderflow.net")


@app.route("/", methods=["GET"])
def index():
    root_dir = os.getcwd()
    return send_from_directory(root_dir, "index.html")

@app.route("/ledger", methods=["GET"])
def ledger():
    global bc
    bc.write_ledger()
    root_dir = os.getcwd()
    return send_from_directory(root_dir, "ledger.json")

@app.route("/post", methods = ['POST'])
def post():
    global bc
    required_fields = [ "sender", "message" ]
    for field in required_fields:
        if field not in request.form:
            return ("Needs: sender, message, tags, ref or title", 400)

    if not ("title" in request.form and "tags" in request.form) and "ref" not in request.form:
        return ("Needs: sender, message, ref or title and tags", 400)

    if "title" in request.form:
        bc.add_post(request.form["sender"], request.form["message"], request.form["tags"], title=request.form["title"])

    if "ref" in request.form:
        bc.add_post(request.form["sender"], request.form["message"], ref=request.form["ref"])

    return ("", 204)

@app.route("/register", methods = ['POST'])
def respond():
    global bc
    if "url" not in request.form:
        return ("No url found to register", 400)
    bc.register(self.form["url"])


@app.route("/length", methods = ['GET'])
def length():
    global bc
    return str(bc.length())

@app.route("/su.png")
def pic():
    root_dir = os.getcwd()
    return send_from_directory(root_dir, "su.png")
