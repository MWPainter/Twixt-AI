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
