import hashlib
import json
import time
from uuid import uuid4

class Message:
    def __init__(self, sender, target, msg_type, topic, payload):
        self.id = str(uuid4())
        self.sender = sender
        self.target = target
        self.type = msg_type
        self.topic = topic
        self.payload = payload
        self.timestamp = time.time()

    def to_dict(self):
        return self.__dict__


class Block:
    def __init__(self, index, previous_hash, messages):
        self.index = index
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        self.messages = messages
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "messages": [m.to_dict() for m in self.messages],
            "nonce": self.nonce
        }, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()


class BulletinChain:
    def __init__(self):
        self.chain = []
        self.pending_messages = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, "0", [])
        self.chain.append(genesis)

    def add_message(self, message):
        self.pending_messages.append(message)

    def mine_block(self):
        last_block = self.chain[-1]
        new_block = Block(
            index=len(self.chain),
            previous_hash=last_block.hash,
            messages=self.pending_messages
        )

        # simple proof-of-work (optional)
        while not new_block.hash.startswith("0000"):
            new_block.nonce += 1
            new_block.hash = new_block.compute_hash()

        self.chain.append(new_block)
        self.pending_messages = []

        return new_block
