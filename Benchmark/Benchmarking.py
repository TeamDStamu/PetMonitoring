import random
import urllib, urllib2, json
import time
import sys, os

# local url
#url = 'http://127.0.0.1:8080/petm/json/insert'
# server url
url = 'http://52.26.35.92:8080/petm/json/insert'

# startup variables
timeInt = 0
auxTime = 0
nextState = 0
currentState = 0
index = 0
randomValue = 0.0
auxPos=0
listProb = []

'''
actions = []
times = []
'''

# action array
maxDict = []

# timed actions array
maxDictTime = []

# load probabilities from a .txt file
def readDoc():
    #os.path.dirname(os.path.realpath(__file__))
    arch = open(os.path.join(sys.path[0], "probabilities.txt"), "r")
    #arch = open('probabilities.txt','r')
    for line in arch:
        listProb.append(float(line.strip('\n')))

readDoc()

print "Starting"

# loop until simulation time is over
while True:
    #Random Value defines probability 0 - 0.99
    randomValue = random.random()

    #Based on last state we will determine our probability for the next one
    currentState = nextState

    #times.append(time)
    auxTime = timeInt

    # if current state is 'nap' define its next action based on a define range of probability
    if currentState == 0:
        if(randomValue < listProb[2]):
            nextState = 0
            timeInt += 20
        elif(randomValue >= listProb[2] and randomValue < listProb[4]):
            nextState = 1
            timeInt += 5
        else:
            nextState = 2
            timeInt += 10
    # if current state is 'eat' define its next action based on a define range of probability
    elif currentState == 1:
        if(randomValue < listProb[2]):
            nextState = 0
            timeInt += 20
        elif(randomValue >= listProb[2]and randomValue < listProb[3]):
            nextState = 1
            timeInt += 5
        elif(randomValue >= listProb[3] and randomValue < listProb[5]):
            nextState = 1
            timeInt += 10
        else:
            nextState = 3
            timeInt += 3
    # if current state is 'eat' define its next action based on a define range of probability
    elif currentState == 2:
        if(randomValue < listProb[2]):
            nextState = 0
            timeInt += 20
        elif(randomValue >= listProb[2] and randomValue < listProb[4]):
            nextState = 1
            timeInt += 5
        else:
            nextState = 3
            timeInt += 3
    # if current state is 'eat' define its next action based on a define range of probability
    elif currentState == 3:
        if(randomValue < listProb[0]):
            nextState = 0
            timeInt += 20
        elif(randomValue >= listProb[0] and randomValue < listProb[1]):
            nextState = 1
            timeInt += 5
        else:
            nextState = 2
            timeInt += 10

    #actions.append(nextState)
    maxDict.append( { 'action':nextState, 'time':auxTime } )

    # when max time is reacher, break loop
    if(timeInt >= 1440):
        break

'''We will transform action data to timed data'''

# We will play with the time between each action
timeDelta = 5 # in seconds
timeInt = 0
index = 0

# loop until simulation time is over
while True:

    if(index < len(maxDict)):
        # get actions based on index
        auxObject = maxDict[index]
    else:
        auxObject = { 'action':0, 'time':timeInt }

    # append item based on current action and time
    maxDictTime.append( { 'action':auxObject['action'], 'time':timeInt } )

    # increase time
    timeInt = timeInt + 10

    # if sampled time has surpassed current action, iterate to following action
    if(timeInt > auxObject['time']):
        index = index + 1

    # when max time is reacher, break loop
    if(timeInt >= 1440):
        break

print("Finished")
#print actions
#print times
#print (maxDict)
#print (maxDictTime)
#print len(maxDictTime)

# json formatting
values = {
    'data' : maxDictTime
}

data = json.dumps(values)
clen = len(data)

# milliseconds
millis = time.time() * 1000

# number of operations
n = 1000

for y in range(0, 50):
    for x in range(0, n):
        # make post request - upload data to the server
        req = urllib2.Request(url, data, {'Content-Type': 'application/json', 'Content-Length': clen})
        response = urllib2.urlopen(req)
        the_page = response.read()

    if(n >= 100):
        print "still alive"

#milliseconds
millis2 = time.time() * 1000

# print time required to make n operations (in milliseconds)
millisDiff = millis2 - millis
millisDiff = millisDiff / 50

print millisDiff

'''

# make post request - upload data to the server
req = urllib2.Request(url, data, {'Content-Type': 'application/json', 'Content-Length': clen})
response = urllib2.urlopen(req)
print response.geturl()
print response.info()
the_page = response.read()
print the_page

'''