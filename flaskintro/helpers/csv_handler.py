import pandas as pd
import math  

def process_csv(file, data):
    df = pd.read_csv(file, encoding='unicode_escape') # read the csv file using pandas
    # 1. delete the previous data stored in the data object as new variable names and datapoints will be created
    data.delete_data()
    # 2. get the columns
    columns = df.columns
    # assume first column is name/id of the candidate
    variable_names = columns[1:].values.tolist()
    # 3. update variable count to columns - 1 (account for name)
    data.variables = len(variable_names)
    # 4. update variable names to column names
    data.variable_names = variable_names
    # 5. update candidates with the data
    for i in range(len(df)):
        candidate = {}
        candidate['id'] = df.iloc[i, 0]
        candidate['cost'] = 10 # cost is assumed to be 10 by default
        for j in range(len(variable_names)):
            candidate[j] = format(float(df.iloc[i, j + 1]), ".2f")
        data.candidates.append(candidate)

    # set maximum value for sliders
    data.max = math.ceil(df.max(numeric_only=True).max())
    # set minimum value for sliders
    data.min = math.floor(df.min(numeric_only=True).min())
    data.default_min = False

    # create new average voter
    data.average_voter = data.create_average_voter()
    data.average_voter = data.update_average_voter()
    
    return df