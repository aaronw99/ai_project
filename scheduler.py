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
		startState = self.world.getStartState()
		item = Item(0, startState, [])
		heapq.heappush(pq, item)
		while pq:
			#print(pq)
			cur = heapq.heappop(pq)
			utility = cur.getUtility()
			state = cur.getState()
			schedule = cur.getSchedule()
			# reaches maximum depth
			if len(schedule) == maxDepth:
				if -1 * utility > maxUtility:
					result = copy.deepcopy(schedule)
					maxUtility = -1 * utility
			# explores current state if new
			else:
				if state not in visited:
					visited.append(state)
					# expands fringe
					for successor in self.world.getSuccessors(state):
						nextState = successor[0]
						nextAction = successor[1]
						nextUtility = self.world.getExpectedUtility(nextState, len(schedule) + 1)
						#print(nextAction, "eu:", nextUtility)
						nextSchedule = schedule + [[nextAction, nextUtility]]
						nextItem = Item(-1 * nextUtility, nextState, copy.deepcopy(nextSchedule))
						if nextState not in visited:
							heapq.heappush(pq, nextItem)
							# maintains a fix-sized heap
							if len(pq) > maxSize:
								pq.pop()
						#print(pq)
		return result

