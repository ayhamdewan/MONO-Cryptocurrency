# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify
 
# Building a Blockchain
class Blockchain:
 
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0') # Genesis block
 
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
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
 
 
# Creating a Web App
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
 
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
    block = blockchain.create_block(current_proof, previous_hash)
    
    # Formatting a response to display
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200 # HTTP Status Code 200 indicates successful request
 
# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET']) # Routing and specifying method
def get_chain():
    response = {'length': len(blockchain.chain),
                'chain': blockchain.chain}
    return jsonify(response), 200
 
# Checking if the Blockchain is valid
@app.route('/validity', methods = ['GET']) # Routing and specifying method
def validity():
    valid = blockchain.is_chain_valid(blockchain.chain)
    if valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'PROBLEM! The Blockchain is NOT VALID.'}
    return jsonify(response), 200
 
# Running the app
app.run(host = '0.0.0.0', port = 5000)
