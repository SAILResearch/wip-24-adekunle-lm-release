import re
import os
import requests
from huggingface_hub import ModelCard
import pandas as pd
from huggingface_hub import HfApi
from unidecode import unidecode
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import base64
import json
# import yaml
import time
from collections import Counter

hugging_token = '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'
api = HfApi(token=hugging_token)

data = "/Users/adekunleajibode/Desktop/CISC_877_doc/RQ1_Experiment/stage3_dataset.xlsx"

df = pd.read_excel(data)

small = df[624:628]

variant = []
for index, row in df.iterrows():

    owner = row["owner"]
    model_name = row["model_name"]
    time_upload = row["time_upload"]
    pipeline_tag = row["pipeline_tag"]
    category = row["category"]
    github_link = row["github_link"]
    millions = row["millions"]
    billions = row["billions"]
    custom_archi = row["custom_archi"]
    base = row["base"]
    download = row["download"]
    like = row['like']

    versioning = []
    name_separate = model_name.split("-")
    if any(substring.lower() in name_element.lower() for name_element in name_separate for substring in
           ["4bits", "4bit", "8bits", "8bit", "awq", "float32", "int8", "Int4", "ptq", "q8", "quantized", "QAT",
            "float16"]):
        versioning.append("quantized")
    elif "distilled" in [name_element.lower() for name_element in name_separate]:
        versioning.append("compressed")
    elif "deduped" in [name_element.lower() for name_element in name_separate]:
        versioning.append("deduplicated")
    else:
        # Fetch the config file from Hugging Face
        config_url = f"https://huggingface.co/{model_name}/raw/main/config.json"
        response = requests.get(config_url)

        if response.status_code == 200:
            try:
                config_data = json.loads(response.text)

                # Ensure that config_data is not None before accessing attributes
                if config_data is not None:
                    _name_or_path_in_config = config_data.get("_name_or_path", "")
                    if isinstance(_name_or_path_in_config, str):
                        _name_or_path_in_config = _name_or_path_in_config.lower()

                        # Compare _name_or_path in the config file with the model_name
                        if _name_or_path_in_config == model_name.lower():
                            versioning.append("standard")
                        else:
                            versioning.append("finetuned")
                    else:
                        print(f"_name_or_path_in_config is not a string for model at index {index} with model_name: {model_name}")
                        versioning.append("finetuned")
                else:
                    print(f"Config data is None for model at index {index} with model_name: {model_name}")
                    versioning.append("finetuned")  # Default to "finetuned" if config_data is None
            except json.decoder.JSONDecodeError as e:
                print(f"Error decoding JSON for model at index {index} with model_name: {model_name}. Error: {e}")
                versioning.append("finetuned")  # Default to "finetuned" if unable to decode JSON
        else:
            print(f"Unable to fetch config file for model at index {index} with model_name: {model_name}")
            versioning.append("finetuned")  # Default to "finetuned" if unable to fetch config file

    variant.append(
        [owner, model_name, time_upload, pipeline_tag, category, github_link, millions, billions, custom_archi, base,
         download, like, ",".join(versioning)])

    print(f"Processed model at index {index} with model_name: {row['model_name']}")

columns = ["owner", "model_name", "time_upload", "pipeline_tag", "category", "github_link", "millions", "billions",
           "custom_archi", "base", "download", "like", "variants"]
new_d = pd.DataFrame(variant, columns=columns)

new_d.to_csv("/Users/adekunleajibode/Desktop/CISC_877_doc/RQ1_Experiment/stage4_dataset.csv", index=None)

print(new_d)
