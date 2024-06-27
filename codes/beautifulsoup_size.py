import os
import pandas as pd
import traceback
from huggingface_hub import HfApi
import requests
from bs4 import BeautifulSoup

hugging_token = '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'
api = HfApi(token=hugging_token)

data = "/Users/adekunleajibode/Desktop/CISC_877_doc/RQ1_Experiment/nlp_more_than_1m.xlsx"

df = pd.read_excel(data)

small = df[0:1]

for index, row in small.iterrows():
    try:
        owner = row['owner']
        model_name = row["model_name"]
        time_upload = row['time_upload']
        pipeline = row['pipeline_tag']
        category = row['category']
        github = row['github_link']
        init_size = row['model_size']

        url = f"https://huggingface.co/{model_name}"
        result = requests.get(url)

        # Check if the request was successful
        if result.status_code == 200:
            soup = BeautifulSoup(result.text, "html.parser")
            print(soup)
            # Find parameter count
            params_element = soup.find("div", {"class": "flex-auto min-width-0 p-2 pr-6"})
            if params_element:
                num_params = params_element.find("p").text.split()[-1]
                print(f"Number of parameters for {model_name}: {num_params}")
            else:
                print(f"Could not find parameter count for {model_name}")
        else:
            print(f"Error fetching {url}. Status code: {result.status_code}")

    except requests.RequestException as e:
        print(f"Error making request for model {model_name}: {e}")
    except Exception as e:
        print(f"Error processing model {model_name}: {e}")
        traceback.print_exc()


# Create a DataFrame from the result list
#result_df = pd.DataFrame(result_list)

# Save the DataFrame to a CSV file
#result_df.to_excel("/Users/adekunleajibode/Desktop/CISC_877_doc/RQ1_Experiment/updated_dataset1.xlsx", index=None)

