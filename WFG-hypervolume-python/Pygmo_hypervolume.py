import pygmo as pg

def calculate_hypervolume(pareto_front, reference_point):
    """
    Calculate the hypervolume of the given Pareto front with respect to a reference point.

    :param pareto_front: A list of lists, where each inner list contains the objective values of a solution.
    :param reference_point: A list containing the reference point.
    :return: The hypervolume value.
    """
    hv = pg.hypervolume(pareto_front)
    hypervolume_value = hv.compute(reference_point)
    return hypervolume_value

# Example usage:
pareto_front = [
    [0.5, 1.0, 2.0],
    [0.6, 0.8, 2.5],
    [1.0, 0.7, 1.5]
]

reference_point = [1.1, 1.1, 3.0]

hv = calculate_hypervolume(pareto_front, reference_point)
print("Hypervolume:", hv)