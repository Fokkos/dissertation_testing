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
    global data
    error = None
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
        elif action == 'set_variable_names':
            data.update_variable_names(form)
        elif action == 'csv':
            file = request.files.get('file')
            if file:
                process_csv(file, data)
            else:
                print("no file")
                error = 'Invalid file'
    return render_template('index.html', error=error, data=data)

if __name__ == "__main__":
    app.run(debug=True)
