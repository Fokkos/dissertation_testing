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

# TODO - add a way to select the election type
# TODO - add edit var names to top row
# TODO - add a settings modal for num of variables and var names. material symbols settings
# TODO - look into WebGL for rendering visualizations
# TODO - let user decide which 3 properties to use as axes in a 3d space
# TODO - Select all option for chartjs modal
# TODO - move chartjs modal to index
# https://threejs.org/docs/index.html#manual/en/introduction/Drawing-lines

@app.route('/', methods=['GET', 'POST'])
def index():
    global data
    error = None
    refresh = True
    if request.method == 'POST':
        form = request.form
        action = form['form_type']
        
        if action == 'add_candidate':
            data.add_data_point('candidate', form)
        elif action == 'delete_candidate':
            data.delete_data_point('candidate', form)
        if action == 'add_voter':
            data.add_data_point('voter', form)
        elif action == 'delete_voter':
            data.delete_data_point('voter', form)
        elif action == 'set_variables':
            data.variables = int(form['variables'])
            data.assign_default_variable_names()
        elif action == 'set_distance_measure':
            print("setting distance measure")
            data.distance_measure = form['distance_measure']
            if data.results:
                print("updating results")
                data.update_results()
        elif action == 'calculate_distances':
            data.update_results()
            print(data.results)
        elif action == 'set_variable_names':
            data.update_variable_names(form)
        elif action == 'csv':
            file = request.files.get('file')
            process_csv(file, data)
    if refresh:
        return render_template('index.html', error=error, data=data)
    
@app.get('/voters')
def voters():
    return render_template('viewall.html', variables=data.variables, dataset=data.voters, type='voter')

@app.get('/candidates')
def candidates():
    return render_template('viewall.html', variables=data.variables, dataset=data.candidates, type='candidate')

@app.get('/chart-test')
def chart_test():
    return render_template('chart_test.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
