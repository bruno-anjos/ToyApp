import random
import time
import hashlib
import MySQLdb

#Feeds the random generator with the current UNIX timestamp as seed
random.seed(time.time())

#Returns a hash using SHA256 algorithm and the current UNIX timestamp
#plus a random float number to add even more randomness to the timestamp
def getHash():
    data = time.time() + random.random() * 10000
    hashKey = hashlib.sha256()
    #The string object has to be encoded to UTF-8 due to hashing requisites
    hashKey.update(str(data).encode('utf-8'))
    return hashKey.hexdigest()


def getNum():
    return random.randint(1, 1000)


print('Hash: ' + getHash())
print('Number: ' + str(getNum()))
