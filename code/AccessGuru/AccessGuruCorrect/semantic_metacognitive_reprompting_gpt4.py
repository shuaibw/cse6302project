import os
import json
import pandas as pd
import requests
import re
import time
import csv
from openai import OpenAI
import base64

gpt_API_KEY = "API_KEY"
client = OpenAI(api_key=gpt_API_KEY)
# MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions" #For correction -->threw error
# API_KEY = "API_KEY"  # Replace with your actual API key
# Openrouter_API_URL = "https://openrouter.ai/api/v1/chat/completions" #used this on Semantic_implementation
# API_KEY = "API_KEY"  # Replace with your actual API key

# model_name = "mistralai/pixtral-12b"
# model_name = "qwen/qwen-vl-plus"
model_name='gpt-4-turbo'


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


def send_prompt(prompt, chat_history, img_path=None):
    """Send a structured prompt and optional image to an LLM while maintaining conversation history."""

    time.sleep(10)  # Avoid flooding the API

    # Step 1: Prepare content
    if img_path:
        with open(img_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            image_url = f"data:image/png;base64,{encoded_image}"
        user_content = [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": image_url}}
        ]
    else:
        user_content = [{"type": "text", "text": prompt}]

    # Step 2: Append prompt to history
    chat_history.append({"role": "user", "content": user_content})

    # Step 3: Call the Openrouter API
    # print("====>chat_history:", chat_history)
    # response = requests.post(
    #     Openrouter_API_URL,
    #     headers={
    #         "Authorization": f"Bearer {API_KEY}",
    #         "Content-Type": "application/json"
    #     },
    #     json={
    #         "model": model_name,  # Swap here for other models like OpenAI GPT-4-V
    #         "messages": chat_history
    #     }
    # )

    # Step 4: Process Openrouter response
    # if response.status_code == 200:
    #     chat_response = response.json()["choices"][0]["message"]["content"]
    #     chat_history.append({"role": "assistant", "content": chat_response})
    #     return chat_response
    # else:
    #     return f"Error: {response.status_code}, {response.text}"

    # Call the GPT API
    response = client.chat.completions.create(
            model='gpt-4-turbo',
            messages=chat_history)

    # Process response GPT RESPONSE
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
def analyze_web_accessibility_violation(category, category_description, violationType, violationDescription, impact, URL, HTMLElement, guideline,img_path):
    """Executes the metacognitive evaluation workflow for web accessibility violations."""
    print("====HERE=====")
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
    You are analyzing a web accessibility issue. Prioritize the **attached image** of a web page (which visually shows the UI element with a possible accessibility violation) and use the **corresponding HTML** only to validate your findings.

    ### Your tasks:
    1. **Interpret the visual content** of the attached image.
    2. **Identify the UI element** (e.g. a button or icon) shown in the image.
    3. **Determine whether the element is accessible** (e.g., does it have a clear label, alt text, and function?).
    4. **Compare your findings** with the **corresponding HTML** provided and highlight any mismatches.
    5. **Suggest an accessibility-compliant fix** if there's a violation.

    ### Metadata:
    Violation Category: "{category}": {category_description},
    Violation type: "{violationType}",
    Violation description: "{violationDescription}",
    Impact: "{impact}" (Impact is a rating determined by the severity of the violation, indicating the extent to which it hinders user interaction with the Web content. The scale is [cosmetic, minor, moderate, serious, critical]).
    Web page URL: "{URL}"
    Affected HTML Element(s): "{HTMLElement}"
    """

    # Apply corrective re-prompting for violations that are not fixed.
    re_prompt_comprehension_clarification = f"""
    You are analyzing a web accessibility issue, using an attached webpage screenshot and a snippet of Affected HTML Element(s). Follow these strict rules.
    The screenshot is the **single source‑of‑truth** for what users actually see.  The HTML is *only* for verification.

    ### Your Inputs:
    - IMAGE: an image (PNG/JPG) that visually shows the UI element with the suspected violation.
    - Violation Category: "{category}": {category_description}
    - Violation Type: "{violationType}"
    - Violation Description: "{violationDescription}"
    - Impact: "{impact}" (Severity: cosmetic, minor, moderate, serious, critical)
    - Web Page URL: "{URL}"
    - Affected HTML Element(s): ```html{HTMLElement}```

    ################  ABSOLUTE RULES  ################
    IGNORE these rules → your answer will be rejected.
    1. **Image‑First**:
      - You *must* list at least **three concrete visual details** you see (e.g. colours, shapes, text, position).
      - If the screenshot is missing or unreadable, reply exactly: `NO_IMAGE_PROVIDED` and stop.

    2. **No Translation / No Hallucination**:
      - Do **NOT** translate, re‑write, or invent content, CSS, forms, headers, sections, scripts, or attributes that are **not** present in BOTH the screenshot *and* HTML.
      - Modify *only* the minimal code required to fix the violation.

    3. **Minimal Patch**:
      - Return **only** the lines you changed **inside a fenced block**.
      - Leave every other part of the HTML untouched.

    4. **Evidence Driven**:
      - Every claim about accessibility *must* point to a visual cue you listed in step 1.

    ################  TASKS  ################
    1. **List Visual Observations** – bullet‑list ≥3 details from the screenshot.
    2. **Identify UI Element** – name the element that has (or might have) the violation.
    3. **Explain Violation** – why it’s a problem, citing both image + HTML.
    4. **Provide Minimal Fix** – only the changed lines.
    """

    print("\n### Step 1: Comprehension Clarification ###",chat_history)
    s1 = send_prompt(re_prompt_comprehension_clarification, chat_history,img_path)
    print(s1)

    # Step 2: Preliminary Judgment & Correction
    prompt_preliminary_judgment = f"""
    Based on your understanding, provide a preliminary correction for the web accessibility violation based on the following WCAG guideline(s): "{guideline}".
    Make sure your generated code corrects the web accessibility violation without introducing new violations.
    Ensure you generate the complete corrected code, not just a snippet.
    """
    print("\n### Step 2: Preliminary Correction ###",chat_history)
    s2 = send_prompt(prompt_preliminary_judgment, chat_history)
    # print(s2)

    # Step 3: Critical Evaluation of the Correction
    prompt_critical_evaluation = """
    Critically assess your preliminary correction, make sure to correct the initial web accessibility violation without introducing new web accessibility violations.
    Only make corrections if the previous answer is incorrect.
    Make sure your generated code corrects the web accessibility violation without introducing new violations.
    """
    print("\n### Step 3: Critical Evaluation ###",chat_history)
    s3 = send_prompt(prompt_critical_evaluation, chat_history)
    # print(s3)

    # Step 4: Decision Confirmation
    prompt_decision_confirmation = """
    Confirm your final decision on whether the correction is accurate or not and provide the reasoning for your decision.
    Only suggest further corrections if the initial response contains errors.
    Make sure your generated code corrects the web accessibility violation without introducing new violations.
    Enclose your corrected HTML code to replace the initial code with violations between these two marker strings: "###albidaya###" as first line and "###alnihaya###" as last line.
    """
    print("\n### Step 4: Decision Confirmation ###",chat_history)
    s4 = send_prompt(prompt_decision_confirmation, chat_history)

    # Step 5: Confidence Level Evaluation
    # prompt_confidence_level = """
    # Evaluate your confidence (0-100%) in your correction, enclose your confidence score between these two marker strings: "###albidaya###" as first line and "###alnihaya###" as last line.
    # Provide an explanation for this confidence level, enclose your explanation between these two marker strings: "###albidaya2###" as first line and "###alnihaya2###" as last line.
    # """
    # s6 = send_prompt(prompt_confidence_level, chat_history)

    prompt_confidence_level = """
    Evaluate your confidence (0-100%) in your correction, enclose your confidence score as "Score: <score>".
    Provide an explanation for this confidence level, enclose your explanation as "Explanation: <explanation>".
    """
    print("\n### Step 5: Confidence Level Evaluation ###",chat_history)
    s5 = send_prompt(prompt_confidence_level, chat_history)

    # Pattern to extract between markers
    # match1 = re.search(r'###albidaya###(.*?)###alnihaya###', s5, re.DOTALL)
    # match2 = re.search(r'###albidaya2###(.*?)###alnihaya2###', s5, re.DOTALL)
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

    # # Extracted values
    # Confidence_Score = match1.group(1).strip() if match1 else None
    # Explanation = match2.group(1).strip() if match2 else None

    # print("*"*20)
    # print(s5)
    # print("*"*20)
    # return s1,s2,s3,s4,Confidence_Score,Explanation

    return s4,Confidence_Score,Explanation,s5


def test1_sample():
	violationType = "lang-mismatch"
	HTMLElement = """
	<! –– Accessibility Violation starts here ––>    <html lang="nl">  <head>  <title>Fireworks over Paris</title>  </head>  <body>  <img alt="Fireworks over Paris"   src="/WAI/content-assets/wcag-act-rules/test-assets/shared/fireworks.jpg"/>  <p lang="nl">  Gelukkig nieuwjaar!  </p>  </body>  </html>  
	"""
	url = "https://www.w3.org/WAI/content-assets/wcag-act-rules/testcases/ucwvc8/c4eaf50df4fa37f931374c74ac369a018b780ec6.html"
	violationDescription="Page language attribute does not match the actual language of the content."
	img_path="/content/accessguru_semantic_violations_sampled_dataset_supp_material/7.png" #-1 from CSV

	s4,Confidence_Score,Explanation,s5 = analyze_web_accessibility_violation(
	    category = "Semantic",
	    category_description = get_category("Semantic"),
	    violationType=violationType,
	    violationDescription=violationDescription,
	    impact="Critical",
	    URL=url,
	    HTMLElement=HTMLElement,
	    guideline = get_guidelines(violationType),
	    img_path=img_path
	)

	print("====Decision_Confirmation====")
	print(s4)
	print()
	print("====Confidence_Score====")
	print(Confidence_Score)
	print()
	print("====Explanation====")
	print(Explanation)
	print()
	print("====s5_OrgPrompt====")
	print(s5)
	print()




df = pd.read_csv("/content/accessguru_sampled_semantic_violations.csv")
# category_df = pd.read_csv("/content/violation_taxonomy.csv")
# df = df.merge(category_df, left_on='Violation Type', right_on='violationnumberID', how='left')
# df.drop(columns=['violationnumberID'], inplace=True)
df['category'] = 'Semantic'

new_column1 = "Decision_Confirmation"
new_column2 = "Confidence_Score"
new_column3 = "Explanation"
new_column4 = "s5_OrgPrompt"
our_fields = ['#', 'Violation Type', 'webURL', 'Impact', 'Description',
       'Affected HTML','category',new_column1,new_column2,new_column3,new_column4]

output_path = ""
output_filename = "metacognitivePrompting_results_accessguru_sampled_semantic_dataset_pixtral12b.csv"

filename = os.path.join(output_path, output_filename)
file_exists = os.path.exists(filename)

with open(filename, "a") as csvfile:
    # 3. CHANGE FIELDNAMES VALUE
    writer = csv.DictWriter(csvfile, fieldnames=our_fields)

    if not file_exists:
        writer.writeheader()
    for index, row in df.iterrows():
    # for index, row in df.iloc[20:21].iterrows():
        print("==> Processing index", index)

        # PATH TO THE SCREENSHOTS
        image_path = "/content/accessguru_semantic_violations_sampled_dataset_supp_material/" + str(row['#'])+".png"

        category = row['category']
        category_description = get_category(category)


        try:
            Decision_Confirmation, Confidence_Score, Explanation,s5 = analyze_web_accessibility_violation(category = category,category_description = category_description,violationType = row['Violation Type'], guideline = get_guidelines(row['Violation Type']),violationDescription = row['Description'],impact = row['Impact'],  URL = row['webURL'], HTMLElement = row['Affected HTML'],img_path=image_path)

        except:
            Decision_Confirmation = "Server Error"
            Confidence_Score = "Server Error"
            Explanation = "Server Error"
            s5 = "Server Error"

        mydict = {
                      '#':row['#'],
                      'Violation Type':row['Violation Type'],
                      'webURL':row['webURL'],
                      'Impact':row['Impact'],
                      'Description':row['Description'],
                      'Affected HTML':row['Affected HTML'],
                      'category':row['category'],
                      new_column1: Decision_Confirmation,
                      new_column2: Confidence_Score,
                      new_column3:Explanation,
                      new_column4:s5
            }

        writer.writerows([mydict])
    print(f"Experiment completed! Results saved to {filename}")

