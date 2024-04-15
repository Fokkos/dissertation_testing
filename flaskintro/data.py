from calculations import choose_candidate

class Data:
    def __init__(self):
        self.candidates = []
        self.voters = []
        self.variables = 2
        self.distance_measure = 'euclidean'
        self.election_type = 'single-winner'
        self.voting_style = 'plurality'
        self.results = False
        self.variable_names = ['x', 'y']
        self.min = 0
        self.max = 10
        self.default_min = True
        self.average_voter = self.create_average_voter()

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
            self.candidates.remove(point)
        elif type == 'voter':
            # if there are results, remove them so that the voter can be found for deletion
            for voter in self.voters:
                if 'distances' in voter:
                    del voter['distances']
            self.voters.remove(point)
            self.average_voter = self.update_average_voter()
        self.results = False
    
    def extract_point(self, form):
        points = {}
        points['id'] = form['id']
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
        voter['distances'] = [[None], [None]]
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


    