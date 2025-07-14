

!apt install chromium-chromedriver

!pip install nest_asyncio
!pip install playwright
!playwright install

impactScore = {
  "critical": 5,
  "serious": 4,
  "moderate": 3,
  "minor": 2,
  "cosmetic": 1,
  "accessible":0
}

print(impactScore['serious'])

import pandas as pd

mp_final_results = pd.read_csv('/content/baseline1_results.csv')
mp_final_results.head()

#baseline2_results = pd.read_csv('/content/baseline2_results.csv')
#baseline2_results.iloc[0]['corrected_Code']

import asyncio
import nest_asyncio
from playwright.async_api import async_playwright
import pandas as pd
import tempfile

# Apply nest_asyncio to allow running in environments with an existing event loop
nest_asyncio.apply()

async def check_accessibility_from_html(html_content):
    try:
        async with async_playwright() as p:
            # Start Chromium browser
            browser = await p.chromium.launch()
            page = await browser.new_page()

            # Create a temporary HTML file from the snippet
            with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as temp_file:
                temp_file.write(html_content.encode('utf-8'))
                temp_file_path = temp_file.name

            # Navigate to the temporary HTML file
            await page.goto(f"file://{temp_file_path}")

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

async def main(html_content):

    print("HTML content provided for accessibility testing.")
    results = await check_accessibility_from_html(html_content)

    if results:
        # Extract and print violations
        violations = results['violations']
        if violations:
            print(f"Number of accessibility violations: {len(violations)}")
            for violation in violations:
                print(f"\nViolation Name: {violation['id']}")
                print(f"\nDescription: {violation['description']}")
                print(f"Impact: {violation['impact']}")
                print(f"Help URL: {violation['helpUrl']}")
                for node in violation['nodes']:
                    print(f"Element affected: {node['html']}")

        else:
            print("No accessibility violations found.")

    else:
        print("No results returned or an error occurred.")

# Example HTML snippet
html_snippet = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Incorrect List Example</title>
</head>
<body>

    <h2>Incorrectly Structured List</h2>

    <!-- Incorrect use: Divs instead of proper list elements -->
    <div>
        <li>Item 1</li>
        <li>Item 2</li>
        <li>Item 3</li>
    </div>

    <!-- Missing <ul> or <ol> parent element -->
    <li>Orphan List Item</li>

    <!-- Improperly nested list (ul inside li without a proper structure) -->
    <ul>
        <li>Item A
            <ul>
                <li>Subitem A1</li>
        </li> <!-- Closing the li incorrectly -->
        <li>Item B</li>
    </ul>

</body>
</html>

"""


# Running the main function with asyncio
if __name__ == "__main__":
    asyncio.run(main(html_snippet))

import asyncio
import nest_asyncio
from playwright.async_api import async_playwright
import pandas as pd
import tempfile

# Apply nest_asyncio to allow running in environments with an existing event loop
nest_asyncio.apply()

async def check_accessibility_from_html(html_content):
    try:
        async with async_playwright() as p:
            # Start Chromium browser
            browser = await p.chromium.launch()
            page = await browser.new_page()

            # Create a temporary HTML file from the snippet
            with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as temp_file:
                temp_file.write(html_content.encode('utf-8'))
                temp_file_path = temp_file.name

            # Navigate to the temporary HTML file
            await page.goto(f"file://{temp_file_path}")

            # Inject axe-core from CDN
            await page.add_script_tag(url="https://cdn.jsdelivr.net/npm/axe-core@4.4.1/axe.min.js")

            # Run axe accessibility checks
            results = await page.evaluate("""
            () => axe.run(document, {
                runOnly: {
                    type: 'tag',
                    values: ['cat.aria', 'wcag2a', 'wcag131', 'wcag412', 'EN-301-549', 'EN-9.1.3.1', 'EN-9.4.1.2']
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

async def main(html_content):

    print("HTML content provided for accessibility testing.")
    results = await check_accessibility_from_html(html_content)

    if results:
        # Extract and print violations
        violations = results['violations']
        if violations:
            print(f"Number of accessibility violations: {len(violations)}")
            for violation in violations:
                print(f"\nDescription: {violation['description']}")
                print(f"Impact: {violation['impact']}")
                print(f"Help URL: {violation['helpUrl']}")
                for node in violation['nodes']:
                    print(f"Element affected: {node['html']}")

        else:
            print("No accessibility violations found.")

    else:
        print("No results returned or an error occurred.")

# Example HTML snippet language or title
html_snippet = """



"""
# Running the main function with asyncio
if __name__ == "__main__":
    asyncio.run(main(html_snippet))

import asyncio
import nest_asyncio
from playwright.async_api import async_playwright
import tempfile

new_score = []
#new_description = []


# Apply nest_asyncio to allow running in environments with an existing event loop
nest_asyncio.apply()

async def check_accessibility_from_html_snippet(html_snippet):
    try:
        async with async_playwright() as p:
            # Start Chromium browser
            browser = await p.chromium.launch()
            page = await browser.new_page()

            # Create a temporary HTML file with a basic structure and the provided snippet
            minimal_html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width,minimum-scale=1,maximum-scale=1,user-scalable=no">
                <title>Test Page</title>
            </head>
            <body>
                {html_snippet}
            </body>
            </html>
            """
            with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as temp_file:
                temp_file.write(minimal_html.encode('utf-8'))
                temp_file_path = temp_file.name

            # Navigate to the temporary HTML file
            await page.goto(f"file://{temp_file_path}")

            # Inject axe-core from CDN
            await page.add_script_tag(url="https://cdn.jsdelivr.net/npm/axe-core@4.4.1/axe.min.js")

            # Run axe accessibility checks
            results = await page.evaluate("""
            () => axe.run(document.body, {
                runOnly: {
                    type: 'tag',
                    values: ['wcag2a', 'wcag2aa']
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

async def main(html_snippet):

    print("HTML snippet provided for accessibility testing.")
    results = await check_accessibility_from_html_snippet(html_snippet)

    if results:
        # Extract and print violations
        violations = results['violations']
        if violations:
            vScore = []
            #vDescription = []
            print(f"Number of accessibility violations: {len(violations)}")
            for violation in violations:
                print(f"\nDescription: {violation['description']}")
                print(f"Impact: {violation['impact']}")
                print(f"Help URL: {violation['helpUrl']}")
                for node in violation['nodes']:
                    print(f"Element affected: {node['html']}")

                vScore.append(impactScore[violation['impact']])
                #vDescription.append(violation['description'])
            new_score.append(sum(vScore))




        else:
            print("No accessibility violations found.")
            new_score.append(0)


    else:
        print("No results returned or an error occurred.")
        new_score.append(-1)


# Example HTML snippet
#html_snippet = mp_final_results.iloc[0]['Corrected_code']

# Running the main function with asyncio
if __name__ == "__main__":
    for i in range(len(mp_final_results)):
      if mp_final_results.iloc[i]['filtered_response'] != 'nan':
        html_snippet = mp_final_results.iloc[i]['filtered_response']
        #html_snippet =baseline2_results.iloc[i]['corrected_Code']

        asyncio.run(main(html_snippet))
        print("--------------------------------------------------------------------------")
      else:
        new_score.append(-1)
        print("--------------------------------------------------------------------------")

dfnewScore = pd.DataFrame(new_score, columns=['finalImpactScore'])

mp_final_results_new_scores = pd.concat([mp_final_results, dfnewScore], axis=1)
#baseline2_results_new_scores = pd.concat([baseline2_results, dfnewScore], axis=1)

mp_final_results_new_scores.head()
#baseline2_results_new_scores.head()

mp_final_results_new_scores.to_csv('baseline1_final_results_new_scores_final.csv', index=False)
#baseline2_results_new_scores.to_csv('baseline2_results_new_scores.csv', index=False)







import pandas as pd

fixed_data = pd.read_csv('/content/fixed_data.csv')
fixed_data.head()

# Define the initial and final scores
R_initial = 3.953125
R_fix = 0.7734375

# Calculate the percentage decrease using the formula from the image
I = (1 - (R_fix / R_initial)) * 100
I

