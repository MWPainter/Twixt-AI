import twixt


######################################################################################
## implementing minimax

class MinimaxAgent(object):

	def __init__(self, depth = '2'):
		self.index = 0
		self.depth = int(depth)


	def evaluationFunction(self, currentGameState):
		return currentGameState.getScore()

	def getAction(self, gameState):

		def oppMove(gameState, currentDepth):

			legalMoves = gameState.getLegalAction(gameState.agent)
			if legalMoves == set([]):
				return (self.evaluationFunction(gameState), None)

			optimalScoreActionPair = (float('inf'), None)
			for action in legalMoves:
				score, optimalAction = agentMove(gameState.generateSuccessor(gameState.agent, action), currentDepth-1)
				if score < optimalScoreActionPair[0]:
					optimalScoreActionPair = (score, action)

                        return optimalScoreActionPair

                def agentMove(gameState, currentDepth):

			if (currentDepth == 0):
				return (self.evaluationFunction(gameState), None)

			legalMoves = gameState.getLegalAction(gameState.agent)
			print legalMoves
			if legalMoves == set([]):
				return (self.evaluationFunction(gameState), None)

			optimalScoreActionPair = (-float('inf'), None)
			for action in legalMoves:
				score, optimalAction = oppMove(gameState.generateSuccessor(gameState.agent, action), currentDepth)        
				if score > optimalScoreActionPair[0]:
					optimalScoreActionPair = (score, action)

			return optimalScoreActionPair

                ## function implementaiton starts here
                return agentMove(gameState, self.depth)[1]

    # END_YOUR_CODE
