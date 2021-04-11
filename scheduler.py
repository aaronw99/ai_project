import heapq
import copy

# The Item class represents the partial schedule stored in the heap
class Item:
    # __init__
    # this constructs the Item object
    # @utility(int): the expected utility
    # @state(dict): the world state
    # @schedule(list): the partial schedule
    def __init__(self, utility, state, schedule):
        self.utility = utility
        self.state = state
        self.schedule = schedule
    
    # getUtility
    # this returns self.utility
    def getUtility(self):
        return self.utility
    
    # getState
    # this returns self.state
    def getState(self):
        return self.state
    
    # getSchedule
    # this returns self.schedule
    def getSchedule(self):
        return self.schedule
    
    # __lt__
    # this is the < operator
    # note: if two partial schedules have the same expected utility,
    #       the one with fewer actions is larger
    # @other(obj): an object
    def __lt__(self, other):
        if isinstance(other, Item):
            if self.utility == other.utility:
                return len(self.schedule) > len(other.schedule)
            else:
                return self.utility < other.utility
        else:
            return False
    # __le__
    # this is the <= operator
    # @other(obj): an object
    def __le__(self, other):
        if isinstance(other, Item):
            return self.utility <= other.utility
        else:
            return False

# The Scheduler class is the research algorithm
class Scheduler:
    # __init__
    # this constructs the Scheduler object
    # @world(obj): an instance of the World class
    def __init__(self, world):
        self.world = world
    
    # search
    # this searches for the best schedules in terms of expected utility
    # with a depth limit and a frontier limit
    # @maxDepth(int): the max depth
    # @maxSize(int): the frontier width
    def search(self, maxDepth, maxSize, multiplier):
        pq = []
        visited = []
        result = []
        #maxUtility = float('-inf')
        startState = self.world.getStartState()
        item = Item(0, startState, [])
        heapq.heappush(pq, item)
        while pq:
            cur = heapq.heappop(pq)
            #utility = cur.getUtility()
            state = cur.getState()
            schedule = cur.getSchedule()
            # reaches maximum depth
            if len(schedule) == maxDepth:
                #if -1 * utility > maxUtility:
                    #result = copy.deepcopy(schedule)
                    #maxUtility = -1 * utility
                heapq.heappush(result, cur)
            # explores current state if new
            else:
                if state not in visited:
                    # marks current state as visited
                    visited.append(state)
                    # expands fringe
                    for successor in self.world.getSuccessors(state):
                        nextState = successor[0]
                        nextAction = successor[1]
                        nextUtility = self.world.getExpectedUtility(state, nextState, len(schedule) + 1, nextAction, multiplier)
                        #print(nextAction.toString(), "eu:", nextUtility)
                        nextSchedule = schedule + [[nextAction.toString(), nextUtility]]
                        nextItem = Item(-1 * nextUtility, nextState,
                                        copy.deepcopy(nextSchedule))
                        if nextState not in visited:
                            heapq.heappush(pq, nextItem)
                            # maintains a fix-sized heap
                            if len(pq) > maxSize:
                                pq.pop()
        return result
