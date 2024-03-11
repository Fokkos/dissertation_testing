from flask import Flask, render_template, url_for, request
from csv_handler import process_csv
from data import Data

app = Flask(__name__)

data = Data()

# Election types to implement
# single winner
# multiple winners
# single transferable vote
# participatory budgeting
# approval voting

@app.route('/', methods=['GET', 'POST'])
def index():
    global data  # Declare variables as global so they can be used inside index()
    error = None
    if request.method == 'POST':
        form = request.form
        
        if form['form_type'] == 'add_candidate':
            point = extract_point(form)
            data.candidates.append(point)
        elif form['form_type'] == 'delete_candidate':
            point = extract_point(form)
            data.candidates.remove(point)
        if form['form_type'] == 'add_voter':
            point = extract_point(form)
            data.voters.append(point)
        elif form['form_type'] == 'delete_voter':
            point = extract_point(form)
            data.voters.remove(point)
        elif form['form_type'] == 'set_variables':
            # TODO add confirmation for deleting all candidates and voters
            data.variables = int(form['variables'])
            data.assign_default_variable_names()
            data.candidates = []
            data.voters = []
        elif form['form_type'] == 'set_distance_measure':
            print("setting distance measure")
            data.distance_measure = form['distance_measure']
            if data.results:
                print("updating results")
                data.update_results()
        elif form['form_type'] == 'calculate_distances':
            data.update_results()
        elif form['form_type'] == 'set_variable_names':
            print("setting variable names")
            data.update_variable_names(form)
            print(data.variable_names)
        elif form['form_type'] == 'csv':
            file = request.files.get('file')
            if file:
                process_csv(file, data)
            else:
                print("no file")
                error = 'Invalid file'
    return render_template('index.html', error=error, data=data)

def extract_point(form):
    points = {}
    points['id'] = form['id']
    for i in range(data.variables):
        # FOR VOTERS, need to make it so that it gets the results and winners. should just need to pass through in the html
        points[i] = (int(form['variable_' + str(i)]))
    return points

if __name__ == "__main__":
    app.run(debug=True)
