from collections import defaultdict
from util import printc, bcolors

def ccw(pin1, pin2, pin3):
    return (pin3[1] - pin1[1]) * (pin2[0] - pin1[0]) > (pin2[1] - pin1[1]) * (pin3[0] - pin1[0])

# the following function returns true if two bridges intersect
def intersect(bridge1, bridge2):
    pin11 = bridge1[0]
    pin12 = bridge1[1]
    pin21 = bridge2[0]
    pin22 = bridge2[1]
    return ccw(pin11, pin21, pin22) != ccw(pin12, pin21, pin22) and ccw(pin11, pin12, pin21) != ccw(pin11, pin12, pin22)

def copyDictDict(d):
    e = defaultdict(dict)
    for x in d:
        for y in d[x]:
            e[x][y] = d[x][y]
    return e

def copyDictInt(d):
    e = defaultdict(int)
    for x in d:
        e[x] = d[x]
    return e

def copyDictSet(d):
    e = defaultdict(set)
    for x in d:
        for y in d[x]:
            e[x].add(y)
    return e

def dotProduct(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]

def moveForward(direction, pin, neighbors):
    results = []
    for pin2 in neighbors:
        v = (pin[0] - pin2[0], pin[1] - pin2[1])
        x = dotProduct(direction, v)
        if x == 0:
            x = 1
            print "should not be here!"
        results.append(x/abs(x))
    if abs(sum(results)) == len(results):
        return True
    else:
        return False
    

class twixtBoard:
    def __init__(self, N):
        # size of the table, including the exclusive rows and columns
        self.N = N
        # the following two variables together represent the current state of the game
        # positions of the pins on the board
        self.pins = defaultdict(int)
        # last added pin
        self.lastAddedPin = [(0,0), (0,0)]
        # bridges placed on the table. remember to have both pin1: pin2 and pin2: pin1
        self.bridges = defaultdict(dict)
        # agent is either 0 or 1. agent 0 owns the top and bottom rows (0 and N-1)
        self.agent = 0
        # empty holes available on the main board
        self.boardActions = set()
        # empty holes available only to one of the players
        self.agentActions = defaultdict(set)
        # pin label
        self.label = defaultdict(int)
        # label assignment
        self.assignment = defaultdict(dict)
        # label counter
        self.counter = 0
        # running score
        self.runningScore = 0
        self.initializeActions()

    # this function initializes the actions lists
    def initializeActions(self):
        for i in range(1, self.N - 1):
            self.agentActions[1].add((i, 0))
            self.agentActions[1].add((i, self.N - 1))
            self.agentActions[0].add((0, i))
            self.agentActions[0].add((self.N - 1, i))
            for j in range(1, self.N - 1):
                self.boardActions.add((i, j))

    # remember that the state of the game is composed of both pins and bridges.
    # position of the pins on the board
    def getPins(self):
        return self.pins

    # position of the bridges on the board
    def getBridges(self):
        return self.bridges

    # returns whose turn it is
    def turnAgent(self):
        return self.agent

    # returns whether we are at the initial state
    def startState(self):
        return len(self.pins == 0) and len(self.bridges == 0)

    # returns the possible actions of the agent
    def getLegalAction(self, agent):
        return set(list(self.agentActions[agent]) + list(self.boardActions))

    # check this one+
    def bridgePossible(self, oldPin, newPin, agent):
        # check if the pins are valid
        if (oldPin not in self.pins) or newPin in self.pins:
            #print "invalid pins", oldPin, newPin
            return False
        # check if the bridge is already on the table
        if oldPin in self.bridges:
            if newPin in self.bridges[oldPin]:
                #print self.pins
                #print oldPin, newPin, "Bridge already on board"
                return False
        # check whether oldPin and newPin make a bridge
        if not ((abs(oldPin[0] - newPin[0]) == 1 and abs(oldPin[1] - newPin[1]) == 2) or (abs(oldPin[0] - newPin[0]) == 2 and abs(oldPin[1] - newPin[1]) == 1)):
            #print oldPin, newPin, "dont make a bridge"
            return False
        # check whether oldPin and newPin belong to the same agent
        if self.pins[oldPin] != agent:
            #print self.pins[oldPin], agent, "different agents"
            return False
        # the following four pins are all those which could potentially be one side of a conflicting bridge
        watchList = [(oldPin[0], newPin[1]), (newPin[0], oldPin[1])]
        if abs(oldPin[0] - newPin[0]) == 2:
            watchList.append(((oldPin[0] + newPin[0])/2, oldPin[1]))
            watchList.append(((oldPin[0] + newPin[0])/2, newPin[1]))
        else:
            watchList.append((oldPin[0], (oldPin[1] + newPin[1])/2))
            watchList.append((newPin[0], (oldPin[1] + newPin[1])/2))
        # check to see whether any bridges connected to the watchlist conflict
        for pin in watchList:
            if pin in self.bridges:
                otherPins = [x for x in self.bridges[pin]]
                for other in otherPins:
                    if intersect((pin, other), (oldPin, newPin)):
                        #print oldPin, newPin, "bridge conflict with", pin, otherpin
                        return False
        #print "all is cool"
        return True

    # returns the possible L-neighbors of a newly added pin
    def possibleNeighbors(self, pin):
        neighbors = []
        neighbors.append((pin[0] - 1, pin[1] - 2))
        neighbors.append((pin[0] - 1, pin[1] + 2))
        neighbors.append((pin[0] + 1, pin[1] - 2))
        neighbors.append((pin[0] + 1, pin[1] + 2))
        neighbors.append((pin[0] - 2, pin[1] - 1))
        neighbors.append((pin[0] - 2, pin[1] + 1))
        neighbors.append((pin[0] + 2, pin[1] - 1))
        neighbors.append((pin[0] + 2, pin[1] + 1))
        return neighbors
        
    # update board for every move
    def updateBoard(self, action):
        actions = self.getLegalAction(self.agent)
        if action not in actions:
            #print "Action not allowed!", action
            return
        if action in self.boardActions:
            self.boardActions.remove(action)
        else:
            self.agentActions[self.agent].remove(action)
        neighbors  = self.possibleNeighbors(action)
        bridges = []
        self.lastAddedPin[self.agent] = action
        for i in range(8):
            if self.bridgePossible(neighbors[i], action, self.agent):
                self.bridges[neighbors[i]][action] = self.agent
                self.bridges[action][neighbors[i]] = self.agent         
                bridges.append(neighbors[i])
        if len(bridges) == 0:
            self.label[action] = self.counter
            self.assignment[self.agent][self.counter] = self.counter
            self.counter += 1
        else:
            l = min([self.assignment[self.agent][self.label[x]] for x in bridges])
            self.label[action] = l
            for x in bridges:
                self.assignment[self.agent][self.label[x]] = l
        self.pins[action] = self.agent
        self.updateRunningScore()
        self.agent = 1 - self.agent

    def winner(self):
        assignments = [set(), set(), set(), set()]
        for i in range(1, self.N - 1):
            pins = [(0, i), (i, 0), (self.N - 1, i), (i, self.N - 1)]
            for j in range(4):
                if pins[j] in self.label:
                    assignments[j].add(self.assignment[j%2][self.label[pins[j]]])
        if len(assignments[0].intersection(assignments[2])) != 0:
            return 0
        if len(assignments[1].intersection(assignments[3])) != 0:
            return 1
        if len(self.pins) == self.N**2 - 4:
            return 2
        return -1

    def generateSuccessor(self, agent, action):
        newGame = twixtBoard(self.N)
        newGame.pins = copyDictInt(self.pins)
        newGame.bridges = copyDictDict(self.bridges)
        newGame.agent = agent
        newGame.boardActions = set(self.boardActions)
        newGame.agentActions = copyDictSet(self.agentActions)
        newGame.label = copyDictInt(self.label)
        newGame.assignment = copyDictDict(self.assignment)
        newGame.counter = self.counter
        newGame.runningScore = self.runningScore
        newGame.lastAddedPin = self.lastAddedPin[:]
        newGame.updateBoard(action)
        return newGame

    def getScore(self):
        scores = [set(), set()]
        for k,v in self.assignment[self.agent].iteritems():
            scores[self.agent].add(v);
        for k,v in self.assignment[1-self.agent].iteritems():
            scores[1-self.agent].add(v);
        return len(scores[1-self.agent])-len(scores[self.agent])

    # returns the set of adjacent pins (8 if possible)
    def getNeighbors(self, pin):
        neighbors = []
        change = [-1, 0, 1]
        for c1 in change:
            for c2 in change:
                pinTemp = (pin[0] + c1, pin[1] + c2)
                if pinTemp in self.pins and (c1 != 0 or c2 != 0):
                    neighbors.append(pinTemp)
        return neighbors
    
    # special pins making good strategic options
    def specialPins(self, agent, pin):
        special = []
        direction = (agent, 1-agent)
        # 2-step away pins are the first 6, 3-step away pins are the last 2
        change = [(direction[0] * 4, direction[1] * 4), (1 + direction[0] * 2, 1 + direction[1] * 2), (1 + direction[0] * 2, -(1 + direction[1] * 2)), (-4, -4), (-4, 4), (3, 3), (3, -3)]
        pins = []
        for c in change:
            pins.append((pin[0] + c[0], pin[1] + c[1]))
            pins.append((pin[0] - c[0], pin[1] - c[1]))
        for p in pins:
            if (p in self.pins) and ((pin not in self.bridges) or (p not in self.bridges[pin])):
                if self.pins[p] == agent:
                    special.append(p)
        return special

    # opponent opportunities reduced as a result of placing the new pin
    def oppLoss(self, agent, pin):
        newBridges = []
        for k, v in self.bridges[pin].iteritems():
            newBridges.append(k)
        return 0

    # pretty print
    def pprint(self):
        width = 4
        for i in range(self.N):
            for j in range(self.N):
                if (i == 0 or i == self.N-1) and (j == 0 or j == self.N-1):
                    print "%-*s" % (width, ""),
                else:
                    if (i,j) in self.label:
                        if self.label[(i,j)] in self.assignment[0]:
                            #printc("%-*s" % (width, assignments[0][labels[(i,j)]])),
                            if (i,j) in self.bridges:
                                printc('O', bcolors.OKBLUE, 'bold'),
                            else:
                                printc('O'),
                        elif self.label[(i,j)] in self.assignment[1]:
                            #printc("%-*s" % (width, assignments[1][labels[(i,j)]]), bcolors.FAIL),
                            if (i,j) in self.bridges:
                                printc('O', bcolors.FAIL, 'bold'),
                            else:
                                printc('O', bcolors.FAIL),
                    else:
                        print "%-*s" % (width, "x"),
                if j == self.N-1:
                    print "\n"



    def updateRunningScore(self):
        lastPin = self.lastAddedPin[self.agent]
        direction = (self.agent, 1 - self.agent)
        score = 0
        if abs(self.runningScore) == 10000000:
            return
        if self.winner() == self.agent:
            self.runningScore = 10000000
            return
        elif self.winner() == 1 - self.agent:
            self.runningScore = -10000000
            return

        if len(self.pins) == 1:
            score0 = 2 * self.N - 2 - (abs(self.lastAddedPin[0][0] - self.N/2.0) + abs(self.lastAddedPin[0][1] - self.N/2.0))
            self.runningScore += score0
        if len(self.pins) == 2:
            score1 = 2 * self.N - 2 - (abs(self.lastAddedPin[0][0] - self.N/2.0) + abs(self.lastAddedPin[0][1] - self.N/2.0)) - 2.0 * len(self.getNeighbors(lastPin))
            self.runningScore -= score1
        else:
            # distance one is bad
            score -= 1.0 * len(self.getNeighbors(lastPin))
            # special pins are good
            score += 2.0 * (len(self.specialPins(self.agent, lastPin)) != 0)
            # creating bridges is good if
            # 1. only one new pin has been created or,
            # 2. the new pin does not connect two pins already connected or,
            # 3. the new pin gets closer to either side of the board (good for the agent) than its neighbors
            if lastPin in self.bridges:
                # moving forward
                score += 2.0 * (moveForward(direction, lastPin, [pin for pin, val in self.bridges[lastPin].iteritems()]))
                # connecting points of different label
                score += 1.0 * (len(set([self.label[x] for x in self.bridges[pin]])) != 1)
                # making at least one connection
                score += 1.0 * (len(self.bridges[lastPin]) != 0)
            # reducing opponent possibilities is great
            #score += self.oppLoss(self.agent, lastPin)
            self.runningScore += (1 - 2 * self.agent) * score

    def getBestEval(self, queryAgent):
        score = []

        grid = []
        for i in range(self.N):
            for j in range(self.N):
                if j == 0:
                    grid.append([])
                grid[i].append(+float('inf'))

        for j in range(self.N):
            grid[0][j] = 0
        for i in range(1, self.N):
            for j in range(self.N):
                if (i, j) in self.bridges:
                    for pin, agent in self.bridges[(i, j)].iteritems():
                        if agent == 0:
                            grid[i][j] = min(grid[i][j], grid[i-1][j] + 1, grid[pin[0]][pin[1]])
                        else:
                            grid[i][j] = grid[i-1][j] + 1
                else:
                    grid[i][j] = grid[i-1][j] + 1

        score.append(min(grid[self.N - 1]))
        
        for i in range(self.N):
            for j in range(self.N):
                grid[i][j] = +float('inf')

        for i in range(self.N):
            grid[i][0] = 0
        for j in range(1, self.N):
            for i in range(self.N):
                if (i, j) in self.bridges:
                    for pin, agent in self.bridges[(i, j)].iteritems():
                        if agent == 1:
                            grid[i][j] = min(grid[i][j], grid[i][j-1] + 1, grid[pin[0]][pin[1]])
                        else:
                            grid[i][j] = grid[i][j-1] + 1
                else:
                    grid[i][j] = grid[i][j-1] + 1

        result = float('inf')
        for i in range(self.N):
            if grid[i][self.N-1] < result:
                result = grid[i][self.N-1]
        
        score.append(result)

        return score[1 - queryAgent] - score[queryAgent]

    # returns a better and more specialized score than getScore
    def getBetterScore(self): 
        return self.getBestEval() 
        # return self.runningScore
        
        
        
            
            
        

        
    
