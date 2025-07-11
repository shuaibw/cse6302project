# !apt install chromium-chromedriver
# !pip install nest_asyncio
# !pip install playwright
# !playwright install

import asyncio
import nest_asyncio
from playwright.async_api import async_playwright
import pandas as pd
# Apply nest_asyncio to allow running in environments with an existing event loop
nest_asyncio.apply()

impactScore = {
    "critical": 5,
    "serious": 4,
    "moderate": 3,
    "minor": 2,
    "cosmetic": 1,
}


async def check_accessibility(url):
    try:
        async with async_playwright() as p:
            # Start Chromium browser
            browser = await p.chromium.launch()
            page = await browser.new_page()

            # Navigate to the URL
            await page.goto(url)

            # Inject axe-core from CDN
            await page.add_script_tag(url="https://cdn.jsdelivr.net/npm/axe-core@4.4.1/axe.min.js")

            # Run axe accessibility checks
            results = await page.evaluate("""
            () => axe.run(document, {
                runOnly: {
                    type: 'tag',
                    values: ['ACT' ,'EN-301-549' ,'EN-9.1.1.1' ,'EN-9.1.2.2' ,'EN-9.1.3.1' ,'EN-9.1.3.5',
 'EN-9.1.4.1' ,'EN-9.1.4.12' ,'EN-9.1.4.2', 'EN-9.1.4.3', 'EN-9.1.4.4',
 'EN-9.2.1.1' ,'EN-9.2.1.3' ,'EN-9.2.2.1' ,'EN-9.2.2.2', 'EN-9.2.4.1',
 'EN-9.2.4.2', 'EN-9.2.4.4' ,'EN-9.3.1.1' ,'EN-9.3.1.2', 'EN-9.3.3.2',
 'EN-9.4.1.2' ,'TT11.a' ,'TT11.b', 'TT12.a' ,'TT12.d', 'TT13.a' ,'TT13.c',
 'TT14.b', 'TT17.a' ,'TT2.a' ,'TT2.b' ,'TT4.a' ,'TT5.c', 'TT6.a' ,'TT7.a', 'TT7.b',
 'TT8.a', 'TT9.a', 'TTv5', 'best-practice' ,'cat.aria', 'cat.color' ,'cat.forms',
 'cat.keyboard', 'cat.language', 'cat.name-role-value' , 'cat.parsing',
 'cat.semantics', 'cat.sensory-and-visual-cues' ,'cat.structure',
 'cat.tables' ,'cat.text-alternatives' ,'cat.time-and-media' ,'review-item',
 'section508' ,'section508.22.a', 'section508.22.f' ,'section508.22.g',
 'section508.22.i' ,'section508.22.j' ,'section508.22.n' ,'section508.22.o',
 'wcag111' ,'wcag122' ,'wcag131' ,'wcag135' ,'wcag141' ,'wcag1412' ,'wcag142',
 'wcag143' ,'wcag144' ,'wcag146' ,'wcag211' ,'wcag213' ,'wcag21aa' ,'wcag221' ,
 'wcag222' ,'wcag224', 'wcag22aa', 'wcag241', 'wcag242', 'wcag244' , 'wcag249',
 'wcag258', 'wcag2a', 'wcag2aa' ,'wcag2aaa', 'wcag311' ,'wcag312' ,'wcag325',
 'wcag332', 'wcag412']
                }
            })
            """)

            # Close the browser
            await browser.close()

            # Process and return results
            return results
    except Exception as e:
        print("An error occurred:", e)
        return None

async def check_accessibility_from_html(html_code):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            # Set the raw HTML content instead of navigating to a URL
            await page.set_content(html_code)

            # Inject axe-core from CDN
            await page.add_script_tag(url="https://cdn.jsdelivr.net/npm/axe-core@4.4.1/axe.min.js")

            # Run axe accessibility checks
            results = await page.evaluate("""
            () => axe.run(document, {
                runOnly: {
                    type: 'tag',
                    values: ['ACT' ,'EN-301-549' ,'EN-9.1.1.1' ,'EN-9.1.2.2' ,'EN-9.1.3.1' ,'EN-9.1.3.5',
 'EN-9.1.4.1' ,'EN-9.1.4.12' ,'EN-9.1.4.2', 'EN-9.1.4.3', 'EN-9.1.4.4',
 'EN-9.2.1.1' ,'EN-9.2.1.3' ,'EN-9.2.2.1' ,'EN-9.2.2.2', 'EN-9.2.4.1',
 'EN-9.2.4.2', 'EN-9.2.4.4' ,'EN-9.3.1.1' ,'EN-9.3.1.2', 'EN-9.3.3.2',
 'EN-9.4.1.2' ,'TT11.a' ,'TT11.b', 'TT12.a' ,'TT12.d', 'TT13.a' ,'TT13.c',
 'TT14.b', 'TT17.a' ,'TT2.a' ,'TT2.b' ,'TT4.a' ,'TT5.c', 'TT6.a' ,'TT7.a', 'TT7.b',
 'TT8.a', 'TT9.a', 'TTv5', 'best-practice' ,'cat.aria', 'cat.color' ,'cat.forms',
 'cat.keyboard', 'cat.language', 'cat.name-role-value' , 'cat.parsing',
 'cat.semantics', 'cat.sensory-and-visual-cues' ,'cat.structure',
 'cat.tables' ,'cat.text-alternatives' ,'cat.time-and-media' ,'review-item',
 'section508' ,'section508.22.a', 'section508.22.f' ,'section508.22.g',
 'section508.22.i' ,'section508.22.j' ,'section508.22.n' ,'section508.22.o',
 'wcag111' ,'wcag122' ,'wcag131' ,'wcag135' ,'wcag141' ,'wcag1412' ,'wcag142',
 'wcag143' ,'wcag144' ,'wcag146' ,'wcag211' ,'wcag213' ,'wcag21aa' ,'wcag221' ,
 'wcag222' ,'wcag224', 'wcag22aa', 'wcag241', 'wcag242', 'wcag244' , 'wcag249',
 'wcag258', 'wcag2a', 'wcag2aa' ,'wcag2aaa', 'wcag311' ,'wcag312' ,'wcag325',
 'wcag332', 'wcag412']
                }
            })
            """)

            await browser.close()
            return results

    except Exception as e:
        print("An error occurred:", e)
        return None

async def main_url(url, index, impactScore):
    # Added: violaion_dict_list to add all the violations of each url
    violaion_dict_list = []
    
    url_to_test = url
    print(f"URL to test: {url_to_test}")
    results = await check_accessibility(url_to_test)
    # print("==========DIR========",results)

    if results:
        # Extract and print violations
        violations = results['violations']
        if violations:
            print(f"Number of accessibility violations: {len(violations)}")

            for violation in violations:
                description = violation['description']
                impact = violation['impact']
                help_url = violation ['helpUrl']
                # html_code = ", ".join([node['html'] for node in violation['nodes']]) # Original
                html_code = [node['html'] for node in violation['nodes']]
                failureSummary = ", ".join([node['failureSummary'] for node in violation['nodes']])
                additional_information = []
                for node in violation['nodes']:
                    try:
                        new_info = node["any"][0]['data']
                        if type(new_info)==dict:
                            additional_information.append(new_info)
                    except:
                        pass
                # Add data to the DataFrame
                # df.loc[index] = [url, len(violations), violation['id'], impactScore.get(impact, "Unknown"), description, help_url, html_code]
                index += 1  # Increment index for next row if needed
                # Added: Created a violation_dict which will hold all the informations
                violation_dict = {'webURL':url, 'numViolations':len(violations), 'violationnumberID':violation['id'],
                                  'initialImpactScore':impactScore.get(impact, "Unknown"), 'Description':description, 
                                  'LongDescription':help_url, 'AffectedHTMLElement(s)':html_code,"additional_info":additional_information,"failureSummary":failureSummary}
                # Added: and appending it to the violaion_dict_list
                violaion_dict_list.append(violation_dict)
            
            # Added: return violaion_dict_list which has each violations of the given url
            return violaion_dict_list


        else:
            print("No accessibility violations found.")
            # df.loc[index] = [url, 0, None, 0, "No violations found", None, None]
            
            # Added: instead of adding it to the dataframe, returning it as a list of dict(since other return consist of list of dict).
            return [{'webURL':url, 'numViolations':0, 'violationnumberID':None,
                                  'initialImpactScore':0, 'Description':"No violations found", 
                                  'LongDescription':None, 'AffectedHTMLElement(s)':None,
                    'additional_info':None,"failureSummary":None}]
    else:
        print("No results returned or an error occurred.")
         # Added: return empty list
        return []


async def main_html(html):
    total_impact_score = 0
    results = await check_accessibility_from_html(html)
    if not results or 'violations' not in results:
        print("No results or violations returned.")
        return 0  # No violations or API failed
      
    if results:
        violations = results['violations']
        # total_impact_score = sum(v.get('initialImpactScore', 0) for v in violations)
        if violations:
            print(f"Number of accessibility violations: {len(violations)}")
            
            for violation in violations:
                impact = violation['impact']
                initialImpactScore = impactScore.get(impact, "Unknown")
                total_impact_score = total_impact_score + initialImpactScore

        return total_impact_score
        
def get_playwright_score(html):
    try:
        return asyncio.run(main_html(html))
    except Exception as e:
        print(f"Error for HTML: {e}")
        return 0

##########################
#######Call with URL #####
##########################

# output = pd.DataFrame()
# urls = list(url_df["webURL"].values)
# print(urls)
# # # Running the main function with asyncio
# for url in urls:
#     a = asyncio.run(main_url(url, 0, impactScore))
#     for each_violation in a:
#         df_dictionary = pd.DataFrame([each_violation])
#         output = pd.concat([output, df_dictionary], ignore_index=True)

# # Merge back with original data
# violation_df = pd.merge(output, url_df, left_on="sourceID", right_index=True)

# violation_df = violation_df[[
#     '#', 'webURL', 'numViolations', 'violationnumberID', 'initialImpactScore',
#     'Description', 'LongDescription', 'AffectedHTMLElement(s)',
#     'additional_info', 'failureSummary'
# ]]

# violation_df.to_csv("semantic_playwright_from_html.csv", index=False)


####################################################
#######   Call with html for Total New Score   #####
####################################################

# TEST 1 sample
# html = """ 
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Accessible SVG Example</title>
# </head>
# <body>
#     <svg aria-label="HTML5 logo" role="img" viewbox="0 0 512 512">
#         <path d="M108.46"></path>
#         <path d="M107.6 " fill="#e44d26"></path>
#         <path d="M256 " fill="#f16529"></path>
#         <path d="M142 176" fill="#ebebeb"></path>
#         <path d="M369.613.6v47.2l93-25.8" fill="#fff"></path>
#     </svg>
# </body>
# </html>
# """
# a  = asyncio.run(main_html(html))
# print(a)


url_df = pd.read_csv("/content/LLM_responseHTML_results_accessguru_ablation_semantic_dataset_qwen-vl-plus - LLM_responseHTML_results_accessguru_ablation_semantic_dataset_qwen-vl-plus.csv")

url_df["InitialPlaywrightScore"] = url_df["Extracted_LLM_responseHTML"].apply(get_playwright_score)
url_df["NewPlaywrightScore"] = (
    url_df["New Violation Score"].astype(int) + url_df["InitialPlaywrightScore"].astype(int)
)
url_df.to_csv("Playwright_results_accessguru_ablation_semantic_dataset_qwen-vl-plus.csv", index=False)




