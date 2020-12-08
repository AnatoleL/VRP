import csv
import sys
import math

# Heuristics
def norm(A, B):
    return math.sqrt(pow(B.x - A.x, 2) + pow(B.y - A.y, 2))

def squaredNorm(A, B):
    return pow(B.x - A.x, 2) + pow(B.y - A.y, 2)

def manhattan(A, B):
    return B.x - A.x + B.y - A.y

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
        self.route = list()
        self.totalDistance = 0
        self.warehouse = warehouse

    def addPointToRoute(self, point):
        if len(self.route) == 0:
            self.totalDistance = norm(self.warehouse, point.pos)
        else:
            self.totalDistance += norm(self.route[-1].pos, point.pos)

        self.route.append(point)

    def __str__(self):
        return "i: %d, capacity: %d" % (self.index, self.capacity)

# The solver itself
class Solver:
    def __init__(self):
        print('Solver started. Please load an instance')
        self.i = None
        self.nbVehicles = None
        self.nbPoints = None
        self.vehicles = list()
        self.points = list()
        self.warehouse = None

    def load(self, path):
        print('Loading \'' + path + '\'')
        with open(path, newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            rows = list(reader)
            self.i = rows[0][0]
            self.nbVehicles = int(rows[1][0])
            self.nbPoints = int(rows[2][0])
            self.warehouse = Position(int(rows[3][0]), int(rows[3][1]))
            for i in range(4, 4 + self.nbVehicles):
                self.vehicles.append(Vehicle(int(rows[i][0]), int(rows[i][1]), self.warehouse))
            for i in range(4 + self.nbVehicles, 4 + self.nbVehicles + self.nbPoints):
                self.points.append(Point(int(rows[i][0]), int(rows[i][1]), int(rows[i][2]), int(rows[i][3]), int(rows[i][4])))

    def computeRoadForVehicle(self, vehicle, computeDistance):
        def closestUnvisitedPoint(unvisitedPoints):
            distanceToChosenPoint = sys.float_info.max
            for currentUnvisitedPoint in unvisitedPoints:
                if len(vehicle.route) == 0:
                    distanceToCurrentPoint = computeDistance(self.warehouse, currentUnvisitedPoint.pos)
                else:
                    distanceToCurrentPoint = computeDistance(vehicle.route[-1].pos, currentUnvisitedPoint.pos)

                if distanceToCurrentPoint < distanceToChosenPoint:
                    distanceToChosenPoint = distanceToCurrentPoint
                    chosenPoint = currentUnvisitedPoint

            return chosenPoint

        self.points.sort(key= lambda p : p.value(), reverse=True)
        unvisitedPoints = [point for point in self.points]

        while len(unvisitedPoints):
            chosenPoint = closestUnvisitedPoint(unvisitedPoints)
            vehicle.addPointToRoute(chosenPoint)
            unvisitedPoints.remove(chosenPoint)

    def solve(self):
        self.computeRoadForVehicle(self.vehicles[0], squaredNorm)

    def dumpInstance(self):
        print("I: %s" % self.i)
        print("%d Vehicles:" % self.nbVehicles)
        for vehicle in self.vehicles:
            print(vehicle)
        print("%d Points:" % self.nbPoints)
        for point in self.points:
            print(point)
        print("Warehouse: %s" % self.warehouse)

    def dumpRoads(self):
        for vehicle in self.vehicles:
            print(vehicle)
            print("Distance: %d" % vehicle.totalDistance)
            for point in vehicle.route:
                print(point)