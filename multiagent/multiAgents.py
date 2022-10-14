# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util
import math

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        #print('Moving: ',legalMoves[chosenIndex])
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        #print(newGhostStates[0])
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        score = successorGameState.getScore()
        #print('The score for doing this action is: ', score)

        newGhostPositions = currentGameState.getGhostPositions()
        #print(newGhostPositions)
        for ghostPos in newGhostPositions:
            if util.manhattanDistance(newPos, ghostPos) < 2:
                #print('Ghost is too close!')
                return 0

        #print(newFood)
        distToFood = 1000
        for row in range(newFood.height):
            for col in range(newFood.width):
                if newFood[col][row] == True:
                    newDistance = util.manhattanDistance(newPos, (col,row))
                    if distToFood > newDistance:
                        distToFood = newDistance
        if distToFood == 0:
            distToFood = 0.1
        #print(distToFood)

        score = score + (1/distToFood)

        #print('Returning a score of: ', score)
        return score
        #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()

        def maxValue(state, agentIndex, currentDepth):
            v = -math.inf
            for action2 in state.getLegalActions(agentIndex):
                v = max(v, value(state.generateSuccessor(agentIndex, action2), agentIndex, currentDepth))
            return v

        def minValue(state, agentIndex, currentDepth):
            v = math.inf
            if agentIndex == numAgents-1:
                currentDepth = currentDepth + 1
            for action2 in state.getLegalActions(agentIndex):
                v = min(v, value(state.generateSuccessor(agentIndex, action2), agentIndex, currentDepth))
            return v

        def value(state, agentIndex, currentDepth):
            if state.isWin() or state.isLose() or currentDepth == self.depth:
                return self.evaluationFunction(state)
            elif agentIndex == numAgents - 1:
                return maxValue(state, (agentIndex+1)%numAgents, currentDepth)
            else:
                return minValue(state, (agentIndex+1)%numAgents, currentDepth)


        bestScore = -math.inf
        bestMove = None
        for action in gameState.getLegalActions(0):
            newGameState = gameState.generateSuccessor(0, action)
            score = value(newGameState, 0, 0)
            if score > bestScore:
                bestMove = action
                bestScore = score

        return bestMove

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()

        def maxValue(state, agentIndex, currentDepth, alpha, beta):
            v = -math.inf
            for action2 in state.getLegalActions(agentIndex):
                v = max(v, value(state.generateSuccessor(agentIndex, action2), agentIndex, currentDepth, alpha, beta))
                if v > beta:
                    return v
                alpha = max(v, alpha)
            return v

        def minValue(state, agentIndex, currentDepth, alpha, beta):
            v = math.inf
            if agentIndex == numAgents - 1:
                currentDepth = currentDepth + 1
            for action2 in state.getLegalActions(agentIndex):
                v = min(v, value(state.generateSuccessor(agentIndex, action2), agentIndex, currentDepth, alpha, beta))
                if v < alpha:
                    return v
                beta = min(v, beta)
            return v

        def value(state, agentIndex, currentDepth, alpha, beta):
            if state.isWin() or state.isLose() or currentDepth == self.depth:
                return state.getScore()
            elif agentIndex == numAgents - 1:
                return maxValue(state, (agentIndex + 1) % numAgents, currentDepth, alpha, beta)
            else:
                return minValue(state, (agentIndex + 1) % numAgents, currentDepth, alpha, beta)

        bestScore = -math.inf
        bestMove = None
        alpha1 = -math.inf
        beta1 = math.inf
        for action in gameState.getLegalActions(0):
            w = -math.inf
            newGameState = gameState.generateSuccessor(0, action)
            score = value(newGameState, 0, 0, alpha1, beta1)
            w = max(w, score)
            if score > bestScore:
                bestMove = action
                bestScore = score
            if w > beta1:
                break
            alpha1 = max(alpha1, w)

        return bestMove

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()

        def value(state, agentIndex, currentDepth):
            if state.isWin() or state.isLose() or currentDepth == self.depth:
                return self.evaluationFunction(state)
            elif agentIndex == numAgents - 1:
                return maxValue(state, (agentIndex+1)%numAgents, currentDepth)
            else:
                return expValue(state, (agentIndex+1)%numAgents, currentDepth)

        def maxValue(state, agentIndex, currentDepth):
            v = -math.inf
            for action2 in state.getLegalActions(agentIndex):
                v = max(v, value(state.generateSuccessor(agentIndex, action2), agentIndex, currentDepth))
            return v

        def expValue(state, agentIndex, currentDepth):
            if agentIndex == numAgents - 1:
                currentDepth = currentDepth + 1
            v = 0
            legalMoves = state.getLegalActions(agentIndex)
            for action2 in legalMoves:
                p = 1/len(legalMoves)
                v = v + (p*value(state.generateSuccessor(agentIndex, action2), agentIndex, currentDepth))
            return v

        bestScore = -math.inf
        bestMove = None
        for action in gameState.getLegalActions(0):
            newGameState = gameState.generateSuccessor(0, action)
            score = value(newGameState, 0, 0)
            if score > bestScore:
                bestMove = action
                bestScore = score

        return bestMove

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newFood = currentGameState.getFood()
    #print(newFood)
    newGhostStates = currentGameState.getGhostStates()
    # print(newGhostStates[0])
    #newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    score = currentGameState.getScore()
    newPos = currentGameState.getPacmanPosition()
    # print('The score for doing this action is: ', score)

    # newGhostPositions = currentGameState.getGhostPositions()
    # # print(newGhostPositions)
    # ghostDist = math.inf
    # for ghostPos in newGhostPositions:
    #     newDist = util.manhattanDistance(newPos, ghostPos)
    #     if ghostDist > newDist:
    #         ghostDist = newDist
    #         # print('Ghost is too close!')
    #         #return 0
    #
    # score = score - 0.01*(1/(1+ghostDist))

    # print(newFood)
    distToFood = 1000
    for row in range(newFood.height):
        for col in range(newFood.width):
            if newFood[col][row] == True:
                newDistance = util.manhattanDistance(newPos, (col, row))
                if distToFood > newDistance:
                    distToFood = newDistance

    #if distToFood == 0:
    #    distToFood = 0.1
    #print(distToFood)

    score = score + (1 / (1+distToFood))

    # print('Returning a score of: ', score)
    return score
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
