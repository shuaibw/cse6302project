

import os
import pandas as pd
token = "TOKEN"
username = "NadeenAhmad"
repo_name = "CorrectWebAccessibilityViolations"

# Form the clone URL using the personal access token
clone_url = f"https://{token}@github.com/{username}/{repo_name}.git"

# Change the working directory to /content
os.chdir("/content")

# Clone the repository
!git clone {clone_url}

dataset = pd.read_csv('/content/CorrectWebAccessibilityViolations/data/Baseline2Dataset.csv')
dataset.head()

import pandas as pd


# Printing unique values in the 'column_name' column
unique_values = dataset['id'].unique()
print(unique_values)

import json
with open('/content/CorrectWebAccessibilityViolations/data/HelpForBaselineOne.json', 'r') as f:
  help_baseline_one = json.load(f)

import json
with open('/content/CorrectWebAccessibilityViolations/data/HelpForBaselineTwo.json', 'r') as f:
  help_baseline_two = json.load(f)

"""# Generate Prompt for Baseline 1

Fostering websites accessibility: A case study on the use of the Large Language Models ChatGPT for automatic remediation

- Citation: Othman, A., Dhouib, A., & Nasser Al Jabor, A. (2023, July). Fostering websites accessibility: A case study on the use of the Large Language Models ChatGPT for automatic remediation. In Proceedings of the 16th International Conference on PErvasive Technologies Related to Assistive Environments (pp. 707-713).

- Link to paper: https://dl.acm.org/doi/pdf/10.1145/3594806.3596542
"""

def fixed_prompt_baseline_one(code,help):
    """
    CODE: corresponds to the AffectedHTMLElement(s)  column in the dataset
    help: corresponds to the Description column in the dataset
    """
    prompt_template = """
    Given the following source code "$CODE$", can you fix the accessibility issue related to the success criteria: ( $help$ ) according to WCAG 2.1?
    """

    # Construct the complete prompt by inserting the source code and WCAG guideline
    full_prompt = prompt_template.replace("$CODE$", code).replace("$help$", help)
    return full_prompt

#generate user message
import ast
def generate_user_message_baseline_one(df, row_index, error_name, code_elements):
  error = df.at[row_index, error_name]
  code = df.at[row_index, code_elements]
  #list_of_lists = ast.literal_eval(code)
  #merged_string = '\n'.join(list_of_lists[0])
  help2 = help_baseline_one[error]
  prompt= fixed_prompt_baseline_one(code,help2)
  #print(prompt)
  return prompt

#Persona for baseline 1
system_message_baseline_one = "You are an assistant"

p1 = generate_user_message_baseline_one(dataset,0,"violationnumberID", "AffectedHTMLElement(s)")
#p1 = generate_user_message_baseline_one(dataset,0,"id", "html")
p1

"""# Generate Prompt for Baseline 2

ACCESS: Prompt Engineering for Automated Web Accessibility Violation Corrections” (Huang et. al., 2024)

- Citation: Huang, C., Ma, A., Vyasamudri, S., Puype, E., Kamal, S., Garcia, J. B., ... & Lutz, M. (2024). ACCESS: Prompt Engineering for Automated Web Accessibility Violation Corrections. arXiv preprint arXiv:2401.16450.

- Link: https://arxiv.org/pdf/2401.16450


"""

def fixed_prompt_baseline_two(webURL,error, description, help, affected_element):
    prompt_template = """You are operating on this website: $WebURL$
        Error: $ERROR$
        Description: $DESCRIPTION$
        Suggested change: $HELP$
        Incorrect: $AFFECTEDELEMENT$
        """

    # Construct the complete prompt by inserting the source code and WCAG guideline
    full_prompt = prompt_template.replace("$WebURL$", webURL).replace("$ERROR$", error).replace("$DESCRIPTION$", description).replace("$HELP$", help).replace("$AFFECTEDELEMENT$", affected_element)
    return full_prompt

import ast
def generate_user_message_baseline_two(df, row_index, webURL,error, description, affected_element):
  webURL = df.at[row_index, webURL]
  error = df.at[row_index, error]
  description = df.at[row_index, description]
  help = help_baseline_two[error]
  affected_element = df.at[row_index, affected_element]
  list_of_lists = ast.literal_eval(affected_element)
  merged_string = '\n'.join(list_of_lists[0])
  prompt= fixed_prompt_baseline_two(webURL,error, description, help, merged_string)
  #print(prompt)
  return prompt

# persona for Baseline 2

system_message_baseline_two = """
                You are a helpful assistant who will correct accessibility issues of a provided website.
                Provide your thought before you provide a fixed version of the results.

                E.g.
                Incorrect: [['<span>Search</span>']]
                Thought: because ... I will ...
                Correct: [['<span class="DocSearch-Button-Placeholder">Search</span>']] """

#p2 = generate_prompt_baseline_two(dataset,0,"webURL","violationnumberID", "Description", "AffectedHTMLElement(s)")
p2 = generate_user_message_baseline_two(dataset,15,"webURL","id", "description", "html")
p2

"""# Generate Prompt for Baseline 3

 On the Interaction with Large Language Models for Web Accessibility: Implications and Challenges

- Citation: Delnevo, Giovanni, Manuel Andruccioli, and Silvia Mirri. "On the Interaction with Large Language Models for Web Accessibility: Implications and Challenges." 2024 IEEE 21st Consumer Communications & Networking Conference (CCNC). IEEE, 2024.

- Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=10454680&casa_token=0_lq2qITcGYAAAAA:Dt-Ws-yH8GbOGKb5sLBYtXQ_iF3YyuFmHjQhMTouKgocIIGb4t7tP6v0PcEGcO6VhY4PPnqgIow

"""

def fixed_prompt_baseline_three(affected_element):
    prompt_template = """Is the following HTML code accessible? "$HTML_CODE$" """

    # Construct the complete prompt by inserting the source code and WCAG guideline
    full_prompt = prompt_template.replace("$HTML_CODE$", affected_element)
    return full_prompt

import ast
def generate_user_message_baseline_three(df, row_index, affected_element):
  affected_element = df.at[row_index, affected_element]
  list_of_lists = ast.literal_eval(affected_element)
  merged_string = '\n'.join(list_of_lists[0])
  prompt= fixed_prompt_baseline_three(merged_string)
  #print(prompt)
  return prompt

# persona for Baseline 3
system_message_baseline_three = "You are an assistant"

#p3 = generate_prompt_baseline_three(dataset,0,"AffectedHTMLElement(s)")
p3 = generate_user_message_baseline_three(dataset,0,"html")
p3

"""# Initialize LLM"""

!pip install openai
from openai import OpenAI

client = OpenAI(api_key='api-key')
def GPT_response(system, user):
        response = client.chat.completions.create(
            model='gpt-4-0125-preview',
            messages=[
                {'role': 'system', 'content': system},
                {'role': 'user', 'content': user}
            ]
        )
        return response.choices[0].message.content

"""# Run Experiments

## Baseline 1
"""

promptsOne = []
responsesOne = []
for i in range(len(dataset)):
  #user_message = generate_user_message_baseline_one(dataset,i,"id", "html")
  user_message = generate_user_message_baseline_one(dataset,i,"violationnumberID", "AffectedHTMLElement(s)")
  response = GPT_response (system_message_baseline_one, user_message)
  promptsOne.append(user_message)
  responsesOne.append(response)
  print(i)

print(len(promptsOne))
print(len(responsesOne))

#Append Prompts and Responses to dataset
dataset['prompts_baseline_one'] = promptsOne
dataset['responses_baseline_one'] = responsesOne

dataset.head()

dataset.to_csv('results_baseline_one_our_dataset_gpt_4_o.csv', index=False)

"""## Baseline 2"""

promptsTwo = []
responsesTwo = []
for i in range(len(dataset)):
  user_message = generate_user_message_baseline_two(dataset,i,"webURL","id", "description", "html")
  #user_message = generate_user_message_baseline_two(dataset,i,"violationnumberID", "AffectedHTMLElement(s)")
  response = GPT_response (system_message_baseline_two, user_message)
  promptsTwo.append(user_message)
  responsesTwo.append(response)
  print(i)

print(len(promptsTwo))
print(len(responsesTwo))

#Append Prompts and Responses to dataset
dataset['prompts_baseline_two'] = promptsTwo
dataset['responses_baseline_two'] = responsesTwo

dataset.to_csv('results_baseline_two_baseline2_dataset_gpt_4.csv', index=False)

"""## Baseline 3"""

promptsThree = []
responsesThree = []
for i in range(len(dataset)):
  user_message = generate_user_message_baseline_three(dataset,i, "html")
  #user_message = generate_user_message_baseline_two(dataset,i, "AffectedHTMLElement(s)")
  response = GPT_response (system_message_baseline_three, user_message)
  promptsThree.append(user_message)
  responsesThree.append(response)
  print(i)

print(len(promptsThree))
print(len(responsesThree))

dataset['prompts_baseline_three'] = promptsThree
dataset['responses_baseline_three'] = responsesThree

dataset.head()

dataset.to_csv('results_baseline_three_baseline2_dataset_gpt_4.csv', index=False)

