import os

import json
import pandas as pd
import requests
import re
import time
from openai import OpenAI
import csv

gpt_API_KEY = "API_KEY"
client = OpenAI(api_key=gpt_API_KEY)


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
    
    re_prompt_comprehension_clarification = f"""
    You are analyzing a web accessibility issue using a snippet of Affected HTML Element(s) and related metadata. Follow these strict rules.

    ### Your Inputs:
    - Violation Category: "{category}": {category_description}
    - Violation Type: "{violationType}"
    - Violation Description: "{violationDescription}"
    - Impact: "{impact}" (Severity: cosmetic, minor, moderate, serious, critical)
    - Web Page URL: "{URL}"
    - Affected HTML Element(s): ```html{HTMLElement}```

    ################  ABSOLUTE RULES  ################
    IGNORE these rules → your answer will be rejected.
    1. **HTML-First Analysis**:
    - Base your analysis strictly on the HTML snippet and metadata provided.
    - Do **not** assume or hallucinate additional structure, styles, or UI elements not present in the HTML.

    2. **No Translation / No Hallucination**:
      - Do **NOT** translate, re‑write, or invent content, CSS, forms, headers, sections, scripts, or attributes that are **not** present in HTML.
      - Modify *only* the minimal code required to fix the violation.

    3. **Minimal Patch**:
      - Return **only** the lines you changed **inside a fenced block**.
      - Leave every other part of the HTML untouched.
    
    4. **Evidence Driven**:
     - Every accessibility concern must be directly justified by something observable in the HTML.

    ################  TASKS  ################
    2. **Identify UI Element** – name the element that has (or might have) the violation.
    3. **Explain Violation** – why it’s a problem, citing evidence from the HTML.
    4. **Provide Minimal Fix** – only the changed lines, in a fenced code block.
    """
    print("\n### Step 1: Comprehension Clarification ###")
    s1 = send_prompt(re_prompt_comprehension_clarification, chat_history)

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



def get_guidelines(violationType):
  guide = []
  json_file_path = '/workspace/Metacognitive/data/mapping_dict_file.json'
  # Open and read the JSON file
  with open(json_file_path, 'r') as file:
     data = json.load(file)
  guidelineNames=data[violationType]
  guidelines= pd.read_csv('/workspace/Metacognitive/data/WCAGGuidelines.csv')
  for x in guidelineNames:
      guide.append(str(x+":" +guidelines[guidelines['guideId'] == x]['description'].values[0]))
  return guide


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

def run_main(file_path,dataset_name):
    print("====running ===",file_path)
    df = pd.DataFrame(pd.read_excel(file_path))
    print("==>len:",len(df))

    if dataset_name == "our":
        df.drop(columns=['Unnamed: 22', 'Unnamed: 23', 'Unnamed: 24', 'Unnamed: 25','Unnamed: 26'])
    elif dataset_name == "baseline":
        df.drop(columns=['Unnamed: 23','Unnamed: 24', 'Syntax & Layout Evaluation', 'Unnamed: 26'])
    
    data_path = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    
    filename_without_ext = os.path.splitext(os.path.basename(file_path))[0]
    output_file = data_path+"/rePrompt_"+filename_without_ext+".csv"

    fieldnames = list(df.columns) + [
        "re-prompt_Decision_Confirmation",
        "re-prompt_Confidence_Score",
        "re-prompt_Explanation",
        "re-prompt_s5_orgPrompt"
    ]

    # Open the output CSV and write headers once
    with open(output_file, mode='w', newline='', encoding='utf-8') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        # Process each row
        for _, row in df.iterrows():
            row = row.to_dict()

            try:
                if row['newImpactScore'] != 0:
                    if dataset_name == "our":
                        category = row['category']
                        category_description = get_category(category)
                        violationType = row['violationnumberID']
                        guideline = get_guidelines(violationType)

                        decision, score, explanation, prompt = analyze_web_accessibility_violation(
                            category=category,
                            category_description=category_description,
                            violationType=violationType,
                            violationDescription=row['description'],
                            impact=row['impact'],
                            URL=row['webURL'],
                            HTMLElement=row['affectedHTMLElement(s)'],
                            guideline=guideline
                        )
                    elif dataset_name == "baseline":
                        category = row['category']
                        category_description = get_category(category)
                        violationType = row['id']
                        guideline = get_guidelines(violationType)

                        decision, score, explanation, prompt = analyze_web_accessibility_violation(
                            category=category,
                            category_description=category_description,
                            violationType=violationType,
                            violationDescription=row['description'],
                            impact=row['impact'],
                            URL=row['webURL'],
                            HTMLElement=row['html'],
                            guideline=guideline
                        )


                    row['re-prompt_Decision_Confirmation'] = decision
                    row['re-prompt_Confidence_Score'] = score
                    row['re-prompt_Explanation'] = explanation
                    row['re-prompt_s5_orgPrompt'] = prompt
                else:
                    row['re-prompt_Decision_Confirmation'] = None
                    row['re-prompt_Confidence_Score'] = None
                    row['re-prompt_Explanation'] = None
                    row['re-prompt_s5_orgPrompt'] = None

            except Exception as e:
                print(f"Error on row with URL={row.get('webURL')}: {e}")
                # Optionally continue with partial output or log

            writer.writerow(row)

our = "/workspace/Metacognitive/data/accessguru_dataset/syntax_layout/GPT4/results_accessguru_ablation_our_dataset_gpt_4.xlsx"
baseline ="/workspace/Metacognitive/data/baseline_dataset/GPT4/results_accessguru_ablation_baseline2_dataset_gpt_4.xlsx"

run_main(our,dataset_name = "our")
run_main(baseline,dataset_name = "baseline")
