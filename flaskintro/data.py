from calculations import choose_candidate

class Data:
    def __init__(self):
        self.candidates = []
        self.voters = []
        self.variables = 2
        self.distance_measure = 'euclidean'
        self.results = False
        self.variable_names = ['x', 'y']

    def assign_default_variable_names(self):
        self.variable_names.clear()
        for i in range(self.variables):
            self.variable_names.append('variable ' + str(i + 1))

    def update_results(self):
        if self.candidates:
            global results
            for voter in self.voters:
                choose_candidate(self, voter)
                voter['winner'] = min(voter['distances'], key=lambda x: x[1])
            self.results = True

    def update_variable_names(self, form):
        self.variable_names.clear()
        for i in range(self.variables):
            self.variable_names.append(form['variable_' + str(i)])