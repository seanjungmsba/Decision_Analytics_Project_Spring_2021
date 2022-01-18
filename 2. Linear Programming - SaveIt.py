#!/usr/bin/python
# This example formulates and solves the SaveIt model from Section 3.4:
# It is a blending problem
# In addition to the optimal solution it prints sensitivity info

from gurobipy import *
try:
	#Profit by grade
	profit = [5.5, 4.5, 3.5]
	#Availability by material
	avail = [3000, 2000, 4000, 1000]
	#Min amount treated by material
	treat = [1500, 1000, 2000, 500]
	#Treatment cost by material
	cost = [3, 6, 4, 5]
	
	#Range of grades and materials
	grades = range(len(profit))
	materials = range(len(avail))
	totconstraints = range(17)
	
	# Create a new model
	m = Model("SaveIt")
	
	# Create variables, use default values
	# Defaults lb=0.0, ub=GRB.INFINITY, obj=0.0, vtype=GRB.CONTINUOUS
	x = m.addVars(grades, materials, name="x")
	
	# Define objective function
	ObjFunc = 5.5*(x[0,0] + x[0,1] + x[0,2] + x[0,3]) + 4.5*(
		x[1,0] + x[1,1] + x[1,2] + x[1,3]) + 3.5*(
		x[2,0] + x[2,1] + x[2,2] + x[2,3])
	
	# Set objective
	m.setObjective(ObjFunc, GRB.MAXIMIZE)
	
	# Add constraints: Mixture Specs
	m.addConstr(x[0,0] <= .3*x.sum(0,'*'), "MixA1")
	m.addConstr(x[0,1] >= .4*x.sum(0,'*'), "MixA2")
	m.addConstr(x[0,2] <= .5*x.sum(0,'*'), "MixA3")
	m.addConstr(x[0,3] == .2*x.sum(0,'*'), "MixA4")
	m.addConstr(x[1,0] <= .5*x.sum(1,'*'), "MixB1")
	m.addConstr(x[1,1] >= .1*x.sum(1,'*'), "MixB2")
	m.addConstr(x[1,3] == .1*x.sum(1,'*'), "MixB4")
	m.addConstr(x[2,0] <= .7*x.sum(2,'*'), "MixC1")
		
	# Add constraints: material availability and amount treated
	for t in materials:
		m.addConstr(x.sum('*',t) <= avail[t],"Avail[%d]" %(t+1))
		m.addConstr(x.sum('*',t) >= treat[t],"Treat[%d]" %(t+1))
	
	# Add constraint: treatment cost
	m.addConstr(
		(3*x.sum('*',0) + 6*x.sum('*',1) + 4*x.sum('*',2)
		+ 5*x.sum('*',3) <= 30000), "TreatCost") 
	
	m.optimize()
	
	print('Optimal obj func value: %g' % m.objVal)
	
	print('Grades A, B and C are 1, 2, and 3 respectively')
	
	for g in grades:
	    for t in materials:
	        print(
	        'Grade %s Material %s Quantity %g Red Cost %g Lower %g Upper %g'
	         % (g+1, t+1, x[g,t].x, x[g,t].RC, x[g,t].SAObjLow, x[g,t].SAObjUp)
            )
			
	for c in m.getConstrs():
		if c.Pi != 0:
			print('Constraint %s Shadow Price %g Lower %g Upper %g' % 
				(c.constrName, c.Pi, c.SARHSLow, c.SARHSUp))
	
	m.write("saveit.mps")
	
	
	
except GurobiError as e:
	print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
	print('Encountered an attribute error')
