from flask import Flask, render_template, url_for, request
from calculations import choose_candidate

app = Flask(__name__)

candidates = []
voters = []
variables = 2
distance_measure = 'euclidean'
results = False
variable_names = ['x', 'y']

# Election types to implement
# single winner
# multiple winners
# single transferable vote
# participatory budgeting
# approval voting

@app.route('/', methods=['GET', 'POST'])
def index():
    global variables, candidates, voters, distance_measure, results, variable_names  # Declare variables as global so they can be used inside index()
    if request.method == 'POST':
        form = request.form
        
        if form['form_type'] == 'add_candidate':
            point = extract_point(form)
            candidates.append(point)
        elif form['form_type'] == 'delete_candidate':
            point = extract_point(form)
            candidates.remove(point)
        if form['form_type'] == 'add_voter':
            point = extract_point(form)
            voters.append(point)
        elif form['form_type'] == 'delete_voter':
            point = extract_point(form)
            voters.remove(point)
        elif form['form_type'] == 'set_variables':
            # TODO add confirmation for deleting all candidates and voters
            variables = int(form['variables'])
            assign_default_variable_names()
            candidates = []
            voters = []
        elif form['form_type'] == 'set_distance_measure':
            print("setting distance measure")
            distance_measure = form['distance_measure']
            if results:
                print("updating results")
                update_results()
        elif form['form_type'] == 'calculate_distances':
            update_results()
        elif form['form_type'] == 'set_variable_names':
            print("setting variable names")
            update_variable_names(form)
            print(variable_names)
    return render_template('index.html', candidates=candidates, voters=voters, variables=variables, distance_measure=distance_measure, results=results, variable_names=variable_names)

def extract_point(form):
    points = {}
    points['id'] = form['id']
    for i in range(variables):
        # FOR VOTERS, need to make it so that it gets the results and winners. should just need to pass through in the html
        points[i] = (int(form['variable_' + str(i)]))
    return points
        
def update_results():
    if candidates:
        global results
        for voter in voters:
            choose_candidate(candidates, voter, distance_measure, variables)
            voter['winner'] = min(voter['distances'], key=lambda x: x[1])
        results = True

def assign_default_variable_names():
    global variables, variable_names
    variable_names.clear()
    for i in range(variables):
        variable_names.append('variable ' + str(i + 1))

def update_variable_names(form):
    global variable_names
    variable_names.clear()
    for i in range(variables):
        variable_names.append(form['variable_' + str(i)])

if __name__ == "__main__":
    app.run(debug=True)
