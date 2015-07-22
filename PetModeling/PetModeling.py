import random
import urllib, urllib2, json

# local url
#url = 'http://127.0.0.1:8080/petm/json/insert'
# server url
url = 'http://52.26.35.92:8080/petm/json/insert'

# startup variables
time = 0
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
    arch = open('probabilities.txt','r')
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
    auxTime = time

    # if current state is 'nap' define its next action based on a define range of probability
    if currentState == 0:
        if(randomValue < listProb[2]):
            nextState = 0
            time += 20
        elif(randomValue >= listProb[2] and randomValue < listProb[4]):
            nextState = 1
            time += 5
        else:
            nextState = 2
            time += 10
    # if current state is 'eat' define its next action based on a define range of probability
    elif currentState == 1:
        if(randomValue < listProb[2]):
            nextState = 0
            time += 20
        elif(randomValue >= listProb[2]and randomValue < listProb[3]):
            nextState = 1
            time += 5
        elif(randomValue >= listProb[3] and randomValue < listProb[5]):
            nextState = 1
            time += 10
        else:
            nextState = 3
            time += 3
    # if current state is 'eat' define its next action based on a define range of probability
    elif currentState == 2:
        if(randomValue < listProb[2]):
            nextState = 0
            time += 20
        elif(randomValue >= listProb[2] and randomValue < listProb[4]):
            nextState = 1
            time += 5
        else:
            nextState = 3
            time += 3
    # if current state is 'eat' define its next action based on a define range of probability
    elif currentState == 3:
        if(randomValue < listProb[0]):
            nextState = 0
            time += 20
        elif(randomValue >= listProb[0] and randomValue < listProb[1]):
            nextState = 1
            time += 5
        else:
            nextState = 2
            time += 10

    #actions.append(nextState)
    maxDict.append( { 'action':nextState, 'time':auxTime } )

    # when max time is reacher, break loop
    if(time >= 1440):
        break

'''We will transform action data to timed data'''

# We will play with the time between each action
timeDelta = 5 # in seconds
time = 0
index = 0

# loop until simulation time is over
while True:

    # get actions based on index
    auxObject = maxDict[index]

    # append item based on current action and time
    maxDictTime.append( { 'action':auxObject['action'], 'time':time } )

    # increase time
    time = time + 5

    # if sampled time has surpassed current action, iterate to following action
    if(time > auxObject['time']):
        index = index + 1

    # when max time is reacher, break loop
    if(time >= 1440):
        break

print("Finished")
#print actions
#print times
print (maxDict)
print (maxDictTime)
#print len(maxDict)

# json formatting
values = {
    'data' : maxDict
}

data = json.dumps(values)
clen = len(data)

'''

# make post request - upload data to the server
req = urllib2.Request(url, data, {'Content-Type': 'application/json', 'Content-Length': clen})
response = urllib2.urlopen(req)
print response.geturl()
print response.info()
the_page = response.read()
print the_page

'''