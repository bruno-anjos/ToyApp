import random
import time
import hashlib
import sys


CONST_USAGE = "Usage: [insertions per second] [averages per second] [timeout in seconds]"



def main(argv):

	#Feeds the random generator with the current UNIX timestamp as seed
	random.seed(time.time())

	if len(argv) != 4:
		print(CONST_USAGE)
		sys.exit(1)

	insertPerMin = argv[1]
	avgPerMin = argv[2]
	timeout = int(argv[3]) * 10000



	print("starting main loop")
	mainLoop(insertPerMin, avgPerMin, timeout)

	sys.exit(0)
	

# main script loop, logs start time and runs until timeout expires
# every x seconds will insert a tuple into the database
def mainLoop(insertPerMin, avgPerMin, timeout):

	startTime = time.time()

	while(True):

		if startTime - time.time() > timeout :
			break 




#Returns a hash using SHA256 algorithm and the current UNIX timestamp
#plus a random float number to add even more randomness to the timestamp
def getHash():
    data = time.time() + random.random() * 10000
    hashKey = hashlib.sha256()
    #The string object has to be encoded to UTF-8 due to hashing requisites
    hashKey.update(str(data).encode('utf-8'))
    return hashKey.hexdigest()

#generates a pseudo-random number between the specified ranges
def getNum(min, max):
    return random.randint(min, max)

#inserts the @param key and @param value into the database
def insertIntoDB(key, value):
	return None

# gets the average from all the tuples and returns it
def getAverage():
	return None


#conventional stuff, dont ask me.
if __name__ == '__main__':
	main(sys.argv)


