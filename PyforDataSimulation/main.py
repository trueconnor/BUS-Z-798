import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler


# Create an empty DataFrame
columns = ["Person", "Time", "Construct1", "Construct2", "Construct3"]
data = pd.DataFrame(columns=columns)


for person_id in range(20):  # Each organization has 10 people, IDs 0-99
    for time_id in range(5):  # Each person has 5 time points, IDs 0-4
        row = {
            "Person": person_id,
            "Time": time_id,
            "Construct1": None,
            "Construct2": None,
            "Construct3": None
        }
        data = pd.concat([data, pd.DataFrame(row, index=[0])], ignore_index=True)


# Prepare data for standardization
scores = data[['Person', 'Time']]
# Standardize to ensure equal variance
scaler = StandardScaler()
scaled_scores = scaler.fit_transform(scores)
# Assign standardized scores to PScore, TScore
data['PScore'] = scaled_scores[:, 0]
data['TScore'] = scaled_scores[:, 1]
# Construct1 is minimal variance within-person and substantial variance between-person
data['Construct1'] = data['TScore'] + 3 * data['PScore']
# Construct2 is substantial variance within-person and minimal variance between-person
data['Construct2'] = 3*data['TScore'] + data['PScore']
# Construct3 is substantial variance within-person and substantial variance between-person
# generate a random number list for construct3
data['Construct3'] = np.random.normal(0, 1, 100)

# Prepare data for normalization
scaler = MinMaxScaler(feature_range=(1, 7))
constructs = data[['Construct1', 'Construct2', 'Construct3']]
scaled_constructs = scaler.fit_transform(constructs)

# Convert the processed data to integers and update back to data DataFrame
data[['Construct1', 'Construct2', 'Construct3']] = np.rint(scaled_constructs).astype(int)

# Save the data DataFrame to a .dta file for Stata to read
data['Person'] = data['Person'].astype(str)
data['Time'] = data['Time'].astype(int)

data.to_stata('data.dta', write_index=False)

