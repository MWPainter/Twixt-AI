import twixt

class MinimaxAgent(object):
	def __init__(self, depth = '2'):
		self.index = 0
		self.depth = int(depth)

	def evaluationFunction(self, currentGameState):
		return currentGameState.getBetterScore()

	def getAction(self, gameState):

		def oppMove(gameState, currentDepth, alpha, beta):
	
			legalMoves = gameState.getLegalAction(gameState.agent)
			if legalMoves == set([]):
				return (self.evaluationFunction(gameState), None)
	    
			optimalScoreActionPair = (float('inf'), None)
			for action in legalMoves:
				score, optimalAction = agentMove(gameState.generateSuccessor(gameState.agent, action), currentDepth-1, alpha, beta)
				
				if score < optimalScoreActionPair[0]:
					optimalScoreActionPair = (score, action)
				if score < beta:
					beta = score
				if alpha >= beta:
					break

			return optimalScoreActionPair

		def agentMove(gameState, currentDepth, alpha, beta):
			
			if (currentDepth == 0):
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
