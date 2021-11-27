from flask import Flask, jsonify
from uuid import uuid4
import requests

from nrcoin import NRCoin


nrcoin = NRCoin()

app = Flask(__name__)

# create address for node on Port 5000
node_address = str(uuid4()).replace('-', '')

@app.route('/mine_block', methods=['GET'])
def mine_block():
    prev_block = nrcoin.get_prev_block()
    prev_proof = prev_block['proof']
    proof = nrcoin.pow(prev_proof)
    prev_hash = nrcoin.hash(prev_block)
    # when miner mines a block, gets some nrcoins
    nrcoin.add_transaction(sender=node_address, receiver='ned', amount=3)
    block = nrcoin.create_block(proof, prev_hash)
    response = {'message': 'Just mined a block',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'prev_hash': block['prev_hash'],
                'transactions': block['transactions']}
    return jsonify(response), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': nrcoin.chain,
                'chain_length': len(nrcoin.chain)}
    return jsonify(response), 200


@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = nrcoin.is_chain_valid(nrcoin.chain)
    if is_valid:
        response = {'message': 'Blockchain is valid'}
    else:
        response = {'message': 'Blockchain is invalid'}
    return jsonify(response), 200


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json_file = requests.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all (key in json_file for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    # get index of next block to put this transaction
    block_index = nrcoin.add_transaction(
        json_file['sender'], json_file['receiver'], json_file['amount']
    )
    response = {'message': f'Transaction added to block {block_index}'}
    return jsonify(response), 201
