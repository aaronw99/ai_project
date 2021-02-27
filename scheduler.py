import heapq 
import copy

class Scheduler:
	def __init__(self, world):
		self.world = world
	
	def search(self, maxDepth, maxSize):
		pq = []
		visited = []
		candidate = []
		result = []
		maxUtility = float('-inf')
		initialState = self.world.getStartState()
		heapq.heappush(pq, (0, initialState, 0))
		while not pq.isEmpty():
			cur = heapq.heappop(pq)
			utility = cur[0]
			state = cur[1]
			depth = cur[2]
			# reaches maximum depth
			if depth == maxDepth:
				if utility >= maxUtility:
					result = copy.deepcopy(candidate)
					maxUtility = utility
					candidate.pop()
			# explores current state if new
			if state not in visited:
				visited.append(state)
				# expands fringe
				for successor in self.world.getSuccessors(state):
					nextState = successor[0]
					nextAction = successor[1]
					nextUtility = self.world.getExpectedUtility(nextState, depth)
					candidate.append([nextAction, nextUtility])
					if nextState not in visited:
						heapq.heappush(pq, (nextUtility, nextState, depth + 1))
						# maintains a fix-sized heap
						if len(pq) > maxSize:
							heapq.heappop(pq)
		return result

