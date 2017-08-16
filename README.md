# CS221: An Intelligent, Artificial Look into Twixt

**N.B. Input does little validation, and incorrect inputs may cause the program to crash.**

Usage:
``` python code/run.py <agent_1> <agent_2> <board_size> ```

```board_size``` refers to the size of the board to play on, it should be an integer greater than 5.

The agents may be any one of the following:
```
MCTreeSearch
PureMC
Minmax
HumanAgent
```

which respectively will make the first or second player one of the following:

### MCTreeSearch Agent

An agent that will run the MCTS algorithm.

### PureMC Agent

A naive MC agent, that will simulate games (by choosing moves uniformly randomly) and pick the next move that lead to the most wins.

### Minmax Agent

An agent that performs minmax tree search.

### HumanAgent Agent

You get to play!

