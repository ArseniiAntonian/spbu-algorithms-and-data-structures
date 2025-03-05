with open('assignment3/sources/cracked.txt', 'r') as hf:
        salted_phones = [int(line.strip()[-11:]) for line in hf.readlines()]
    
with open('assignment3/scources/phones.txt', 'r') as rf:
    real_phones = [int(line.strip()) for line in rf.readlines()]

for i in salted_phones:
    counter = 0
    salt = i-real_phones[0]
    for j in salted_phones:
        if j-salt in real_phones:
            counter +=1
    if counter == len(real_phones):
        break

print(f'Найденная соль: {salt}')

with open('assignment3/sources/cracked.txt', 'r') as phones, open('assignment3/sources/real_phones.txt', 'w') as real_phones:
    for line in phones:
        real_phone = str(int(line.strip()[-11:]) - salt)
        real_phones.write(real_phone + '\n')

