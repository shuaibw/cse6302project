import os
import pandas as pd
from openai import OpenAI
import time
import base64
import json
from openai import OpenAI
import ast
import csv
import requests

import torch
from transformers import BitsAndBytesConfig
from langchain import HuggingFacePipeline
from langchain import PromptTemplate, LLMChain
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from huggingface_hub import login
login('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')


with open('/data/prompts_support/violations_short_description.json', 'r') as f:
  help_baseline_ = json.load(f)

############################
#       DATASET
############################
def load_dataset():
	dataset = pd.read_csv('/data/accessguru_dataset/accessguru_sampled_syntax_layout_dataset.csv')
	dataset= dataset.rename(columns={"#": "ID"})
	return dataset


############################
#       MISTRAL MODEL
############################
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

llm = HuggingFacePipeline(pipeline=pipeline_inst)gpt_API_KEY = "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"


def generate_response(question, template):
  prompt = PromptTemplate(template=template, input_variables=["question","context"])
  llm_chain = LLMChain(prompt=prompt, llm=llm)
  response = llm_chain.run({"question":question})
  filtered_response = response.split("[/INST]", 1)[1].strip()
  return filtered_response

############################
#       BASELINE-1
############################
#Persona for baseline 1
system_message_baseline_one = "You are an assistant"

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
def generate_user_message_baseline_one(df, row_index, error_name, code_elements,data_name):
    error = df.at[row_index, error_name]
    code = df.at[row_index, code_elements]
    help_text = help_baseline_[error]

    return fixed_prompt_baseline_one(code, help_text)
    

############################
#       BASELINE-2
############################
system_message_baseline_two = """
                You are a helpful assistant who will correct accessibility issues of a provided website.
                Provide your thought before you provide a fixed version of the results.

                E.g.
                Incorrect: [['<span>Search</span>']]
                Thought: because ... I will ...
                Correct: [['<span class="DocSearch-Button-Placeholder">Search</span>']] """

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


def generate_user_message_baseline_two(df, row_index, webURL,error, description, affected_element):
    webURL = df.at[row_index, webURL]
    error = df.at[row_index, error]
    description = df.at[row_index, description]
    help = help_baseline_[error]
    affected_element = df.at[row_index, affected_element]
    prompt= fixed_prompt_baseline_two(webURL,error, description, help, affected_element)
    return prompt

############################
#       BASELINE-3
############################
# persona for Baseline 3
system_message_baseline_three = "You are an assistant"

def fixed_prompt_baseline_three(affected_element):
    prompt_template = """Is the following HTML code accessible? "$HTML_CODE$" """

    # Construct the complete prompt by inserting the source code and WCAG guideline
    full_prompt = prompt_template.replace("$HTML_CODE$", affected_element)
    return full_prompt

def generate_user_message_baseline_three(df, row_index, affected_element):
    affected_element = df.at[row_index, affected_element]
    prompt= fixed_prompt_baseline_three(affected_element)
    return prompt
    
############################
#       EXPERIMENT
############################
run_experiment(chosen_baseline,output_path):
	print("=====Running Experiment======")
    dataset = load_dataset()
    
    new_column1 = 'prompts_' + chosen_baseline
    new_column2 = 'responses_' + chosen_baseline

    our_fields = ['id', 'category', 'webURL', 'numViolations', 'violationnumberID',
       'initialImpactScore', 'description', 'affectedHTMLElement(s)',
       'additional_info', 'failureSummary', 'impact', 'testcase',
       'Additional Context Needed',new_column1, new_column2]

	output_filename = "results_"+prompts+"_syntax_layout_dataset_gpt_4.csv"
	filename = os.path.join(output_path, output_filename)
	file_exists = os.path.exists(filename)

	with open(filename, "a") as csvfile:
	    writer = csv.DictWriter(csvfile, fieldnames=our_fields)
	    if not file_exists:
	        writer.writeheader()
	    for i, row in dataset.iterrows():
	        print("==> Processing index", i)
	        if chosen_baseline == "baseline_one"
	        	prompt = generate_user_message_baseline_one(dataset,i,"Violation Type", "Affected HTML")
                try:
                    response = generate_response(prompt, template_baseline_one)
                except Exception as e:
                    print(f"Error at index {i}: {e}")
                    response = "Error"

	        elif chosen_baseline == "baseline_two":
	        	prompt = generate_user_message_baseline_two(dataset,i,"webURL","Violation Type","Description", "Affected HTML")
                try:
                  response = generate_response(prompt, template_baseline_two)
                except:
                  response = "Error"

	        elif chosen_baseline == "baseline_three":
	        	prompt = generate_user_message_baseline_three(dataset,i, "Affected HTML")
                try:
                  response = generate_response(prompt, template_baseline_three)
                except:
                  response = "Error"

	        else:
	        	return "Error: Choose one of the baseline:baseline_one, baseline_two, baseline_three"
	        

	        new_column1 = 'prompts_' + chosen_baseline
            new_column2 = 'responses_' + chosen_baseline

            mydict = {
                'id': row['id'], 'category': row['category'], 'webURL': row['webURL'],
                'numViolations': row['numViolations'], 'violationnumberID': row['violationnumberID'],
                'initialImpactScore': row['initialImpactScore'], 'description': row['description'],
                'affectedHTMLElement(s)': row['affectedHTMLElement(s)'], 'additional_info': row['additional_info'],
                'failureSummary': row['failureSummary'], 'impact': row['impact'],
                'testcase': row['testcase'], 'Additional Context Needed': row['Additional Context Needed'],
                new_column1: prompt, new_column2: response
            }


	        writer.writerows([mydict])
	        print(f"Processed {i+1}/{len(dataset)} - Saved to CSV")

	    print(f"Experiment completed! Results saved to {filename}")


############################
#       RUN
############################
output_path = "/results" #path to save the final result
run_experiment(chosen_baseline="baseline_one",output_path) #baseline_one, baseline_two, baseline_three

