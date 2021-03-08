import heapq
import copy


class Item:
    def __init__(self, utility, state, schedule):
        self.utility = utility
        self.state = state
        self.schedule = schedule

    def getUtility(self):
        return self.utility

    def getState(self):
        return self.state

    def getSchedule(self):
        return self.schedule

    def __lt__(self, other):
        if isinstance(other, Item):
            if self.utility == other.utility:
                return len(self.schedule) > len(other.schedule)
            else:
                return self.utility < other.utility
        else:
            return False

    def __le__(self, other):
        if isinstance(other, Item):
            return self.utility <= other.utility
        else:
            return False


class Scheduler:
    def __init__(self, world):
        self.world = world

    def search(self, maxDepth, maxSize):
        pq = []
        visited = []
        result = []
        maxUtility = float('-inf')
        initialState = self.world.getStartState()
        heapq.heappush(pq, (0, initialState, []))
        while pq:
            cur = heapq.heappop(pq)
            utility = cur[0]
            state = cur[1]
            schedule = cur[2]
            # reaches maximum depth
            if len(schedule) == maxDepth:
                if utility >= maxUtility:
                    result = copy.deepcopy(schedule)
                    maxUtility = utility
            # explores current state if new
            if state not in visited:
                visited.append(state)
                # expands fringe
                for successor in self.world.getSuccessors(state):
                    nextState = successor[0]
                    nextAction = successor[1]
                    nextUtility = self.world.getExpectedUtility(
                        nextState, len(schedule) + 1)
                    nextSchedule = schedule + [[nextAction, nextUtility]]
                    if nextState not in visited:
                        heapq.heappush(
                            pq, (-nextUtility, nextState, nextSchedule))
                        # maintains a fix-sized heap
                        if len(pq) > maxSize:
                            heapq.heappop(pq)
        return result
