import pandas as pd
import math  

def process_csv(file, data):
    df = pd.read_csv(file, encoding='unicode_escape')
    # 1. warn user that this will overwrite existing data DONE
    data.delete_data()
    # 2. get the columns
    columns = df.columns
    # assume first column is name
    variable_names = columns[1:].values.tolist()
    # 3. update variable count to columns - 1 (account for name)
    data.variables = len(variable_names)
    # 4. update variable names to column names
    data.variable_names = variable_names
    # 5. update candidates with the data
    for i in range(len(df)):
        candidate = {}
        candidate['id'] = df.iloc[i, 0]
        for j in range(len(variable_names)):
            candidate[j] = format(float(df.iloc[i, j + 1]), ".2f")
        data.candidates.append(candidate)

    #print("processing csv")
    #print(df)
    # set maximum value for sliders
    data.max = math.ceil(df.max(numeric_only=True).max())
    print(data.max)
    # set minimum value for sliders
    data.min = math.floor(df.min(numeric_only=True).min())
    print(data.min)
    data.default_min = False
    return df


# df works!! now need to
    # 1. warn user that this will overwrite existing data DONE
    # 2. get the columns
    # 3. update variable count to columns - 1 (account for name)
    # 4. update variable names to column names
    # 5. update candidates / voters with the data
    # IDEA: have a SELECT to ask for voter or candidate data