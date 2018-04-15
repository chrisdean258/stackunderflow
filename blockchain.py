import hashlib
import json
from time import time

def hash(string):
    return hashlib.sha256(string).hexdigest()

class blockchain:
    blocksize = 1
    def __init__(self, url):
        self.url = url
        self.blocks = []
        self.network = set([])
        self.posts = []
        self.update_ledger()

    def add_post(self, sender, message, tags=None, ref=None, title=None):
        if ref is None:
            self.posts.append({ "title" : title, "sender": sender, "message": message, "tags": tags })
        else:
            self.posts.append({ "sender": sender, "message": message, "ref": ref })
        if len(self.posts) == blockchain.blocksize:
            self.create_block()

    def create_block(self):
        to_process = self.posts[:blockchain.blocksize]
        self.posts = self.posts[blockchain.blocksize:]
        self.update_ledger()
        for i,post in enumerate(to_process):
            post["id"] = i + len(self.blocks) * blockchain.blocksize
        self.blocks.append({
            "posts" : to_process,
            "timestamp" : time(),
            "previous" : hash(json.dumps(self.blocks[-1], sort_keys = True).encode("ascii"))
        })
        self.write_ledger()

    @staticmethod
    def get_blocks():
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

    def write_ledger(self):
        with open("ledger.json", "w") as f:
            f.write(json.dumps(self.blocks))

    def update_ledger(self):
        m = self.length()
        murl = ""
        for url in self.network:
            request = requests.get(url + "/length")
            if request.status_code == 200 and int(request.text) > m:
                m = int(request.text)
                murl = url

        if murl:
            new_ledger = requests.get(url + "/ledger")
            with open("ledger.json", "w") as f:
                f.write(new_ledger)
        else:
            self.write_ledger()
        self.blocks = blockchain.get_blocks()

    def register(self, url):
        self.network.add(url)
        requests.post(url + "/register", data = { "url" : self.url } )

    def length(self):
        return len(self.blocks)
