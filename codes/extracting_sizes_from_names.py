import os
import pandas as pd

data = "/Users/adekunleajibode/Desktop/CISC_877_doc/RQ1_Experiment/nlp_more_than_1m.xlsx"

df = pd.read_excel(data)

def convert_to_millions(number, unit):
    if unit.lower() == 'b':
        return number * 1e3  # Convert billion to million
    elif unit.lower() == 'm':
        return number
    else:
        return 0.00

extracted_data = []

for index, row in df.iterrows():
    try:
        owner = row['owner']
        model_name = row["model_name"]
        model = row['model']
        time_upload = row['time_upload']
        pipeline = row['pipeline_tag']
        category = row['category']
        github = row['github_link']
        init_size = row['model_size']

        model_parts = model.replace('-', '_').split('_')

        extracted_millions = []
        extracted_billions = []

        for part in model_parts:
            if 'b' in part.lower() or 'm' in part.lower():
                num_str = ''.join(char for char in part if char.isdigit() or char == '.')
                try:
                    if num_str:
                        unit = part.lower()[-1]
                        part_number = convert_to_millions(float(num_str), unit)
                        if part_number is not None:
                            if unit == 'm':
                                extracted_millions.append(part_number)
                                extracted_billions.append(0.0)
                            elif unit == 'b':
                                extracted_millions.append(0.0)
                                extracted_billions.append(part_number)
                except ValueError:
                    pass

        extracted_data.append({
            'owner': owner,
            'model': model_name,
            'time_upload': time_upload,
            'pipeline': pipeline,
            'category': category,
            'github': github,
            'init_size': init_size,
            'extracted_millions': extracted_millions,
            'extracted_billions': extracted_billions
        })

    except Exception as e:
        print(f"Error processing model {model_name}: {e}")

# Create a new DataFrame from the extracted data
result_df = pd.DataFrame(extracted_data)

# Replace None with 0.0
result_df['extracted_millions'] = result_df['extracted_millions'].apply(lambda x: 0.0 if x is None else x)
result_df['extracted_billions'] = result_df['extracted_billions'].apply(lambda x: 0.0 if x is None else x)

# Convert values to strings and remove brackets
result_df['extracted_millions'] = result_df['extracted_millions'].astype(str).str.replace(r'\[|\]', '')
result_df['extracted_billions'] = result_df['extracted_billions'].astype(str).str.replace(r'\[|\]', '')

# Save the DataFrame as a CSV file
result_df.to_excel("/Users/adekunleajibode/Desktop/CISC_877_doc/RQ1_Experiment/extracted_data.xlsx", index=None)

print("CSV file created successfully.")
