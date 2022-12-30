import time
from grid import Grid
from plot_results import PlotResults

def ac3(grid, var):
    """
        This is a domain-specific implementation of AC3 for Sudoku. 

        It keeps a set of arcs to be processed (arcs) which is provided as input to the method. 
        Since this is a domain-specific implementation, we don't need to maintain a graph and a set 
        of arcs in memory. We can store in arcs the cells of the grid and, when processing a cell, 
        we ensure arc consistency of all variables related to this cell by removing the value of
        cell from all variables in its column, row, and unit. 

        For example, if the method is used as a preprocessing step, then arcs is initialized with 
        all cells that start with a number on the grid. This method ensures arc consistency by
        removing from the domain of all variables in the row, column and unit the values of 
        the cells given as input. The method adds to the set of arcs all variables that have
        their values assigned during the propagation of the contrains. 
    """
    if not type(var) == list:
        arcs = [var]
    else:
        arcs = var
    checked = set()
    while len(arcs):
        cell = arcs.pop()
        checked.add(cell)

        assigned_row, failure = grid.remove_domain_row(cell[0], cell[1])
        if failure: return failure

        assigned_column, failure = grid.remove_domain_column(cell[0], cell[1])
        if failure: return failure

        assigned_unit, failure = grid.remove_domain_unit(cell[0], cell[1])
        if failure: return failure

        arcs.extend(assigned_row)
        arcs.extend(assigned_column)
        arcs.extend(assigned_unit)    
    return False
#
def pre_process_ac3(grid):
    """
    This method enforces arc consistency for the initial grid of the puzzle.

    The method runs AC3 for the arcs involving the variables whose values are 
    already assigned in the initial grid. 
    """
    arcs_to_make_consistent = []

    for var in range(grid.get_width()):
        for var2 in range(grid.get_width()):
            if len(grid.get_cells()[var][var2]) == 1:
                arcs_to_make_consistent.append((var, var2))

    ac3(grid, arcs_to_make_consistent)
#The select_variable_fa function simply iterates through the grid 
#Returns the first variable with a domain size greater than 1.
def select_variable_fa(grid):
    for var in range(grid.get_width()):
        for var2 in range(grid.get_width()):
            domain= grid.get_cells()[var][var2]
            if len(domain)>1:
                return (var,var2)

#The select_variable_mrv function iterates through the grid 
#Finds the variables with the smallest domain size, breaking ties in any way you prefer.
def select_variable_mrv(grid):
    small_domain=10
    row_grid=-1
    col_grid=-1
    for var in range(grid.get_width()):
        for var2 in range(grid.get_width()):
            domain= grid.get_cells()[var][var2]
            if len(domain)>1:
                if len(domain)<small_domain:
                    small_domain=len(domain)
                    row_grid=var
                    col_grid=var2
    return (row_grid,col_grid)

# implementation of the search function using the 
# 1. select_variable_fa 
# 2.select_variable_mrv 
def search(grid, var_selector):
    if grid.is_solved():
        return grid, True
    call = var_selector(grid)
    for domain in grid.get_cells()[call[0]][call[1]]:
        if grid.is_value_consistent(domain, call[0], call[1]):
            gridcopy = grid.copy()
            gridcopy.get_cells()[call[0]][call[1]] = domain
            if (ac3(gridcopy, call) == False):
                i, j = search(gridcopy, var_selector)
                if j:
                    return i, True
    return None, False

# test your backtracking implementation without inference here
# this test instance is only meant to help you debug your backtracking code
# once you have implemented forward checking, it is fine to find a solution to this instance with inference

#Reding the file top95.txt
file = open('top95.txt', 'r')
problems = file.readlines()

runtime_fa = []
runtime_mrv = []

#using the grid given in top95.txt
for var in problems:
    g = Grid()
    g.read_file(var)
   
    g_copy_fa = g.copy()
    g_copy_mrv = g.copy()

    start_time_fa = time.time()
    pre_process_ac3(g_copy_fa)
    correct_grid_fa, check_fa = search(g_copy_fa, select_variable_fa)
    end_time_fa = time.time()
    runtime_fa.append(end_time_fa-start_time_fa)
    
    start_time_mrv = time.time()
    pre_process_ac3(g_copy_mrv)
    corrected_grid_mrv, check_mrv = search(g_copy_mrv, select_variable_mrv)
    end_time_mrv = time.time()
    runtime_mrv.append(end_time_mrv-start_time_mrv)
plotter = PlotResults()
plotter.plot_results(runtime_mrv, runtime_fa,
"Running Time Backtracking (MRV)",
"Running Time Backtracking (FA)", "running_time")

file = open('tutorial_problem.txt', 'r')
problems = file.readlines()
for var in problems:
    g = Grid()
    g.read_file(var)
