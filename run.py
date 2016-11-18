import twixt
import agent

tb = twixt.twixtBoard(5)
iteration = 1
agent = [agent.MinimaxAgent(2), agent.MinimaxAgent(1)]
while tb.winner() == -1:
    print "iteration: ", iteration
    action = agent[tb.agent].getAction(tb)
    print "agent, action: ", tb.agent, action
    tb.updateBoard(action)
    print "pins: ", tb.pins
    print "bridges: ", tb.bridges
    print tb.winner()
    iteration += 1

