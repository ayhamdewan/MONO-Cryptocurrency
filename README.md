# MONO-Cryptocurrency
Cryptocurrency called MONO created using Blockchain technology

The program allows the MONO crypto to be mined, validated, and transacted. Additionally, the MONO blockchain can be retreived and the transactions stored inside each block can be seen. Nodes can also be connected to expand the MONO network. The program also contains a consensus algorithm that ensures every blockchains of every node is identical to the rest. The validation algorithm enforces blockchain security standards and runs two checks:
  1. Makes sure that the current block's previous hash is the same as the previous block's hash
  2. Ensures proof of each block is valid (solved cryptographic puzzle correctly)

***IMPORTANT: Postman API is used to test and process the MONO cryptocurrency and its blockchain

Below is information on the contents of the files/folders of this repository:

MONO_Blockchain.py:
The MONO_Blockchain file contains the fundamental blockchain technology that was used to build upon and create the final crptocurrency.

MONO_Cryptocurrency:
This folder contains all the components of the MONO cryptocurrency.
  
  MONO.py:
  The full MONO cryptocurrency program.
  
  MONO_node_5001:
  Replica of MONO.py with the receiver set to "Receiver 1".
  Node #1.
  Used for testing in Postman.
  
  MONO_node_5002:
  Replica of MONO.py with the receiver set to "Receiver 2".
  Node #2.
  Used for testing in Postman.
  
  MONO_node_5003:
  Replica of MONO.py with the receiver set to "Receiver 3".
  Node #3.
  Used for testing in Postman.
  
  nodes.json:
  Contents of this file need to be pasted into Postman and filled in accordingly of the nodes that need to be connected.
  Used for the connect_node request.
  
  transaction.json:
  Contents of this file need to be pasted into Postman and filled in accordingly with the desired specifications.
  Used for the add_transactions request.
  All fields need to be filled in for the add_transaction request to work.
