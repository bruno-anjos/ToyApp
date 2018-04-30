import random
import time
import hashlib
import sys
import MySQLdb
import ipaddress
import socket
import gc
from collections import deque

# Constants used throught the program
CONST_USAGE = """Usage: python3 toyapp.py | insertions_per_minute | max_insertions |
                     number_of_clients | starting_ip | batch_size"""
CONST_DB_HOST = "localhost"
CONST_DB_USER = "username"
CONST_DB_PASSWORD = "password"
CONST_DB_NAME = "dummy_db"
CONST_DB_TABLENAME = "dummy_table"
CONST_DB_SYNCED_TABLENAME = "synced_table"
CONST_DB_NUM_COL_NAME = "num"
CONST_DB_SYNCED_COL_NAME = "synced"
CONST_DB_CONNECT_TIMEOUT = 4
CONST_ARG_FILE_NAME = "args.txt"

CONST_MIN_NUM = 1
CONST_MAX_NUM = 100

DEBUG_MODE = True
BASELINE_MODE = False

def main(argv):
    print("Starting toyapp")
    # Feeds the random generator with the current UNIX timestamp as seed
    random.seed(time.time())

    global DEBUG_MODE
    global BASELINE_MODE

    argv = argv[1::]


    if len(argv) < 5:
        argv = readArgsFromFile()
   
    if len(argv) < 5:
        print(CONST_USAGE)
        sys.exit(1)

    elif len(argv) == 5:

        DEBUG_MODE = True
        BASELINE_MODE = False
        

    elif len(argv) > 5:
        for arg in argv[5::]:
            if str(arg) == "debug":
                DEBUG_MODE = True
                print("debug mode ON")
                
            if str(arg) == "baseline":
                BASELINE_MODE = True
                print("Baseline mode ON")
    

    # Get starting parameters
    insertPerMin = int(argv[0])
    maxInsertions = int(argv[1])
    numClients = int(argv[2])
    startingIP = ipaddress.ip_address(argv[3])
    batchSize = int(argv[4])

    if DEBUG_MODE:
        print("[DEBUG] Starting main loop")
    mainLoop(insertPerMin, maxInsertions, numClients, startingIP, batchSize)

    sys.exit(0)



def readArgsFromFile():
    if DEBUG_MODE:
        print("[DEBUG] Reading args...")

    file = open(CONST_ARG_FILE_NAME, "r")
    args = file.read().split(" ")

    file.close()

    return args


# Converts @param timesPerMin to how much time to wait in order to 
# have @param timesPerMin happen that many times per minute
def getSleepTime(timesPerMin):
    return 60 / int(timesPerMin)


# main script loop, runs until it has inserted @arg maxInsertions tuples
# every x seconds will insert a tuple into the database
def mainLoop(insertPerMin, maxInsertions, numClients, startingIP, batchSize):
    startTime = time.time()
    sleepTime = getSleepTime(insertPerMin)

    if DEBUG_MODE:
        print("[DEBUG] Sleep time between insertions: " + str(sleepTime))

    counter = 0

    db = setupDatabase(CONST_DB_HOST)
    master_node = False

    if get_ip_address() == startingIP:
        print("[DEBUG] This is master node")
        master_node = True
        masterDB = db
    else:
        print("[DEBUG] Master node is " + str(startingIP))
        masterDB = setupDatabase(startingIP)

    ip_list = build_ip_list(startingIP, numClients)

    if DEBUG_MODE:
        print("[DEBUG] IP List: " + str(ip_list))

    remote_dbs = init_db_connections(numClients, ip_list)

    if DEBUG_MODE:
        print("[DEBUG] Remote connections: " + str(remote_dbs))

    queuedInserts = deque([])

    # Guarantees everyone is synced
    if DEBUG_MODE:
        print("[DEBUG] Starting sync phase...")
        sync_dbs(masterDB, numClients)
        print("[DEBUG] Synced.")

    while counter < maxInsertions:
        # Gets data to insert
        key = getHash()
        value = random.randint(CONST_MIN_NUM, CONST_MAX_NUM)

        # Inserts in local DB
        insertionTime = time.time()
        insertIntoDB(db.cursor(), [(key, value)])
        afterInsertionTime = time.time()
        timeTook = afterInsertionTime - insertionTime
        if DEBUG_MODE:
            print("[DEBUG] Inserted \"" + key + "\" with value " + str(value) + " and took " + str(
                round(timeTook, 2)) + " seconds")

        if not BASELINE_MODE:
            # Adds to queue
            queuedInserts.append((key, value))

            # Checks if need to flush queue to remote DBs
            if len(queuedInserts) >= batchSize:
                insertionTime = time.time()
                for rdb in remote_dbs:
                    insertIntoDB(rdb.cursor(), queuedInserts)
                afterInsertionTime = time.time()
                while queuedInserts:
                    queuedInserts.pop()
                if DEBUG_MODE:
                    print("[DEBUG] Took " + str(
                        afterInsertionTime - insertionTime) + " seconds to insert in remote databases.")

        # Sleeps remaining time
        if DEBUG_MODE:
            print("[DEBUG] Will sleep " + str(sleepTime - timeTook) + " seconds.")
        if sleepTime - timeTook < 0:
            print("[DEBUG] can't keep up!, late by " + str(sleepTime - timeTook) + " ms")
        else:
            time.sleep(sleepTime - timeTook)
        counter += 1

    if len(queuedInserts) > 0:
        for rdb in remote_dbs:
            insertIntoDB(rdb.cursor(), queuedInserts)

    if DEBUG_MODE:
        print("[DEBUG] Closing DB connections.")

    closeConnections(remote_dbs, masterDB , master_node)

    endTime = time.time()
    runningTime = endTime - startTime

    if DEBUG_MODE:
        print("[DEBUG] Closing Toy App. App ran for " + str(runningTime) + " seconds.")

    localCursor = db.cursor()

    writeStatsToFile(runningTime, getAverage(localCursor) , getDatabaseSize(localCursor))

    localCursor.close()
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
    sum_col = 0
    counter = 0
    for row in cursor.fetchall():
        sum_col += row[0]
        counter+= 1
    avg = sum_col / counter

    print("Sum is: " + str(sum_col))
    print("Row count is: " + str(counter))
    print("Average is: " + str(avg))

    return avg

def getDatabaseSize(cursor):
    query = '''SELECT table_schema "DB Name",
        ROUND(SUM(data_length + index_length) / 1024 / 1024, 1) "DB Size in MB" 
        FROM information_schema.tables 
        GROUP BY table_schema; '''
    cursor.execute(query)
    size = cursor.fetchone()

    if DEBUG_MODE:
        print("[DEBUG] Database size in MB is: " + str(size[1]))
    return str(size[1])




def writeStatsToFile(runningTime, avg , sizeDB):
    if DEBUG_MODE:
        print("[DEBUG] Writing stats to file...")

    statsFile = open("/log/" + socket.gethostname(), "w")
    statsFile.write("Ran for " + str(runningTime) + " seconds\n")
    statsFile.write("Average in DB is " + str(avg) + "\n")
    statsFile.write("Database size in MB is " + str(sizeDB) + "\n")

    if DEBUG_MODE:
        print("[DEBUG] Finished writing stats to file " + statsFile.name)

    statsFile.close()

# Tries connection to a DB in IP
def setupDatabase(ip):
    success = False
    db = None
    while not success:
        try:
            if DEBUG_MODE:
                print("[DEBUG] Will try to connect to " + str(ip))
            db = MySQLdb.connect(host=str(ip),
                                 user=CONST_DB_USER,
                                 passwd=CONST_DB_PASSWORD,
                                 db=CONST_DB_NAME,
                                 connect_timeout=CONST_DB_CONNECT_TIMEOUT)
            db.autocommit(True)
            success = True
        except MySQLdb.OperationalError:
            if DEBUG_MODE:
                print("[DEBUG] Failed to connect to " + str(ip))
            time.sleep(2)
            continue

    return db


# Starts connections to the other clients databases and stores the DBs in a list
def init_db_connections(numClients, ip_list):
    remote_dbs = []

    for i in range(1, numClients):
        db = setupDatabase(ip_list[i - 1])
        remote_dbs.append(db)

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


def closeConnections(remote_dbs, masterDB , master_node):
    synced = False

    deleteString = "DELETE FROM " + CONST_DB_SYNCED_TABLENAME + " WHERE " + CONST_DB_SYNCED_COL_NAME + " = " + "\'" + str(get_ip_address()) + "\'"

    cursor = masterDB.cursor()
    cursor.execute(deleteString)

    while not synced:
        cursor.execute("SELECT " + CONST_DB_NUM_COL_NAME + " FROM " + CONST_DB_SYNCED_TABLENAME)
        fetchedValues = cursor.fetchall()

        if DEBUG_MODE:
            print("[DEBUG] Current value in DB sync field: " + str(len(fetchedValues)))
        if len(fetchedValues) == 0:
            synced = True
            if master_node:
                time.sleep(10)
        else:
            time.sleep(0.2)

    #close all remote connections first
    for rdb in remote_dbs:
        try:
            rdb_cursor = rdb.cursor()
            rdb_cursor.close()
            rdb.close()
        except MySQLdb.OperationalError:
            print("[DEBUG] DB already closed")

    # there might be cursors laying around, calling garbage collector just to be safe
    gc.collect()


# Syncs the clients to guarantee that all the databases are initiated
def sync_dbs(masterDB, numClients):
    synced = False

    # Query used to update the synced value in remote databases
    insertString = "INSERT INTO " + CONST_DB_SYNCED_TABLENAME + " VALUES "
    insertString += ("(\"" + str(get_ip_address()) + "\", " + str(1) + ")")

    # Guarantees transaction isolation level allows the correct read
    cursor = masterDB.cursor()
    cursor.execute("set session transaction isolation level read committed")

    # Insert in local database
    cursor.execute(insertString)

    while not synced:
        cursor.execute("SELECT " + CONST_DB_NUM_COL_NAME + " FROM " + CONST_DB_SYNCED_TABLENAME)
        fetchedValues = cursor.fetchall()

        if DEBUG_MODE:
            print("[DEBUG] Current value in DB sync field: " + str(len(fetchedValues)))
        if len(fetchedValues) == numClients:
            synced = True
        else:
            time.sleep(2)


# Gets own IP address
def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((startingIP, 8080))
        ip = ipaddress.ip_address(s.getsockname()[0])
        if DEBUG_MODE:
            print("[DEBUG] Host IP: " + str(ip))
        s.close()
    except OSError:
    	if DEBUG_MODE:
    		print("[DEBUG] got OSError")
        ip = socket.gethostbyname(socket.gethostname())
        if(DEBUG_MODE):
            print("[DEBUG] Host IP: " + str(ip))
        return ip
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
