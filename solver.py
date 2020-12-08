from utils import distanceType, Point, Position, Vehicle, norm, manhattan, squareNorm
import csv

class Solver:
    def __init__(self, path):
        print('Solver started. Please load an instance')
        self.vehicles = list()
        self.points = list()
        self.load(path)

    def solve(self):
        self.computeRoadForVehicle(self.vehicles[0])

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
                self.vehicles.append(Vehicle(float(rows[i][0]), float(rows[i][1]), self.warehouse))
            for i in range(4 + self.nbVehicles, 4 + self.nbVehicles + self.nbPoints):
                self.points.append(Point(float(rows[i][0]), float(rows[i][1]), float(rows[i][2]), float(rows[i][3]), float(rows[i][4])))

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

    def dump(self):
        with open("./output_%s.dat" % self.i, "w+") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([self.i])
            for vehicle in self.vehicles:
                writer.writerow([vehicle.index, vehicle.totalDistance, vehicle.totalUtility])
                for point in vehicle.route:
                    if point.index != -1:
                        writer.writerow([point.index])
