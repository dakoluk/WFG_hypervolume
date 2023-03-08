import numpy as np
import scipy.spatial.distance as dist

def calculate_hypervolume(points, reference_point, num_samples=100000):
    # normalize the points and reference point
    points_norm = points - np.min(points, axis=0)
    reference_norm = reference_point - np.min(points, axis=0)
    
    # calculate the hypervolume of the region dominated by the points
    dists = dist.cdist(points_norm, reference_norm.reshape(1, -1), 'euclidean')
    dominated = np.all(points_norm <= points_norm[np.argmin(dists)], axis=1)
    dominated_points = points_norm[dominated]
    
    if len(dominated_points) == 0:
        return 0.0
    
    # generate random samples in the space
    samples = np.random.rand(num_samples, len(reference_point))
    samples = samples * np.max(points_norm, axis=0)
    
    # calculate the hypervolume of the region dominated by the points
    dists = dist.cdist(dominated_points, samples, 'euclidean')
    hypervolume_value = np.sum(np.all(dists <= reference_norm.reshape(1, -1), axis=0)) * np.prod(reference_norm)
    
    # calculate the hypervolume of the entire space
    total_hypervolume = np.prod(np.max(points_norm, axis=0))    
    hypervolume_ratio = hypervolume_value / total_hypervolume
    
    return hypervolume_ratio


#Example
# define a set of points and a reference point
points = np.array([[3, 4], [5, 2], [6, 1], [2, 7]])
reference_point = np.array([7, 8])

# calculate the hypervolume using the function
hypervolume_ratio = calculate_hypervolume(points, reference_point)

# print the hypervolume ratio
print("Hypervolume ratio:", hypervolume_ratio)
