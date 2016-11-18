import twixt
import agent


minMaxAgent = agent.MinimaxAgent(1)
actions = [(1,3), (3,4), (5,3), (2,1), (3,2)]
for iteration in range(10):
        for action in actions:
                tb.updateBoard(action)
                print tb.getBetterScore()

