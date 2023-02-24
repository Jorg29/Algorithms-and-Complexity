import pygame
import random
import sys
from disjoint_set import DisjointSet

# pygame variables
HEIGHT = 1000
WIDTH = 800
CELL_SIZE = 40

ROWS = int(sys.argv[1])
COLUMNS = int(sys.argv[2])

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# tfunctionhat converts the edges from a list of tuples to a dictionary
def make_graph(V: list[int],E: list[tuple]) -> dict:
    graph = {}
    for elem in V:
        tempList = []
        for item in E:
            if elem in item:
                if elem == item[0]:
                    tempList.append(item[1])
                else:
                    tempList.append(item[0])
        graph[elem] = tempList
        tempList = []
    return graph

class Cell(object):
    def __init__(self, x, y, SCREEN):
        # position in matrix 
        self.x = x
        self.y = y
        self.SCREEN = SCREEN
        # keeps track of which walls are still visible
        self.walls = [True, True, True, True]
        # checks if cell has been visited during generation 
        self.generated = False
        # checks if cell is on path during solving 
        self.on_path = False
        # checks if cell has been visited during solving 
        self.visited = False
        self.starting_point = False
        self.finishing_point = False

    def draw_cell(self):
        # coordinates on self.SCREEN
        x = self.x * CELL_SIZE + 10
        y = self.y * CELL_SIZE + 10 
        # draws a wall if it still exists
        if self.walls[0]:
            pygame.draw.line(self.SCREEN, BLACK, (x, y), (x + CELL_SIZE, y), 5)
        if self.walls[1]:
            pygame.draw.line(self.SCREEN, BLACK, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 5)
        if self.walls[2]:
            pygame.draw.line(self.SCREEN, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 5)
        if self.walls[3]:
            pygame.draw.line(self.SCREEN, BLACK, (x, y), (x, y + CELL_SIZE), 5)
        # marks white if generated during generation
        if self.generated:
            pygame.draw.rect(self.SCREEN, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
        # marks black if on path during solving
        if self.on_path:
            pygame.draw.rect(self.SCREEN, BLACK, (x + 5, y + 5 , CELL_SIZE* 0.75, CELL_SIZE* 0.75))
        if self.starting_point:
            pygame.draw.rect(self.SCREEN, BLUE, (x + 5, y + 5, CELL_SIZE*0.75 , CELL_SIZE*0.75))
        if self.finishing_point:
            pygame.draw.rect(self.SCREEN, RED, (x + 5, y + 5 , CELL_SIZE* 0.75, CELL_SIZE* 0.75))

def initiate_maze(SCREEN):
    maze = []
    for x in range(COLUMNS):
        for y in range(ROWS):
            cell = Cell(y, x, SCREEN)
            maze.append(cell)
    if sys.argv[3] == "U":
        maze[int(sys.argv[4])].walls[0] = False
        maze[int(sys.argv[4])].starting_point = True
    if sys.argv[3] == "D":
        maze[-int(sys.argv[4]) - 1].walls[1] = False
        maze[-int(sys.argv[4]) - 1].starting_point = True
    if sys.argv[3] == "L":
        maze[int(sys.argv[4]) * ROWS].walls[3] = False
        maze[int(sys.argv[4]) * ROWS].starting_point = True
    if sys.argv[3] == "R":
        maze[int(sys.argv[4]) * ROWS + (COLUMNS) - 1].walls[2] = False
        maze[int(sys.argv[4]) * ROWS + (COLUMNS) - 1].starting_point = True
    if sys.argv[5] == "U":
        maze[int(sys.argv[6])].walls[0] = False
        maze[int(sys.argv[6])].finishing_point = True
    if sys.argv[5] == "D":
        maze[-int(sys.argv[6]) - 1].walls[1] = False
        maze[-int(sys.argv[6]) - 1].finishing_point = True
    if sys.argv[5] == "L":
        maze[int(sys.argv[6]) * ROWS].walls[3] = False
        maze[int(sys.argv[6]) * ROWS].finishing_point = True
    if sys.argv[5] == "R":
        maze[(int(sys.argv[6]) + 1) * ROWS - 1].walls[2] = False
        maze[(int(sys.argv[6]) + 1) * ROWS - 1].finishing_point = True
    return maze

def in_bounds(x, y):
    return 0 <= x < COLUMNS and 0 <= y < ROWS

def find_neighbours(x, y):
    neighbors = []
    dx, dy = [1, -1, 0, 0], [0, 0, 1, -1]
    for d in range(4):
        # add cell to neighbor list if it is in bounds and not generated
        if in_bounds(x + dx[d], y + dy[d]):
            neighbors.append((x * ROWS + y, (x + dx[d]) * ROWS + (y + dy[d])))
    return neighbors

def find_edges():
    dx, dy = [1, -1, 0, 0], [0, 0, 1, -1]
    edges = set()
    for x in range(COLUMNS):
        for y in range(ROWS):
            for d in range(4):
                if in_bounds(x + dx[d], y + dy[d]):
                    x1 = x * ROWS + y
                    x2 = (x + dx[d]) * ROWS + (y + dy[d])
                if x1 < x2:
                    x1, x2 = x2, x1
                    edges.add((x1, x2))
    return edges

def remove_wall(maze: list[Cell], c1: int, c2: int):
    # horizontal edge
    if c1 - c2 == 1:
        maze[c1].walls[3] = False
        maze[c2].walls[2] = False
    # vertical edge
    if c1 - c2 >= 3:
        maze[c1].walls[0] = False
        maze[c2].walls[1] = False
    maze[c1].generated = True
    maze[c2].generated = True

# pygame window 
pygame.init()
SCREEN = pygame.display.set_mode((HEIGHT,WIDTH))
pygame.display.set_caption("Labyrinth")
clock = pygame.time.Clock()
fps = 60

def bfs(maze: list[Cell], s: int, f: int, path: list[tuple]):
    # vertices representing cells of maze
    vertices = [i for i in range(ROWS * COLUMNS)]
    start = f
    queue = [start]
    maze[start].visited = True
    bfsPath = {}
    graph = make_graph(vertices, path)
    while queue:
        current = queue.pop(0)
        if current == s:
            break
        for d in [-ROWS, ROWS, -1, 1]:
            if current + d in graph[current]:
                child = current + d
            else:
                continue
            if maze[child].visited:
                continue
            queue.append(child)
            maze[child].visited = True
            maze[child].on_path = True
            draw_screen(maze)
            pygame.time.delay(100)
            bfsPath[child] = current
    for cell in maze:
        cell.on_path = False
    fwdPath = {}
    t = s
    while t != start:
        fwdPath[bfsPath[t]] = t
        t = bfsPath[t]
        maze[t].on_path = True

def draw_screen(maze: list[Cell]):
    SCREEN.fill(WHITE)
    for i in range(ROWS * COLUMNS):
        maze[i].draw_cell()
    pygame.display.update()

if __name__ == "__main__":
    maze = initiate_maze(SCREEN)
    edges = find_edges()
    path = []
    
    # find positions in maze of starting point and finishing point
    for i in range(len(maze)):
        if maze[i].starting_point:
            s = i
        elif maze[i].finishing_point:
            f = i

    # make disjoint set
    ds = DisjointSet()
    for i in range(ROWS * COLUMNS):
        ds.find(i)

    # game parameters
    running = True
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.type == pygame.QUIT:
                    running = False

        # if disjoint set becomes singleton, start finding path and end program
        if len(list(ds.itersets())) == 1:
            bfs(maze, s, f, path)
            draw_screen(maze)
            pygame.time.delay(3000)
            break

        # maze generation algorithm
        e = random.sample(edges, 1)
        edges.remove((e[0][0], e[0][1]))
        u = ds.find(e[0][0])
        v = ds.find(e[0][1])
        if not ds.connected(u, v):
            path.append((e[0][0], e[0][1]))
            ds.union(u, v)
            remove_wall(maze, e[0][0], e[0][1])
        draw_screen(maze)
pygame.quit()
