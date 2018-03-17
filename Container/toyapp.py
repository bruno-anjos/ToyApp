import random
import time
import hashlib
import sys
import MySQLdb
import ipaddress
from collections import deque

# CONST_USAGE = "Usage: [insertions per second] [averages per second] [timeout in seconds]"


CONST_USAGE = "Usage: python3 toyapp.py [insertions per minute] [max insertions] [number of clients] [starting ip] [batch size]"
CONST_DB_HOST = "localhost"
CONST_DB_USER = "root"
CONST_DB_PASSWORD = "toor"
CONST_DB_NAME = "dummy_db"
CONST_DB_TABLENAME = "dummy_table"
CONST_DB_NUM_COL_NAME = "num"

CONST_MIN_NUM = 1
CONST_MAX_NUM = 100



def main(argv):

    print("Starting toyapp")
    # Feeds the random generator with the current UNIX timestamp as seed
    random.seed(time.time())

    #testDatabase()

    if len(argv) != 4:
        print(CONST_USAGE)
        sys.exit(1)

    insertPerMin = int(argv[1])
    maxInsertions = int(argv[2])
    numClients = int(argv[3])
    startingIP = ipaddress.ip_address(argv[4])
    batchSize = int(argv[5])

    print("Starting main loop")
    mainLoop(insertPerMin, maxInsertions, numClients, startingIP, batchSize)

    sys.exit(0)


# Converts @param timesPerMin to how much time to wait in order to 
# have @param timesPerMin happen that many times per minute
def getSleepTime(timesPerMin):
    return 60 / int(timesPerMin)


# main script loop, runs until it has inserted @arg maxInsertions tuples
# every x seconds will insert a tuple into the database
# where x is how many times it inserts per minute
def mainLoop(insertPerMin, maxInsertions, numClients, startingIP, batchSize):
    startTime = time.time()
    sleepTime = getSleepTime(insertPerMin)
    counter = 0
    db = setupDatabase(CONST_DB_HOST)
    remote_dbs = init_db_connections(startingIP, numClients)
    queuedInserts = deque([])

    while counter < maxInsertions:
        # Gets data to insert
        key = getHash()
        value = random.randint(CONST_MIN_NUM, CONST_MAX_NUM)

        # Inserts in local DB
        insertionTime = time.time()
        insertIntoDB(db.cursor(), [(key, value)])
        afterInsertionTime = time.time()
        timeTook = afterInsertionTime - insertionTime
        print("Inserted \"" + key + "\" with value " + str(value) + " and took " + round(timeTook, 2) + " seconds")

        # Adds to queue
        queuedInserts.append((key, value))

        # Checks if need to flush queue
        if len(queuedInserts) == batchSize:
            insertionTime = time.time()
            for rdb in remote_dbs:
                insertIntoDB(rdb.cursor(), queuedInserts)
            afterInsertionTime = time.time()
            print("Took " + (afterInsertionTime - insertionTime) + " seconds to insert in remote databases.")

        # Sleeps remaining time
        print("Will sleep " + str(sleepTime) + " seconds.")
        time.sleep(sleepTime - timeTook)

        counter += 1

    db.close()


# Returns a hash using SHA256 algorithm and the current UNIX timestamp
# plus a random float number to add even more randomness to the timestamp
def getHash():
    data = time.time() + random.random() * 10000
    hashKey = hashlib.sha256()
    # The string object has to be encoded to UTF-8 due to hashing requisites
    hashKey.update(str(data).encode('utf-8'))
    return hashKey.hexdigest()


# inserts the @param key and @param value into the database
def insertIntoDB(cursor, values):
    insertString = "INSERT INTO " + CONST_DB_TABLENAME + " VALUES "
    insertString += ("(\"" + values[0] + "\", " + str(values[1]) + ")")

    iterValues = iter(values)
    next(iterValues)

    for v in iterValues:
        insertString += (", (\"" + v[0] + "\", " + str(v[1]) + ")")

    cursor.execute(insertString)


# gets the average from all the tuples in the database and returns it
def getAverage(cursor):
    cursor.execute("SELECT " + CONST_DB_NUM_COL_NAME + " FROM " + CONST_DB_TABLENAME)
    for row in cursor.fetchall():
        print(row[0])


# Tries connection to a DB in IP
def setupDatabase(ip):
    db = MySQLdb.connect(host=str(ip),
                         user=CONST_DB_USER,
                         passwd=CONST_DB_PASSWORD,
                         db=CONST_DB_NAME)
    db.autocommit(True)
    return db

# Starts connections to the other clients databases and stores the DBs in a list
def init_db_connections(startingIP, numClients):
    remote_dbs = []

    for i in range(1, numClients):
        remote_dbs.append(setupDatabase(startingIP + i))

    return remote_dbs

# Tests local database
def testDatabase():
    db = setupDatabase(CONST_DB_HOST)
    cursor = db.cursor()
    key = getHash()
    value = random.randint(CONST_MIN_NUM, CONST_MAX_NUM)
    insertIntoDB(cursor, [(key, value)])
    getAverage(cursor)
    sys.exit(0)

# conventional stuff, dont ask me.
if __name__ == '__main__':
    main(sys.argv)
