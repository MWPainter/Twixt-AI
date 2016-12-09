from collections import defaultdict
import random, operator
import twixt
import util
import copy

class HumanAgent(object):
    def __init__(self, agentIndex):
        self.index = agentIndex

    def getAction(self, gameState):
        while True:
            print 'Enter x:'
            x = raw_input().strip()
            print 'Enter y:'
            y = raw_input().strip()
            if (int(x), int(y)) in gameState.getLegalAction(self.index):
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
        self.value = 0.0 # average value witnessed at this state
        self.numVisits = 0 # times visited node
        self.children = {} # a dictionary of (action -> successor tree node) values
        self.weight = weight # weight of selecting this node from parent originally
        self.parent = parent # pointer to parent, if pointer is None then root node

    
    def getActionToWeightMap(self):
        """
        :return: a map from possible actions to weights (according to the children nodes)
        """
        actionMap = {}
        for action in self.children:
            actionMap[action] = self.children[action].getWeight()
        return actionMap


    def witnessValue(self, value):
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


    def endState(self):
        """
        If there is no winner yet explicitly, or there are no legal moves left, then we 
        are in an end state

        :return: If this is the tree node for an end state
        """
        return not(self.state.winner() == -1 and len(self.state.getLegalAction(self.state.agent)) > 0)



    def getSuccInTree(self, action):
        """
        Operates entirely within the current tree. Nodes with a value of 'numVisits' of zero 
        are considered NOT part of the tree here. If the successor state of the tree's state 
        is in the tree, we return it.

        :param action: The action we are trying to take
        :return: Successor state's node after taking action 'action'. Return None if successor 'not' in tree
        """
        if not action in self.children: return None
        if self.children[action].numVisits == 0: return None
        return self.children[action]


    def getSuccAfterExpand(self, action):
        """
        Gets the successor to the current node according to some action 'action'. Assumes that we are 
        in what was a leaf node and have expanded this node. If used properly, we should be returning 
        a 'newly created' node, which has 'numVisits' equal to 0

        :param action: action that we are taking
        :return: The successor state's node after taking action 'action'.
        """
        if self.children == {}: 
            raise Exception("Called 'TreeNode.getSuccAfterExpand' either on a end state of the game or without calling expand before")
        if not action in self.children: return None
        return self.children[action]


    def expand(self, policy):
        """
        Populates the dictionary of children nodes, initialising the weights to the weights allocated 
        by some stochastic policy. Here we take liberty of assuming that different actions will lead 
        to unique states. This assumption isn't necessarily true, but we make it for game playing. 
        (And is true in this case). 

        To populate children we basically look at the policy for this state, iterate through the 
        actions and add a node for each action, with the successor state, weight and link back to 
        this node

        We also hard code that this is for a two player game, with agents 0, 1. As used in twixt.py

        Finally, note that when we expand in pure MCTS we one node to child list. Here we add all of 
        the children in one go. We may call expand on this node again to add 'another child', but in 
        the implementation we added all children in one go. So if children is non empty, then return 
        immediately

        :param policy: A stochastic policy, taking a state and returning a map, actions -> weights
        """
        if self.children != {}: return
        actionWeights = policy(self.state)
        newAgent = 1 - self.state.agent
        for action in actionWeights:
            succ = self.state.generateSuccessor(newAgent, action)
            self.children[action] = TreeNode(succ, actionWeights[action], self)

        
    def pprint(self):
        """
        Pretty print the tree rooted at this node, displaying all the values encorporated
        """
        def pprintStr(node):
            s = "(" + str(node.value) 
            for action in node.children:
                s = s + ", " + pprintStr(node.children[action])
            s = s + ")"
            return s

        print pprintStr(self)




class MCTreeSearch(object):
    def __init__(self, selectionPolicy, simulationPolicy, iter='50000', simulationDepth = 0, evalFn = None):
        """
        :param iter: Number of iterations for each 'getAction' search
        :param selectonPolicy: Stochastic policy used for selecting nodes to expand, takes a 
            state as an argument and returns a dict of (action -> weight) values
        :param simulationPolicy: Stochastic policy used for simulating a game. (action -> weight) values again
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

        Finally, after all the searching, we look at the action that leads to the best avg reward
        from the rootNode (the node with state 'gameState'), and return that action to play.

        :param gameState: The current state of the game
        :return: The action leading to the best (avg) reward from the search
        """
        rootNode = TreeNode(gameState, 1)
        rootNode.expand(self.selPolicy) 
        agent = rootNode.state.agent
        for i in range(self.iter):
            leafNode = self.walkTree(rootNode) # selection
            if (leafNode.endState()): continue # if our node we wish to expand is an end state, we can't do anything (and the value is deterministic and correct already) so skip it
            self.expand(leafNode) # expansion1
            newLeafNode = self.step(leafNode) # expansion2: select one of the new children
            value = self.simulate(newLeafNode, agent) # simulation
            self.backPropogation(newLeafNode, value) # back propogation

        optAction = None
        optValue = -float('inf')
        for action in rootNode.children:
            childNode = rootNode.children[action]
            if childNode.value > optValue:
                optAction = action
                optValue = childNode.value

        return optAction


    def walkTree(self, root):
        """
        Selection.
        We stochastically walk the tree according to the distribution of weights stored in the 
        tree. The original weights were computed using 'self.selPolicy', but we decay the weights 
        in the tree over time. We walk the tree until we reach a leaf node, which we return

        Leaf nodes are indicated by 'getSuccInTree' returning None
        
        When walking the tree we repetatively do the following:
        1. get weights for actions at current state
        2. if weights empty, then there are no children, node is a leaf and we should return it
        3. pick a random action
        4. check if the successor is in the tree
        5. if not, then we need 
        6. update node iterating variable

        :param root: The base TreeNode that we will be starting the walk from
        :return: A leaf node, rooted at 'root', arrived to by stochastically walking tree 
        """
        node = root
        while True:
            actionToWeight = node.getActionToWeightMap()
            if actionToWeight == {}:
                return node
            action = util.selectRandomKey(actionToWeight)
            nextNode = node.getSuccInTree(action)
            if nextNode == None:
                return node
            node = nextNode


    def expand(self, node):
        """
        Expansion. (Part 1).
        We expand the tree node 'node'. In this implementation we add all possible successors 
        to the children map of 'node', with weights according to 'selPolicy'

        :param node: The node to expand
        """
        node.expand(self.selPolicy)


    def step(self, node):
        """
        Expansion. (Part 2).
        Take one step from (just expanded) node 'node', randomly according to selection policy.

        :param node: The node to take a step from
        :return: The successor node
        """
        actionToWeight = node.getActionToWeightMap()
        action = util.selectRandomKey(actionToWeight)
        return node.getSuccAfterExpand(action)


    def simulate(self, root, agent):
        """
        Simulate.
        Simulates the rest of the game, stochastically, from node 'root', using policy 
        'simPolicy'. Returns a value of the game. (1 if the agent wins, -1 if they don't, 
        0 for a draw). We keep on simulating whilst "no one has one and there is a legal 
        move left"

        Remember to copy the state so that we don't clobber the state in the tree

        :param root: the node to simulate the game from
        :param agent: the agent who we are trying to pick a good move for (back in the call to 
            'getAction').
        """
        state = copy.deepcopy(root.state)
        while state.winner() == -1 and len(state.getLegalAction(state.agent)) > 0:
            actionToWeight = self.simPolicy(state)
            action = util.selectRandomKey(actionToWeight)
            state.updateBoard(action)

        winner = state.winner()
        if winner == agent:
            return 1.0
        elif winner == 1-agent:
            return -1.0
        elif winner == 2 or winner == -1: # 2 indicates a draw, -1 means no one has won, but if here there is no legal move left
            return 0.0
        else:
            raise Exception("Something's weird with win conditions. In 'simulate', for MCTS")


    def backPropogation(self, leafNode, value):
        """
        Backpropogation.
        Having observed a game of value 'value' from leaf node, we wish to add this 
        information to all nodes on the path from 'leafNode' to the root. Telling each of
        the nodes in turn will cause them to update their running average 

        :param leafNode: The leaf node the game was simulated from and we have an observed value
        :param value: The value that we observed by stochastically simulating game
        """
        node = leafNode
        while node != None:
            node.witnessValue(value)
            node = node.parent


# Cheap dirty policy for testing
def uniformPolicy(state):
    actions = state.getLegalAction(state.agent)
    return {action: 1 for action in actions}

def randomPolicy(state):
    actions = state.getLegalAction(state.agent)
    return {action: random.random() for action in actions}
