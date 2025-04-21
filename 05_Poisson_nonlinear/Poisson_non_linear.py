from __future__ import print_function
from fenics import *

def q(u):
    "Return non-linear coefficient"
    return 1+u**2

import sympy as sym

x, y = sym.symbols('x[0], x[1]')
u= 1 + x + 2*y
f= sym.diff(q(u)*sym.diff(u,x),x) - sym.diff(q(u)*sym.diff(u,y),y)
f = sym.simplify(f) 
u_code = sym.printing.ccode(u)
f_code = sym.printing.ccode(f)
print('u = ', u_code)
print('f =', f_code)

# Create mesh and define function space

mesh = UnitSquareMesh(8,8)
V = FunctionSpace(mesh, 'P', 1)


# Define boundary condition
u_D = Expression(u_code, degree = 2)

def boundary(x, on_boundary):
    return on_boundary

bc = DirichletBC(V, u_D, boundary)

# Define variational problem
u = Function(V)
v = TestFunction(V)
f = Expression(f_code, degree = 2)
F =  q(u)*dot(grad(u), grad(v))*dx - f*v*dx

# Compute solution
solve(F == 0, u, bc)

# Plot solution 
plot(u)

# Compute maximum error at vertices. This computation illustrates 
# an alterantive to using compute_vertex_values as in poisson.py

u_e = interpolate(u_D, V)
import numpy as np
error_max = np.abs(u_e.vector().array() - u.vector().array()).max()
print('error_max =', error_max)

# Hold plot
interactive()
