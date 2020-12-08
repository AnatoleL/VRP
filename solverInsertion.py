from solver import Solver
from utils import norm
import sys
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

class SolverInsertion(Solver):
    def __init__(self, path):
        Solver.__init__(self, path)

    def computeRoadForVehicle(self, vehicle):

        def distanceDelta(posA, posB, newPos):
            return norm(posA, newPos) + norm(newPos, posB) - norm(posA, posB)

        for currentPoint in self.points:
            minimumPotentialDistance = sys.float_info.max
            for i in range(0, len(vehicle.route)):
                potentialDistance = vehicle.totalDistance + distanceDelta(vehicle.route[i - 1].pos, vehicle.route[i].pos, currentPoint.pos)
                if potentialDistance < minimumPotentialDistance:
                    minimumPotentialDistance = potentialDistance
                    potentialPointIndex = i
            
            vehicle.insertPointToRoute(currentPoint, potentialPointIndex)


    def plotRoads(self, figpath):
        # verts = [(self.warehouse.x, self.warehouse.y)] + 
        verts = self.vehicles[0].routeToVertices()

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
        fig.suptitle("Total distance: %d, computed with insertion" % (self.vehicles[0].totalDistance))
        plt.savefig(figpath)
        plt.close(fig)