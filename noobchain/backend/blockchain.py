from backend.block import Block
from backend.transaction import Transaction
import json
import requests
from collections import OrderedDict
from hashlib import sha256
import json
import time


class Blockchain:
    def __init__(self, ring, my_id):

        self.ring = ring  # List of ring nodes

        # Genesis block
        self.genesis = Block(index=0, previous_hash=1, transactions=[], nonce=0)
        self.my_id = my_id
        # Genesis transaction
        transaction = Transaction(sender_address="0", receiver_address=self.ring[0]['public_key'], amount=500,
                                  transaction_inputs='', wallet=None, ids="id0", genesis=True)

        self.genesis.transactions.append(transaction)
        self.genesis.timestamp=0
        self.genesis.current_hash = self.genesis.get_hash()

        self.blocks = [self.genesis]  # List of added blocks (aka chain)
        self.resolve = False  # Check chain updates (bigger was found)

    def __str__(self):
        chain = f'{self.genesis.index} ({0})'

        # ignore genesis
        for block in self.blocks[1:]:
            chain += f' -> {block.index} ({block.current_hash})'

        return chain

    def add_block(self, new_block):
        self.blocks.append(new_block)
        return self

    def mine_block(self, block, difficulty, continue_mine):

        # We mine the whole block until the conditions are met or we get the block from another user
        nonce = 0
        block_to_mine = block
        block_to_mine.nonce = nonce

        # update hash
        block_hash = block_to_mine.get_hash_obj()
        # try new hashes until first n characters are 0
        while block_hash.hexdigest()[:difficulty] != '0' * difficulty and continue_mine():
            # block_hash.update(f'{nonce}{prev_hash.hexdigest()}'.encode('utf-8'))
            block_hash = block_to_mine.get_hash_obj()
            nonce += 1
            block_to_mine.nonce = nonce

        # update with new calculated hash
        if continue_mine():
            print("I GOT A BLOCK")
            block_to_mine.current_hash = block_hash.hexdigest()
            block_to_mine.nonce = nonce - 1
            self.broadcast_block(block_to_mine)
        return

    def broadcast_block(self, block):

        # Actually post it at http://{address}/broadcast/block
        for member in self.ring:
            # Don't send it to myself
            if self.my_id != f'id{member.get("id")}':
                url = f'{member.get("address")}/broadcast/block'
                print(url)
                response = requests.post(url, json=block.to_json())
                if response.status_code == 400 or response.status_code == 500:
                    print('Block declined, needs resolving')
                if response.status_code == 409:
                    self.resolve = True

        # send it to my self, remember everyone is equal
        for member in self.ring:
            if self.my_id == f'id{member.get("id")}':
                url = f'{member.get("address")}/broadcast/block'
                response = requests.post(url, json=block.to_json())
                if response.status_code == 400 or response.status_code == 500:
                    print('Block declined, needs resolving')
                if response.status_code == 409:
                    self.resolve = True

        return self

    def resolve_conflict(self):

        for member in self.ring:
            # This time we do really care about the others and not ourself
            if self.my_id != f'id{member.get("id")}':

                # Request chain from nodes
                new_blocks = requests.get(f'{member.get("address")}/chain').json()

                # Generate correct blocks in order to replace ones in the chain
                new_blocks = json.loads(new_blocks)
                tmp_blockchain = []
                # parse the json block to an actual block item
                for block in new_blocks["blockchain"]:
                    transactions = []

                    # Load transactions for that block
                    for t in block["transactions"]:
                        transaction = Transaction(sender_address=t["sender_address"],
                                                  receiver_address=t["receiver_address"],
                                                  amount=t["amount"], wallet=None,
                                                  transaction_inputs=t["transaction_inputs"],
                                                  ids=t["node_id"])

                        transaction.transaction_id = t["transaction_id"]
                        transaction.signature = t["signature"]
                        transaction.transaction_outputs = t["transaction_outputs"]
                        transaction.change = t["change"]

                        # Dont need this?!
                        # transaction = transaction.to_od()
                        transactions.append(transaction)

                    block = Block(block["index"], transactions, block["nonce"], block["previous_hash"],
                                  block["timestamp"])

                    block.current_hash = block.get_hash()

                    tmp_blockchain.append(block)

                print(f'Collected chain')
                # If bigger is to be found, replace existing chain
                if len(tmp_blockchain) > len(self.blocks) and self.validate_chain(tmp_blockchain):
                    print("\n\n\n\n\nI changed my blockchain WOOHOO!")
                    self.blocks = tmp_blockchain
                    return True
                elif len(tmp_blockchain) == len(self.blocks):
                    print("We are equal")
                    return False
                else:
                    print("MINE IS BIGGER AND BETTER")
                    return False

    def to_od(self):
        od = OrderedDict([
            ('blockchain', [block.to_od() for block in self.blocks])
        ])

        return od

    def to_json(self):
        # Convert object to json
        # return json.dumps(self.to_od())
        return json.dumps(self.to_od(), default=str)

# ---------------------------------------------- VERIFICATION FUNCTIONS ----------------------------------------------

    def validate_block(self, block, difficulty):
        # check the proof of work
        if difficulty * "0" != block.get_hash_obj().hexdigest()[:difficulty]:
            print("I failed the nonce test")
            return False
        # check tha it sticks to our chain
        if self.blocks[-1].current_hash != block.previous_hash and block.index != 1:
            print("I failed the previous hash test")
            return False

        return True

    def validate_chain(self, blockchain):
        # Loop chain to validate that hashes are connected
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.current_hash != block.get_hash():
                print("My blocks are wrong :(")
                return False
            if block.previous_hash != blockchain[index - 1].current_hash:
                print("I am not well connected :(")
                return False

        return True
