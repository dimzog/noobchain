from backend.block import Block
from backend.transaction import Transaction
import json
import requests
from collections import OrderedDict
from hashlib import sha256
import json


class Blockchain:
    def __init__(self, ring):

        self.ring = ring  # List of ring nodes

        # Genesis block
        self.genesis = Block(index=0, previous_hash=1, transactions=[], nonce=0)

        # Genesis transaction
        transaction = Transaction(sender_address="0", receiver_address=self.ring[0]['public_key'], amount=500,
                                  transaction_inputs='', wallet=None, ids="id0", genesis=True)

        self.genesis.transactions.append(transaction)
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

    def mine_block(self, difficulty):

        # grab hash of latest block in the chain
        prev_hash = self.blocks[-1].get_hash_obj()
        nonce = 0

        # update hash
        prev_hash.update(f'{nonce}{prev_hash.hexdigest()}'.encode('utf-8'))

        # try new hashes until first n characters are 0
        while prev_hash.hexdigest()[:difficulty] != '0' * difficulty:
            prev_hash.update(f'{nonce}{prev_hash.hexdigest()}'.encode('utf-8'))
            nonce += 1

        # update with new calculate hash
        self.blocks[-1].current_hash = prev_hash.hexdigest()

        # TODO
        # Fix code below for open transactions (if capacity > 1?!?!)
        #copied_transactions = self.__open_transactions[:]
        #for tx in copied_transactions:
        #    if not Wallet.verify_transaction(tx):
        #        return None
        #copied_transactions.append(reward_transaction)

        # Create new block
        block = Block(index=len(self.blocks), previous_hash=self.blocks[-1].current_hash,
                      transactions=[], nonce=nonce)

        #print(f'\nBlock to broadcast: {block.to_json()}')
        #self.blocks.append(block)

        return block

    def broadcast_block(self, block):
        # Actually post it at http://{address}/broadcast/block
        for member in self.ring:
            url = f'{member.get("address")}/broadcast/block/'
            response = requests.post(url, block.to_json())
            if response.status_code == 400 or response.status_code == 500:
                print('Block declined, needs resolving')
            if response.status_code == 409:
                self.resolve = True

        return self

    def resolve_conflict(self):

        for member in self.ring:
            # Request chain from nodes
            new_blocks = requests.get(f'http://{member.get("address")}/chain').json()

            # Build it using json
            # Change this when classes are finalised
            # Replace wallet
            # Generate correct blocks in order to replace ones in the chain
            blocks = [
                Block(index=block["index"], transactions=[
                    Transaction(sender_address=t["sender_address"], receiver_address=t["receiver_address"],
                                amount=t["amount"], transaction_inputs=t["transaction_inputs"],
                                wallet=t["wallet"], ids=t["node_id"]) for t in block["transactions"]
                ],
                      nonce=block["nonce"], previous_hash=block["previous_hash"], timestamp=block["timestamp"]) for
                block in
                new_blocks["blockchain"]
            ]

            print(f'\nCollected chain {new_blocks}\n')
            # If bigger is to be found, replace existing chain
            if len(new_blocks) > len(self.blocks) and self.validate_chain(new_blocks):
                self.blocks = blocks

        self.resolve = False

        return self

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

    def validate_block(self, block):

        if block.current_hash != block.get_hash():
            return False

        if self.blocks[-1].current_hash != block.previous_hash:
            return False

        return True

    def validate_chain(self, blockchain):

        # Loop chain to validate that hashes are connected
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != blockchain[index - 1].current_hash:
                return False
            if block.current_hash != block.get_hash():
                return False

        return True
