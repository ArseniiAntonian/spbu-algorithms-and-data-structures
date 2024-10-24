import hashlib

def hash_sha3_256(data):
    return hashlib.sha3_256(data.encode()).hexdigest()

def hash_sha1(data):
    data_bytes = data.encode('utf-8')
    sha1 = hashlib.sha1(data_bytes)
    return sha1.hexdigest()

with open('assignment3/real_phones.txt', 'r') as f:
    phone_numbers = [line.strip()[-11:] for line in f]


salts = [1, 12345678, 13579]

for salt in salts:

    sha3_hashes = []
    sha1_hashes = []

    for phone in phone_numbers:
        
        salted_phone = salt + int(phone)

        sha3_hashed = hash_sha3_256(str(salted_phone))
        sha3_hashes.append(sha3_hashed)

        sha1_hashed = hash_sha1(str(salted_phone))
        sha1_hashes.append(sha1_hashed)

    with open(f'assignment3/salted_and_hashed/sha3_hashes_salt_{salt}.txt', 'w') as f_sha3:
        for sha3_hash in sha3_hashes:
            f_sha3.write(sha3_hash + '\n')

    with open(f'assignment3/salted_and_hashed/sha1_hashes_salt_{salt}.txt', 'w') as f_sha1:
        for sha1_hash in sha1_hashes:
            f_sha1.write(sha1_hash + '\n')

    print(f"Хеширование завершено для соли {salt}. Результаты сохранены в файлы 'sha3_hashes_salt_{salt}.txt' и 'sha1_hashes_salt_{salt}.txt'.")
