import pandas as pd
import re
import os
import requests
from huggingface_hub import HfApi, get_repo_discussions
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from requests.exceptions import RequestException
import pytz
from huggingface_hub import ModelCard
from difflib import SequenceMatcher
from nltk.tokenize import word_tokenize

hugging_token = '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'
api = HfApi(token=hugging_token)

data = "/Users/adekunleajibode/Desktop/CISC_877_doc/RQ1_Experiment/new_data/minor_manual_work_with_version.csv"

df = pd.read_csv(data)

nlp_data = []

small = df[0:10]

for index, row in df.iterrows():
    owner = row['Owner']
    first_version = row['main_model_name']
    second_version = row["to_compare"]
    model_links = row['link']
    type = row['type']
    url1 = f"https://huggingface.co/api/models/{first_version}"
    url2 = f"https://huggingface.co/api/models/{second_version}"

    total_lfs_first = 0
    total_pointer_size_first = 0
    try:
        large_files_first = api.list_files_info(first_version)

        for item1 in large_files_first:
            try:
                if item1.lfs:
                    total_lfs_first += item1.lfs['size'] / (1.24 * 1.24)
                    total_pointer_size_first += item1.lfs['pointer_size']
            except KeyError:
                total_lfs_first = 0
                total_pointer_size_first = 0
    except Exception as e:
        print(f"Error accessing files for model '{first_version}': {e}")

    total_lfs_second = 0
    total_pointer_size_second = 0
    try:
        large_files_second = api.list_files_info(second_version)

        for item2 in large_files_second:
            try:
                if item2.lfs:
                    total_lfs_second += item2.lfs['size'] / (1.24 * 1.24)
                    total_pointer_size_second += item2.lfs['pointer_size']
            except KeyError:
                total_lfs_second = 0
                total_pointer_size_second = 0
    except Exception as e:
        print(f"Error accessing files for model '{second_version}': {e}")

    try:
        first_info = requests.get(url1)
        #first_info = api.model_info(first_version)
        first_json = first_info.json()
        try:
            first_base_model = first_json["config"]["model_type"]
        except KeyError:
            first_base_model = "none"

        second_info = requests.get(url2)
        second_json = second_info.json()
        try:
            second_base_model = second_json["config"]["model_type"]
        except KeyError:
            second_base_model = "none"

        urls1 = f"https://huggingface.co/api/models/{first_version}"
        urls2 = f"https://huggingface.co/api/models/{second_version}"
        things1 = requests.get(urls1)
        things2 = requests.get(urls2)
        model_json1 = things1.json()
        model_json2 = things2.json()
        safetensors_total1 = model_json1.get("safetensors", {}).get("total", None)
        safetensors_total2 = model_json2.get("safetensors", {}).get("total", None)

        readme_size_first = 0
        readme_first = api.list_files_info(first_version)
        try:
            for item_readme1 in readme_first:
                if item_readme1.path == 'README.md':
                    readme_size_first = item_readme1.size
                    break
        except AttributeError:
            pass

        readme_size_second = 0
        readme_second = api.list_files_info(second_version)
        try:
            for item_readme2 in readme_second:
                if item_readme2.path == 'README.md':
                    readme_size_second = item_readme2.size
                    break
        except AttributeError:
            pass

        def get_model_card(model_name):
            try:
                model_card = ModelCard.load(model_name)
                return model_card
            except FileNotFoundError as e:
                # Handle the specific error when the metadata block is not found
                if "Repo card metadata block was not found" in str(e):
                    return 'metadata_not_found'
                else:
                    return None
            except Exception as e:
                # Catch any other exceptions and return None
                return None

        def has_model_card1(model_name):
            try:
                model_card = ModelCard.load(model_name)
                return 'card_found'
            except requests.exceptions.HTTPError as e:
                # Check for a 404 error and return 'no_card_found'
                if e.response.status_code == 404:
                    return 'no_card_found'
                else:
                    return 'no_card'
            except Exception as e:
                # Catch any other exceptions and return 'no_card'
                return 'no_card'

        def has_model_card2(model_name):
            try:
                model_card = ModelCard.load(model_name)
                return 'card_found'
            except requests.exceptions.HTTPError as e:
                # Check for a 404 error and return 'no_card_found'
                if e.response.status_code == 404:
                    return 'no_card_found'
                else:
                    return 'no_card'
            except Exception as e:
                # Catch any other exceptions and return 'no_card'
                return 'no_card'

        first_card_status = has_model_card1(first_version)
        second_card_status = has_model_card2(second_version)

        model_card_first = get_model_card(first_version)
        model_card_second = get_model_card(second_version)

        first_card_text = str(model_card_first)
        second_card_text = str(model_card_second)

        main_readme = f"https://huggingface.co/{first_version}/blob/main/README.md"
        compare_readme = f"https://huggingface.co/{second_version}/blob/main/README.md"

        main_response = requests.get(main_readme)
        main_html_content = main_response.text
        main_soup = BeautifulSoup(main_html_content, 'html.parser')
        main_target_paragraph = main_soup.find('pre')
        if main_target_paragraph:
            main_target_text = main_target_paragraph.text.strip()
        else:
            main_target_text = 'None'

        compare_response = requests.get(main_readme)
        compare_html_content = compare_response.text
        compare_soup = BeautifulSoup(compare_html_content, 'html.parser')
        compare_target_paragraph = compare_soup.find('pre')
        if compare_target_paragraph:
            compare_target_text = compare_target_paragraph.text.strip()
        else:
            compare_target_text = 'None'

        def word_sequence_matcher(first_card_text, second_card_text):
            # Tokenize the input sequences into words
            words1 = [word for paragraph in first_card_text.split('\n') for word in word_tokenize(paragraph)]
            words2 = [word for paragraph in second_card_text.split('\n') for word in word_tokenize(paragraph)]
            matcher = SequenceMatcher(None, words1, words2)
            similarity_ratio = matcher.ratio()
            edit_operations = matcher.get_opcodes()
            return similarity_ratio, edit_operations, words1, words2

        similarity_ratio, edit_operations, words1, words2 = word_sequence_matcher(first_card_text, second_card_text)
        replaced_words = None
        for tag, i1, i2, j1, j2 in edit_operations:
            if tag == 'replace':
                replaced_words = f"Replaced '{' '.join(words1[i1:i2])}' with '{' '.join(words2[j1:j2])}'"

        def readme_word_sequence_matcher(main_target_text, compare_target_text):
            # Tokenize the input sequences into words
            readme_main = [readme for paragraph in main_target_text.split('\n') for readme in word_tokenize(paragraph)]
            readme_comp = [readme for paragraph in compare_target_text.split('\n') for readme in word_tokenize(paragraph)]
            readme_matcher = SequenceMatcher(None, readme_main, readme_comp)
            readme_similarity_ratio = readme_matcher.ratio()
            readme_edit_operations = readme_matcher.get_opcodes()
            return readme_similarity_ratio, readme_edit_operations, readme_main, readme_comp

        readme_similarity_ratio, readme_edit_operations, main_target_text, compare_target_text = readme_word_sequence_matcher(main_target_text, compare_target_text)
        readme_replaced_words = None
        for tags, a1, a2, b1, b2 in readme_edit_operations:
            if tags == 'replace':
                readme_replaced_words = f"Replaced '{' '.join(main_target_text[a1:a2])}' with '{' '.join(compare_target_text[b1:b2])}'"


        nlp_data.append({
            "Owner": owner,
            "main_model_name": first_version,
            "to_compare": second_version,
            "model_link": model_links,
            "version_type": type,
            "main_base_model": first_base_model,
            "compared_base_model": second_base_model,
            "main_size": safetensors_total1,
            "compare_size": safetensors_total2,
            "main_model_file": total_lfs_first,
            "compared_model_file": total_lfs_second,
            "main_file_pointer": total_pointer_size_first,
            "compared_file_pointer": total_pointer_size_second,
            "main_model_readme": readme_size_first,
            "compared_model_readme": readme_size_second,
            "first_card_status": first_card_status,
            "second_card_status": second_card_status,
            "card_similar_score": similarity_ratio,
            "replaced_words": replaced_words,
            "readme_similar_score": readme_similarity_ratio,
            "readme_replaced_words": readme_replaced_words,
        })

        print(f"Done with {index} model name {first_version}")

    except Exception as e:
        print(f"Error occurred for the first model '{first_version}': {e}")
        print(f"Error occurred for the compared model '{second_version}': {e}")
        nlp_data.append({
            "Owner": owner,
            "main_model_name": first_version,
            "to_compare": second_version,
            "model_link": model_links,
            "version_type": type,
            "main_base_model": first_base_model,
            "compared_base_model": second_base_model,
            "main_size": safetensors_total1,
            "compare_size": safetensors_total2,
            "main_model_file": total_lfs_first,
            "compared_model_file": total_lfs_second,
            "main_file_pointer": total_pointer_size_first,
            "compared_file_pointer": total_pointer_size_second,
            "main_model_readme": readme_size_first,
            "compared_model_readme": readme_size_second,
            "first_card_status": 'None',
            "second_card_status": 'None',
            "card_similar_score": 'None',
            "replaced_words": 'None',
            "readme_similar_score": 'None',
            "readme_replaced_words": 'None',
        })
        continue

output_df = pd.DataFrame(nlp_data)
output_df.to_csv("/Users/adekunleajibode/Desktop/CISC_877_doc/RQ1_Experiment/new_data/minor_versions_comparison.csv", index=False)
print(output_df)
