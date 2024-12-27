import hashlib
import time

# Class untuk merepresentasikan sebuah blok
class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash_function):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash_function = hash_function
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Menghitung hash blok dengan fungsi hash yang dipilih
        block_content = (
            str(self.index)
            + self.previous_hash
            + str(self.timestamp)
            + self.data
        )
        return self.hash_function(block_content.encode()).hexdigest()

# Class untuk Blockchain
class Blockchain:
    def __init__(self, hash_function):
        self.hash_function = hash_function
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # Membuat blok genesis (blok pertama)
        return Block(0, "0", time.time(), "Genesis Block", self.hash_function)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        # Menambahkan blok baru ke blockchain
        latest_block = self.get_latest_block()
        new_block = Block(
            latest_block.index + 1,
            latest_block.hash,
            time.time(),
            data,
            self.hash_function
        )
        self.chain.append(new_block)

    def is_chain_valid(self):
        # Validasi blockchain untuk memastikan integritas
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Periksa apakah hash blok saat ini sesuai dengan data blok
            if current_block.hash != current_block.calculate_hash():
                return False

            # Periksa apakah previous_hash sesuai dengan hash blok sebelumnya
            if current_block.previous_hash != previous_block.hash:
                return False

        return True

# Fungsi untuk membandingkan performa hashing
def compare_hash_performance():
    data = "Performance testing for hashing algorithms in blockchain."
    iterations = 10000

    # SHA256
    start_time = time.time()
    for _ in range(iterations):
        hashlib.sha256(data.encode()).hexdigest()
    sha256_time = time.time() - start_time

    # BLAKE2
    start_time = time.time()
    for _ in range(iterations):
        hashlib.blake2b(data.encode()).hexdigest()
    blake2_time = time.time() - start_time

    print(f"SHA256 time for {iterations} iterations: {sha256_time:.6f} seconds")
    print(f"BLAKE2 time for {iterations} iterations: {blake2_time:.6f} seconds")

# Main Program
if __name__ == "__main__":
    print("Testing SHA256 blockchain:")
    sha256_blockchain = Blockchain(hashlib.sha256)
    sha256_blockchain.add_block("Transaction 1: Alice pays Bob 10 BTC")
    sha256_blockchain.add_block("Transaction 2: Bob pays Charlie 5 BTC")

    for block in sha256_blockchain.chain:
        print(f"Index: {block.index}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Data: {block.data}")
        print(f"Hash: {block.hash}\n")

    print("Testing BLAKE2 blockchain:")
    blake2_blockchain = Blockchain(hashlib.blake2b)
    blake2_blockchain.add_block("Transaction 1: Alice pays Bob 10 BTC")
    blake2_blockchain.add_block("Transaction 2: Bob pays Charlie 5 BTC")

    for block in blake2_blockchain.chain:
        print(f"Index: {block.index}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Data: {block.data}")
        print(f"Hash: {block.hash}\n")

    print("Comparing hash performance:")
    compare_hash_performance()
