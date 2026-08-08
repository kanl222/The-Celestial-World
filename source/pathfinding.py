import heapq
import math
from config import TILESIZE

class Pathfinder:
    """Класс для поиска пути с использованием алгоритма A* (A-Star)."""
    def __init__(self, grid: list[list[int]]):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0
        # Кэшируем размер тайла — не импортируем каждый вызов
        self._tilesize = TILESIZE

    def get_neighbors(self, node: tuple[int, int]) -> list[tuple[int, int]]:
        r, c = node
        neighbors = []
        # Направления: 4 ортогональных и 4 диагональных
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.grid[nr][nc] == 0:
                    # Предотвращаем срез углов (проход по диагонали сквозь углы стен)
                    if dr != 0 and dc != 0:
                        if self.grid[r + dr][c] != 0 or self.grid[r][c + dc] != 0:
                            continue
                    neighbors.append((nr, nc))
        return neighbors

    def heuristic(self, a: tuple[int, int], b: tuple[int, int]) -> float:
        # Окто-расстояние (для 8-связной сетки)
        dr = abs(a[0] - b[0])
        dc = abs(a[1] - b[1])
        return (dr + dc) + (1.414 - 2) * min(dr, dc)

    def find_path(self, start_pos: tuple[float, float], end_pos: tuple[float, float]) -> list[tuple[float, float]]:
        """Находит кратчайший путь в пиксельных координатах.
        Возвращает список точек (x, y) для прохождения.
        """
        ts = self._tilesize
        start_node = (int(start_pos[1] // ts), int(start_pos[0] // ts))
        end_node = (int(end_pos[1] // ts), int(end_pos[0] // ts))

        # Проверка выхода за границы сетки
        if not (0 <= start_node[0] < self.rows and 0 <= start_node[1] < self.cols):
            return []
        if not (0 <= end_node[0] < self.rows and 0 <= end_node[1] < self.cols):
            return []

        # Если конечная точка заблокирована, найдем ближайшую свободную
        if self.grid[end_node[0]][end_node[1]] != 0:
            free_neighbors = []
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = end_node[0] + dr, end_node[1] + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] == 0:
                        free_neighbors.append((nr, nc))
            if free_neighbors:
                end_node = min(free_neighbors, key=lambda n: abs(n[0] - end_node[0]) + abs(n[1] - end_node[1]))
            else:
                return []

        # priority queue: (f_score, g_score, node)
        queue = []
        heapq.heappush(queue, (0, 0, start_node))
        
        g_score = {start_node: 0}
        came_from = {}
        visited: set = set()

        while queue:
            _, current_g, current = heapq.heappop(queue)

            if current in visited:
                continue
            visited.add(current)

            if current == end_node:
                path = []
                node = current
                while node in came_from:
                    pixel_x = node[1] * ts + ts // 2
                    pixel_y = node[0] * ts + ts // 2
                    path.append((pixel_x, pixel_y))
                    node = came_from[node]
                path.reverse()
                return path

            for neighbor in self.get_neighbors(current):
                weight = 1.414 if (neighbor[0] != current[0] and neighbor[1] != current[1]) else 1.0
                tentative_g = current_g + weight

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f = tentative_g + self.heuristic(neighbor, end_node)
                    came_from[neighbor] = current
                    heapq.heappush(queue, (f, tentative_g, neighbor))

        return []
