import hashlib
import json
from datetime import datetime

class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        content = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, {
            "message": "Supply Chain Genesis Block",
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }, "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        previous_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            data=data,
            previous_hash=previous_block.hash
        )
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def get_chain_json(self):
        return [{
            "index": block.index,
            "timestamp": block.timestamp,
            "data": block.data,
            "hash": block.hash[:12] + "...",
            "previous_hash": block.previous_hash[:12] + "...",
        } for block in self.chain]

supply_chain_blockchain = Blockchain()

def record_shipment(stage, location, quantity, product, status="verified"):
    block = supply_chain_blockchain.add_block({
        "stage": stage,
        "location": location,
        "quantity": quantity,
        "product": product,
        "status": status,
        "recorded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    return block

def get_full_trail():
    return supply_chain_blockchain.get_chain_json()

def verify_chain():
    return supply_chain_blockchain.is_chain_valid()

if __name__ == "__main__":
    print("Testing blockchain...")
    record_shipment("Kisan", "Punjab", "500kg", "Wheat")
    record_shipment("Factory", "Pune", "12000 packets", "Maggi")
    record_shipment("Godown", "Bhiwandi", "11800 packets", "Maggi")
    record_shipment("Transport", "Mumbai Highway", "11800 packets", "Maggi")
    record_shipment("Dukaan", "Andheri", "11800 packets", "Maggi")
    
    print("Chain valid:", verify_chain())
    for block in get_full_trail():
        print(f"Block {block['index']}: {block['data'].get('stage', 'Genesis')} | Hash: {block['hash']}")