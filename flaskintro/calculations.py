def choose_candidates(candidates, voters, distance_measure):
    if distance_measure == 'euclidean':
        return euclidean_distance(candidates, voters)
    else:
        return "Distance measure not implemented"

def euclidean_distance(voter, candidate):
    distance = 0
    for i in range(len(voter)):
        distance += (voter[i] - candidate[i]) ** 2
    return distance ** 0.5

