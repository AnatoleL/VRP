import csv
import sys
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from enum import Enum
from utils import distanceType, Point, Position, Vehicle, norm, manhattan, squaredNorm

# The solver itself
class Solver:
    def __init__(self, path, method):
        print('Solver started. Please load an instance')
        self.vehicles = list()
        self.points = list()
        self.method = method
        self.load(path)

        if (method == distanceType.MANHATTAN):
            self.computeDistance = manhattan
        elif (method == distanceType.NORM):
            self.computeDistance = norm
        elif (method == distanceType.SQUARED_NORM):
            self.computeDistance = squaredNorm

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

    def computeRoadForVehicleClosest(self, vehicle):
        def closestUnvisitedPoint(unvisitedPoints):
            distanceToChosenPoint = sys.float_info.max
            for currentUnvisitedPoint in unvisitedPoints:
                if len(vehicle.route) == 0:
                    distanceToCurrentPoint = self.computeDistance(self.warehouse, currentUnvisitedPoint.pos)
                else:
                    distanceToCurrentPoint = self.computeDistance(vehicle.route[-1].pos, currentUnvisitedPoint.pos)

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
    
    # def computeRoadForVehicleInsertion(self, vehicle):
    #     unvisitedPoints = [point for point in self.points]
    #     while len(unvisitedPoints):
    #         if len(self.vehicles)

    def solve(self):
        self.computeRoadForVehicleClosest(self.vehicles[0])

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

    def plotRoads(self, figpath):
        verts = [(self.warehouse.x, self.warehouse.y)] + self.vehicles[0].routeToVertices() + [(self.warehouse.x, self.warehouse.y)]

        codes = [Path.MOVETO]
        for i in range(len(verts) - 2):
            codes.append(Path.LINETO)
        codes.append(Path.CLOSEPOLY)

        path = Path(verts, codes)

        fig, ax = plt.subplots()
        patch = patches.PathPatch(path, facecolor='none', lw=2)
        ax.add_patch(patch)
        ax.set_xlim(-1000, 1000)
        ax.set_ylim(-1000, 1000)
        fig.suptitle("Total distance: %d, computed with %s" % (self.vehicles[0].totalDistance, self.method.value))
        plt.savefig(figpath)