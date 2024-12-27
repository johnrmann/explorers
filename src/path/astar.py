import heapq

from src.world.terrain import Terrain
from src.math.adj import keyed_adj_cells
from src.math.distance import planet_manhattan_distance

def _always_false(_):
	return False

def astar(start, goal, terrain: Terrain, is_cell_occupied=None):
	"""
	Perform an A* search on the terrain to find the shortest path from the
	start cell to the goal.

	TODO(jm) - make it take in a player object, to account for different
	terrain negotiation skills.
	"""
	if is_cell_occupied is None:
		is_cell_occupied = _always_false
	if is_cell_occupied(goal):
		return []

	dims = terrain.dimensions
	goal_height = terrain.height_at(goal)

	def heuristic(cell):
		z = abs(terrain.height_at(cell) - goal_height)
		xy = planet_manhattan_distance(dims, cell, goal)
		return xy + z

	def cost(src, direction):
		delta_h = abs(terrain.height_delta(src, direction))
		return delta_h + 1

	open_set = []
	heapq.heappush(open_set, (0, start))
	came_from = {}
	g_score = {start: 0}
	f_score = {start: heuristic(start)}

	while open_set:
		_, current = heapq.heappop(open_set)

		if current == goal:
			# Reconstruct the path by backtracking
			path = []
			while current in came_from:
				path.append(current)
				current = came_from[current]
			path.append(start)
			return path[::-1]  # Reverse to get path from start to goal

		for (direction, nxt) in keyed_adj_cells(dims, current).items():
			if is_cell_occupied(nxt):
				continue

			tentative_g_score = g_score[current] + cost(current, direction)

			if nxt not in g_score or tentative_g_score < g_score[nxt]:
				came_from[nxt] = current
				g_score[nxt] = tentative_g_score
				f_score[nxt] = tentative_g_score + heuristic(nxt)
				heapq.heappush(open_set, (f_score[nxt], nxt))

	# Return an empty path if there's no path to the goal
	return []
