from flask import Flask, render_template, url_for, request, redirect
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

# TODO - add a way to select the election type
# TODO - add edit var names to top row
# TODO - add a settings modal for num of variables and var names. material symbols settings
# TODO - look into WebGL for rendering visualizations
# TODO - let user decide which 3 properties to use as axes in a 3d space
# https://threejs.org/docs/index.html#manual/en/introduction/Drawing-lines

@app.get('/')
def index():
    global data
    # push any errors through to a flash message
    error = None
    return render_template('index.html', error=error, data=data, type='home')
    

# routes to add candidates and voters
@app.post('/add_candidate')
def add_candidate():
    form = request.form
    data.add_data_point('candidate', form)
    data.update_results()
    return redirect(url_for('index'))
    
@app.post('/add_voter')
def add_voter():
    form = request.form
    data.add_data_point('voter', form)
    data.update_results()
    return redirect(url_for('index'))

# routes to delete candidates and voters
@app.post('/delete_candidate')
def delete_candidate():
    form = request.form
    data.delete_data_point('candidate', form)
    data.update_results()
    if form['location'] == 'index':
        return redirect(url_for('index'))
    if form['location'] == 'view_all':
        return redirect(url_for('candidates'))

@app.post('/delete_voter')
def delete_voter():
    form = request.form
    data.delete_data_point('voter', form)
    data.update_results()
    if form['location'] == 'index':
        return redirect(url_for('index'))
    if form['location'] == 'view_all':
        return redirect(url_for('voters'))

# route to set the variable count and assign default variable names
@app.post('/set_variables')
def set_variables():
    form = request.form
    data.variables = int(form['variables'])
    data.assign_default_variable_names()
    data.average_voter = data.create_average_voter()
    return redirect(url_for('index'))

# route to set variable names
@app.post('/set_variable_names')
def set_variable_names():
    form = request.form
    data.update_variable_names(form)
    return redirect(url_for('index'))

# route to set the distance measure used for calculations
@app.post('/set_distance_measure')
def set_distance_measure():
    form = request.form
    data.distance_measure = form['distance_measure']
    # if results already exist, update them with the new measure
    if data.results:
        data.update_results()
    return redirect(url_for('index'))

# route to calculate the distances between voters and candidates
@app.post('/calculate_distances')
def calculate_distances():
    form = request.form
    data.update_results()
    if form['location'] == 'index':
        return redirect(url_for('index'))
    if form['location'] == 'view_all':
        return redirect(url_for('results'))

# route to process a csv file and store the contents in the candidates object
@app.post('/csv')
def csv():
    file = request.files.get('file')
    process_csv(file, data)
    return redirect(url_for('index'))

# routes to view all candidates and voters
@app.get('/voters')
def voters():
    global data
    query = request.args.get('name')
    if query:
        voters = [voter for voter in data.voters if query in voter['id']]
    else:
        voters = data.voters
    return render_template('viewall.html', dataset=voters, data=data, type='voter')

@app.get('/candidates')
def candidates():
    global data
    query = request.args.get('name')
    if query:
        candidates = [candidate for candidate in data.candidates if query in candidate['id']]
    else:
        candidates = data.candidates
    return render_template('viewall.html', dataset=candidates, data=data, type='candidate')

# Results page
@app.get('/results')
def results():
    global data
    return render_template('results.html', data=data, type='results')

# visualisations page
@app.get('/visualisations')
def visualisations():
    global data
    return render_template('visualisations.html', data=data, type='visualisations')

if __name__ == "__main__":
    app.run(debug=True)
