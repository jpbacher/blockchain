import json
import datetime
from hashlib import sha256
from uuid import uuid4
from urllib.parse import urlparse
import requests
from flask import Flask, jsonify, request


class NRCoin:
    
    def __init__(self):
        
        self.chain = []
        # before integrated into a block
        self.transactions = []
        # create genesis block
        self.create_block(proof=1, prev_hash='0')
        self.nodes = set()
        
    def create_block(self, proof, prev_hash):
        """Returns new block

        Args:
            proof (integer): the mine function that was solved
            prev_hash (string): previous hash from previous block - links previous block to one just mined
            transactions (list): as soon as miner mines the next block
        """
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'prev_hash': prev_hash,
                 'transactions': self.transactions}
        # reset transactions - cannot have duplicate transactions in different blocks
        self.transactions = []
        self.chain.append(block)
        return block
    
    def add_transaction(self, sender, receiver, amount):
        """Appends transaction to transaction list and returns index of new block

        Args:
            sender (string): sender of a trasnaction
            receiver (string): receiver of a transaction
            amount (float): amount of nrcoin for transaction
        """
        transaction = {'sender': sender,
                       'receiver': receiver,
                       'amount': amount}
        self.transactions.append(transaction)
        
        previous_block = self.get_prev_block()
        new_block_index = previous_block['index'] + 1
        return new_block_index
    
    def add_node(self, address):
        """Add the node's address (a url and port) to set of nodes

        Args:
            address (string): the url node address
        """
        parsed_url = urlparse(address)
        # get url and port from parsed_url
        self.nodes.add(parsed_url.netloc)
    
    def get_prev_block(self):
        """Returns previous block from blockchain
        """
        return self.chain[-1]
    
    def pow(self, prev_proof):
        """Defines the problem to solve and solves the problem by trial & error
        Proof of work principal: 'hard to find, easy to verify'
        sha256 - 64 hexadecimal characters, regex: [A-Fa-f0-9]{64}
        
        Args:
            prev_proof (integer): mine function that was solved  
        """
        # start at 1
        new_proof = 1
        is_proof = False
        while is_proof is False:
            # make operation non-symmetrical 
            hash_operation = sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                is_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        """Returns sha256 cryptographic hash of a block

        Args:
            block (dictionary): a block from the blockchain
        """
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        """Check if entire blockchain is valid

        Args:
            chain (list): the chain of blockchain
        """
        # start w/ first block
        prev_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            # check previous hash of block = hash of previous block
            block = chain[block_index]
            if block['prev_hash'] != self.hash(prev_block):
                return False
            # check if current proof is valid
            prev_proof = prev_block['proof']
            proof = block['proof']
            hash_operation = sha256(str(proof**2 - prev_proof**2)).encode().hexdigest()
            if hash_operation[:4] != '0000':
                return False
            prev_block = block
            block_index +=1
        return True
    
    def replace_chain(self):
        """
        """
        network = self.nodes
        longest_chain = None
        max_chain_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code != 200:
                break
            chain_length = response.json()['length']
            chain = response.json()['chain']
            if chain_length > max_chain_length and self.is_chain_valid(chain):
                max_chain_length = chain_length
                longest_chain = chain
        # if chain was replaced
        if longest_chain:
            return True
            