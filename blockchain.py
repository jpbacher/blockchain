import json
import datetime
import hashlib
from flask import Flask, jsonify


class Blockchain:
    
    def __init__(self):
        
        self.chain = []
        # genesis block
        self.create_block(proof=1, prev_hash='0')
        
    def create_block(self, proof, prev_hash):
        """[summary]

        Args:
            proof ([type]): [description]
            prev_hash ([type]): [description]
        """
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'prev_hash': prev_hash}
        