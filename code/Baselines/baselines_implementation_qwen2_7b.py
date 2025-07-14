

!pip install requests
!pip install openai

"""# Load the model
[Qwen Model](https://huggingface.co/Qwen/Qwen1.5-7B-Chat)
<br><br>
**Note:** <br>
The code of Qwen1.5 has been in the latest Hugging face transformers and we advise you to install transformers>=4.37.0, or you might encounter the following error:

**KeyError: 'qwen2'**
"""

"""
Generate Prompt for Baseline 1

Fostering websites accessibility: A case study on the use of the Large Language Models ChatGPT for automatic remediation

Citation: Othman, A., Dhouib, A., & Nasser Al Jabor, A. (2023, July). Fostering websites accessibility: A case study on the use of the Large Language Models ChatGPT for automatic remediation. In Proceedings of the 16th International Conference on PErvasive Technologies Related to Assistive Environments (pp. 707-713).

Link to paper: https://dl.acm.org/doi/pdf/10.1145/3594806.3596542
"""

import os
import requests
import pandas as pd
import ast
import json
import torch
import time
import csv
import requests

# OpenRouter API Key (Replace with your actual key)
API_KEY = "" # Nadeen
# OpenRouter API URL
URL = "https://openrouter.ai/api/v1/chat/completions"



"""# Baseline 1"""

#Persona for baseline 1
persona_baseline_one = "You are an assistant"
template_baseline_one = """[INST] """+ persona_baseline_one +""" :
{question} [/INST]
"""

def fixed_prompt_baseline_one(code, help_text):
    """
    Generates a fixed prompt based on the given code and help description.
    """
    prompt_template = """
    Given the following source code "$CODE$", can you fix the accessibility issue related to the success criteria: ( $help$ ) according to WCAG 2.1?
    """
    full_prompt = prompt_template.replace("$CODE$", str(code)).replace("$help$", str(help_text))
    return full_prompt

def generate_prompt_baseline_one(df, row_index, error_name, code_elements, help_baseline_one,data_name):
    """
    Generates the prompt for a specific row in the dataset.
    """
    if data_name=="our":
        error = df.at[row_index, error_name]
        code = df.at[row_index, code_elements]
        help_text = help_baseline_one[error]

        return fixed_prompt_baseline_one(code, help_text)
    elif data_name=="baseline":
      error = df.at[row_index, error_name]
      code = df.at[row_index, code_elements]
      list_of_lists = ast.literal_eval(code)
      merged_string = '\n'.join(list_of_lists[0])
      help2 = help_baseline_one[error]
      prompt= fixed_prompt_baseline_one(merged_string,help2)
      #print(prompt)
      return prompt

def generate_response(question):
    """
    Sends a request to the OpenRouter API with the generated prompt.
    """
    retries=3
    initial_wait=10
    messages = [
        {"role": "system", "content": "You are an assistant."},
        {"role": "user", "content": question}
    ]

    payload = {
        "model": "qwen/qwen-2-7b-instruct:free",  # Model name
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 128000  # Reduce from 128000 to 512 avoid excessive token usage
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    for attempt in range(retries):

        try:
            time.sleep(20) # Delay for 1 minute (20 seconds).
            response = requests.post(URL, json=payload, headers=headers)
            response.raise_for_status()
            if response.status_code  == 200:
                if "choices" in response.json():
                    return response.json()["choices"][0]["message"]["content"]
                elif "error" in response.json():
                              wait_time = initial_wait * (2 ** attempt)  # Exponential backoff
                              print(f"Rate limit exceeded. Waiting {wait_time} seconds before retrying... (Attempt {attempt+1}/{retries})")
                              time.sleep(wait_time)
                              continue  # Retry request
          # Handle rate limit errors (429)
            elif response.status_code == 429:
                wait_time = initial_wait * (2 ** attempt)  # Exponential backoff
                print(f"Rate limit exceeded. Waiting {wait_time} seconds before retrying... (Attempt {attempt+1}/{retries})")
                time.sleep(wait_time)
                continue  # Retry request
            # Handle other errors
            else:
                return f"Error: {response.status_code}, {response.text}"
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}. Retrying... (Attempt {attempt+1}/{retries})")
            time.sleep(initial_wait * (2 ** attempt))  # Exponential backoff

# import requests
# generate_response("Name 3 American singers.")

import time
datapath = "/content"
output_path = "/content/"

# dataset = pd.read_csv(datapath+'/Our_dataset_Final_Final.csv')
dataset = pd.read_csv(datapath+'/Baseline2Dataset.csv')
dataset["prompts_baseline_one"] = ""
dataset["responses_baseline_one"] = ""
print("=====(len(dataset)):",(len(dataset)))

#For running specific range:
# dataset = dataset.iloc[168:]  # This selects rows 2, 3, 4.

print("=====(len(dataset)):",(len(dataset)))

# FOR baseline:
# violationnumberID=color-contrast-enhanced affectedHTMLElement= <>
# html->affectedHTMLElement, id ->violationnumberID
dataset.head(2)



f=("/content/results_baseline_one_baseline_dataset_qwen.csv")
# baseline_fields = ['Unnamed: 0.3', 'Unnamed: 0.2', 'Unnamed: 0.1', 'Unnamed: 0', 'webURL',
#        'numViolations', 'id', 'impact', 'tags', 'description', 'help',
#        'helpUrl', 'html', 'failureSummary', 'DOM', 'prompts_baseline_one',
#        'responses_baseline_one']
# with open(f, "a") as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=baseline_fields)
#     writer.writeheader()

d = pd.read_csv(f)
print(len(d))
d.head(2)

with open(datapath+"/violations_short_description.json", 'r') as f:
  help_baseline_one = json.load(f)

"""#  run"""

import csv
import time
import requests

st = time.time()

print("=====Running Experiment======")

our_fields = ['id', 'category', 'webURL', 'numViolations', 'violationnumberID',
       'initialImpactScore', 'description', 'affectedHTMLElement(s)',
       'additional_info', 'failureSummary', 'impact', 'testcase',
       'Additional Context Needed', 'prompts_baseline_one',
       'responses_baseline_one']

baseline_fields = ['Unnamed: 0.3', 'Unnamed: 0.2', 'Unnamed: 0.1', 'Unnamed: 0', 'webURL',
       'numViolations', 'id', 'impact', 'tags', 'description', 'help',
       'helpUrl', 'html', 'failureSummary', 'DOM', 'prompts_baseline_one',
       'responses_baseline_one']

def experiment_baseline_one(df, error_name, code_elements,filename,data_name):
    file_exists = os.path.exists(filename)

    with open(filename, "a") as csvfile:

        if data_name == "our":
            writer = csv.DictWriter(csvfile, fieldnames=our_fields)
            if not file_exists:
                writer.writeheader()
            for i, row in df.iterrows():
                print("==> Processing index", i)
                prompt = generate_prompt_baseline_one(df, i, error_name, code_elements, help_baseline_one,data_name)

                try:
                    response = generate_response(prompt)
                except Exception as e:
                    print(f"Error at index {i}: {e}")
                    response = "Error"

                mydict = {
                    'id': row['id'], 'category': row['category'], 'webURL': row['webURL'],
                    'numViolations': row['numViolations'], 'violationnumberID': row['violationnumberID'],
                    'initialImpactScore': row['initialImpactScore'], 'description': row['description'],
                    'affectedHTMLElement(s)': row['affectedHTMLElement(s)'], 'additional_info': row['additional_info'],
                    'failureSummary': row['failureSummary'], 'impact': row['impact'],
                    'testcase': row['testcase'], 'Additional Context Needed': row['Additional Context Needed'],
                    'prompts_baseline_one': prompt, 'responses_baseline_one': response
                }

                writer.writerows([mydict])
                print(f"Processed {i+1}/{len(df)} - Saved to CSV")

            print(f"Experiment completed! Results saved to {filename}")

        if data_name == "baseline":
            writer = csv.DictWriter(csvfile, fieldnames=baseline_fields)
            if not file_exists:
                writer.writeheader()
            for i, row in df.iterrows():
                print("==> Processing index", i)
                prompt = generate_prompt_baseline_one(df, i, error_name, code_elements, help_baseline_one,data_name)

                try:
                    response = generate_response(prompt)
                except Exception as e:
                    print(f"Error at index {i}: {e}")
                    response = "Error"

                mydict = {
                    'Unnamed: 0.3': row['Unnamed: 0.3'], 'Unnamed: 0.2':row['Unnamed: 0.2'],
                    'Unnamed: 0.1':row['Unnamed: 0.1'], 'Unnamed: 0':row['Unnamed: 0'],
                    'webURL':row['webURL'],'numViolations':row['numViolations'],
                    'id':row['id'], 'impact':row['impact'], 'tags':row['tags'],
                    'description':row['description'], 'help':row['help'],
                    'helpUrl':row['helpUrl'], 'html':row['html'],
                    'failureSummary':row['failureSummary'], 'DOM':row['DOM'],
                    'prompts_baseline_one': prompt, 'responses_baseline_one': response
                }

                writer.writerows([mydict])
                print(f"Processed {i+1}/{len(df)} - Saved to CSV")

            print(f"Experiment completed! Results saved to {filename}")



# For Our Dataset
# filename = os.path.join(output_path, f'results_baseline_one_our_dataset_qwen.csv')
# experiment_baseline_one(dataset, "violationnumberID", "affectedHTMLElement(s)",filename,data_name="our")

# For Baseline Dataset
filename = os.path.join(output_path, f'results_baseline_one_baseline_dataset_qwen.csv')
experiment_baseline_one(dataset, "id", "html",filename,data_name="baseline")
print("===TIME TAKEN:===", time.time()-st)

"""# View result"""

# view_result = pd.read_csv(output_path+'results_baseline_one_our_dataset_qwen.csv')
view_result = pd.read_csv(output_path+'results_baseline_one_baseline_dataset_qwen.csv')
print(len(view_result))
view_result.tail()

len(view_result)

view_result.columns



"""# Baseline 2"""

"""
Generate Prompt for Baseline 2

ACCESS: Prompt Engineering for Automated Web Accessibility Violation Corrections” (Huang et. al., 2024)

Citation: Huang, C., Ma, A., Vyasamudri, S., Puype, E., Kamal, S., Garcia, J. B., ... & Lutz, M. (2024). ACCESS: Prompt Engineering for Automated Web Accessibility Violation Corrections. arXiv preprint arXiv:2401.16450.

Link: https://arxiv.org/pdf/2401.16450
"""


#Persona for baseline 2
persona_baseline_two = """
                You are a helpful assistant who will correct accessibility issues of a provided website.
                Provide your thought before you provide a fixed version of the results.

                E.g.
                Incorrect: [['<span>Search</span>']]
                Thought: because ... I will ...
                Correct: [['<span class="DocSearch-Button-Placeholder">Search</span>']] """

template_baseline_two = """[INST] """+ persona_baseline_two +""" :
{question} [/INST]
"""


def fixed_prompt_baseline_two(webURL,error, description, help, affected_element):
    prompt_template = """You are operating on this website: $WebURL$
        Error: $ERROR$
        Description: $DESCRIPTION$
        Suggested change: $HELP$
        Incorrect: $AFFECTEDELEMENT$
        """

    # Construct the complete prompt by inserting the source code and WCAG guideline
    full_prompt = prompt_template.replace("$WebURL$", str(webURL)).replace("$ERROR$", str(error)).replace("$DESCRIPTION$", str(description)).replace("$HELP$", str(help)).replace("$AFFECTEDELEMENT$", str(affected_element))
    return full_prompt

def generate_prompt_baseline_two(df, row_index, webURL,error, description, affected_element,data_name):

    if data_name=="our":
        webURL = df.at[row_index, webURL]
        error = df.at[row_index, error]
        description = df.at[row_index, description]
        help = help_baseline_[error]
        affected_element = df.at[row_index, affected_element]
        prompt= fixed_prompt_baseline_two(webURL,error, description, help, affected_element)
        return prompt

    elif data_name=="baseline":
        webURL = df.at[row_index, webURL]
        error = df.at[row_index, error]
        description = df.at[row_index, description]
        help = help_baseline_[error]
        affected_element = df.at[row_index, affected_element]
        list_of_lists = ast.literal_eval(affected_element)
        merged_string = '\n'.join(list_of_lists[0])
        prompt= fixed_prompt_baseline_two(webURL,error, description, help, merged_string)
        return prompt


def generate_response(question):
    retries=3
    initial_wait=10
    """
    Sends a request to the OpenRouter API with the generated prompt.
    """
    messages = [
        {"role": "system", "content": """You are a helpful assistant who will correct accessibility issues of a provided website.
                Provide your thought before you provide a fixed version of the results.

                E.g.
                Incorrect: [['<span>Search</span>']]
                Thought: because ... I will ...
                Correct: [['<span class="DocSearch-Button-Placeholder">Search</span>']]"""},
        {"role": "user", "content": question}
    ]

    payload = {
        "model": "qwen/qwen-2-7b-instruct:free",  # Model name
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 128000  # Reduce from 128000 to 512 avoid excessive token usage
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    for attempt in range(retries):
        try:
            time.sleep(20) # Delay for 1 minute (20 seconds).
            response = requests.post(URL, json=payload, headers=headers)
            response.raise_for_status()
            if response.status_code  == 200:
                print(response.json())
                if "choices" in response.json():
                    return(response.json()["choices"][0]["message"]["content"])
                elif "error" in response.json():
                    wait_time = initial_wait * (2 ** attempt)  # Exponential backoff
                    print(f"Rate limit exceeded. Waiting {wait_time} seconds before retrying... (Attempt {attempt+1}/{retries})")
                    time.sleep(wait_time)
                    continue  # Retry request
            # Handle rate limit errors (429)
            elif response.status_code == 429:
                wait_time = initial_wait * (2 ** attempt)  # Exponential backoff
                print(f"Rate limit exceeded. Waiting {wait_time} seconds before retrying... (Attempt {attempt+1}/{retries})")
                time.sleep(wait_time)
                continue  # Retry request
            # Handle other errors
            else:
                return f"Error: {response.status_code}, {response.text}"
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}. Retrying... (Attempt {attempt+1}/{retries})")
            time.sleep(initial_wait * (2 ** attempt))  # Exponential backoff

"""# Run for full dataset: FIRST RUN"""

import csv
import time
import requests

datapath = "/content"
output_path = "/content"

# dataset = pd.read_csv(datapath+'/Our_dataset_Final_Final.csv')
dataset = pd.read_csv(datapath+'/Baseline2Dataset.csv')

dataset['prompts_baseline_two'] = ""
dataset['responses_baseline_two'] = ""

# To run from specific range
# dataset = dataset.iloc[198:]

print("=====(len(dataset)):",(len(dataset)))

with open(datapath+"/violations_short_description.json", 'r') as f:
  help_baseline_ = json.load(f)

st = time.time()
# ============FIRST RUN===============
print("=====Running Experiment======")

our_fields = ['id', 'category', 'webURL', 'numViolations', 'violationnumberID',
       'initialImpactScore', 'description', 'affectedHTMLElement(s)',
       'additional_info', 'failureSummary', 'impact', 'testcase',
       'Additional Context Needed', 'prompts_baseline_two',
       'responses_baseline_two']

baseline_fields = ['Unnamed: 0.3', 'Unnamed: 0.2', 'Unnamed: 0.1', 'Unnamed: 0', 'webURL',
       'numViolations', 'id', 'impact', 'tags', 'description', 'help',
       'helpUrl', 'html', 'failureSummary', 'DOM', 'prompts_baseline_two',
       'responses_baseline_two']

def experiment_baseline_two(df, webURL,error, description, affected_element,filename,data_name="baseline"):
    file_exists = os.path.exists(filename)
    with open(filename, "a") as csvfile:
        if data_name == "our":
            writer = csv.DictWriter(csvfile, fieldnames=our_fields)
            if not file_exists:
                writer.writeheader()

            for i, row in df.iterrows():
                print("==> Processing index", i)
                prompt = generate_prompt_baseline_two(df, i, webURL,error, description, affected_element,data_name)
                try:
                  response = generate_response(prompt)
                except Exception as e:
                    print(f"Error at index {i}: {e}")
                    response = "Error"

                mydict = {
                    'id': row['id'], 'category': row['category'], 'webURL': row['webURL'],
                    'numViolations': row['numViolations'], 'violationnumberID': row['violationnumberID'],
                    'initialImpactScore': row['initialImpactScore'], 'description': row['description'],
                    'affectedHTMLElement(s)': row['affectedHTMLElement(s)'], 'additional_info': row['additional_info'],
                    'failureSummary': row['failureSummary'], 'impact': row['impact'],
                    'testcase': row['testcase'], 'Additional Context Needed': row['Additional Context Needed'],
                    'prompts_baseline_two': prompt, 'responses_baseline_two': response
                }

                writer.writerows([mydict])
                print(f"Processed {i+1}/{len(df)} - Saved to CSV")

            print(f"Experiment completed! Results saved to {filename}")
        elif data_name == "baseline":
            writer = csv.DictWriter(csvfile, fieldnames=baseline_fields)
            if not file_exists:
                writer.writeheader()
            for i, row in df.iterrows():
                print("==> Processing index", i)
                prompt = generate_prompt_baseline_two(df, i, webURL,error, description, affected_element,data_name)

                try:
                    response = generate_response(prompt)
                except Exception as e:
                    print(f"Error at index {i}: {e}")
                    response = "Error"

                mydict = {
                    'Unnamed: 0.3': row['Unnamed: 0.3'], 'Unnamed: 0.2':row['Unnamed: 0.2'],
                    'Unnamed: 0.1':row['Unnamed: 0.1'], 'Unnamed: 0':row['Unnamed: 0'],
                    'webURL':row['webURL'],'numViolations':row['numViolations'],
                    'id':row['id'], 'impact':row['impact'], 'tags':row['tags'],
                    'description':row['description'], 'help':row['help'],
                    'helpUrl':row['helpUrl'], 'html':row['html'],
                    'failureSummary':row['failureSummary'], 'DOM':row['DOM'],
                    'prompts_baseline_two': prompt, 'responses_baseline_two': response
                }

                writer.writerows([mydict])
                print(f"Processed {i+1}/{len(df)} - Saved to CSV")

            print(f"Experiment completed! Results saved to {filename}")

# Our Dataset
# filename = os.path.join(output_path, f'results_baseline_two_our_dataset_qwen.csv')
# experiment_baseline_two(dataset,"webURL", "violationnumberID", "description", "affectedHTMLElement(s)",filename,data_name="our")
# print("===TIME TAKEN:===", time.time()-st)

# BAselineDataset
filename = os.path.join(output_path, f'results_baseline_two_baseline_dataset_qwen.csv')
experiment_baseline_two(dataset,"webURL", "id", "description", "html",filename,data_name="baseline")
print("===TIME TAKEN:===", time.time()-st)



# ===== VIEW=======
# view_result = pd.read_csv(output_path+'results_baseline_two_our_dataset_qwen.csv')
view_result = pd.read_csv("/content/results_baseline_two_baseline_dataset_qwen.csv")
view_result.head(2)

len(view_result)



"""# BASELINE 3"""

"""
Generate Prompt for Baseline 3

On the Interaction with Large Language Models for Web Accessibility: Implications and Challenges

Citation: Delnevo, Giovanni, Manuel Andruccioli, and Silvia Mirri. "On the Interaction with Large Language Models for Web Accessibility: Implications and Challenges." 2024 IEEE 21st Consumer Communications & Networking Conference (CCNC). IEEE, 2024.

Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=10454680&casa_token=0_lq2qITcGYAAAAA:Dt-Ws-yH8GbOGKb5sLBYtXQ_iF3YyuFmHjQhMTouKgocIIGb4t7tP6v0PcEGcO6VhY4PPnqgIow
"""


#Persona for baseline 3
persona_baseline_three = "You are an assistant."
template_baseline_three = """[INST] """+ persona_baseline_three +""" :
{question} [/INST]
"""

def fixed_prompt_baseline_three(affected_element):
    prompt_template = """Is the following HTML code accessible? "$HTML_CODE$" """

    # Construct the complete prompt by inserting the source code and WCAG guideline
    full_prompt = prompt_template.replace("$HTML_CODE$", str(affected_element))
    return full_prompt

def generate_prompt_baseline_three(df, row_index, affected_element,data_name):
    if data_name=="our":
        affected_element = df.at[row_index, affected_element]
        # list_of_lists = ast.literal_eval(affected_element)
        # merged_string = '\n'.join(list_of_lists[0])
        prompt= fixed_prompt_baseline_three(affected_element)
        #print(prompt)
        return prompt

    elif data_name=="baseline":
        affected_element = df.at[row_index, affected_element]
        list_of_lists = ast.literal_eval(affected_element)
        merged_string = '\n'.join(list_of_lists[0])
        prompt= fixed_prompt_baseline_three(merged_string)
        #print(prompt)
        return prompt


def generate_response(question):
    retries=3
    initial_wait=10
    """
    Sends a request to the OpenRouter API with the generated prompt.
    """
    messages = [
        {"role": "system", "content": "You are an assistant."},
        {"role": "user", "content": question}
    ]

    payload = {
        "model": "qwen/qwen-2-7b-instruct:free",  # Model name
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 128000  # Reduce from 128000 to 512 avoid excessive token usage
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    for attempt in range(retries):
        try:
            time.sleep(20) # Delay for 1 minute (20 seconds).
            response = requests.post(URL, json=payload, headers=headers)
            response.raise_for_status()
            if response.status_code  == 200:
                if "choices" in response.json():
                    return(response.json()["choices"][0]["message"]["content"])
                elif "error" in response.json():
                    wait_time = initial_wait * (2 ** attempt)  # Exponential backoff
                    print(f"Rate limit exceeded. Waiting {wait_time} seconds before retrying... (Attempt {attempt+1}/{retries})")
                    time.sleep(wait_time)
                    continue  # Retry request
            # Handle rate limit errors (429)
            elif response.status_code == 429:
                wait_time = initial_wait * (2 ** attempt)  # Exponential backoff
                print(f"Rate limit exceeded. Waiting {wait_time} seconds before retrying... (Attempt {attempt+1}/{retries})")
                time.sleep(wait_time)
                continue  # Retry request
            # Handle other errors
            else:
                return f"Error: {response.status_code}, {response.text}"
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}. Retrying... (Attempt {attempt+1}/{retries})")
            time.sleep(initial_wait * (2 ** attempt))  # Exponential backoff

"""#  RUN On Dataset"""

datapath = "/content"
output_path = "/content"

# dataset = pd.read_csv(datapath+'/Our_dataset_Final_Final.csv')
dataset = pd.read_csv(datapath+'/Baseline2Dataset.csv')

dataset['prompts_baseline_three'] = ""
dataset['responses_baseline_three'] = ""

# dataset = dataset.iloc[274:]  # To RUN FROM SPECIFIC ROWS 75, 274

print("=====(len(dataset)):",(len(dataset)))

with open(datapath+"/violations_short_description.json", 'r') as f:
  help_baseline_ = json.load(f)

# d = pd.read_csv("/content/results_baseline_three_our_dataset_qwen.csv")
# print(len(d))
# d.head(2)



st = time.time()

print("=====Running Experiment======")

our_fields = ['id', 'category', 'webURL', 'numViolations', 'violationnumberID',
       'initialImpactScore', 'description', 'affectedHTMLElement(s)',
       'additional_info', 'failureSummary', 'impact', 'testcase',
       'Additional Context Needed', 'prompts_baseline_three',
       'responses_baseline_three']

baseline_fields = ['Unnamed: 0.3', 'Unnamed: 0.2', 'Unnamed: 0.1', 'Unnamed: 0', 'webURL',
       'numViolations', 'id', 'impact', 'tags', 'description', 'help',
       'helpUrl', 'html', 'failureSummary', 'DOM', 'prompts_baseline_three',
       'responses_baseline_three']

def experiment_baseline_three(df, affected_element,filename,data_name):
    file_exists = os.path.exists(filename)
    with open(filename, "a") as csvfile:
        if data_name == "our":
            writer = csv.DictWriter(csvfile, fieldnames=our_fields)
            if not file_exists:
                writer.writeheader()

            for i, row in df.iterrows():
                print("==> Processing index", i)
                prompt = generate_prompt_baseline_three(df, i, affected_element,data_name)
                try:
                    response = generate_response(prompt)
                except Exception as e:
                    print(f"Error at index {i}: {e}")
                    response = "Error"

                mydict = {
                    'id': row['id'], 'category': row['category'], 'webURL': row['webURL'],
                    'numViolations': row['numViolations'], 'violationnumberID': row['violationnumberID'],
                    'initialImpactScore': row['initialImpactScore'], 'description': row['description'],
                    'affectedHTMLElement(s)': row['affectedHTMLElement(s)'], 'additional_info': row['additional_info'],
                    'failureSummary': row['failureSummary'], 'impact': row['impact'],
                    'testcase': row['testcase'], 'Additional Context Needed': row['Additional Context Needed'],
                    'prompts_baseline_three': prompt, 'responses_baseline_three': response
                }

                writer.writerows([mydict])
                print(f"Processed {i+1}/{len(df)} - Saved to CSV")

            print(f"Experiment completed! Results saved to {filename}")

        elif data_name == "baseline":
            writer = csv.DictWriter(csvfile, fieldnames=baseline_fields)
            if not file_exists:
                writer.writeheader()
            for i, row in df.iterrows():
                print("==> Processing index", i)
                prompt = generate_prompt_baseline_three(df, i, affected_element,data_name)
                try:
                    response = generate_response(prompt)
                except Exception as e:
                    print(f"Error at index {i}: {e}")
                    response = "Error"

                mydict = {
                    'Unnamed: 0.3': row['Unnamed: 0.3'], 'Unnamed: 0.2':row['Unnamed: 0.2'],
                    'Unnamed: 0.1':row['Unnamed: 0.1'], 'Unnamed: 0':row['Unnamed: 0'],
                    'webURL':row['webURL'],'numViolations':row['numViolations'],
                    'id':row['id'], 'impact':row['impact'], 'tags':row['tags'],
                    'description':row['description'], 'help':row['help'],
                    'helpUrl':row['helpUrl'], 'html':row['html'],
                    'failureSummary':row['failureSummary'], 'DOM':row['DOM'],
                    'prompts_baseline_three': prompt, 'responses_baseline_three': response
                }

                writer.writerows([mydict])
                print(f"Processed {i+1}/{len(df)} - Saved to CSV")

            print(f"Experiment completed! Results saved to {filename}")


# For Our Dataset
# filename = os.path.join(output_path, f'results_baseline_three_our_dataset_qwen.csv')
# experiment_baseline_three(dataset, "affectedHTMLElement(s)",filename,data_name="our")


# For Baseline Dataset
filename = os.path.join(output_path, f'results_baseline_three_baseline_dataset_qwen.csv')
experiment_baseline_three(dataset,"html",filename,data_name="baseline")
print("===TIME TAKEN:===", time.time()-st)



# ===== VIEW=======
# view_result = pd.read_csv(output_path+'results_baseline_three_our_dataset_qwen.csv')
view_result = pd.read_csv("/content/results_baseline_three_baseline_dataset_qwen.csv")
view_result.tail()

