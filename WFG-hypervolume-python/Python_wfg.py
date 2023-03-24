import numpy as np

def dominates(p, q): #to check if point p dominates point q
    return np.all(p <= q) and np.any(p < q)

def wfg(points, reference_point):
    num_objectives = points.shape[1] #Get the number of objectives (columns) in the points array: 3 in this case
    points = points[np.argsort(points[:, -1])] #Sort the points array by the last column (the last objective)
    hv = 0.0

    for i in range(points.shape[0]):
        if i == 0 or not dominates(points[i], points[i - 1]):
            partial_volume = 1.0
            for j in reversed(range(num_objectives)):
                partial_volume *= (reference_point[j] - points[i, j])
                if i > 0 and j > 0:
                    partial_volume -= (reference_point[j] - points[i - 1, j]) * (points[i, j - 1] - points[i - 1, j - 1])
            hv += partial_volume

    return hv

# Example usage
pareto_front = np.array([
    [0.1, 1.2, 2.1],
    [0.01, 1.8, 2.4],
    [0.9, 1.9, 1.4]
])

reference_point = np.array([1.0, 3.2, 2.0])

hv = wfg(pareto_front, reference_point)
print("Hypervolume:", hv)