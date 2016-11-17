import twixt

def evaluationFunction(self, currentGameState):
	
	return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
	"""
	This class provides some common elements to all of your
	multi-agent searchers.  Any methods defined here will be available
	to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

	You *do not* need to make any changes here, but you can if you want to
	add functionality to all your adversarial search agents.  Please do not
	remove anything, however.

	Note: this is an abstract class: one that should not be instantiated.  It's
	only partially specified, and designed to be extended.  Agent (game.py)
	is another abstract class.
	"""

	def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
	self.index = 0 # Pacman is always agent index 0
	self.evaluationFunction = util.lookup(evalFn, globals())
	self.depth = int(depth)

######################################################################################
## implementing minimax

class MinimaxAgent(MultiAgentSearchAgent):

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