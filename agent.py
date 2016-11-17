import twixt

class MultiAgentSearchAgent(Object):

	def __init__(self, depth = '2'):
		self.index = 0
		self.depth = int(depth)

######################################################################################
## implementing minimax

class MinimaxAgent(MultiAgentSearchAgent):

	self.evaluationFunction = evaluationFunction

	def evaluationFunction(self, currentGameState):
		return currentGameState.getScore()

	def getAction(self, gameState):

		def oppMove(gameState, agentIndex, currentDepth):

			legalMoves = gameState.getLegalActions(agentIndex)
			if legalMoves == []:
				return (self.evaluationFunction(gameState), None)

			optimalScoreActionPair = (float('inf'), None)
			for action in legalMoves:
				score, optimalAction = agentMove(gameState.generateSuccessor(agentIndex, action), 1-agentIndex, currentDepth-1)
				if score < optimalScoreActionPair[0]:
					optimalScoreActionPair = (score, action)

		return optimalScoreActionPair

	def agentMove(gameState, agentIndex, currentDepth):

			if (currentDepth == 0):
				return (self.evaluationFunction(gameState), None)

			legalMoves = gameState.getLegalActions(agentIndex)
			if legalMoves == []:
				return (self.evaluationFunction(gameState), None)

			optimalScoreActionPair = (-float('inf'), None)
			for action in legalMoves:
				score, ghostAction = oppMove(gameState.generateSuccessor(agentIndex, action), 1-agentIndex, currentDepth)        
				if score > optimalScoreActionPair[0]:
					optimalScoreActionPair = (score, action)

			return optimalScoreActionPair

	## function implementaiton starts here
	return agentMove(gameState, agentIndex = 0, self.depth)[1]

    # END_YOUR_CODE