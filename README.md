# Blockchain Messaging and Transaction Platform

## Overview
This project implements a platform for exchanging messages and a digital currency called BCC using a blockchain. The blockchain utilizes the proof-of-stake algorithm for consensus, where validators are selected based on the amount of coins owned by each node. Communication between nodes is facilitated through TCP sockets for reliability and security. Cryptographic algorithms for communication and data security are implemented using the PyCryptodome library, providing a flexible and reliable implementation of cryptographic functions.

## System Design
The implementation of the system consists of several core components:

### Core Blockchain Classes
- `block.py`: Implements the basic structure of a block in the blockchain, including its index, timestamp, transactions, validator, and hash.
- `blockchain.py`: Acts as a container for blocks, providing functions for managing the blockchain.
- `transaction.py`: Represents transactions and messages created by users, including functions for handling transactions.
- `transaction_pool.py`: Stores pending transactions until they are added to a block.
- `wallet.py`: Manages keys, transactions, and blocks, and interacts with the blockchain.

### Node Communication
- `message.py`: Helper class for creating messages sent between nodes.
- `node.py`: Represents each node in the system, initializes the node with its IP address and port, creates a wallet and peer-to-peer object, and handles node communication and the CLI.
- `p2p.py`: Implements a peer-to-peer network for node communication using TCP sockets.

## Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`

## Usage
1. Start the application by running the `docker-compose up` or if you are on Windows run `./start.ps1` to also automatically open N terminals for better viewing. In future versions we will change the script to version Linux and Mac OS too.
   
2. The process will start and each user (container) will read from its own input file and try to execute the transactions.

## File Structure

```bash
DistributedSystems-Blockchain
├──  input_5
│   └──  transX.txt
├──  input_10
│   └──  transX.txt
├──  block.py
├──  blockchain.py
├──  commands.py
├──  config.py
├──  docker-compose.yml
├──  dockerfile
├──  main.py
├──  message.py
├──  node.py
├──  p2p.py
├──  proof_of_stake.py
├──  requirements.txt
├──  running_script.py
├──  start.ps1
├──  stop.ps1
├──  transaction.py
├──  transaction_pool.py
├──  utils.py
└──  wallet.py
