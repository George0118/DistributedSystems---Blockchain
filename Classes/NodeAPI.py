"""Node API for communication with the node"""

from flask_classful import FlaskView, route
from flask import Flask, jsonify, request
from BlockChainUtils import BlockChainUtils

node = None


class NodeAPI(FlaskView):
    """
    Node API for communication with the node
    """

    def __init__(self):
        self.app = Flask(__name__)

    def start(self, apiPort):
        """
        Starts the API
        """
        NodeAPI.register(self.app, route_base="/")
        self.app.run(host="localhost", port=apiPort)

    def inject_node(self, injectedNode):
        global node
        node = injectedNode

    @route("/info", methods=["GET"])
    def info(self):
        return "This Is A Communication Interface To A Nodes Blockchain", 200

    @route("/blockchain", methods=["GET"])
    def blockchain(self):
        return node.blockchain.to_dict(), 200

    @route("transaction_pool", methods=["GET"])
    def transaction_pool(self):
        transactions = {}
        for ctr, transaction in enumerate(node.transaction_pool.transactions):
            transactions[ctr] = transaction.to_dict()
        return jsonify(transactions), 200

    @route("transaction", methods=["POST"])
    def transaction(self):
        values = request.get_json()
        if not "transaction" in values:
            return "Missing Transaction Value", 400
        transaction = BlockChainUtils.decode(values["transaction"])
        node.handle_transactions(transaction)
        response = {"message": "Received transaction"}
        return jsonify(response), 201