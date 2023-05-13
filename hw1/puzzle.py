from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q
import resource


bfs_visited = []
bfs_max_depth = 0
bfs_final_state = None


#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """

        """
        First, you obviously need to plus one for cost since you take an action
        Second, after you take a move, you have a new state, and the previous state becomes the parent
        Third, managing the config is important, moving up is essentially swapping with the number 
            3 index behind the blanc space
        Fourth, check if each move is a valid move, like check boundary, if it is not a valid move, simply return None
        """

        curr0 = self.blank_index
        # If out of boundary, or we are switching back to a parents, return none
        if curr0 - self.n < 0:
            return None
        else:
            prevConfig = self.config.copy()
            num = prevConfig[curr0 - self.n]
            prevConfig[curr0] = num
            prevConfig[curr0 - self.n] = 0
            if prevConfig in bfs_visited:
                return None
            state = PuzzleState(prevConfig, self.n, parent=self, action=self.action+",Up", cost=self.cost+1)
            return state


    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        curr0 = self.blank_index
        if curr0 + self.n > len(self.config) - 1:
            return None
        else:
            prevConfig = self.config.copy()
            num = prevConfig[curr0 + self.n]
            prevConfig[curr0] = num
            prevConfig[curr0 + self.n] = 0
            if prevConfig in bfs_visited:
                return None
            state = PuzzleState(prevConfig, self.n, parent=self, action=self.action+",Down", cost=self.cost + 1)
            return state



    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        curr0 = self.blank_index
        if (curr0 + 1) % 3 == 1:
            return None
        else:
            prevConfig = self.config.copy()
            num = prevConfig[curr0 - 1]
            prevConfig[curr0] = num
            prevConfig[curr0 - 1] = 0
            if prevConfig in bfs_visited:
                return None
            state = PuzzleState(prevConfig, self.n, parent=self, action=self.action+",Left", cost=self.cost + 1)
            return state




    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        curr0 = self.blank_index
        if (curr0+1) % 3 == 0:
            return None
        else:
            prevConfig = self.config.copy()
            num = prevConfig[curr0 + 1]
            prevConfig[curr0] = num
            prevConfig[curr0 + 1] = 0
            if prevConfig in bfs_visited:
                return None
            state = PuzzleState(prevConfig, self.n, parent=self, action=self.action+",Right", cost=self.cost + 1)
            return state


def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children

# Function that Writes to output.txt


### Students need to change the method to have the corresponding parameters
def writeOutput(searchCode, runningTime, ram):
    ### Student Code Goes here
    if searchCode == "bfs":
        path = list(bfs_final_state.action[bfs_final_state.action.index(",")+1:].split(","))
        with open('output.txt', 'w') as f:
            f.write(f'path_to_goal: {path}\n')
            f.write(f'cost_of_path: {bfs_final_state.cost}\n')
            f.write(f"nodes_expanded: {len(bfs_visited)}\n")
            f.write(f'search_depth: {bfs_final_state.cost}\n')
            f.write(f"max_search_depth: {bfs_max_depth}\n")
            f.write(f"running_time: {runningTime}\n")
            f.write(f"max_ram_usage: {ram}")




def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###
    global bfs_max_depth
    queue = Q.Queue()
    queue.put(initial_state)
    while not queue.empty():
        currState = queue.get()
        bfs_visited.append(currState.config)
        # The stop condition needs to be checked clearly
        if currState.blank_index == 0:
            targetList = list(range(1, currState.n * currState.n))
            if currState.config[1:] == targetList:
                bfs_final_state = currState
                return
        childrenList = expand(currState)
        for child in childrenList:
            if child.cost > bfs_max_depth:
                bfs_max_depth = child.cost
            queue.put(child)



def dfs_search(initial_state):
    """DFS search"""
    ### STUDENT CODE GOES HERE ###
    pass

def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###
    pass

def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###
    pass

def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###
    pass

def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    pass

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()

    start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    
    if   search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")

    end_time = time.time()
    end_ram = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss-start_ram)/(2**20)

    print("Program completed in %.3f second(s)"%(end_time-start_time))
    writeOutput("bfs", end_time-start_time, end_ram)

if __name__ == '__main__':
    main()
