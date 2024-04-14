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
    return render_template('index.html', error=error, data=data)
    

# routes to add candidates and voters
@app.post('/add_candidate')
def add_candidate():
    form = request.form
    data.add_data_point('candidate', form)
    return redirect(url_for('index'))
    
@app.post('/add_voter')
def add_voter():
    form = request.form
    data.add_data_point('voter', form)
    return redirect(url_for('index'))

# routes to delete candidates and voters
@app.post('/delete_candidate')
def delete_candidate():
    form = request.form
    data.delete_data_point('candidate', form)
    return redirect(url_for('index'))

@app.post('/delete_voter')
def delete_voter():
    form = request.form
    data.delete_data_point('voter', form)
    return redirect(url_for('index'))

# route to set the variable count and assign default variable names
@app.post('/set_variables')
def set_variables():
    form = request.form
    data.variables = int(form['variables'])
    data.assign_default_variable_names()
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
    data.update_results()
    return redirect(url_for('index'))

# route to process a csv file and store the contents in the candidates object
@app.post('/csv')
def csv():
    file = request.files.get('file')
    process_csv(file, data)
    return redirect(url_for('index'))

# routes to view all candidates and voters
@app.get('/voters')
def voters():
    return render_template('viewall.html', variables=data.variables, dataset=data.voters, type='voter')

@app.get('/candidates')
def candidates():
    return render_template('viewall.html', variables=data.variables, dataset=data.candidates, type='candidate')

if __name__ == "__main__":
    app.run(debug=True)
