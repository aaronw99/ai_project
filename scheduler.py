import heapq 
import copy

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
			try:
				cur = heapq.heappop(pq)
				# print('successful heappop')
			except:
				# print('Dicts not comparable, heappop')
				continue
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
					nextUtility = self.world.getExpectedUtility(nextState, len(schedule) + 1)
					nextSchedule = schedule + [[nextAction, nextUtility]]
					if nextState not in visited:
						try:
							heapq.heappush(pq, (-nextUtility, nextState, nextSchedule))
							# print('successful heappush')
						except:
							# print('Dicts not comparable, heappush')
							pass
						# maintains a fix-sized heap
						if len(pq) > maxSize:
							try:
								heapq.heappop(pq)
							except:
								pass
		return result

