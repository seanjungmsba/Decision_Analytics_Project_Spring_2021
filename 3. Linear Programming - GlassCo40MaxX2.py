# This example formulates and solves the following primal LP:
# maximize 70x0 + 20x1 + 50x2
# subject to
# 10x0 + 20x1 + 10x2 <= 4300
# 30x0        + 20x2 <= 4600
# 10x0 + 40x1        <= 4200
# x0, x1, x2 >= 0
# Max x2 st opt solution >=13500
# Note this is GlassCo but adding 40 to X0 obj func coefficient
# and maximizing X2 to fund alternate optimal solution

from gurobipy import *
try:
    # Create a new model
    m = Model("GlassCo")

    # Create variables, use default values
    # Defaults lb=0.0, ub=GRB.INFINITY, obj=0.0, vtype=GRB.CONTINUOUS
    x = m.addVars(3, name="x")
	
    # Set objective
    m.setObjective(x[2], GRB.MAXIMIZE)

    # Add constraint: 10x0 + 20x1 + 10x2 <= 4300
    m.addConstr(10*x[0] + 20*x[1] + 10*x[2] <= 4300, "c1")

    # Add constraint: 30x0 + 20x2 <= 4600
    m.addConstr(30*x[0] + 20*x[2] <= 4600, "c2")

    # Add constraint:  10x0 + 40x1 <= 4200
    m.addConstr(10*x[0] + 40*x[1] <= 4200, "c3")
	
	# Add constraint so original obj func >= 13500
    m.addConstr(70*x[0] + 20*x[1] + 50*x[2] >= 13500, "c4")
	
    m.optimize()

    print('Optimal Obj Func Value: %g' % m.objVal)
    	
    for v in m.getVars():
        print('%s %g Red Cost %g Lower %g Upper %g' 
        % (v.varName, v.x, v.RC, v.SAOBJLow, v.SAObjUp)
        )

    for c in m.getConstrs():
    #    if c.Pi != 0:
            print('Constraint %s Shadow Price %g Lower %g Upper %g' % 
                (c.constrName, c.Pi, c.SARHSLow, c.SARHSUp))

    m.write("GlassCo.mps")

except GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')
