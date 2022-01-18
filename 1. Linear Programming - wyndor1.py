#!/usr/bin/python
# This example formulates and solves the Wyndor model from Section 3.1:
# maximize 3x0 + 5x1
# subject to
# x0 <= 4
# 2x1 <= 12
# 3x0 + 2x1 <=18
# x0, x1 >= 0
from gurobipy import *
try:
	# Create a new model
	m = Model("wyndor1")
	
	# Create variables, use default values
	# Defaults lb=0.0, ub=GRB.INFINITY, obj=0.0, vtype=GRB.CONTINUOUS
	x = m.addVars(2, name="x")
		
	# Set objective
	m.setObjective(3 * x[0] + 5 * x[1], GRB.MAXIMIZE)
	
	# Add constraint: x0 <= 4
	m.addConstr(x[0] <= 4, "c1")
	
	# Add constraint: 2x1 <= 12
	m.addConstr(2 * x[1] <= 12, "c2")
	
	# Add constraint: 3x0 + 2x1 <= 18
	m.addConstr(3 * x[0] + 2 * x[1] <= 18, "c3")
	
	m.optimize()
	
	for v in m.getVars():
		print('%s %g' % (v.varName, v.x))
	
	print('Obj: %g' % m.objVal)
except GurobiError as e:
	print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
	print('Encountered an attribute error')
