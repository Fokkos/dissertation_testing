import sys
import os

# Add the /helpers directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'helpers'))

from calculations import choose_candidate

class Data:
    def __init__(self):
        self.candidates = []
        self.voters = []
        self.variables = 2
        # distance measures are 'euclidean', 'manhattan' and 'chebyshev'
        self.distance_measure = 'euclidean'
        # election types are 'single-winner', 'multi-winner' and 'participatory-budget'
        self.election_type = 'multi-winner'
        # voting styles are 'average-voter', 'ranked-choice' and 'plurality'
        self.voting_style = 'ranked-choice'
        self.results = False
        self.variable_names = ['x', 'y']
        self.min = 0
        self.max = 10
        self.default_min = True
        self.average_voter = self.create_average_voter()

        # k value for multi-winner elections
        self.k = 10

        # budget for participatory budgeting elections
        self.budget = 100

    def assign_default_variable_names(self):
        self.delete_data()
        self.default_min = True
        for i in range(self.variables):
            self.variable_names.append('variable ' + str(i + 1))

    def update_results(self):
        if self.candidates:
            global results
            choose_candidate(self, self.average_voter)
            for voter in self.voters:
                choose_candidate(self, voter)
            self.results = True

    def update_variable_names(self, form):
        self.variable_names.clear()
        for i in range(self.variables):
            self.variable_names.append(form['variable_' + str(i)])

    def add_data_point(self, type: str, form):
        point = self.extract_point(form)
        if type == 'candidate':
            self.candidates.append(point)
        elif type == 'voter':
            self.voters.append(point)
            self.average_voter = self.update_average_voter()
        self.results = False
    
    def delete_data_point(self, type: str, form):
        point = self.extract_point(form)
        if type == 'candidate':
            if point in self.candidates:
                self.candidates.remove(point)
        elif type == 'voter':
            # if there are results, remove them so that the voter can be found for deletion
            for voter in self.voters:
                if 'distances' in voter:
                    del voter['distances']
            if point in self.voters:
                self.voters.remove(point)
                self.average_voter = self.update_average_voter()
        self.results = False
    
    def extract_point(self, form):
        points = {}
        points['id'] = form['id']
        if 'cost' in form:
            points['cost'] = int(form['cost'])
        for i in range(self.variables):
            points[i] = format(float(form['variable_' + str(i)]), ".2f")
        return points
    
    def delete_data(self):
        self.candidates = []
        self.voters = []
        self.variable_names = []
        self.results = False
        self.max = 10
        self.min = 0
        self.average_voter = self.create_average_voter()

    def create_average_voter(self):
        voter = {}
        voter['id'] = 'average voter'
        for i in range(self.variables):
            voter[i] = format(float(0), ".2f")
        voter['distances'] = [ (None, None) ]
        return voter

    def update_average_voter(self):
        average_voter = self.create_average_voter()
        if len(self.voters) == 0:
            return average_voter
        else:
            for i in range(self.variables):
                total = 0
                for voter in self.voters:
                    total += float(voter[i])
                average_voter[i] = format(total / len(self.voters), ".2f")
            return average_voter

    def findWinner(self):
        if self.election_type == 'single-winner':
            return self.findSingleWinner()
        if self.election_type == 'multi-winner':
            return self.findMultiWinner()
        if self.election_type == 'participatory-budget':
            return self.findBudget()

    def findSingleWinner(self):
        if self.voting_style == 'average-voter':
            return self.average_voter['distances'][0]
        if self.voting_style == 'ranked-choice':
            return self.getBordaScores()[0]
        if self.voting_style == 'plurality':
            return self.getPluralityVotes()[0]

    def findMultiWinner(self):
        winners = []
        if self.voting_style == 'average-voter':
            for i in range(min(self.k, len(self.candidates))):
                winners.append(self.average_voter['distances'][i])
        if self.voting_style == 'ranked-choice':
            for i in range(min(self.k, len(self.candidates))):
                winners.append(self.getBordaScores()[i])
        if self.voting_style == 'plurality':
            for i in range(min(self.k, len(self.candidates))):
                winners.append(self.getPluralityVotes()[i])
            # remove all candidates with 0 votes, votes are at index 1
            winners = [winner for winner in winners if winner[1] > 0]
        return winners

    def findBudget(self):
        # todo implement participatory budgeting
        winners = []
        budget = self.budget

        if self.voting_style == 'average-voter':
            candidates = self.average_voter['distances']
        elif self.voting_style == 'ranked-choice':
            candidates = self.getBordaScores()
        elif self.voting_style == 'plurality':
            candidates = self.getPluralityVotes()
            # remove all candidates with 0 votes, votes are at index 1
            candidates = [candidate for candidate in candidates if candidate[1] > 0]

        for i in range(len(candidates)):
            # get the cost of the candidate ranked i
            candidate_id = candidates[i][0]
            for candidate in self.candidates:
                if candidate['id'] == candidate_id:
                    cost = candidate['cost']
                    break

            # if the cost is less than the budget, add the candidate to the winners
            if cost <= budget:
                id, metric = candidates[i]
                winners.append((id, metric, cost))
                budget -= cost

        # return the remaining budget and the winners
        return budget, winners

    # for ranked-choice elections, finds the Borda score of each candidate
    def getBordaScores(self):
        borda_scores = {}
        for candidate in self.candidates:
            borda_scores[candidate['id']] = 0
        for voter in self.voters:
            for i in range(len(self.candidates)):
                # take away 1 to account for 0 indexing
                borda_scores[voter['distances'][i][0]] += len(self.candidates) - i - 1
        # sort the scores by highest to lowest
        return sorted(list(borda_scores.items()), key=lambda x: x[1], reverse=True)

    # for plurality elections, finds the number of votes each candidate received
    def getPluralityVotes(self):
        votes = {}
        for candidate in self.candidates:
            votes[candidate['id']] = 0
        for voter in self.voters:
            votes[voter['distances'][0][0]] += 1
        # sort the votes by highest to lowest
        return sorted(list(votes.items()), key=lambda x: x[1], reverse=True)


    


    