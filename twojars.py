import search
import random

# Module Classes


class TwoJarsState:
    """
    This class represents a configuration of the two jars.
    """

    def __init__(self, capacitys):
        """
          Constructs a new configuration.

        The configuration of the two jars is stored in a 2-tuple. 
         - The first position stores the amount of water in the first jar (with capacity 4l).
         - The second position stores the amount of water in the second jar (with capacity 3l).

        Both jars ware initially empty.
        """
        self.jars = (capacitys[0], capacitys[1])

    def isGoal(self):
        """
          Checks to see if the pair of jars is in its goal state.

            ---------
            | 2 | * |
            ---------

        >>> TwoJarsState((2, 1)).isGoal()
        True

        >>> TwoJarsState((2, 0)).isGoal()
        True

        >>> TwoJarsState((1, 0)).isGoal()
        False
        """
        "*** YOUR CODE"
        x, y = self.jars
        if x == 2:
            return True
        return False

    def legalMoves(self):
        """
          Returns a list of legal actions from the current state.

        Actions consist of the following:
        - fillJ3 (encher J3)
        - fillJ4 (encher J4)
        - pourJ3intoJ4 (despejar J3 em J4)
        - pourJ4intoJ3 (despejar J4 em J3)
        - emptyJ3 (esvaziar J3)
        - emptyJ4 (esvaziar 43)

        These are encoded as strings: 'fillJ3', 'fillJ4', 'pourJ3intoJ4', 'pourJ4intoJ3', 'emptyJ3', 'emptyJ4'.

        >>> TwoJarsState((1, 3)).legalMoves()
        ['fillJ4', 'pourJ3intoJ4', 'emptyJ3', 'emptyJ4']
        """
        "*** YOUR CODE"
        moves = []
        j4, j3 = self.jars
        if j3 != 0:
            moves.append('emptyJ3')
            if j4 < 4:
                moves.append('pourJ3intoJ4')
        if j3 < 3:
            moves.append('fillJ3')

        if j4 > 0:
            moves.append('emptyJ4')
            if j3 < 3:
                moves.append('pourJ4intoJ3')
        if j4 < 4:
            moves.append('fillJ4')
        return moves

    def result(self, move):
        """
          Returns an object TwoJarsState with the current state based on the provided move.

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        NOTE: This function *does not* change the current object.  Instead,
        it returns a new object.
        """
        "*** YOUR CODE HERE ***"
        novo = TwoJarsState(self.jars)
        x, y = novo.jars
        if move == "fillJ4":
            novo.jars = (4, y)
        elif move == "fillJ3":
            novo.jars = (x, 3)
        elif move == "emptyJ4":
            novo.jars = (0, y)
        elif move == "emptyJ3":
            novo.jars = (x, 0)
        elif move == "pourJ3intoJ4" and x+y <= 4:
            novo.jars = (x+y, 0)
        elif move == "pourJ4intoJ3" and x+y <= 3:
            novo.jars = (0, y+x)
        elif move == "pourJ4intoJ3" and y < 3:
            novo.jars = (x+y-4, 3)
        elif move == "pourJ3intoJ4" and x < 4:
            novo.jars = (4, x+y-3)
        return novo

    # Utilities for comparison and display
    def __eq__(self, other):
        """
            Overloads '==' such that two pairs of jars with the same volume of water
          are equal.

          >>> TwoJarsState((0, 1)) == \
              TwoJarsState((1, 0)).result('left')
          True
        """
        "*** YOUR CODE"
        # if self.jars[0] == other.jars[1] and self.jars[1] == other.jars[0]:
        #     return True
        if self.jars[0] == other.jars[0] and self.jars[1] == other.jars[1]:
            return True
        return False

    def __hash__(self):
        return hash(str(self.jars))

    def __getAsciiString(self):
        """
          Returns a display string for the maze
        """
        "*** YOUR CODE HERE ***"
        return str(self.jars)

    def __str__(self):
        return self.__getAsciiString()


class TwoJarsSearchProblem(search.SearchProblem):
    """
      Implementation of a SearchProblem for the Two Jars domain

      Each state is represented by an instance of an TwoJarsState.
    """

    def __init__(self, start_state):
        "Creates a new TwoJarsSearchProblem which stores search information."
        self.start_state = start_state

    def getStartState(self):
        return start_state

    def isGoalState(self, state):
        return state.isGoal()

    def expand(self, state):
        """
          Returns list of (child, action, stepCost) pairs where
          each child is either left, right, up, or down
          from the original state and the cost is 1.0 for each
        """
        child = []
        for a in self.getActions(state):
            next_state = self.getNextState(state, a)
            child.append(
                (next_state, a, self.getActionCost(state, a, next_state)))
        return child

    def getActions(self, state):
        return state.legalMoves()

    def getActionCost(self, state, action, next_state):
        assert next_state == state.result(action), (
            "getActionCost() called on incorrect next state.")
        return 1

    def getNextState(self, state, action):
        assert action in state.legalMoves(), (
            "getNextState() called on incorrect action")
        return state.result(action)

    def getCostOfActionSequence(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)


def createRandomTwoJarsState(moves=10):
    """
      moves: number of random moves to apply

      Creates a random state by applying a series 
      of 'moves' random moves to a solved state.
    """
    volume_of_J3 = random.randint(0, 4)
    a_state = TwoJarsState((2, volume_of_J3))
    for i in range(moves):
        # Execute a random legal move
        a_state = a_state.result(random.sample(a_state.legalMoves(), 1)[0])
    return a_state


if __name__ == '__main__':
    start_state = createRandomTwoJarsState(8)
    print('A random initial state:')
    print(start_state)

    problem = TwoJarsSearchProblem(start_state)
    path = search.breadthFirstSearch(problem)
    print('BFS found a path of %d moves: %s' % (len(path), str(path)))
    curr = start_state
    i = 1
    for a in path:
        curr = curr.result(a)
        print('After %d move%s: %s' % (i, ("", "s")[i > 1], a))
        print(curr)

        input("Press return for the next state...")   # wait for key stroke
        i += 1
