import numpy as np
import random as rand
#vertices,pos_edges,neg_edges,weights
def betweenness_reduction(tau,beta,c,vertices,pos_edges,neg_edges,weights):
    if (beta < 1) or (tau < 1) or (tau > len(vertices)) or (c <= 1):
        raise ValueError
    rand.seed(42)

    n = len(vertices)
    sample_size = c*tau*np.ceil(np.log(n))
    T = rand.sample(vertices,sample_size)

    for x in T:
        