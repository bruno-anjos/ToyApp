import random
import time
import hashlib
import sys

import MySQLdb
import ipaddress
import socket
from collections import deque

# Constants used throught the program
CONST_USAGE = "Usage: python3 toyapp.py [insertions per minute] [max insertions] [number of clients] [starting ip] [batch size]"
CONST_DB_HOST = "localhost"
CONST_DB_USER = "username"
CONST_DB_PASSWORD = "password"
CONST_DB_NAME = "dummy_db"
CONST_DB_TABLENAME = "dummy_table"
CONST_DB_SYNCED_TABLENAME = "synced_table"
CONST_DB_NUM_COL_NAME = "num"
CONST_DB_SYNCED_COL_NAME = "synced"

CONST_MIN_NUM = 1
CONST_MAX_NUM = 100



def main(argv):

    print("Starting toyapp")
    # Feeds the random generator with the current UNIX timestamp as seed
    random.seed(time.time())

    #testDatabase()

    if len(argv) != 6:
        print(argv)
        print(CONST_USAGE)
        sys.exit(1)

    # Get starting parameters
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
def mainLoop(insertPerMin, maxInsertions, numClients, startingIP, batchSize):
    startTime = time.time()
    sleepTime = getSleepTime(insertPerMin)
    counter = 0
    db = setupDatabase(CONST_DB_HOST)
    ip_list = build_ip_list(startingIP, numClients)
    remote_dbs = init_db_connections(startingIP, numClients, ip_list)
    print("Remote connections: " + str(remote_dbs))
    queuedInserts = deque([])

    # Guarantees everyone is synced
    sync_dbs(db, numClients, remote_dbs)

    while counter < maxInsertions:
        # Gets data to insert
        key = getHash()
        value = random.randint(CONST_MIN_NUM, CONST_MAX_NUM)

        # Inserts in local DB
        insertionTime = time.time()
        insertIntoDB(db.cursor(), [(key, value)])
        afterInsertionTime = time.time()
        timeTook = afterInsertionTime - insertionTime
        print("Inserted \"" + key + "\" with value " + str(value) + " and took " + str(round(timeTook, 2)) + " seconds")

        # Adds to queue
        queuedInserts.append((key, value))

        # Checks if need to flush queue to remote DBs
        if len(queuedInserts) == batchSize:
            insertionTime = time.time()
            for rdb in remote_dbs:
                insertIntoDB(rdb.cursor(), queuedInserts)
            afterInsertionTime = time.time()
            while queuedInserts:
                queuedInserts.pop()
            print("Took " + str(afterInsertionTime - insertionTime) + " seconds to insert in remote databases.")

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
    insertString += ("(\"" + str(values[0][0]) + "\", " + str(values[0][1]) + ")")

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
def init_db_connections(startingIP, numClients, ip_list):
    remote_dbs = []

    for i in range(1, numClients):
        remote_dbs.append(setupDatabase(ip_list[i-1]))

    return remote_dbs

# Builds a list with the other clients IPs (this only works based on an incremental IP system)
def build_ip_list(startingIP, numClients):
    localIP = get_ip_address()
    ip_list = []

    # Inserts all IPs except own IP
    for i in range(0, numClients):
        if (startingIP + i) == localIP:
            continue
        else:
            ip_list.append(startingIP + i)

    return ip_list


# Syncs the clients to guarantee that all the databases are initiated
def sync_dbs(db, numClients, remote_dbs):
    synced = False
    num = 0

    # Query used to update the synced value in remote databases
    insertString = "INSERT INTO " + CONST_DB_SYNCED_TABLENAME + " VALUES "
    insertString += ("(\"synced\", " + str(1) + ")")
    updateString = CONST_DB_NUM_COL_NAME + "=" + CONST_DB_NUM_COL_NAME + "+1"

    # Guarantees transaction isolation level allows the correct read
    cursor = db.cursor()
    cursor.execute("set session transaction isolation level read committed")

    cursor.execute("SELECT " + CONST_DB_NUM_COL_NAME + " FROM " + CONST_DB_SYNCED_TABLENAME)
    fetchedValues = cursor.fetchall();

    # Insert in local database
    print("Decision: " + str(fetchedValues))
    if len(fetchedValues) > 0 and len(fetchedValues[0]) > 0 and fetchedValues[0][0] > 0:
        cursor.execute("UPDATE " + CONST_DB_SYNCED_TABLENAME + " SET " + updateString + " WHERE " + CONST_DB_SYNCED_COL_NAME + "=\"" + CONST_DB_SYNCED_COL_NAME + "\"")
    else :
        cursor.execute(insertString)

    # Updates value in remote databases
    for rdb in remote_dbs:
        rdb_cursor = rdb.cursor();
        rdb_cursor.execute("set session transaction isolation level read committed")
        rdb_cursor.execute("SELECT " + CONST_DB_NUM_COL_NAME + " FROM " + CONST_DB_SYNCED_TABLENAME)
        fetchedValues = rdb_cursor.fetchall();
        if len(fetchedValues) > 0 and len(fetchedValues[0]) > 0 and fetchedValues[0][0] > 0:
            rdb_cursor.execute("UPDATE " + CONST_DB_SYNCED_TABLENAME + " SET " + updateString + " WHERE " + CONST_DB_SYNCED_COL_NAME + "=\"" + CONST_DB_SYNCED_COL_NAME + "\"")
        else:
            rdb_cursor.execute(insertString)

    # Waits till current synced value gets incremented by all other clients. Checks every second.
    while not synced:
        cursor.execute("SELECT " + CONST_DB_NUM_COL_NAME + " FROM " + CONST_DB_SYNCED_TABLENAME)
        fetchedValues = cursor.fetchall()
        print(fetchedValues)
        if len(fetchedValues) > 0 and len(fetchedValues[0]) > 0:
            num = fetchedValues[0][0]
            print(str(num))
        if num == numClients:
            synced = True
        else:
            time.sleep(1)


# Gets own IP address
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = ipaddress.ip_address(s.getsockname()[0])
    s.close()
    return ip

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
