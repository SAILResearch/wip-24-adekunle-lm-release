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

data = "/Users/adekunleajibode/Desktop/CISC_877_doc/RQ1_Experiment/stage4_dataset.xlsx"

df = pd.read_excel(data)

versions = []
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
    variants = row["variants"]

    # Split model_name by "/" and get the last part
    last_part = model_name.split("/")[-1]

    # Split the last part by "-" and look for versions starting with "v"
    version_match = re.search(r'v\d+(\.\d+)?', last_part, flags=re.IGNORECASE)

    if version_match:
        versions.append(version_match.group())
    else:
        versions.append("standalone")

df["versions"] = versions

versioning_counts = Counter(df["versions"])
for value, count in versioning_counts.items():
    print(f"{value}: {count}")

print(len(versions))

df.to_excel("/Users/adekunleajibode/Desktop/CISC_877_doc/RQ1_Experiment/stage5_dataset.xlsx", index=None)

print(df)
