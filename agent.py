from collections import defaultdict
import random, operator
import twixt

class HumanAgent(object):
	def __init__(self, agentIndex):
		self.index = agentIndex

	def getAction(self, gameState):
		while True:
			print 'Enter x:',
			x = raw_input().strip()
			print 'Enter y:',
			y = raw_input().strip()
			if (int(x), int(y)) in gameState.getLegalAction(self.index):
                print "Please enter valid move"
				break
		return (int(x), int(y))

class MinimaxAgent(object):
	def __init__(self, depth = '2'):
		self.depth = int(depth)

	def evaluationFunction(self, currentGameState):
		return currentGameState.getBestEval(currentGameState.agent)

	def getAction(self, gameState):

		def oppMove(gameState, currentDepth, alpha, beta):

			if (gameState.winner() >= 0):
				gameState.agent = 1 - gameState.agent
				return (self.evaluationFunction(gameState), None, self.depth - currentDepth)
			
			legalMoves = gameState.getLegalAction(gameState.agent)
			if legalMoves == set([]):
				return (self.evaluationFunction(gameState), None, self.depth)
	    
			optimalScoreActionPair = (float('inf'), None, None)
			for action in legalMoves:
				score, optimalAction, endDepth = agentMove(gameState.generateSuccessor(gameState.agent, action), currentDepth-1, alpha, beta)
				
				if score < optimalScoreActionPair[0] or (score == optimalScoreActionPair[0] and endDepth < optimalScoreActionPair[2]):
					optimalScoreActionPair = (score, action, endDepth)
				if score < beta:
					beta = score
				if alpha >= beta:
					break

			return optimalScoreActionPair

		def agentMove(gameState, currentDepth, alpha, beta):

			if (currentDepth == 0) or (gameState.winner() >= 0):
				return (self.evaluationFunction(gameState), None, self.depth - currentDepth)
            
			legalMoves = gameState.getLegalAction(gameState.agent)
			if legalMoves == set([]):
				return (self.evaluationFunction(gameState), None, self.depth)
	    
			optimalScoreActionPair = (-float('inf'), None, None)
			for action in legalMoves:
				score, optimalAction, endDepth = oppMove(gameState.generateSuccessor(gameState.agent, action), currentDepth, alpha, beta)

				if score > optimalScoreActionPair[0] or (score == optimalScoreActionPair[0] and endDepth < optimalScoreActionPair[2]):
					optimalScoreActionPair = (score, action, endDepth)
				if score > alpha:
					alpha = score
				if alpha >= beta:
					break
	    		
			return optimalScoreActionPair

		return agentMove(gameState, self.depth, -float('inf'), float('inf'))[1]

class MaximinAgent(object):
	def __init__(self, depth = '2'):
		self.depth = int(depth)

	def evaluationFunction(self, currentGameState):
		return currentGameState.getBestEval(currentGameState.agent)

	def getAction(self, gameState):

		def agentMove(gameState, currentDepth, alpha, beta):

			if (currentDepth == 0) or (gameState.winner() >= 0):
				return (self.evaluationFunction(gameState), None)
	
			legalMoves = gameState.getLegalAction(gameState.agent)
			if legalMoves == set([]):
				return (self.evaluationFunction(gameState), None)
	    
			optimalScoreActionPair = (float('inf'), None)
			for action in legalMoves:
				score, optimalAction = oppMove(gameState.generateSuccessor(gameState.agent, action), currentDepth, alpha, beta)
				
				if score < optimalScoreActionPair[0]:
					optimalScoreActionPair = (score, action)
				if score < beta:
					beta = score
				if alpha >= beta:
					break

			return optimalScoreActionPair

		def oppMove(gameState, currentDepth, alpha, beta):

			if (gameState.winner() >= 0):
				gameState.agent = 1 - gameState.agent
				return (self.evaluationFunction(gameState), None)

			legalMoves = gameState.getLegalAction(gameState.agent)
			if legalMoves == set([]):
				return (self.evaluationFunction(gameState), None)
	    
			optimalScoreActionPair = (-float('inf'), None)
			for action in legalMoves:
				score, optimalAction = agentMove(gameState.generateSuccessor(gameState.agent, action), currentDepth-1, alpha, beta)

				if score > optimalScoreActionPair[0]:
					optimalScoreActionPair = (score, action)
				if score > alpha:
					alpha = score
				if alpha >= beta:
					break
	    
			return optimalScoreActionPair

		return agentMove(gameState, self.depth, -float('inf'), float('inf'))[1]

class ExpectimaxAgent(object):

	def __init__(self, depth = '2'):
		self.depth = int(depth)

	def evaluationFunction(self, currentGameState):
		return currentGameState.getBetterScore()

	def getAction(self, gameState):

		def oppMove(gameState, currentDepth, alpha, beta):

			if (gameState.winner() >= 0):
				return (self.evaluationFunction(gameState), None)
			
			legalMoves = gameState.getLegalAction(gameState.agent)
			if legalMoves == set([]):
				return (self.evaluationFunction(gameState), None)
	    
			optimalScoreActionPair = (float('inf'), None)
			randScore = 0
			for action in legalMoves:
				score, optimalAction = agentMove(gameState.generateSuccessor(gameState.agent, action), currentDepth-1, alpha, beta)
				randScore = randScore + score

      			return (randScore/float(len(legalMoves)), None)

		def agentMove(gameState, currentDepth, alpha, beta):

			if (currentDepth == 0) or (gameState.winner() >= 0):
				return (self.evaluationFunction(gameState), None)
            
			legalMoves = gameState.getLegalAction(gameState.agent)
			if legalMoves == set([]):
				return (self.evaluationFunction(gameState), None)
	    
			optimalScoreActionPair = (-float('inf'), None)
			for action in legalMoves:
				score, optimalAction = oppMove(gameState.generateSuccessor(gameState.agent, action), currentDepth, alpha, beta)

				if score > optimalScoreActionPair[0]:
					optimalScoreActionPair = (score, action)
				if score > alpha:
					alpha = score
				if alpha >= beta:
					break
	    		
			return optimalScoreActionPair

		return agentMove(gameState, self.depth, -float('inf'), float('inf'))[1]

class PureMCAgent(object):

	def __init__(self, iter = '50000'):
		self.iter = int(iter)

	def getAction(self, gameState):
		actionCounts = defaultdict(int)
		legalActions = gameState.getLegalAction(gameState.agent)

		for i in range(self.iter):
			firstAction = random.sample(legalActions, 1)[0]
			mc = gameState.generateSuccessor(gameState.agent, firstAction)
			
			if mc.winner() == gameState.agent:
				actionCounts[firstAction] = actionCounts[firstAction]+1
				continue

			while mc.winner() == -1 and len(mc.getLegalAction(mc.agent)) > 0:
				action = random.sample(mc.getLegalAction(mc.agent), 1)[0]
				mc.updateBoard(action)
			if mc.winner() == gameState.agent:
				actionCounts[firstAction] = actionCounts[firstAction]+1

		if len(actionCounts) == 0:
			return firstAction
		else:
			return max(actionCounts.iteritems(), key=operator.itemgetter(1))[0]



class TreeNode(object):
    def __init__(self, state, weight, parent = None):
        self.state = state # state being represented as this 
        self.value = 0 # average value witnessed at this state
        self.numVisits = 0 # times visited node
        self.children = [] # list of (action, successor tree node) pairs
        self.isLeaf = True # true if tree node is a leaf (self.children == empty list currently)
        self.weight = weight # weight of selecting this node from parent originally
        self.parent = self # pointer to parent, if pointer is to self then root node

    def witnessValue(value):
        """
        Updates the average value (running avg) according to this instance of value we are witnessing
        This incremenets the number of time's we've visited the node also

        :param value: the value we witnesses as a result of playing the game through this node
        :return: None
        """
        self.numVisits += 1
        n = self.numVisits
        self.value = (value + (n-1) * self.value) / n 

    def getWeight(self):
        """
        Returns the original weighting, but decays accoring to the ammount we 
        have explored, where if w is the original weight, and n is the number of 
        times we have visited this state, we return (w/1+n)

        N.B. other weightDecay methods exist and work, arbitrarily following alphaGo here
        """
        return self.weight / (1 + self.numVisits)

    def getSuccInTree(self, action):
        #TODO: Select a successor according to an action given
        #TODO: This needs return none if the successor doesn't exist in tree

    def getSuccAfterExpand(self, action):
        if self.children == []: raise Exception("Called 'TreeNode.getSuccAfterExpand' either on a end state of the game or without calling expand before")
        #TODO: Gets a successor AFTER the node has been expanded
        #TODO: This means that numVisits == 0 is fair game now, and successor list isn't empty

    def forState(self, state):
        """
        Returns if this is a tree node for the state 'state'

        :param state: the state
        :return: true if self.state is equal to state
        """
        #TODO: Implement state equality
        return self.state == state

    def __eq__(self, other):
        """
        Computes if self == other

        :param other: another TreeNode object
        :return: true if TreeNodes are considered equal
        """
        return self.state == other.state

    def __ne__(self, other):
        """
        Computes if self != other

        :param other: another TreeNode object
        :return: true if TreeNodes are considered not equal
        """
        return not self == other



class MCTreeSearch(object):
    def __init__(self, iter='50000', selectionPolicy, simulationPolicy, simulationDepth = 0, evalFn = None):
        """
        :param iter: Number of iterations for each 'getAction' search
        :param selectonPolicy: Stochastic policy used for selecting nodes to expand, takes a 
            state as an argument and returns a list of (action, weight) pairs
        :param simulationPolicy: Stochastic policy used for simulating a game
        :param simulationDepth: depth to simulate to, default 0 means no max depth
        :param evalFn: evaluation function from states to some value, only used if simulationDepth > 0
        """
        self.iter = int(iter)
        self.selPolicy = selectionPolicy
        self.simPolicy = simulationPolicy
        self.simDepth = simulationDepth
        self.eval = evalFn

	def getAction(self, gameState):
        """
        Returns the action accodring to a monte carlo tree search. It makes a root node 
        from the given state, then repeats the 4 stages of MCTS, and finally extracts the 
        optimal action from the root node and it's successors.

        4 stages: Selection, Expansion, Simulation, Backpropogation

        In this implementation expansion is split into two phases. Usually expansion consists 
        of selection until we find a state not cached in the tree, we add that one node. 
        Here we wish to explore according to a policy 'selectionPolicy', so we add all successors 
        to the cache tree at once, we then 'walk the tree' again, which will just select one of 
        the successors. This creates a need to identify nodes with 'numVisits' of 0 as having 
        not been added yet. This implementation detail is dealt with in 'getSuccInTree(action)'
        
        :param gameState: The current state of the game
        :return: The action leading to the best (avg) reward from the search
        """
        rootNode = makeTree(gameState)
        for i in range(self.iter):
            leafNode = self.walkTree(rootNode) # selection
            self.expand(leafState) # expansion1
            newLeafState = leafNode.step(policy) # expansion2: select one of the new children
            value = self.simulate(newLeafState) # simulation
            self.backPropogation(newLeafState, value) #back propocation

        optAction = None
        optValue = -int('inf')
        for (action, childNode) in rootNode.children:
            if childNode.value > optValue:
                optAction = action
                optValue = childNode.value

        return optAction






