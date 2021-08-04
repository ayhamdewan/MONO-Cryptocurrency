# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse

# Building a Blockchain

class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof = 1, previous_hash = '0') # Genesis block
        self.nodes = set()
    
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    # Function to check if cryptographic puzzle has been solved
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            # Hash will use SHA256
            hash_operation = hashlib.sha256(str(new_proof**3 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1 # incremented to retry  cryptographic puzzle until solved
        return new_proof
    
    # Hashing function
    def hash(self, block):
        # Making the block dictionary into a JSON string
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
     # Function to check if chain is valid
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            # Check no.1: Current block's previous hash is same as previous block's hash
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            current_proof = block['proof']
            hash_operation = hashlib.sha256(str(current_proof**3 - previous_proof**2).encode()).hexdigest()
            # Check no.2: Proof of each block is valid (solved cryptographic puzzle correctly)
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True # If nothing is wrong with the blockchain
    
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    
    def add_node(self, address): # address: Address of the node
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    
    def replace_chain(self): # Consensus algorithm
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200: # successfull
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain: # Replacement was made
            self.chain = longest_chain
            return True
        return False

# Mining our Blockchain

# Creating a Web App
app = Flask(__name__)

# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace('-', '')

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods = ['GET']) # Routing and specifying method
def mine_block():
     # Use previous block's proof to find current block's proof
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    current_proof = blockchain.proof_of_work(previous_proof)
    
    # Add new block to blockchain
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender = node_address, receiver = 'Hadelin', amount = 1)
    block = blockchain.create_block(current_proof, previous_hash)
    
    # Formatting a response to display
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    return jsonify(response), 200 # HTTP Status Code 200 indicates successful request

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET']) # Routing and specifying method
def get_chain():
    response = {'length': len(blockchain.chain),
                'chain': blockchain.chain}
    return jsonify(response), 200

# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET']) # Routing and specifying method
def validity():
    valid = blockchain.is_chain_valid(blockchain.chain)
    if valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'PROBLEM! The Blockchain is NOT VALID.'}
    return jsonify(response), 200

# Adding a new transaction to the Blockchain
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json() # Will take input from JSON file
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transaction_keys): # If all the keys in the transaction_keys list is not in the json file
        return 'Some elements of the transaction are missing', 400 # 400 - bad request error code
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount']) # add a transaction
    response = {'message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201 # Transaction created; 201: Created status code

# Decentralizing our Blockchain

# Connecting new nodes
@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes') # Will be address of nodes
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All the nodes are now connected. The MONO Blockchain now contains the following nodes:',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201

# Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    replaced = blockchain.replace_chain()
    if replaced:
        response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'All good. The chain is the largest one.',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 200

# Running the app
app.run(host = '0.0.0.0', port = 5000)
