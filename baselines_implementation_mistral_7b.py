import os
import pandas as pd
token = "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"
username = "NadeenAhmad"
repo_name = "CorrectWebAccessibilityViolations"

# Form the clone URL using the personal access token
clone_url = f"https://{token}@github.com/{username}/{repo_name}.git"

# Change the working directory to /content
os.chdir("/content")

# Clone the repository
!git clone {clone_url}

dataset = pd.read_csv('/content/CorrectWebAccessibilityViolations/data/OurDataset.csv')
dataset.head()

import json
with open('/content/CorrectWebAccessibilityViolations/data/HelpForBaselineOne.json', 'r') as f:
  help_baseline_one = json.load(f)

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

import ast
def generate_prompt_baseline_one(df, row_index, error_name, code_elements):
  error = df.at[row_index, error_name]
  code = df.at[row_index, code_elements]
  list_of_lists = ast.literal_eval(code)
  merged_string = '\n'.join(list_of_lists[0])
  help2 = help_baseline_one[error]
  prompt= fixed_prompt_baseline_one(merged_string,help2)
  #print(prompt)
  return prompt

#Persona for baseline 1
persona_baseline_one = "You are an assistant"
template_baseline_one = """[INST] """+ persona_baseline_one +""" :
{question} [/INST]
"""

#p1 = generate_prompt_baseline_one(dataset,0,"violationnumberID", "AffectedHTMLElement(s)")
p1 = generate_prompt_baseline_one(dataset,0,"id", "html")
p1

"""# Generate Prompt for Baseline 2

ACCESS: Prompt Engineering for Automated Web Accessibility Violation Corrections” (Huang et. al., 2024)

- Citation: Huang, C., Ma, A., Vyasamudri, S., Puype, E., Kamal, S., Garcia, J. B., ... & Lutz, M. (2024). ACCESS: Prompt Engineering for Automated Web Accessibility Violation Corrections. arXiv preprint arXiv:2401.16450.

- Link: https://arxiv.org/pdf/2401.16450


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
    full_prompt = prompt_template.replace("$WebURL$", webURL).replace("$ERROR$", error).replace("$DESCRIPTION$", description).replace("$HELP$", help).replace("$AFFECTEDELEMENT$", affected_element)
    return full_prompt

import ast
def generate_prompt_baseline_two(df, row_index, webURL,error, description, affected_element):
  webURL = df.at[row_index, webURL]
  error = df.at[row_index, error]
  description = df.at[row_index, description]
  help = help_baseline_two[error]
  affected_element = df.at[row_index, affected_element]
  #list_of_lists = ast.literal_eval(affected_element)
  #merged_string = '\n'.join(list_of_lists[0])
  prompt= fixed_prompt_baseline_two(webURL,error, description, help, affected_element)
  #print(prompt)
  return prompt

p2 = generate_prompt_baseline_two(dataset,0,"webURL","violationnumberID", "Description", "AffectedHTMLElement(s)")
#p2 = generate_prompt_baseline_two(dataset,15,"webURL","id", "description", "html")
p2

"""# Generate Prompt for Baseline 3

 On the Interaction with Large Language Models for Web Accessibility: Implications and Challenges

- Citation: Delnevo, Giovanni, Manuel Andruccioli, and Silvia Mirri. "On the Interaction with Large Language Models for Web Accessibility: Implications and Challenges." 2024 IEEE 21st Consumer Communications & Networking Conference (CCNC). IEEE, 2024.

- Link: https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=10454680&casa_token=0_lq2qITcGYAAAAA:Dt-Ws-yH8GbOGKb5sLBYtXQ_iF3YyuFmHjQhMTouKgocIIGb4t7tP6v0PcEGcO6VhY4PPnqgIow

"""

#Persona for baseline 3
persona_baseline_three = "You are an assistant"
template_baseline_three = """[INST] """+ persona_baseline_three +""" :
{question} [/INST]
"""

def fixed_prompt_baseline_three(affected_element):
    prompt_template = """Is the following HTML code accessible? "$HTML_CODE$" """

    # Construct the complete prompt by inserting the source code and WCAG guideline
    full_prompt = prompt_template.replace("$HTML_CODE$", affected_element)
    return full_prompt

def generate_prompt_baseline_three(df, row_index, affected_element):
  affected_element = df.at[row_index, affected_element]
  list_of_lists = ast.literal_eval(affected_element)
  merged_string = '\n'.join(list_of_lists[0])
  prompt= fixed_prompt_baseline_three(merged_string)
  #print(prompt)
  return prompt

#p3 = generate_prompt_baseline_three(dataset,0,"AffectedHTMLElement(s)")
p3 = generate_prompt_baseline_three(dataset,0,"html")
p3

"""# Initialize LLM"""

!pip install huggingface_hub
from huggingface_hub import login
login('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')
!pip install langchain
!pip install langchain_community
!pip install -q -U langchain transformers bitsandbytes accelerate

import torch
from transformers import BitsAndBytesConfig
from langchain import HuggingFacePipeline
from langchain import PromptTemplate, LLMChain
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
)
model_4bit = AutoModelForCausalLM.from_pretrained( "mistralai/Mistral-7B-Instruct-v0.1", device_map="auto",quantization_config=quantization_config, )
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")
pipeline_inst = pipeline(
        "text-generation",
        model=model_4bit,
        tokenizer=tokenizer,
        use_cache=True,
        device_map="auto",
        max_length=10500,
        do_sample=True,
        top_k=5,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,
)

llm = HuggingFacePipeline(pipeline=pipeline_inst)

def generate_response(question, template):
  prompt = PromptTemplate(template=template, input_variables=["question","context"])
  llm_chain = LLMChain(prompt=prompt, llm=llm)
  response = llm_chain.run({"question":question})
  filtered_response = response.split("[/INST]", 1)[1].strip()
  return filtered_response

"""# Run Baseline Experiments

## Baseline 1
"""

promptsOne = []
responsesOne = []
def experiment_baseline_one(df, error_name, code_elements):
  for i in range(len(dataset)):
    prompt = generate_prompt_baseline_one(df, i, error_name, code_elements)
    response = generate_response(prompt, template_baseline_one)
    promptsOne.append(prompt)
    responsesOne.append(response)
    print(i)

#experiment_baseline_one(dataset,"violationnumberID", "AffectedHTMLElement(s)")
experiment_baseline_one(dataset,"id", "html")

print(len(promptsOne))
print(len(responsesOne))

#Append Prompts and Responses to dataset
dataset['prompts_baseline_one'] = promptsOne
dataset['responses_baseline_one'] = responsesOne

dataset.head()

#Save Results
dataset.to_csv('results_baseline_one_baseline2_dataset_mistral.csv', index=False)

"""## Baseline 2"""

promptsTwo = []
responsesTwo = []
def experiment_baseline_two(df, webURL,error, description, affected_element):
  for i in range(len(dataset)):
  #for i in range(2):
    prompt = generate_prompt_baseline_two(df, i, webURL,error, description, affected_element)
    response = generate_response(prompt, template_baseline_two)
    promptsTwo.append(prompt)
    responsesTwo.append(response)
    print(i)

experiment_baseline_two(dataset,"webURL", "violationnumberID", "Description", "AffectedHTMLElement(s)")
#experiment_baseline_two(dataset,"webURL", "id", "description", "html")

print(len(promptsTwo))
print(len(responsesTwo))

#Append Prompts and Responses to dataset
dataset['prompts_baseline_two'] = promptsTwo
dataset['responses_baseline_two'] = responsesTwo

dataset.head()

#Save Results
dataset.to_csv('results_baseline_two_our_dataset_mistral.csv', index=False)

"""## Baseline 3"""

promptsThree = []
responsesThree = []
def experiment_baseline_three(df, affected_element):
  for i in range(len(dataset)):
  #for i in range(2):
    prompt = generate_prompt_baseline_three(df, i, affected_element)
    response = generate_response(prompt, template_baseline_three)
    promptsThree.append(prompt)
    responsesThree.append(response)
    print(i)

#experiment_baseline_three(dataset, "AffectedHTMLElement(s)")
experiment_baseline_three(dataset, "html")

len(dataset)

print(len(promptsThree))
print(len(responsesThree))

#Append Prompts and Responses to dataset
dataset['prompts_baseline_three'] = promptsThree
dataset['responses_baseline_three'] = responsesThree

dataset.head()

#Save Results
dataset.to_csv('results_baseline_three_baseline2_dataset_mistral.csv', index=False)

