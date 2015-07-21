# -----------------
# User Instructions
#
# Modify the bridge_problem(here) function so that it
# tests for goal later: after pulling a state off the
# frontier, not when we are about to put it on the
# frontier.




def bsuccessors(state):
    """Return a dict of {state:action} pairs.  A state is a (here, there, t) tuple,
    where here and there are frozensets of people (indicated by their times) and/or
    the light, and t is a number indicating the elapsed time."""
    here, there, t = state
    if 'light' in here:
        return dict(((here  - frozenset([a,b, 'light']),
                      there | frozenset([a, b, 'light']),
                      t + max(a, b)),
                     (a, b, '->'))
            for a in here if a is not 'light'
            for b in here if b is not 'light')
    else:
        next = min([a for a in there if a is not 'light'])
        return dict({(here  | frozenset([next, next, 'light']),
                      there - frozenset([next, next, 'light']),
                      t + next)
                    :(next, next, '<-')}
                     )

def elapsed_time(path):
    return path[-1][2]

def bridge_problem(here):
    """Modify this to test for goal later: after pulling a state off frontier,
    not when we are about to put it on the frontier."""
    ## modify code below
    here = frozenset(here) | frozenset(['light'])
    explored = set() # set of states we have visited
    # State will be a (people-here, people-there, time-elapsed)
    frontier = [ [(here, frozenset(), 0)] ] # ordered list of paths we have blazed
    if not here:
        return frontier[0]
    results = []
    while frontier:
        path = frontier.pop(0)
        for (state, action) in bsuccessors(path[-1]).items():
            if '->' in action:
                opposite = action[0:2] + ('<-',)
            else:
                opposite = action[0:2] + ('->',)
            if opposite not in path:
                here, there, t = state
                path2 = path + [action, state]
                if not here:  ## That is, nobody left here
                    results.append(path2)
                else:
                    frontier.append(path2)

    target = min(results, key=elapsed_time)
    return target

def test():
    assert bridge_problem(frozenset((1, 2),))[-1][-1] == 2 # the [-1][-1] grabs the total elapsed time
    assert bridge_problem(frozenset((1, 2, 5, 10),))[-1][-1] == 17
    return 'tests pass'

#print test()


# -----------------
# User Instructions
#
# Write a function, csuccessors, that takes a state (as defined below)
# as input and returns a dictionary of {state:action} pairs.
#
# A state is a tuple with six entries: (M1, C1, B1, M2, C2, B2), where
# M1 means 'number of missionaries on the left side.'
#
# An action is one of the following ten strings:
#
# 'MM->', 'MC->', 'CC->', 'M->', 'C->', '<-MM', '<-MC', '<-M', '<-C', '<-CC'
# where 'MM->' means two missionaries travel to the right side.
#
# We should generate successor states that include more cannibals than
# missionaries, but such a state should generate no successors.

def csuccessors(state):
    """Find successors (including those that result in dining) to this
    state. But a state where the cannibals can dine has no successors."""
    M1, C1, B1, M2, C2, B2 = state
    # your code here
    if M1 < C1 or M2 < C2:
        return {}
    if B1:
        return dict(
        (
            (M1-i, C1-j, 0, M2+i, C2+j, 1), 'M'*i + 'C'*j + '->'
        )
        for i in range(3) if i <= M1
        for j in range(3) if j <= C1 and i + j <= 2 and i + j != 0
        )
    if B2:
        return dict(
            (
                (M1+i, C1+j, 1, M2-i, C2-j, 0), '<-' + 'M'*i + 'C'*j
                )
                for i in range(3) if i <= M2
                for j in range(3) if j <= C2  and i + j <= 2 and i + j != 0
        )


def test():
    assert csuccessors((2, 2, 1, 0, 0, 0)) == {(2, 1, 0, 0, 1, 1): 'C->',
                                               (1, 2, 0, 1, 0, 1): 'M->',
                                               (0, 2, 0, 2, 0, 1): 'MM->',
                                               (1, 1, 0, 1, 1, 1): 'MC->',
                                               (2, 0, 0, 0, 2, 1): 'CC->'}
    assert csuccessors((1, 1, 0, 4, 3, 1)) == {(1, 2, 1, 4, 2, 0): '<-C',
                                               (2, 1, 1, 3, 3, 0): '<-M',
                                               (3, 1, 1, 2, 3, 0): '<-MM',
                                               (1, 3, 1, 4, 1, 0): '<-CC',
                                               (2, 2, 1, 3, 2, 0): '<-MC'}
    assert csuccessors((1, 4, 1, 2, 2, 0)) == {}
    return 'tests pass'

#print test()
# -----------------
# User Instructions
#
# In this problem, you will solve the pouring problem for an arbitrary
# number of glasses. Write a function, more_pour_problem, that takes
# as input capacities, goal, and (optionally) start. This function should
# return a path of states and actions.
#
# Capacities is a tuple of numbers, where each number represents the
# volume of a glass.
#
# Goal is the desired volume and start is a tuple of the starting levels
# in each glass. Start defaults to None (all glasses empty).
#
# The returned path should look like [state, action, state, action, ... ]
# where state is a tuple of volumes and action is one of ('fill', i),
# ('empty', i), ('pour', i, j) where i and j are indices indicating the
# glass number.



def more_pour_problem(capacities, goal, start=None):
    """The first argument is a tuple of capacities (numbers) of glasses; the
    goal is a number which we must achieve in some glass.  start is a tuple
    of starting levels for each glass; if None, that means 0 for all.
    Start at start state and follow successors until we reach the goal.
    Keep track of frontier and previously explored; fail when no frontier.
    On success return a path: a [state, action, state2, ...] list, where an
    action is one of ('fill', i), ('empty', i), ('pour', i, j), where
    i and j are indices indicating the glass number."""
    # your code here
    if not start:
        start = [0 for i in capacities]
    return shortest_path_search(tuple(start), goal, capacities, successor, is_goal)

def is_goal(state, goal):
    if goal in state:
        return True
    return False

def successor(state, capacities):
    result = {}
    length = len(capacities)
    for i, current in enumerate(state):
        if not current:
            delta = fill(i, get_capacity(i, capacities), length)

            result[tuple(sum(state, delta))] = ('fill', i)
        elif current in range(1, get_capacity(i, capacities)+1):
            delta = empty(i, current, length)

            result[tuple(sum(state, delta))] = ('empty', i)
            for j, target in enumerate(state):
                if j != i and target < get_capacity(j, capacities):
                    #pour i to j
                    if get_capacity(j, capacities) - target >= current:
                        state_i = 0
                        state_j = target + current
                    else:
                        state_j = get_capacity(j, capacities)
                        state_i = target + current - state_j
                    pour_state = []
                    for k, s in enumerate(state):
                        if k == i:
                            pour_state.append(state_i)
                        elif k == j:
                            pour_state.append(state_j)
                        else:
                            pour_state.append(s)

                    result[tuple(pour_state)] = ('pour', i, j)

    return result


def sum(state, delta):
    return [x+y for x, y in zip(state, delta)]

def fill(i, capacity, length):
    return (0,) * i + (capacity,) + (0,) * (length - i - 1)

def empty(i, capacity, length):
    return (0,) * i + ((-1) * capacity,) + (0,) * (length - i - 1)

def get_capacity(i, capacities):
    return capacities[i]



def shortest_path_search(start, goal, capacities, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start, goal):
        return [start]
    explored = set()
    frontier = [ [start] ]

    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s, capacities).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state, goal):
                    return path2
                else:
                    frontier.append(path2)
    return Fail
Fail = []



def test_more_pour():
    assert more_pour_problem((1, 2, 4, 8), 4) == [
        (0, 0, 0, 0), ('fill', 2), (0, 0, 4, 0)]
    assert more_pour_problem((1, 2, 4), 3) == [
        (0, 0, 0), ('fill', 2), (0, 0, 4), ('pour', 2, 0), (1, 0, 3)]
    starbucks = (8, 12, 16, 20, 24)
    assert not any(more_pour_problem(starbucks, odd) for odd in (3, 5, 7, 9))
    assert all(more_pour_problem((1, 3, 9, 27), n) for n in range(28))
    assert more_pour_problem((1, 3, 9, 27), 28) == []
    return 'test_more_pour passes'

print test_more_pour()



