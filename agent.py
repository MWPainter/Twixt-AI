import twixt

class MinimaxAgent(object):
    def __init__(self, depth = '2'):
        self.index = 0
	self.depth = int(depth)

    def evaluationFunction(self, currentGameState):
	return currentGameState.getScore()

    def getAction(self, gameState):
	def oppMove(gameState, currentDepth):
	    legalMoves = gameState.getLegalAction(gameState.agent)
	    print gameState.agent, legalMoves
	    if legalMoves == set([]):
		return (self.evaluationFunction(gameState), None)
	    optimalScoreActionPair = (float('inf'), None)
	    for action in legalMoves:
                print action
		score, optimalAction = agentMove(gameState.generateSuccessor(gameState.agent, action), currentDepth-1)
		if score < optimalScoreActionPair[0]:
		    optimalScoreActionPair = (score, action)
            return optimalScoreActionPair

        def agentMove(gameState, currentDepth):
	    if (currentDepth == 0):
		return (self.evaluationFunction(gameState), None)
            legalMoves = gameState.getLegalAction(gameState.agent)
            print gameState.agent, legalMoves
	    if legalMoves == set([]):
		return (self.evaluationFunction(gameState), None)
	    optimalScoreActionPair = (-float('inf'), None)
	    for action in legalMoves:
                print action
		score, optimalAction = oppMove(gameState.generateSuccessor(gameState.agent, action), currentDepth)
		if score > optimalScoreActionPair[0]:
		    optimalScoreActionPair = (score, action)
	    return optimalScoreActionPair
        return agentMove(gameState, self.depth)[1]
