from flask import Flask, jsonify

from blockchain import Blockchain


# create web app
app = Flask(__name__)

# create blockchain
blockchain = Blockchain()
