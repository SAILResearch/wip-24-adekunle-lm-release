import pandas as pd

data = "/Users/adekunleajibode/Desktop/CISC_877_doc/RQ1_Experiment/NLP.csv"

# Specify encoding as 'ISO-8859-1' or 'latin1'
#df = pd.read_excel(data)
df = pd.read_csv(data)

owners = []
model_names = []

# Iterate through the DataFrame rows
for index, row in df.iterrows():
    model_name = row['model_name']

    # Check if "/" is present in the model_name
    if '/' in model_name:
        owner, model = model_name.split('/', 1)
    else:
        # If "/" is not present, consider the whole value as owner and model_name
        owner = model_name
        model = model_name

    # Append the values to the lists
    owners.append(owner)
    model_names.append(model)

# Add new columns to the DataFrame with the extracted values
df['owner'] = owners
df['model'] = model_names

df.to_excel("/Users/adekunleajibode/Desktop/CISC_877_doc/RQ1_Experiment/NLP.xlsx", index = None)