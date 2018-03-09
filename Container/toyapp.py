import random
import time
import hashlib
import sys
import MySQLdb

# CONST_USAGE = "Usage: [insertions per second] [averages per second] [timeout in seconds]"


CONST_USAGE = "Usage: [insertions per minute] [timeout in minutes]"
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

    if len(argv) != 3:
        print(CONST_USAGE)
        sys.exit(1)

    insertPerMin = argv[1]
    timeout = int(argv[2])

    print("Starting main loop")
    mainLoop(insertPerMin, timeout)

    sys.exit(0)


# Converts @param timesPerMin to how much time to wait in order to 
# have @param timesPerMin happen that many times per minute
def getSleepTime(timesPerMin):
    return 60 / int(timesPerMin)


# main script loop, logs start time and runs until timeout expires
# every x seconds will insert a tuple into the database
def mainLoop(insertPerMin, timeout):
    startTime = time.time()
    sleepTime = getSleepTime(insertPerMin)

    db = setupDatabase()
    cursor = db.cursor()

    while (True):
        key = getHash()
        value = random.randint(CONST_MIN_NUM, CONST_MAX_NUM)
        insertIntoDB(cursor, key, value)
        print("Inserted \"" + key + "\" with value " + str(value))

        print("Will sleep " + str(sleepTime) + " seconds.")
        time.sleep(sleepTime)
        if time.time() - startTime > timeout:
            break

    db.close()
    sys.exit(0)


# Returns a hash using SHA256 algorithm and the current UNIX timestamp
# plus a random float number to add even more randomness to the timestamp
def getHash():
    data = time.time() + random.random() * 10000
    hashKey = hashlib.sha256()
    # The string object has to be encoded to UTF-8 due to hashing requisites
    hashKey.update(str(data).encode('utf-8'))
    return hashKey.hexdigest()


# inserts the @param key and @param value into the database
def insertIntoDB(cursor, key, value):
    cursor.execute("INSERT INTO " + CONST_DB_TABLENAME + " VALUES (\"" + key + "\", " + str(value) + ")")


# gets the average from all the tuples in the database and returns it
def getAverage(cursor):
    cursor.execute("SELECT " + CONST_DB_NUM_COL_NAME + " FROM " + CONST_DB_TABLENAME)
    for row in cursor.fetchall():
        print(row[0])


# connects to the database
def setupDatabase():
    db = MySQLdb.connect(host=CONST_DB_HOST,
                         user=CONST_DB_USER,
                         passwd=CONST_DB_PASSWORD,
                         db=CONST_DB_NAME)
    db.autocommit(True)
    return db

def testDatabase():
    db = setupDatabase()
    cursor = db.cursor()
    key = getHash()
    value = random.randint(CONST_MIN_NUM, CONST_MAX_NUM)
    insertIntoDB(cursor, key, value)
    getAverage(cursor)
    sys.exit(0)

# conventional stuff, dont ask me.
if __name__ == '__main__':
    main(sys.argv)
