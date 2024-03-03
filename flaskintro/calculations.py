# For a single voter, calc distance for each candidate, return the candidate with the smallest distance
def choose_candidate(candidates, voter, distance_measure, variables):
    distances = []
    for candidate in candidates:
        if distance_measure == 'euclidean':
            distances.append((candidate['id'], euclidean_distance(voter, candidate, variables)))
        elif distance_measure == 'manhattan':
            distances.append((candidate['id'], manhattan_distance(voter, candidate, variables)))
        # TODO: minkowski, discrete and hamming
        # research mahalanobis, cosine, jaccard, pearson, spearman, kendall
    voter['distances'] = distances

def euclidean_distance(voter, candidate, variables):
    distance = 0
    for i in range(variables):
        distance += (voter[i] - candidate[i]) ** 2
    return distance ** 0.5

def manhattan_distance(voter, candidate, variables):
    distance = 0
    for i in range(variables):
        distance += abs(voter[i] - candidate[i])
    return distance

