



def twixtToGrid(twixt):
    """
    Helper function.
    Takes and instance of a twixt game and converts it into a grid of ints. +1 for agent 1, -1 for agent 0 and 0 if no 
    pin. Twixat.pins is a dict from (i,j) coordinates to 0,1, representing which agent the pin (i,j) belongs to. The
    function 2x-1 maps 1->1, 0->-1. 

    :param twixt: A state of the game of twixt
    :return: A grid of pins
    """
    grid = [[0 for _ in twixt.N] for _ in twixt.N]
    for (i,j) in twixt.pins:
        grid[i][j] = twixt.pins[(i,j)] * 2 - 1


def flipGrid(grid):
    """
    Helper function.
    Swaps agents 0 and agents 1 on the board, to exploit symmetry of the game. Requires changing all -1 to 1 and 1 to 
    -1 (i.e. multiplication by -1), and transposing the board. Assumes valid input.

    :param grid: A grid containing all the pins on the board, as created by twixtToGrid
    :return: A grid with agents 0 and 1 swapped
    """
    newGrid = [[0 for _ in range(grid)] for _ in range(grid[0])]
    width = len(grid)
    height = len(grid[0])
    for i in width:
        for j in height:
            newGrid[i][j] = grid[j][i] * -1
    return newGrid

