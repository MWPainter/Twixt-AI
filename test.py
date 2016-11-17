import twixt
import agent

tb = twixt.twixtBoard(7)
minMaxAgent = agent.MinimaxAgent(1)
actions = [(0,3), (1,1), (1,5), (3,3), (2,3), (2,2), (4,3), (4,2), (3,1)]
for action in actions:
	tb.updateBoard(action)
	print tb.label
	print tb.assignment
print tb.getScore()
tb2 = tb.generateSuccessor(tb.agent, (4,5))
print tb2.label
print tb2.assignment
print tb2.getLegalAction(tb2.agent), "here"
print minMaxAgent.getAction(tb2)
print tb.label
print tb.assignment
