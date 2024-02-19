from flask import Flask, render_template, url_for, request

app = Flask(__name__)

candidates = []
voters = []
variables = 2

@app.route('/', methods=['GET', 'POST'])
def index():
    print(request.method)
    if request.method == 'POST':
        form = request.form
        if request.form['form_type'] == 'add_candidate':
            point = extract_point()
            candidates.append(point)
        elif request.form['form_type'] == 'delete_candidate':
            point = extract_point()
            candidates.remove(point)
        if request.form['form_type'] == 'add_voter':
            point = extract_point()
            voters.append(point)
        elif request.form['form_type'] == 'delete_voter':
            point = extract_point()
            voters.remove(point)
    return render_template('index.html', candidates=candidates, voters=voters, variables=variables)

def extract_point():
    x = int(request.form['x'])
    y = int(request.form['y'])
    return {'x': x, 'y': y}

if __name__ == "__main__":
    app.run(debug=True)