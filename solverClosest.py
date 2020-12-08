import sys
import csv
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from enum import Enum
from utils import distanceType, Point, Position, Vehicle, norm, manhattan, squareNorm
from solver import Solver

# The solver itself
class SolverClosest(Solver):
    def __init__(self, path, method):
        Solver.__init__(self, path)
        self.method = method
        if (method == distanceType.MANHATTAN):
            self.computeDistance = manhattan
        elif (method == distanceType.NORM):
            self.computeDistance = norm
        elif (method == distanceType.SQUARE_NORM):
            self.computeDistance = squareNorm

    def computeRoadForVehicle(self, vehicle):
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