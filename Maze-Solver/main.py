from email.policy import default
from PIL import Image
import numpy
from collections import defaultdict
from queue import PriorityQueue
import pygame

print("MAZE SOLVER")
print("PLEASE USE A SQUARE PNG IMAGE OF BLACK AND WHITE PIXELS\nYOUR IMAGE SHOULD ALSO HAVE A BLACK BORDER EXCEPT FOR\nONE WHITE PIXEL IN THE TOP ROW FOR THE ENTRACE AND ONE WHITE PIXEL IN THE BOTTOM ROW FOR THE EXIT\nMAKE SURE YOUR PNG IS IN THE SAME FOLDER AS THIS PYTHON SCRIPT")
maze_file = input("NAME OF FILE: ")
if maze_file.count(".png") == 1:
    map_img = Image.open(f"./{maze_file}")
    pygame_img = pygame.image.load(f"./{maze_file}")
else:
    map_img = Image.open(f"./{maze_file}.png")
    pygame_img = pygame.image.load(f"./{maze_file}.png")
map_sequence = map_img.getdata()
cols, rows = map_img.size
surface = pygame.Surface((cols,rows))
map_numpy_array = numpy.array(map_sequence)
map_array = []
for row in map_numpy_array:
    if (row[0] + row[1] + row[2])/3 > 230:
        map_array.append(1)
    else:
        map_array.append(0)

nodes = []
start = 0
end = 0

def draw(path):
    surface.blit(pygame_img,(0,0))
    for i in range(len(path)-1):
        x1 = path[i]%cols
        y1 = path[i]//rows
        x2 = path[i+1]%cols
        y2 = path[i+1]//rows
        pygame.draw.line(surface,(255,0,0),(x1,y1),(x2,y2),1)
    if maze_file.count(".png") == 1:
        pygame.image.save(surface, f"./solved_{maze_file}")
    else:
        pygame.image.save(surface, f"./solved_{maze_file}.png")

for x in range(cols):
    if map_array[x] == 1:
        start = x
    if map_array[cols*(rows-1)+x] == 1:
        end = cols*(rows-1)+x
nodes.append(start)

class node:
    def __init__(self,index,prev,weight):
        self.index = index
        self.prev = prev
        self.weight = weight

for x in range(rows*cols):
    xConnects = 0
    yConnects = 0
    wallCount = 0
    if map_array[x] == 1 and x != start and x != end:
        if map_array[x-1] == 1 or map_array[x+1] == 1:
            xConnects += 1
        if map_array[x-cols] == 1 or map_array[x+cols] == 1:
            yConnects += 1
        if map_array[x-1] == 0:
            wallCount += 1
        if map_array[x+1] == 0:
            wallCount += 1
        if map_array[x-cols] == 0:
            wallCount += 1
        if map_array[x+cols] == 0:
            wallCount += 1
    if xConnects > 0 and yConnects > 0:
        nodes.append(x)
    if wallCount > 2:
        nodes.append(x)

nodes.append(end)


class graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def create_graph(self,nodes):
        for col in range(cols):
            prev = None
            for row in range(rows):
                if row*cols+col in nodes:
                    if not prev:
                        prev = row*cols+col
                    else:
                        weight = ((row*cols+col)-prev)//cols
                        self.graph[prev].append((row*cols+col,weight))
                        self.graph[row*cols+col].append((prev,weight))
                        prev = row*cols+col
                if map_array[row*cols+col] == 0:
                    prev = None
        for row in range(rows):
            prev = None
            for col in range(cols):
                if row*cols+col in nodes:
                    if not prev:
                        prev = row*cols+col
                    else:
                        weight = row*cols+col-prev
                        self.graph[prev].append((row*cols+col,weight))
                        self.graph[row*cols+col].append((prev,weight))
                        prev = row*cols+col
                if map_array[row*cols+col] == 0:
                    prev = None

    def print_graph(self):
        print(self.graph)

    def djikstras(self):
        tie_breaker = 0
        visited = set([])
        prev_tracker = [0 for x in range(rows*cols)]
        s = node(start,None,0)
        q = PriorityQueue()
        q.put((s.weight,tie_breaker,s))
        tie_breaker += 1
        path = [end]
        while q:
            item = q.get()
            curr_node = item[2]
            curr_weight = curr_node.weight
            visited.add(curr_node.index)
            if(curr_node.index == end):
                break
            for neighbor in self.graph[curr_node.index]:
                if neighbor[0] not in visited:
                    new_weight = curr_weight + neighbor[1]
                    new_node = node(neighbor[0],curr_node.index,new_weight)
                    prev_tracker[neighbor[0]] = curr_node.index
                    q.put((new_weight,tie_breaker,new_node))
                    tie_breaker += 1
        curr = end
        while path[len(path)-1] != start:
            curr = prev_tracker[curr]
            path.append(curr)
        path = path[::-1]
        return path

g = graph()
g.create_graph(nodes)
p = g.djikstras()
draw(p)



                    
            








