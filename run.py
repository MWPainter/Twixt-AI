from twixt import twixtBoard
import agent
from util import printc, bcolors

n = 7
iter = 1
depth = 1
agent = [agent.MinimaxAgent(depth), agent.MinimaxAgent(depth)]

def drawBoard(n, labels, assignments):
	for i in range(n):
		for j in range(n):
			if (i == 0 or i == n-1) and (j == 0 or j == n-1):
				print "%-*s" % (8, ""),
			else:
				if (i,j) in labels:
					if labels[(i,j)] in assignments[0]:
						printc("%-*s" % (8, assignments[0][labels[(i,j)]]))
					elif labels[(i,j)] in assignments[1]:
						printc("%-*s" % (8, assignments[1][labels[(i,j)]]), bcolors.FAIL),
				else:
					print "%-*s" % (8, "x"),
			if j == n-1:
				print "\n"

tb = twixtBoard(n)
while tb.winner() == -1:
    print "iteration: ", iter
    iter += 1


    action = agent[tb.agent].getAction(tb)
    #print "agent, action: ", tb.agent, action
    tb.updateBoard(action)
    #print "pins: ", tb.pins
    #print "bridges: ", tb.bridges
    drawBoard(n, tb.label, tb.assignment)

print tb.winner()

