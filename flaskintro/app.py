from flask import Flask, render_template, url_for, request

app = Flask(__name__)

candidates = []
voters = []
variables = 2

@app.route('/', methods=['GET', 'POST'])
def index():
    global variables, candidates, voters  # Declare variables as global so they can be used inside index()
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
    return render_template('index.html', candidates=candidates, voters=voters, variables=variables)

def extract_point(form):
    points = {}
    for i in range(variables):
        # add point to temp dictionary
        # TODO ideally have the ids be names by user
        points[i] = (int(form['variable_' + str(i)]))
    return points
        

if __name__ == "__main__":
    app.run(debug=True)