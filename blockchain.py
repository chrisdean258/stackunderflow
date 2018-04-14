import hashlib
import json
from time import time

def hash(string):
    return hashlib.sha256(string).hexdigest()

class blockchain:
    blocksize = 1
    def __init__(self):
        self.blocks = blockchain.getBlocks()
        self.posts = []

    def add_post(self, sender, message, tags, ref=None):
        id_ = len(self.blocks) * blockchain.blocksize + len(self.posts)
        if ref is None:
            self.posts.append({ "id": id_, "sender": sender, "message": message, "tags": tags })
        else:
            self.posts.append({ "id": id_, "sender": sender, "message": message, "tags": tags, "ref": ref })
        if len(self.posts) == blockchain.blocksize:
            self.create_block()

    def create_block(self):
        self.blocks = blockchain.getBlocks()
        to_process = self.posts[:blockchain.blocksize]
        self.posts = self.posts[blockchain.blocksize:]
        self.blocks.append({
            "posts" : to_process,
            "timestamp" : time(),
            "previous" : hash(json.dumps(self.blocks[-1], sort_keys = True).encode("ascii"))
        })

    @staticmethod
    def getBlocks():
        blocks = None
        with open("ledger.json", "r") as f:
            blocks = json.loads(f.read())
        if len(blocks) == 0:
            blocks.append({
                "posts" : [],
                "timestamp": time(),
                "previous" : ""
            })
        return blocks

    def update_ledger(self):
        with open("ledger.json", "w") as f:
            f.write(json.dumps(self.blocks))
