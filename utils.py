from enum import Enum
import math
import sys

# Heuristics
def norm(A, B):
    return math.sqrt(pow(B.x - A.x, 2) + pow(B.y - A.y, 2))

def squareNorm(A, B):
    return pow(B.x - A.x, 2) + pow(B.y - A.y, 2)

def manhattan(A, B):
    return abs(B.x - A.x) + abs(B.y - A.y)

class distanceType(Enum):
    MANHATTAN = "Manhattan"
    NORM = "Norm"
    SQUARE_NORM = "Square norm"

# Describes a position on the plan
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(%d, %d)" % (self.x, self.y)

# A point in the VRP problem, with coordinates, wight and utility
class Point:
    def __init__(self, index, x, y, weight, utility):
        self.index = index
        self.pos = Position(x, y)
        self.weight = weight
        self.utility = utility

    def value(self):
        if self.weight != 0:
            return self.utility/self.weight
        else:
            return self.utility

    def __str__(self):
        return "i: %d, pos: %s, weight: %d, utility: %d (, value: %.2f)" % (self.index, self.pos, self.weight, self.utility, self.value())

# A vehicle in the VRP problem with a capacity
class Vehicle:
    def __init__(self, index, capacity, warehouse):
        self.index = index
        self.capacity = capacity
        self.route = [
            Point(-1, warehouse.x, warehouse.y, 0, sys.float_info.max),
            Point(-1, warehouse.x, warehouse.y, 0, sys.float_info.max)
        ]
        self.totalDistance = 0
        self.totalUtility = 0
        self.warehouse = warehouse

    def addPointToRoute(self, point):
        if len(self.route) == 0:
            self.totalDistance = norm(self.warehouse, point.pos)
        else:
            self.totalDistance += norm(self.route[-1].pos, point.pos)

        self.route.append(point)

    def insertPointToRoute(self, point, index):
        self.totalDistance += norm(self.route[index - 1].pos, point.pos) + norm(point.pos, self.route[index].pos) - norm(self.route[index - 1].pos, self.route[index].pos) 
        self.route.insert(index, point)
        self.totalUtility += point.utility
        

    def routeToVertices(self):
        return [(point.pos.x, point.pos.y) for point in self.route]

    def __str__(self):
        return "i: %d, capacity: %d" % (self.index, self.capacity)
