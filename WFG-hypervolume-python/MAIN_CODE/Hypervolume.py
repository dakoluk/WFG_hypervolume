import numpy as np
import platypus
from platypus import Problem, Solution

solution_set = [
    [0.1, 0.2, 0.8, 0.7],
    [0.2, 0.4, 0.7, 0.6],
    [0.3, 0.3, 0.6, 0.5],
    [0.4, 0.1, 0.5, 0.8]
]
"""
class Problem:
    def __init__(self, nobjs, directions):
        self.nobjs = nobjs
        self.directions = directions

class Solution:
    def __init__(self, objectives, problem):
        self.objectives = objectives
        self.problem = problem
        self.normalized_objectives = objectives.copy()
        self.constraint_violation = 0.0
        """
#to store the problem and solution information, 
#we need to import the Problem and Solution classes from platypus.

#let's create a problem instance with 4 objectives and the corresponding 
#solutions using the Problem and Solution classes:
problem = Problem(nobjs=4, directions=[Problem.MINIMIZE]*4)
solutions = [Solution(objectives, problem) for objectives in solution_set]



def normalize(solution_set, minimum, maximum):
    for solution in solution_set:
        for i in range(len(solution.objectives)):
            solution.normalized_objectives[i] = (solution.objectives[i] - minimum[i]) / (maximum[i] - minimum[i])
    return minimum, maximum


class Hypervolume:
    def __init__(self, reference_set=None, minimum=None, maximum=None):
        if reference_set is not None:
            if minimum is not None or maximum is not None:
                raise ValueError("minimum and maximum must not be specified if reference_set is defined")
            self.reference_set = [s for s in reference_set if s.constraint_violation == 0.0]
            self.minimum, self.maximum = normalize(reference_set)
        else:
            if minimum is None or maximum is None:
                raise ValueError("minimum and maximum must be specified when no reference_set is defined")
            self.minimum, self.maximum = minimum, maximum

    def invert(self, solution):
        for i in range(solution.problem.nobjs):
            if solution.problem.directions[i] == Problem.MINIMIZE:
                solution.normalized_objectives[i] = 1.0 - max(0.0, min(1.0, solution.normalized_objectives[i]))

    def calculate(self, solution_set):
        feasible = [s for s in solution_set if s.constraint_violation == 0.0]
        normalize(feasible, self.minimum, self.maximum)
        feasible = [s for s in feasible if all([o <= 1.0 for o in s.normalized_objectives])]

        if len(feasible) == 0:
            return 0.0

        for s in feasible:
            self.invert(s)

        return self.calc_internal(feasible, len(feasible), solution_set[0].problem.nobjs)

    def calc_internal(self, solutions, nsols, nobjs):
        solutions.sort(reverse=True, key=lambda s: s.normalized_objectives[nobjs - 1])
        hypervolume = 0
        ref_vol = [1] * (nobjs - 1)

        while solutions:
            current = solutions.pop()
            for i in range(nobjs - 1):
                ref_vol[i] = min(ref_vol[i], current.normalized_objectives[i])

            if solutions:
                hypervolume += self.calc_hypervolume_contribution(current, solutions[-1], ref_vol, nobjs)
            else:
                hypervolume += self.calc_hypervolume_contribution(current, None, ref_vol, nobjs)

        return hypervolume

    def calc_hypervolume_contribution(self, current, next, ref_vol, nobjs):
        if next is None:
            return np.prod([ref_vol[i] - current.normalized_objectives[i] for i in range(nobjs - 1)])
        else:
            return np.prod([ref_vol[i] - current.normalized_objectives[i] for i in range(nobjs - 1)]) - np.prod(
                [ref_vol[i] - next.normalized_objectives[i] for i in range(nobjs - 1)])


# Define the minimum and maximum bounds for each objective
minimum = [0.0, 0.0, 0.0, 0.0]
maximum = [1.0, 1.0, 1.0, 1.0]

# Create a Hypervolume instance with the specified minimum and maximum bounds
hv = Hypervolume(minimum=minimum, maximum=maximum)

# Calculate the hypervolume using the defined Hypervolume class
hypervolume = hv.calculate(solutions)

print("Hypervolume:", hypervolume)

