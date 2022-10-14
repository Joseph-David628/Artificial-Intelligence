# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import pacman

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH

    #initialization
    allStates = util.Stack()
    visited = set()
    state = problem.getStartState()
    visited.add(state)

    for succ in problem.getSuccessors(state):
        allStates.push([succ])
    a = 1
    while a>0:
        path = allStates.pop()
        #print(path)
        state = path[-1][0]
        print(state)
        visited.add(state)
        for succ in problem.getSuccessors(state):
            if succ[0] not in visited:
                path_new = path[:]
                path_new.append(succ)
                allStates.push(path_new)
                if problem.isGoalState(succ[0]):
                    a = -1

    myPath = allStates.pop()

    #print(myPath)

    myPlan = [item[1] for item in myPath]
    print(myPlan)

    for i in range(len(myPlan)):
        if myPlan[i] == 'South':
            myPlan[i] = s
        if myPlan[i] == 'North':
            myPlan[i] = n
        if myPlan[i] == 'East':
            myPlan[i] = e
        if myPlan[i] == 'West':
            myPlan[i] = w

    return myPlan

    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH

    # initialization
    allStates = util.Queue()
    visited = set()
    state = (problem.getStartState(),'',0)
    allStates.push([state])
    visited.add(state[0])

    a = 1
    while a > 0:
        path = allStates.pop()
        #print(path)
        state = path[-1][0]
        if problem.isGoalState(state):
            a = -1
            break
        #print('Current state:', state)
        #print('We have visited these states:', visited)
        #print(problem.getSuccessors(state))
        for succ in problem.getSuccessors(state):
            if succ[0] not in visited:
                visited.add(succ[0])
                #print('Successor:', succ[0])
                path_new = path[:]
                path_new.append(succ)
                #print('Appended path:', path_new)
                allStates.push(path_new)

    myPath = path
    myPath.remove((problem.getStartState(), '', 0))
    #print(myPath)

    myPlan = [item[1] for item in myPath]
    #print(myPlan)

    for i in range(len(myPlan)):
        if myPlan[i] == 'South':
            myPlan[i] = s
        if myPlan[i] == 'North':
            myPlan[i] = n
        if myPlan[i] == 'East':
            myPlan[i] = e
        if myPlan[i] == 'West':
            myPlan[i] = w

    return myPlan

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH

    # initialization
    allStates = util.PriorityQueue()
    visited = set()
    state = problem.getStartState()
    #visited.add(state)
    allStates.push([(state, '', 0)], 0)

    #for succ in problem.getSuccessors(state):
    #    visited.add(succ[0])
    #    allStates.push([succ], succ[2])
    a = 1
    while a > 0:
        path = allStates.pop()
        #print('Current path: ', path)
        state = path[-1][0]
        #print(state)
        if problem.isGoalState(state):
            a = -1
            break
        if state not in visited:
            visited.add(state)
            for succ in problem.getSuccessors(state):
                #print('Thinking of adding state:',succ)
                if succ[0] not in visited:
                    path_new = path[:]
                    path_new.append(succ)
                    total_cost = sum([item[2] for item in path_new])
                    #print('Total Cost for path', path_new, ' is: ', total_cost)
                    allStates.push(path_new, total_cost)

    myPath = path
    myPath.remove((problem.getStartState(), '', 0))
    #print(myPath)

    myPlan = [item[1] for item in myPath]
    #print(myPlan)

    for i in range(len(myPlan)):
        if myPlan[i] == 'South':
            myPlan[i] = s
        if myPlan[i] == 'North':
            myPlan[i] = n
        if myPlan[i] == 'East':
            myPlan[i] = e
        if myPlan[i] == 'West':
            myPlan[i] = w

    return myPlan

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH

    # initialization
    allStates = util.PriorityQueue()
    visited = set()
    state = problem.getStartState()
    #visited.add(state)
    allStates.push([(state, '', 0)], 0)

    #for succ in problem.getSuccessors(state):
    #    allStates.push([succ], succ[2])
    a = 1
    while a > 0:
        path = allStates.pop()
        #print(path)
        state = path[-1][0]
        #print('The current state is: ', state)
        #print(visited)
        if problem.isGoalState(state):
            a = -1
            break
        if state not in visited:
            visited.add(state)
            for succ in problem.getSuccessors(state):
                if succ[0] not in visited:
                    #print(succ[0])
                    path_new = path[:]
                    path_new.append(succ)
                    total_cost = sum([item[2] for item in path_new]) + heuristic(succ[0],problem)
                    allStates.push(path_new, total_cost)

    myPath = path

    # print(myPath)

    myPlan = [item[1] for item in myPath]
    myPlan.remove('')
    # print(myPlan)

    for i in range(len(myPlan)):
        if myPlan[i] == 'South':
            myPlan[i] = s
        if myPlan[i] == 'North':
            myPlan[i] = n
        if myPlan[i] == 'East':
            myPlan[i] = e
        if myPlan[i] == 'West':
            myPlan[i] = w

    return myPlan

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
