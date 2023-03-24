import numpy as np
from platypus import NSGAII, Problem, Real

def dominates2way(p, q):
    for i in range(len(p)):
        if p[i] > q[i]:
            for j in range(i + 1, len(p)):
                if q[j] > p[j]:
                    return 0
            return -1
        elif q[i] > p[i]:
            for j in range(i + 1, len(p)):
                if p[j] > q[j]:
                    return 0
            return 1
    return 2

def make_dominated_bit(ps, p):
    fr = []
    z = len(ps) - 1 - p
    for i in range(z):
        fr.append(np.minimum(ps[p], ps[p + 1 + i]))
    
    filtered_fr = []
    for i in range(len(fr)):
        j = 0
        keep = True
        while j < len(filtered_fr) and keep:
            dom = dominates2way(fr[i], filtered_fr[j])
            if dom == -1:
                filtered_fr[j] = filtered_fr[-1]
                filtered_fr.pop()
            elif dom == 0:
                j += 1
            else:
                keep = False
        if keep:
            filtered_fr.append(fr[i])

    return filtered_fr

def hv(ps, ref):
    ps = np.array(sorted(ps, key=lambda x: tuple(x), reverse=True))
    n = len(ref)
    
    if n == 2:
        volume = abs((ps[0][0] - ref[0]) * (ps[0][1] - ref[1]))
        for i in range(1, len(ps)):
            volume += abs((ps[i][0] - ref[0]) * (ps[i][1] - ps[i - 1][1]))
        return volume

    volume = 0
    for i in range(len(ps)):
        volume += np.prod(np.abs(ps[i] - ref)) - hv(make_dominated_bit(ps, i), ref)
    return volume

def schaffer(x):
    return [x[0]**2, (x[0] - 2)**2]

problem = Problem(1, 2)
problem.types[:] = Real(-10, 10)
problem.function = schaffer

algorithm = NSGAII(problem)
algorithm.run(10000)

pareto_front = np.array([s.objectives for s in algorithm.result])

reference_point = np.array([10, 10])
hypervolume = hv(pareto_front, reference_point)
print("Hypervolume:", hypervolume)

# Visualization
import matplotlib.pyplot as plt

plt.scatter(pareto_front[:, 0], pareto_front[:, 1], c='r', label='Pareto front')
plt.xlabel('Objective 1')
plt.ylabel('Objective 2')
plt.title('Pareto Front')
plt.legend()
plt.show()
