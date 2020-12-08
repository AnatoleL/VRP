from utils import distanceType
from solverInsertion import SolverInsertion
from solverClosest import SolverClosest

solver = SolverInsertion('./instances/multiVehicles500.dat')
solver.solve()
solver.plotRoads('norm.png')
solver.dump()

solver = SolverClosest('./instances/multiVehicles500.dat', distanceType.SQUARE_NORM)
solver.solve()
solver.plotRoads('square.png')

# solver = SolverClosest('./instances/multiVehicles200.dat', distanceType.SQUARE_NORM)
# solver.solve()
# solver.plotRoads('squared_norm.png')

# solver = SolverClosest('./instances/multiVehicles200.dat', distanceType.MANHATTAN)
# solver.solve()
# solver.plotRoads('manhattan.png')