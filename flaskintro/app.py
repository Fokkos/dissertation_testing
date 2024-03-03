from flask import Flask, render_template, url_for, request
from calculations import choose_candidate

app = Flask(__name__)

candidates = []
voters = []
variables = 2
distance_measure = 'euclidean'
results = False

# Election types to implement
# single winner
# multiple winners
# single transferable vote
# participatory budgeting
# approval voting

@app.route('/', methods=['GET', 'POST'])
def index():
    global variables, candidates, voters, distance_measure, results  # Declare variables as global so they can be used inside index()
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
    return render_template('index.html', candidates=candidates, voters=voters, variables=variables, distance_measure=distance_measure, results=results)

def extract_point(form):
    points = {}
    points['id'] = form['id']
    for i in range(variables):
        # add point to temp dictionary
        # TODO ideally have the ids be names by user
        points[i] = (int(form['variable_' + str(i)]))
    return points
        
def update_results():
    global results
    for voter in voters:
        choose_candidate(candidates, voter, distance_measure, variables)
        voter['winner'] = min(voter['distances'], key=lambda x: x[1])
    results = True

if __name__ == "__main__":
    app.run(debug=True)
