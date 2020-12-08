import csv

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
        self.coords = Position(x, y)
        self.weight = weight
        self.utility = utility

    def value(self):
        if self.weight != 0:
            return self.utility/self.weight
        else:
            return self.utility

    def __str__(self):
        return "i: %d, coords: %s, weight: %d, utility: %d (, value: %.2f)" % (self.index, self.coords, self.weight, self.utility, self.value())

# A vehicle in the VRP problem with a capacity
class Vehicle:
    def __init__(self, index, capacity):
        self.index = index
        self.capacity = capacity

    def __str__(self):
        return "i: %d, capacity: %d" % (self.index, self.capacity)

# The solver itself
class Solver:
    def __init__(self):
        print('Solver started. Please load an instance')
        self.i = None
        self.vehicles = list()
        self.nbVehicles = None
        self.points = list()
        self.nbPoints = None
        self.wareHouse = None

    def load(self, path):
        print('Loading \'' + path + '\'')
        with open(path, newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            rows = list(reader)
            self.i = rows[0][0]
            self.nbVehicles = int(rows[1][0])
            self.nbPoints = int(rows[2][0])
            self.wareHouse = Position(int(rows[3][0]), int(rows[3][1]))
            for i in range(4, 4 + self.nbVehicles):
                self.vehicles.append(Vehicle(int(rows[i][0]), int(rows[i][1])))
            for i in range(4 + self.nbVehicles, 4 + self.nbVehicles + self.nbPoints):
                self.points.append(Point(int(rows[i][0]), int(rows[i][1]), int(rows[i][2]), int(rows[i][3]), int(rows[i][4])))
                

    def dump(self):
        print("I: %s" % self.i)
        print("%d Vehicles:" % self.nbVehicles)
        for vehicle in self.vehicles:
            print(vehicle)
        print("%d Points:" % self.nbPoints)
        for point in self.points:
            print(point)
        print("Warehouse: %s" % self.wareHouse)
