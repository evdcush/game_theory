import numpy as np

def compute_pareto_frontier(agent1_values, agent2_values, counts):

    '''
    return [(agent1_utility, agent2_utility), ...] 所有可能的frontier上的utility对

    agent1_values是(x, y, z)，xyx分别是三个物品对于agent1来说的value
    agent2_values是(a, b, c)，abc分别是三个物品对于agent2来说的value

    counts是(number of books, number of hats, number of balls)
    '''

    possible_utilities = []
    frontier_utilities = []

    agent1_values = np.array(agent1_values)
    agent2_values = np.array(agent2_values)

    counts = np.array(counts)

    for i in range(counts[0]+1):
        for j in range(counts[1]+1):
            for k in range(counts[2]+1):
                value_1 = np.sum(np.array([i,j,k]) * agent1_values)
                value_2 = np.sum((counts - np.array([i,j,k])) * agent2_values)
                possible_utilities.append((value_1,value_2))

    possible_utilities.sort(reverse=True)

    frontier_utilities.append(possible_utilities[0])

    for i in range(1,len(possible_utilities)):
        if possible_utilities[i][0] != possible_utilities[i-1][0]:
            frontier_utilities.append(possible_utilities[i])
    
    return frontier_utilities

print(compute_pareto_frontier([1,2,3],[3,2,1],[3,3,3]))