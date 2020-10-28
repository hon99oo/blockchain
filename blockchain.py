import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request


class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # 문제
        self.new_block(previous_hash='1', proof=100)

    def register_node(self, address):
        """
        Add a new node to the list of nodes

        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
        # 문제
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # 문제
            self.nodes.add(parsed_url.path)
        # 문제
        else:
            raise ValueError('Invalid URL')


    def valid_chain(self, chain):
        # 문제
        last_block = chain[0]
        # 문제
        current_index = 1
        # 문제
        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # 문제
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            # 문제
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        # 문제
        # 문제
        neighbours = self.nodes
        # 문제
        new_chain = None

        # 문제
        max_length = len(self.chain)

        # 문제
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            # 문제
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # 문제
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    # 문제
                    new_chain = chain

        # 문제
        if new_chain:
            self.chain = new_chain
            return True
        # 문제
        return False

    def new_block(self, proof, previous_hash):
        # 문제
        # 문제
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # 문제
        self.current_transactions = []
        # 문제
        self.chain.append(block)
        return block
    # 문제
    def new_transaction(self, sender, recipient, amount):
        # 문제
        # 문제
        self.current_transactions.append({
                    'sender': sender,
                    'recipient': recipient,
                    'amount': amount,
                })
        # 문제
        return self.last_block['index'] + 1

    @property
    # 문제
    def last_block(self):
        return self.chain[-1]
    # 문제
    @staticmethod
    def hash(block):
        # 문제
        # 문제
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        # 문제
        # 위에서 설정한 last_block의 proof 값은 last_proof으로 설정
        last_proof = last_block['proof']
        # 마지막 블록을 해시한 것이 마지막 해시값
        last_hash = self.hash(last_block)
        # valid proof가 옳게될 때까지 proof 값을 더한다. 
        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof
    # 위에서 말한 valid proof
    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        # 문제
        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        # 첫 4개가 0이 되어야만 통과
        return guess_hash[:4] == "0000"


# 문제
app = Flask(__name__)

# 문제
node_identifier = str(uuid4()).replace('-', '')

# 문제
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # 문제
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # 문제
    # 문제
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # 문제
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    # 문제
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

# 문제
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # 문제
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # 문제
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

# 문제
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

# 문제
@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

# 문제
@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

# 문제
if __name__ == '__main__':
    from argparse import ArgumentParser
    # 문제
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
