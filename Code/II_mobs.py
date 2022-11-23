import pygame as pg
from heapq import *
from numpy import array
from Sitting import TILESIZE


class IIMoving():
    def __init__(self, grid):
        self.cols, self.rows = len(grid), len(grid[0])
        self.TILE = TILESIZE
        self.grid = grid
        self.visited = {}
        self.create_graph()

    def create_graph(self):
        self.graph = {}
        for y, row in enumerate(self.grid):
            for x, _ in enumerate(row):
                self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_neighbours(x,
                                                                                      y)

    def get_circle(self, x, y):
        return (x * self.TILE + self.TILE // 2,
                y * self.TILE + self.TILE // 2), self.TILE // 4

    def get_neighbours(self, x, y):
        check_neighbour = lambda x,y: True if 0 <= x < self.cols and 0 <= y < self.rows else False
        ways = [-1, 0], [0, -1], [1, 0], [0, 1]  # , [-1, -1], [1, -1], [1, 1], [-1, 1]
        return [(self.grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if
                check_neighbour(x + dx, y + dy)]

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def dijkstra(self, start, goal, graph):
        queue = []
        heappush(queue, (0, start))
        cost_visited = {start: 0}
        visited = {start: None}

        while queue:
            cur_cost, cur_node = heappop(queue)
            if cur_node == goal:
                break

            neighbours = graph[cur_node]
            for neighbour in neighbours:
                neigh_cost, neigh_node = neighbour
                new_cost = cost_visited[cur_node] + neigh_cost

                if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                    priority = new_cost + self.heuristic(neigh_node, goal)
                    heappush(queue, (priority, neigh_node))
                    cost_visited[neigh_node] = new_cost
                    visited[neigh_node] = cur_node
        return visited

    def xy_(self, cords: tuple):
        return tuple(array(cords) // self.TILE)

    def move_in_point(self, player, start_pos
                      , ClassMobs):
        self.start_pos = self.xy_(start_pos)
        self.end_pos = self.xy_(player.rect.center)
        visited = self.dijkstra(self.start_pos,
                                     self.end_pos,
                                     self.graph)
        print(visited)
        visited = [tuple(array(k) - array(v)) if v is not None else (0,0) for k, v in visited.items()][1:]
        print(visited,self.start_pos,self.end_pos)
        while visited:
            ClassMobs.direction = pg.math.Vector2(visited.pop(0))
            print(ClassMobs.direction)
            ClassMobs.move(ClassMobs.speed)
