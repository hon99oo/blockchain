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

        # 제네시스 블록을 만드는 과정 previous_hash는 1로 proof는 100으로 설정
        self.new_block(previous_hash='1', proof=100)

    def register_node(self, address):
        """
        Add a new node to the list of nodes

        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
# netloc 혹은 path면 nodes에 그 상황에 맞게 추가한다.
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
# 틀리면 오류를 반환한다.
        else:
            raise ValueError('Invalid URL')


    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid

        :param chain: A blockchain
        :return: True if valid, False if not
        """
# 일단 last block을 chain의 0 즉, 1번째로 설정한다. index 값도 1로 설정한다. 
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.

        :return: True if our chain was replaced, False if not
        """
# 이웃을 노드들로 설정
        neighbours = self.nodes
#new_chain은 None으로 설정
        new_chain = None

        # max_length를 일단 chain의 길이로 설정.
        max_length = len(self.chain)

        # 노드들에게(위에서 설정함) 정보를 요청한다.
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
# code 200은 괜찮은 상황. 200이면 체인의 길이와 정보를 받아온다.
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # 바로 위에서 받은 이웃들의 길이와 그 위에서 설정한 max_length를 비교한다. 만약 이웃 체인의 길이가 더 길면 교체한다.
                if length > max_length and self.valid_chain(chain):
                    max_length = length
# new_chain을 chain으로 설정한다. 
                    new_chain = chain

        # new_chain이 존재하면 내 체인을 new_chain으로 교체하고 True를 반환한다.
        if new_chain:
            self.chain = new_chain
            return True
# new_chain이 없으면 false 값을 반환한다. 
        return False

    def new_block(self, proof, previous_hash):
        """
        Create a new Block in the Blockchain

        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """
#블록의 구조. 현재 체인의 길이에 1을 더한다. timestamp는 현재 시간, transactions는 현재의 거래들, proof는 그대로, previous hash 값은 현존하는 체인의 마지막 블록의 해시값 마지막은 chain[-1]으로 표현
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # 새로운 블록이 만들어졌으니, 기존의 거래 내역들은 초기화한다.
        self.current_transactions = []
# 체인에 블록을 추가한다. 
        self.chain.append(block)
        return block
#새로운 거래
    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block

        :param sender: Address of the Sender
        :param recipient: Address of the Recipient
        :param amount: Amount
        :return: The index of the Block that will hold this transaction
        """
        
# 거래의 구조는, sender, recipient, amount로 이루어짐. 거래는 생길 때마다 추가한다. (append)
self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
#last block의 index값에 1을 더한다. 
        return self.last_block['index'] + 1

    @property
#가장 마지막 블록은 체인의 마지막 블록 [-1]은 가장 마지막을 의미함
    def last_block(self):
        return self.chain[-1]
#블록의 해시값 구하기
    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block

        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        """
        Simple Proof of Work Algorithm:

         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - Where p is the previous proof, and p' is the new proof
         
        :param last_block: <dict> last Block
        :return: <int>
        """
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
        """
        Validates the Proof

        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :param last_hash: <str> The hash of the Previous Block
        :return: <bool> True if correct, False if not.

        """

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
# 첫 4개가 0이 되어야만 통과
        return guess_hash[:4] == "0000"


# Instantiate the Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


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


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
