#!/usr/bin/env python3
import requests
import sys
import json

url="http://0.0.0.0"
ledgerfile = "ledger.json"
blocks = []
#request = requests.post(url + "/post", data = { "message" : "hi\n{\ntest\n}", "tags": "tags", "sender":"from" , "ref":14})
def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def post():
    title = input("Title: ")
    tags = input("Tags: ")
    from_ = input("Signature: ")
    line = ""
    segments = []
    while line.strip().lower() != "done":
        segments.append(line.rstrip())
        line = input()
    segments = segments[1:]
    message = "\n".join(segments)
    request = requests.post(url + "/post", data = { "message" : message, "tags":tags, "sender": from_ , "title":title})
    print(request.text)

def reply():
    ref = input("Replying to: ")
    while not RepresentsInt(ref):
       print("Replying to must be an int")
       ref = input("Replying to: ")
    from_ = input("Signature: ")
    line = ""
    segments = []
    while line.strip().lower() != "done":
        segments.append(line.strip())
        line = input()
    segments = segments[1:]
    message = "\n".join(segments)
    request = requests.post(url + "/post", data = { "message" : message, "sender": from_ , "ref":ref})
    print(request.text)

def print_post(postnum, indent=""):
    global blocks
    for block in blocks:
        for post in block["posts"]:
            if str(postnum) == str(post["id"]):
                if "title" in post:
                    print(indent + "%d. %s" % (post["id"], post["title"]), end = "\n" + indent + "\t")
                else:
                    print(indent + str(post["id"]) + ". ", end = "")
                print("By: " + post["sender"])
                if "tags" in post:
                    print(indent + "\t" + "Tags: " + post["tags"])
                print(indent + "\t" + ("\n\t"+indent).join(post["message"].split("\n")))
                print()
            elif "ref" in post and post["ref"] == str(postnum):
                print_post(post["id"], indent+"\t")


def search_posts(string):
    global blocks
    for block in blocks:
        for post in block["posts"]:
            if "title" in post:
                print("%s. %s" % (post["id"], post["title"]))

def update():
    request = requests.get(url + "/ledger")
    with open(ledgerfile, "w") as f:
        f.write(request.text)
    blocks = json.loads(request.text)

def list_():
    global blocks
    for block in blocks:
        for post in block["posts"]:
            if "title" in post:
                print("%s. %s" % (post["id"], post["title"]))



def parse_and_execute(string):
    commands = {
        "update": update,
        "post": post,
        "reply": reply,
        "list": list_
    }

    if string.strip().lower() in commands:
        commands[string.strip().lower()]()

    elif RepresentsInt(string.strip()):
        print_post(int(string))
    else:
        search_posts(string)


def main():
    global blocks
    try:
        with open(ledgerfile, "r") as f:
            blocks = json.loads(f.read())
    except:
        update()

    if len(sys.argv) != 1:
        parse_and_execute(" ".join(sys.argv[1:]))
    else:
        #try:
            ip = input("Input a command or search query: ")
            while ip != "quit" and ip != "exit":
                parse_and_execute(ip)
                ip = input("Input a command or search query: ")
        #except:
            #return
main()



#print(request.text)
