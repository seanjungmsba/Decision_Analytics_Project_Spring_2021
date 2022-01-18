# This example formulates and solves the following dual LP:
# minimize 4300y0 + 4600y1 + 4200y2
# subject to
# 10y0 + 30y1 + 10y2 >= 30
# 20y0        + 40y2 >= 20
# 10y0 + 20y1        >= 50
# y0, y1, y2 >= 0
from gurobipy import *
try:
    # Create a new model
    m = Model("GlassCoDual")

    # Create variables, use default values
    # Defaults lb=0.0, ub=GRB.INFINITY, obj=0.0, vtype=GRB.CONTINUOUS
    y = m.addVars(3, name="y")
	
    # Set objective
    m.setObjective(4300*y[0] + 4600*y[1] + 4200*y[2], GRB.MINIMIZE)

    # Add constraints noted above
    m.addConstr(10*y[0] + 30*y[1] + 10*y[2] >= 30, "c1")

    m.addConstr(20*y[0] + 40*y[2] >= 20, "c2")

    m.addConstr(10*y[0] + 20*y[1] >= 50, "c3")

    m.optimize()

    print('Optimal Obj Func Value: %g' % m.objVal)
    	
    for v in m.getVars():
        print('%s %g Red Cost %g Lower %g Upper %g' 
        % (v.varName, v.x, v.RC, v.SAOBJLow, v.SAObjUp)
        )

    for c in m.getConstrs():
            print('Constraint %s Shadow Price %g Lower %g Upper %g' % 
                (c.constrName, c.Pi, c.SARHSLow, c.SARHSUp))

    m.write("GlassCo.mps")

except GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')
