import twixt
import agent

bridge1 = ((5,4),(3,5))
bridge2 = ((5,3),(4,5))
print bridge1, bridge2, twixt.intersect(bridge1,bridge2)
print bridge1, bridge2, twixt.intersect(bridge2,bridge1)
# bridges1 = [((5,3),(4,5)), ((-1,2),(1,3)), ((0,2),(2,3)), ((0,2),(1,4)), ((2,2),(0,3)), ((-1,3),(1,4)), ((0,3),(2,4)), ((1,3),(-1,4))]

# for bridge in bridges1:
#         print bridge1, bridge, twixt.intersect(bridge, bridge1)
#         print bridge1, bridge, twixt.intersect(bridge1, bridge)

#minMaxAgent = agent.MinimaxAgent(1)
#actions = [(1,3), (3,4), (5,3), (2,1), (3,2)]
#for iteration in range(10):
#        for action in actions:
#                tb.updateBoard(action)
#                print tb.getBetterScore()

# tb = twixt.twixtBoard(7)
# actions = [(1,3), (1,1), (3,4), (2,2), (5,3), (4,1), (0,1), (1,2), (6,1)]
# for action in actions:
# 	tb.updateBoard(action)
# print tb.getBestEval(0)