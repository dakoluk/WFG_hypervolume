import numpy as np
from platypus import NSGAII, DTLZ2

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

n_objectives = 4
problem = DTLZ2(n_objectives)

algorithm = NSGAII(problem)
algorithm.run(10000)

pareto_front = np.array([s.objectives for s in algorithm.result])

reference_point = np.ones(n_objectives) * 1.1
hypervolume = hv(pareto_front, reference_point)
print("Hypervolume:", hypervolume)

'''
# Visualization for 3-objective optimization
if n_objectives == 3:
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(pareto_front[:, 0], pareto_front[:, 1], pareto_front[:, 2], c='r', label='Pareto front')
    ax.set_xlabel('Objective 1')
    ax.set_ylabel('Objective 2')
    ax.set_zlabel('Objective 3')
    ax.set_title('Pareto Front')
    ax.legend()
    plt.show()
'''