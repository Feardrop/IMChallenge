from __future__ import print_function
from ortools.linear_solver import pywraplp
import math as m
import numpy as np
import dataIMC as d

def main():
    # # Instantiate the Glop solver "IMChallenge".
    # solver = pywraplp.Solver('IMChallenge',
    #                                             pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    """Example of simple linear program with natural language API."""
    solver = pywraplp.Solver('IMChallenge',
                   optimization_problem_type)

    infinity = solver.infinity()

    alpha_p     = solver.BoolVar('alpha_p')
    g_v         = solver.BoolVar('g_v')
    e_jt        = solver.BoolVar('e_jt')
    x_cjt       = solver.BoolVar('x_cjt')
    y_icp       = solver.BoolVar('y_icp')
    y_cdp       = solver.BoolVar('y_cdp')
    y_0dp       = solver.BoolVar('y_0dp')
    st_cp       = solver.IntVar(0, infinity, 'st_cp')
    l_cjvr      = solver.BoolVar('l_cjvr')
    beta_vjkr   = solver.BoolVar('beta_vjkr')
    f_vrj       = solver.IntVar(0, infinity, 'f_vrj')
    z_vr        = solver.IntVar(0, infinity, 'z_vr')



    # x1, x2 and x3 are continuous non-negative variables.
    x1 = solver.NumVar(0.0, infinity, 'x1')
    x2 = solver.NumVar(0.0, infinity, 'x2')
    x3 = solver.NumVar(0.0, infinity, 'x3')

    solver.Maximize(10 * x1 + 6 * x2 + 4 * x3)
    c0 = solver.Add(10 * x1 + 4 * x2 + 5 * x3 <= 600, 'ConstraintName0')
    c1 = solver.Add(2 * x1 + 2 * x2 + 6 * x3 <= 300)
    sum_of_vars = sum([x1, x2, x3])
    c2 = solver.Add(sum_of_vars <= 100.0, 'OtherConstraintName')

    SolveAndPrint(solver, [x1, x2, x3], [c0, c1, c2])
    # Print a linear expression's solution value.
    print(('Sum of vars: %s = %s' % (sum_of_vars, sum_of_vars.solution_value())))


# Create the two variables and let them take on any value.
    alpha_p     =


    x = solver.NumVar(-solver.infinity(), solver.infinity(), 'x')
    y = solver.NumVar(-solver.infinity(), solver.infinity(), 'y')

# Constraint 1: x + 2y <= 14.
    constraint1 = solver.Constraint(-solver.infinity(), 14)
    constraint1.SetCoefficient(x, 1)
    constraint1.SetCoefficient(y, 2)

    # Constraint 2: 3x - y >= 0.
    constraint2 = solver.Constraint(0, solver.infinity())
    constraint2.SetCoefficient(x, 3)
    constraint2.SetCoefficient(y, -1)

    # Constraint 3: x - y <= 2.
    constraint3 = solver.Constraint(-solver.infinity(), 2)
    constraint3.SetCoefficient(x, 1)
    constraint3.SetCoefficient(y, -1)

    # Objective function: 3x + 4y.
    objective = solver.Objective()
    objective.SetCoefficient(x, 3)
    objective.SetCoefficient(y, 4)
    objective.SetMaximization()

    # Solve the system.
    solver.Solve()
    opt_solution = 3 * x.solution_value() + 4 * y.solution_value()
    print('Number of variables =', solver.NumVariables())
    print('Number of constraints =', solver.NumConstraints())
    # The value of each variable in the solution.
    print('Solution:')
    print('x = ', x.solution_value())
    print('y = ', y.solution_value())
    # The objective value of the solution.
    print('Optimal objective value =', opt_solution)
if __name__ == '__main__':
    main()
