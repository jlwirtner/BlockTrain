from hashlib import sha256
from model import get_data, get_model

def update_hash(*args):
    hash_text = ''
    h = sha256()
    for arg in args:
        hash_text += str(arg)
    h.update(hash_text.encode('utf-8'))
    return h.hexdigest()

class Block:
    data = None
    nonce = 0
    previous_hash = '0' * 64

    def __init__(self, data, number=0):
        self.data = data
        self.number = number
    
    def __str__(self):
        return str('Block#: %s\nHash: %s\nData: %s\nNonce: %s\n' % (
            self.number, 
            self.hash(), 
            self.data, 
            self.nonce
        ))
    
    def hash(self):
        return update_hash(
            self.previous_hash, 
            self.number, self.data, 
            self.nonce
        )

class BlockChain:
    difficulty = 1

    def __init__(self, model, dataset, coal=0, chain=[]):
        self.chain = chain
        self.model = model
        self.dataset = dataset
        self.coal = coal

    def add(self, block):
        self.chain.append(block)

    def remove(self, block):
        self.chain.remove(block)

    def mineable(self):
        return self.coal > 0

    def get_info(self):
        return {'meta':self.model.to_json(), 'weights':self.model.get_weights(), 'coal':self.coal}

    def mine(self, block):
        try:
            block.previous_hash = self.chain[-1].hash()
        except IndexError:
            pass

        while True:
            if self.verify_difficulty(block.hash()):
                self.add(block)
                self.model.fit(self.dataset, epochs=1, verbose=0)
                self.coal -= 1
                break
            else:
                block.nonce += 1
    
    def is_valid(self):
        for i in range(1, len(self.chain)):
            previous = self.chain[i].previous_hash
            calculated = self.chain[i - 1].hash()
            if previous != calculated or not self.verify_difficulty(calculated):
                return False
        return True

    def verify_difficulty(self, hash_text):
        return hash_text[:self.difficulty] == '0' * self.difficulty


def main():
    model = get_model(5, 188, 0.065185, 0.001032)
    train_ds, test_ds = get_data()

    # need to fit once so get_info() works
    # TODO: Fix get_info() so I don't need to do this
    model.fit(test_ds, epochs=1)

    blockchain = BlockChain(model, train_ds, coal=30)

    blockchain.model.evaluate(test_ds)

    num = 0
    while blockchain.mineable():
        num += 1
        blockchain.mine(Block(blockchain.get_info(), num))

    blockchain.model.evaluate(test_ds)

    # modify chain so it fails verification - just to test it
    # blockchain.chain[-2].data = "sneaky Bitch!"
    # blockchain.mine(blockchain.chain[-2])

    for block in blockchain.chain:
        print(block)

    print('valid chain: {}'.format(blockchain.is_valid()))

if __name__ == '__main__':
    main()