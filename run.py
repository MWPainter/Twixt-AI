import twixt
import agent

tb = twixt.twixtBoard(4)
iter = 1
agent = [agent.MinimaxAgent(2), agent.MinimaxAgent(2)]
#while tb.winner() == -1:
print "iteration: ", iter
action = agent[tb.agent].getAction(tb)
print "agent, action: ", tb.agent, action
tb.updateBoard(action)
print "pins: ", tb.pins
print tb.winner()

