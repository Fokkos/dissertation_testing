import sys
import os

# Add the /helpers directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'helpers'))

from flask import Flask, render_template, url_for, request, redirect, jsonify, after_this_request
from csv_handler import process_csv
from data import Data
from calculations import find_variances

app = Flask(__name__)
data = Data()

# Election types to implement
# single winner
# multiple winners
# single transferable vote
# participatory budgeting
# approval voting

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

    # if there are not enough candidates and/or voters redirect to index
    if len(data.candidates) < 2 or len(data.voters) == 0:
        return redirect(url_for('index'))

    # get default candidates (top 10 for average voter)
    default_candidates = []
    if len(data.candidates) > 1:
        for id, score in data.average_voter['distances'][:10]:
            for candidate in data.candidates:
                if candidate['id'] == id:
                    default_candidates.append(candidate)
                    break
    return render_template('visualisations.html', data=data, 
        default_candidates=default_candidates, type='visualisations')

# Three.JS testing
@app.get('/threejs')
def threejs():
    global data
    
    # if there are not enough candidates and/or voters redirect to index
    if len(data.candidates) < 2 or len(data.voters) == 0 or data.variables < 3:
        return redirect(url_for('index'))   

    # Have the chosen variables be the top 3 with the highest variance
    chosen_variables = []
    for i, variance in find_variances(data)[:3]:
        chosen_variables.append(i)

    # get the top 20 candidates for the average voter
    default_candidates = []
    if len(data.candidates) > 1:
        for id, score in data.average_voter['distances'][:10]:
            for candidate in data.candidates:
                if candidate['id'] == id:
                    default_candidates.append(candidate)
                    break
    
    # by default, the lines generated are euclidean 
    line_type = 'euclidean'
    
    # colours source: https://sashamaps.net/docs/resources/20-colors/
    colours = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4', '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9', '#ffffff', '#000000']
    return render_template('threejs.html', data=data, type='threejs', colours=colours, chosen_variables=chosen_variables, candidates=default_candidates, line_type=line_type)

# post for threejs
@app.post('/threejs')
def threejs_post():
    global data
    form = request.form
    chosen_variables = [int(form['xAxis']), int(form['yAxis']), int(form['zAxis'])]

    # get the chosen candidates from the form data
    selected_candidates = []
    for i in range(len(data.candidates)):
        if str(i) in form.keys():
            selected_candidates.append(data.candidates[i])

    line_type = form['distance_measure']

    # colours source: https://sashamaps.net/docs/resources/20-colors/
    colours = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4', '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9', '#ffffff', '#000000']
    return render_template('threejs.html', data=data, type='threejs', colours=colours, chosen_variables=chosen_variables, candidates=selected_candidates, line_type=line_type)

# API routes
@app.route('/getWinner', methods=['GET'])
def getWinner():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    if data.election_type == 'participatory-budget':
        remaining_budget, winners = data.findWinner()
    else:
        winners = data.findWinner()
        remaining_budget = None

    jsonResp = {'winner': winners, 'election_type': data.election_type, 'voting_style': data.voting_style, 'k': data.k, 'distance_measure': data.distance_measure, 'remaining_budget': remaining_budget}
    return jsonify(jsonResp)

@app.route('/changeElectionSettings', methods=['POST'])
def changeElectionSettings():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    # update the data object with the new settings
    data.distance_measure = request.form["distance_measure"]
    data.voting_style = request.form["voting_style"]
    data.election_type = request.form["election_type"]
    data.k = int(request.form["k"])
    data.budget = int(request.form["budget"])

    # update the results so that findWinnner() uses the new settings
    data.update_results()

    return jsonify(data.election_type)

@app.route('/updateCost', methods=['POST'])
def updateCost():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    id = request.form["id"]
    newCost = int(request.form["cost"])
    
    for candidate in data.candidates:
        # find the candidate with the matching id
        if candidate['id'] == id:
            candidate['cost'] = newCost
            break

    return jsonify(newCost)

@app.errorhandler(404)
def page_not_found(e):
    global data
    return render_template('errors/404.html', data=data, path=request.path), 404

if __name__ == "__main__":
    app.run(debug=True)