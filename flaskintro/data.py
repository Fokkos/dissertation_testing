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
        self.delete_data()
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

    def add_data_point(self, type: str, form):
        point = self.extract_point(form)
        if type == 'candidate':
            self.candidates.append(point)
        elif type == 'voter':
            self.voters.append(point)
    
    def delete_data_point(self, type: str, form):
        point = self.extract_point(form)
        if type == 'candidate':
            self.candidates.remove(point)
        elif type == 'voter':
            self.voters.remove(point)
    
    def extract_point(self, form):
        points = {}
        points['id'] = form['id']
        for i in range(self.variables):
            points[i] = (int(form['variable_' + str(i)]))
        return points
    
    def delete_data(self):
        self.candidates = []
        self.voters = []
        self.variable_names = []
        self.results = False

    