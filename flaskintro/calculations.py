import numpy as np

# For a single voter, calc distance for each candidate, return the candidate with the smallest distance
def choose_candidate(data, voter):
    distances = []
    for candidate in data.candidates:
        if data.distance_measure == 'euclidean':
            distances.append((candidate['id'], euclidean_distance(voter, candidate, data.variables)))
        elif data.distance_measure == 'manhattan':
            distances.append((candidate['id'], manhattan_distance(voter, candidate, data.variables)))
        # TODO: minkowski, discrete and hamming
        # research mahalanobis, cosine, jaccard, pearson, spearman, kendall
    # sort the distances by shortest to longest
    voter['distances'] = sorted(distances, key=lambda x: x[1])

def euclidean_distance(voter, candidate, variables):
    distance = 0
    for i in range(variables):
        distance += (float(voter[i]) - float(candidate[i])) ** 2
    return distance ** 0.5

def manhattan_distance(voter, candidate, variables):
    distance = 0
    for i in range(variables):
        distance += abs(float(voter[i]) - float(candidate[i]))
    return distance

def find_variances(data):
    # find the variance of each variable
    variances = []
    for i in range(data.variables):
        variances.append((i, np.var([float(candidate[i]) for candidate in data.candidates])))
    # sort the variances by largest to smallest
    variances = sorted(variances, key=lambda x: x[1], reverse=True)
    return variances

