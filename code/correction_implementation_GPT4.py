# !pip install openai

import os
import json
import pandas as pd
import requests
import re
import time
from openai import OpenAI
import csv

gpt_API_KEY = "" #paste your api key here
client = OpenAI(api_key=gpt_API_KEY)



def get_guidelines(violationType):
  guide = []
  json_file_path = '/content/mapping_dict_file.json'
  # Open and read the JSON file
  with open(json_file_path, 'r') as file:
     data = json.load(file)
  guidelineNames=data[violationType]
  guidelines= pd.read_csv('/content/WCAGGuidelines.csv')
  for x in guidelineNames:
      guide.append(str(x+":" +guidelines[guidelines['guideId'] == x]['description'].values[0]))
  return guide

#TEST
# get_guidelines("image-alt-not-descriptive")

def get_category(c):
    categories = {
        "Syntax": """These occur when HTML code lacks essential structural elements or attributes required for accessibility,
        such as missing alt attributes or improper use of heading tags and table elements.
        To correct this type of web accessibility violation, expertise in HTML coding is required.""",
        "Layout": """These relate to design and visual organization issues, such as insufficient color contrast or poor font sizing,
        that reduce readability or usability for visually impaired users.
        Fixes must ensure accessibility without negatively affecting users without impairments or distort the page layout for users without impairments.
        To correct this type of web accessibility violation, knowledge of web design principles and front-end coding is required.""",
        "Semantic": """These involve the misuse or absence of meaningful content or attributes,
        such as vague alt text or improper use of semantic elements like <header> or <section>.
    To correct this type of web accessibility violation, expertise in HTML semantics and coding is required.""",
    }
    return categories.get(c, "No description available for this category.")

def send_prompt(prompt, chat_history):
    """Send a structured prompt to the model while maintaining chat history."""
    time.sleep(10)
    # Append user prompt
    chat_history.append({"role": "user", "content": prompt})
    print("*"*20)
    print(chat_history)
    print("*"*20)
    response = client.chat.completions.create(
        model='gpt-4-0125-preview',
        messages=chat_history
    )

    # Process response
    if "choices" in dir(response):
        chat_response = response.choices[0].message.content
        # chat_response = response.json()["choices"][0]["message"]["content"]
        chat_history.append({"role": "assistant", "content": chat_response})
        return chat_response
    elif "error" in dir(response):
        print(f"Rate limit exceeded.")
        return ("Error",response.text)

    else:
        return ("Error",response.text)

# Function to perform metacognitive prompting step-by-step
def analyze_web_accessibility_violation(category, category_description, violationType, violationDescription, impact, URL, HTMLElement, guideline):
    """Executes the metacognitive evaluation workflow for web accessibility violations."""
    # Initialize chat history
    chat_history = [
        {"role": "system", "content": """You are a Web accessibility expert with a strong proficiency in HTML and a deep commitment to fixing Web accessibility violations.
                                        You are familiar with different types of disabilities and user needs.
                                        You are familiar with assistive technologies such as screen readers and understand how they interact with the Web.
                                        You specialize in analyzing Web pages, identifying issues, and providing immediate, corrected HTML code solutions that meet WCAG 2.1 standards.
                                        Your expertise includes resolving problems like missing or improper Alt text, insufficient heading structure, non-semantic elements, inaccessible forms, and color contrast issues.
                                        You are adept at transforming flawed code into compliant, clean HTML that works seamlessly with assistive technologies, ensuring that Websites are fully navigable by keyboard and readable by screen readers.
                                        You provide the corrected code necessary for immediate implementation, ensuring that Websites are not only compliant but truly inclusive for users with disabilities.
                                        Your mission is to ensure that every Website and Web application is accessible to all users by providing expertly corrected HTML, making the Web a more inclusive space.
                                        You reflect on your own answers, assess their accuracy, and provide corrections only when necessary."""}
    ]

    # Step 1: Comprehension & Clarification
    prompt_comprehension_clarification = f"""
    Clarify your understanding of the following web accessibility violation:
    Violation Category: "{category}": {category_description},
    Violation type: "{violationType}",
    Violation description: "{violationDescription}",
    Impact: "{impact}" (Impact is a rating determined by the severity of the violation, indicating the extent to which it hinders user interaction with the Web content. The scale is [cosmetic, minor, moderate, serious, critical]).
    Web page URL: "{URL}"
    Affected HTML Element(s): "{HTMLElement}"
    """
    print("\n### Step 1: Comprehension Clarification ###")
    s1 = send_prompt(prompt_comprehension_clarification, chat_history)

    # Step 2: Preliminary Judgment & Correction
    prompt_preliminary_judgment = f"""
    Based on your understanding, provide a preliminary correction for the web accessibility violation based on the following WCAG guideline(s): "{guideline}".
    Make sure your generated code corrects the web accessibility violation without introducing new violations.
    Ensure you generate the complete corrected code, not just a snippet.
    """
    print("\n### Step 2: Preliminary Correction ###")
    s2 = send_prompt(prompt_preliminary_judgment, chat_history)

    # Step 3: Critical Evaluation of the Correction
    prompt_critical_evaluation = """
    Critically assess your preliminary correction, make sure to correct the initial web accessibility violation without introducing new web accessibility violations.
    Only make corrections if the previous answer is incorrect.
    Make sure your generated code corrects the web accessibility violation without introducing new violations.
    """
    print("\n### Step 3: Critical Evaluation ###")
    s3 = send_prompt(prompt_critical_evaluation, chat_history)

    # Step 4: Decision Confirmation
    prompt_decision_confirmation = """
    Confirm your final decision on whether the correction is accurate or not and provide the reasoning for your decision.
    Only suggest further corrections if the initial response contains errors.
    Make sure your generated code corrects the web accessibility violation without introducing new violations.
    Enclose your corrected HTML code to replace the initial code with violations between these two marker strings: "###albidaya###" as first line and "###alnihaya###" as last line.
    """
    print("\n### Step 4: Decision Confirmation ###")
    s4 = send_prompt(prompt_decision_confirmation, chat_history)

    # Step 5: Confidence Level Evaluation
    prompt_confidence_level = """
    Evaluate your confidence (0-100%) in your correction, enclose your confidence score as "Score: <score>".
    Provide an explanation for this confidence level, enclose your explanation as "Explanation: <explanation>".
    """
    print("\n### Step 5: Confidence Level Evaluation ###")
    s5 = send_prompt(prompt_confidence_level, chat_history)

    pattern = r"Score:\s*(\d+)%?\s*Explanation:\s*(.*)"

    match = re.search(pattern, s5, re.DOTALL)
    if match:
        try:
            Confidence_Score = match.group(1)
        except:
            Confidence_Score = ""
        try:
            Explanation = match.group(2)
        except:
            Explanation = ""
    else:
      Confidence_Score = ""
      Explanation = ""

    return s4,Confidence_Score,Explanation,s5



df = pd.read_csv("/content/baseline_two_dataset.csv")

# For baseline dataset to assign Categories
cat_data = pd.read_csv("/content/violation_taxonomy.csv")
violation_to_category = cat_data.set_index("violationnumberID")["Category"].to_dict()
print(violation_to_category)
df['category'] = df['id'].map(violation_to_category)
df.head(2)

new_column1 = "Decision_Confirmation"
new_column2 = "Confidence_Score"
new_column3 = "Explanation"
new_column4 = "s5_OrgPrompt"

our_fields = ['id', 'category', 'webURL', 'numViolations', 'violationnumberID',
       'initialImpactScore', 'description', 'affectedHTMLElement(s)',
       'additional_info', 'failureSummary', 'impact', 'testcase',
       'Additional Context Needed',new_column1,new_column2,new_column3,new_column4]

baseline_fields = ['Unnamed: 0.3', 'Unnamed: 0.2', 'Unnamed: 0.1', 'Unnamed: 0', 'webURL',
       'numViolations', 'id', 'impact', 'tags', 'description', 'help',
       'helpUrl', 'html', 'failureSummary', 'DOM','category',new_column1,new_column2,new_column3,new_column4]

output_path = "/content"
output_filename = "results_baseline_dataset_mistral.csv"
filename = os.path.join(output_path, output_filename)
file_exists = os.path.exists(filename)

with open(filename, "a") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=baseline_fields)

    if not file_exists:
        writer.writeheader()
    for index, row in df.iterrows():
        print("==> Processing index", index)

        category = row['category']
        category_description = get_category(category)

        #OUR
        # Decision_Confirmation, Confidence_Score, Explanation,s5 = analyze_web_accessibility_violation(category = category,category_description = category_description,violationType = row['violationnumberID'],guideline = get_guidelines(row['violationnumberID']),violationDescription = row['description'],impact = row['impact'],  URL = row['webURL'], HTMLElement = row['affectedHTMLElement(s)'])
        # mydict = {
        #     'id':row['id'], 'category':row['category'], 'webURL':row['webURL'],\
        #     'numViolations':row['numViolations'], 'violationnumberID':row['violationnumberID'],\
        #     'initialImpactScore':row['initialImpactScore'], 'description':row['description'],\
        #     'affectedHTMLElement(s)':row['affectedHTMLElement(s)'],'additional_info':row['additional_info'],\
        #     'failureSummary':row['failureSummary'], 'impact':row['impact'], \
        #     'testcase':row['testcase'], 'Additional Context Needed':row['Additional Context Needed'],
        #     new_column1: Decision_Confirmation, new_column2: Confidence_Score,new_column3:Explanation,new_column4:s5
	      #   }

        # BASELINE
        Decision_Confirmation, Confidence_Score, Explanation,s5 = analyze_web_accessibility_violation(\
                                                                                                                category = category,\
                                                                                                                category_description = category_description,\
                                                                                                                violationType = row['id'],\
                                                                                                                guideline = get_guidelines(row['id']),\
                                                                                                                violationDescription = row['description'],\
                                                                                                                impact = row['impact'],  \
                                                                                                                URL = row['webURL'], \
                                                                                                                HTMLElement = row['html'])
        mydict = { 'Unnamed: 0.3':row['Unnamed: 0.3'], 'Unnamed: 0.2':row['Unnamed: 0.2'], \
                  'Unnamed: 0.1':row['Unnamed: 0.1'], 'Unnamed: 0':row['Unnamed: 0'], 'webURL':row['webURL'],\
                   'numViolations':row['numViolations'], 'id':row['id'], 'impact':row['impact'], \
                   'tags':row['tags'], 'description':row['description'], 'help':row['help'],\
                   'helpUrl':row['helpUrl'], 'html':row['html'], 'failureSummary':row['failureSummary'], \
                   'DOM':row['DOM'],'category':row['category'],new_column1: Decision_Confirmation, \
                   new_column2: Confidence_Score,new_column3:Explanation,new_column4:s5
	        }
        writer.writerows([mydict])
    print(f"Experiment completed! Results saved to {filename}")
