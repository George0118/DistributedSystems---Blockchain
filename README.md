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
1. Start the application by running the `running_script.py` file from N separate terminals. Provide the IP address, port number, number of nodes, and block capacity as arguments.

   For example, for N=5 and Capacity=10. If the bootstrap node's IP address and port are `(127.0.0.1, 40000)` and you are running locally, execute the following commands from different terminals:

   ```bash
   python running_script.py 127.0.0.1 40000 5 10
   python running_script.py 127.0.0.1 40001 5 10
   python running_script.py 127.0.0.1 40002 5 10
   python running_script.py 127.0.0.1 40003 5 10
   python running_script.py 127.0.0.1 40004 5 10
   ```
   
2. Follow the command-line interface (CLI) prompts to interact with the system. Below are the acceptable commands:

- **t \<number\>**: Perform a transaction with the specified amount.
- **m \<text\>**: Send a message with the provided text.
- **stake \<number\>**: Stake the specified amount.
- **view**: View the last validated block's transactions and validator.
- **balance**: View your current balance (up to the last validated block).

## File Structure

```bash
DistributedSystems-Blockchain
├──  block.py
├──  blockchain.py
├──  commands.py
├──  config.py
├──  message.py
├──  node.py
├──  p2p.py
├──  proof_of_stake.py
├──  requirements.txt
├──  running_script.py
├──  transaction.py
├──  transaction_pool.py
├──  utils.py
└──  wallet.py