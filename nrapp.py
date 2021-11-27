from flask import Flask, jsonify
from uuid import uuid4
from flask.typing import ResponseReturnValue

from werkzeug.wrappers import response

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
