# This example formulates and solves the California Manufacturing
# Company problem from the text:
# maximize 9x0 + 5x1 + 6x2 + 4x3
# subject to
# 6x0 + 3x1 + 5x2 + 2x3 <= 10
#              x2 +  x3 <= 1
# -x0 +        x2       <= 0
#       -x1 +        x3 <= 0
# x0, x1, x2, x3 binary
from gurobipy import *
try:
    # Create a new model
    m = Model("CalCo")

    # Create binary variables
    x = m.addVars(4, vtype=GRB.BINARY, name="x")
	
    # Set objective
    m.setObjective(9*x[0] + 5*x[1] + 6*x[2] + 4*x[3], GRB.MAXIMIZE)

    # Add constraints
    m.addConstr(6*x[0] + 3*x[1] + 5*x[2] + 2*x[3] <= 10, "c1")
    m.addConstr(x[2] +  x[3] <= 1, "c2")
    m.addConstr(x[2] <= x[0], "c3")
    m.addConstr(x[3] <= x[1], "c4")
    m.optimize()

    print('Optimal Obj Func Value: %g' % m.objVal)
    	
    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))

    m.write("CalCo.mps")

except GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')
