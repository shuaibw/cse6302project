"""
!pip install playwright
!playwright install
"""
import pandas as pd
import os
import asyncio
import nest_asyncio
from urllib.parse import urlparse
from playwright.async_api import async_playwright
import pandas as pd
from bs4 import BeautifulSoup
import re
import aiohttp
import json
from SupplementaryInformationExtraction import extract_supplementary_info

nest_asyncio.apply()

async def download_image(url, path):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    with open(path, 'wb') as f:
                        f.write(await resp.read())
                    print(f"📸 Image downloaded: {path}")
                    return True
                else:
                    print(f"Failed to download image, status: {resp.status}")
                    return False
    except Exception as e:
        print(f"Exception during image download: {e}")
        return False


async def save_html(html, url):
    parsed = urlparse(url)
    netloc = parsed.netloc.replace(".", "_")
    path = parsed.path.strip("/") or "home"
    path = "".join([c if c.isalnum() else "_" for c in path])
    file_name = f"{netloc}_{path}.html"
    file_path = os.path.join(output_dir, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)

    return file_path

async def check_accessibility(url):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url)
            html = await page.content()
            html_file_name = await save_html(html, url)  # Save the HTML

            await page.add_script_tag(url="https://cdn.jsdelivr.net/npm/axe-core@4.4.1/axe.min.js")

            results = await page.evaluate("""
            () => axe.run(document, {
                runOnly: {
                    type: 'tag',
                    values: [
                        'ACT', 'EN-301-549', 'EN-9.1.1.1', 'EN-9.1.2.2', 'EN-9.1.3.1', 'EN-9.1.3.5',
                        'EN-9.1.4.1', 'EN-9.1.4.12', 'EN-9.1.4.2', 'EN-9.1.4.3', 'EN-9.1.4.4',
                        'EN-9.2.1.1', 'EN-9.2.1.3', 'EN-9.2.2.1', 'EN-9.2.2.2', 'EN-9.2.4.1',
                        'EN-9.2.4.2', 'EN-9.2.4.4', 'EN-9.3.1.1', 'EN-9.3.1.2', 'EN-9.3.3.2',
                        'EN-9.4.1.2', 'TT11.a', 'TT11.b', 'TT12.a', 'TT12.d', 'TT13.a', 'TT13.c',
                        'TT14.b', 'TT17.a', 'TT2.a', 'TT2.b', 'TT4.a', 'TT5.c', 'TT6.a', 'TT7.a', 'TT7.b',
                        'TT8.a', 'TT9.a', 'TTv5', 'best-practice', 'cat.aria', 'cat.color', 'cat.forms',
                        'cat.keyboard', 'cat.language', 'cat.name-role-value', 'cat.parsing',
                        'cat.semantics', 'cat.sensory-and-visual-cues', 'cat.structure',
                        'cat.tables', 'cat.text-alternatives', 'cat.time-and-media', 'review-item',
                        'section508', 'section508.22.a', 'section508.22.f', 'section508.22.g',
                        'section508.22.i', 'section508.22.j', 'section508.22.n', 'section508.22.o',
                        'wcag111', 'wcag122', 'wcag131', 'wcag135', 'wcag141', 'wcag1412', 'wcag142',
                        'wcag143', 'wcag144', 'wcag146', 'wcag211', 'wcag213', 'wcag21aa', 'wcag221',
                        'wcag222', 'wcag224', 'wcag22aa', 'wcag241', 'wcag242', 'wcag244', 'wcag249',
                        'wcag258', 'wcag2a', 'wcag2aa', 'wcag2aaa', 'wcag311', 'wcag312', 'wcag325',
                        'wcag332', 'wcag412'
                    ]
                }
            })
            """)

            return results, page, browser,html_file_name,html
    except Exception as e:
        print("An error occurred:", e)
        return None, None, None, None, None


def get_full_list_html(web_html: str, affected_html: str) -> str | None:
    soup = BeautifulSoup(web_html, "html.parser")

    # Parse the affected HTML to extract the tag and attributes
    affected_soup = BeautifulSoup(affected_html, "html.parser")
    affected_element = affected_soup.find()

    if not affected_element:
        print("Could not parse affected HTML")
        return None

    # Find matching element in full page HTML
    matches = soup.find_all(affected_element.name, attrs=affected_element.attrs)

    for match in matches:
        # Return the outer HTML of the matching list
        if match.name in ['ul', 'ol']:
            return str(match)

    print("No matching full list element found.")
    return None

async def main(url, index, impactScore):
    violation_dict_list = []
    
    url_to_test = url
    print(f"URL to test: {url_to_test}")
    results, page, browser, html_file_name, web_html = await check_accessibility(url_to_test)

    if results:
        violations = results['violations']
        if violations:
            print(f"Number of accessibility violations: {len(violations)}")
            
            try:
                for violation in violations:
                    supplementary_information_parts = []  # <-- use list to accumulate
                    violation_id = violation['id']
                    print("======violation_id:", violation_id)

                    description = violation['description']
                    impact = violation['impact']
                    help_url = violation['helpUrl']
                    html_code = ", ".join([node['html'] for node in violation['nodes']])

                    # Supplementary Information: Color Violations
                    if violation_id in ['color-only-distinction', 'color-contrast-enhanced', 'color-contrast']:
                        try:
                            data_value = violation['nodes'][0]['any'][0]['data']
                            if isinstance(data_value, dict) and 'fgColor' in data_value:
                                supplementary_information_parts.append(str(data_value))
                        except (IndexError, KeyError):
                            pass

                    screenshot_paths = []

                    # Supplementary Information: Image violations
                    if violation_id in [
                        "image-alt", "input-image-alt", "image-alt-not-descriptive",
                        "image-redundant-alt", "area-alt", "frame-title", "frame-title-unique",
                        "object-alt", "role-img-alt", "svg-img-alt", "button-name", "input-button-name"
                    ]:
                        for i, node in enumerate(violation['nodes']):
                            html = node.get('html', '')
                            img_src_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', html)
                            if img_src_match:
                                img_url = img_src_match.group(1)
                                parsed = urlparse(url)
                                domain = parsed.netloc.replace('.', '_')
                                filename = f"{domain}_{violation_id}_{i}.png"
                                filepath = os.path.join(screenshot_dir, filename)

                                success = await download_image(img_url, filepath)
                                if success:
                                    screenshot_paths.append(filepath)
                            else:
                                print(f"No img src found in node HTML for violation {violation_id}, node index {i}")
                    
                    if screenshot_paths:
                        supplementary_information_parts.append(", ".join(screenshot_paths))

                    # Supplementary Information: List
                    list_html_snippets = []
                    if violation_id == "list":
                        for i, node in enumerate(violation['nodes']):
                            affected_html = node.get('html', '')
                            full_list_html = get_full_list_html(web_html, affected_html)
                            if full_list_html:
                                list_html_snippets.append(full_list_html)

                    if list_html_snippets:
                        supplementary_information_parts.append("\n\n---\n\n".join(list_html_snippets))

                    # Supplementary Information: link-name
                    link_info_list = []
                    if violation_id == "link-name":
                        for node in violation["nodes"]:
                            affected_html = node.get("html", "")
                            print(affected_html)

                            href_match = re.search(r'href=["\']([^"\']+)["\']', affected_html)
                            target_match = re.search(r'target=["\']([^"\']+)["\']', affected_html)

                            href = href_match.group(1) if href_match else None
                            explicit_target = target_match.group(1).lower() if target_match else None

                            if not href or not href.startswith("http"):
                                continue

                            try:
                                if explicit_target == "_blank":
                                    try:
                                        async with async_playwright() as p:
                                            browser1 = await p.chromium.launch()
                                            page = await browser1.new_page()
                                            await page.goto(href, timeout=15000)
                                            html = await page.content()
                                            soup = BeautifulSoup(html, 'html.parser')
                                            title = soup.title.string.strip() if soup.title else "No title found"
                                            link_info_list.append(f"The title of the target {href} link page: {title}")
                                            await browser1.close()
                                    except Exception as e:
                                        print(f"Error processing link '{href}': {e}")

                                elif explicit_target == "_self":
                                    async with async_playwright() as p:
                                        browser1 = await p.chromium.launch()
                                        page1 = await browser1.new_page()
                                        await page1.goto(href, timeout=15000)

                                        page_title = await page1.title()
                                        if not page_title:
                                            html = await page1.content()
                                            soup = BeautifulSoup(html, 'html.parser')
                                            page_title = soup.title.string.strip() if soup.title else "No title found"

                                        link_info_list.append(f"The title of the target {href} link page: {page_title}")
                                        await browser1.close()

                                else:
                                    try:
                                        async with async_playwright() as p:
                                            browser1 = await p.chromium.launch()
                                            page = await browser1.new_page()
                                            await page.goto(href, timeout=15000)
                                            html = await page.content()
                                            soup = BeautifulSoup(html, 'html.parser')
                                            title = soup.title.string.strip() if soup.title else "No title found"
                                            link_info_list.append(f"The title of the target {href} link page: {title}")
                                            await browser1.close()
                                    except Exception as e:
                                        print(f"Error processing link '{href}': {e}")

                            except Exception as e:
                                print(f"Error processing link '{href}': {e}")

                    if link_info_list:
                        supplementary_information_parts.append("\n\n".join(link_info_list))

                    # Final supplementary info
                    supplementary_information = "\n\n".join(supplementary_information_parts)

                    index += 1  
                    violation_dict = {
                        'web_url': url,
                        'violation_count': len(violations),
                        'violation_name': violation_id,
                        'violation_score': impactScore.get(impact, "Unknown"),
                        'violation_description': description,
                        'full_violation_description_url': help_url,
                        'affected_html_elements': html_code,
                        'html_file_name': html_file_name,
                        'supplementary_information': supplementary_information
                    }
                    violation_dict_list.append(violation_dict)

                return violation_dict_list

            except Exception as e:
                print(f"Unexpected error in violation processing: {e}")
            finally:
                print("Closing browser now...")
                await browser.close()
        else:
            print("No accessibility violations found.")
            await browser.close()
            return [{
                'web_url': url,
                'violation_count': 0,
                'violation_name': None,
                'violation_score': 0,
                'violation_description': "No violations found",
                'full_violation_description_url': None,
                'affected_html_elements': None,
                'html_file_name': None,
                'supplementary_information': None
            }]

    else:
        print("No results returned or an error occurred.")
        if browser:
            await browser.close()
        return []



###################### EXTERNAL FILE ###########################
output_dir = "/workspace/FullPipeline/html_pages_async"
html_base_path = output_dir
os.makedirs(output_dir, exist_ok=True)

screenshot_dir = "/workspace/FullPipeline/element_screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

json_file_path = '/workspace/FullPipeline/mapping_dict_file.json'
with open(json_file_path, 'r') as file:
  mapping_dict = json.load(file)

cat_data = pd.read_csv("/workspace/FullPipeline/violation_taxonomy.csv")

def dummy():
    urls = [
        "https://www.futurity.org",
        # "https://arstechnica.com/ai/",
        # "https://www.nationalgeographic.com",
        # "https://www.mashable.com",
        # "https://www.bostonglobe.com",
        # "https://www.metro.co.uk",
        # "https://www.thedailybeast.com"
    ]

    data = []
    base_id = 1001  # Starting ID

    for i, url in enumerate(urls):
        data.append({
            "domain": "Media",
            "web_url": url,
            "weburl_id": base_id + i
        })

    url_df = pd.DataFrame(data)
    return (url_df)

# url_df = dummy()
url_df = pd.read_csv("/workspace/FullPipeline/url_df.csv")

###################### MAIN CODE ###########################
impactScore = {
  "critical": 5,
  "serious": 4,
  "moderate": 3,
  "minor": 2,
  "cosmetic": 1,
}


urls = list(url_df["web_url"].values)
print("====# OF URLS:",len(urls))

output = pd.DataFrame()
# # Running the main function with asyncio
ccount_url = 0
for url in urls:
    ccount_url = ccount_url+1
    print(f"{ccount_url} ====url: {url}")
    a = asyncio.run(main(url, 0, impactScore))
    for each_violation in a:
        df_dictionary = pd.DataFrame([each_violation])
        output = pd.concat([output, df_dictionary], ignore_index=True)

violation_df = pd.merge(output, url_df, on="web_url")
violation_df = violation_df[violation_df['violation_count'] != 0]

violation_df = violation_df[['weburl_id','domain','web_url','violation_count',
                             'violation_name','violation_score','violation_description',
                             'full_violation_description_url','affected_html_elements',
                             'html_file_name','supplementary_information']]

scoreToImpact = {v: k for k, v in impactScore.items()}
violation_df["violation_impact"] = violation_df["violation_score"].map(scoreToImpact)
violation_df["wcag_reference"] = violation_df["violation_name"].map(mapping_dict)

violation_to_category = cat_data.set_index("violationnumberID")["Category"].to_dict()
violation_df['violation_category'] = violation_df['violation_name'].map(violation_to_category)
violation_df.to_csv("/workspace/FullPipeline/ExtendedData.csv",index=False)

# import pdb;pdb.set_trace()
print(violation_df.head())
print("=======PLAYWRIGHT PART COMPLETED======")
violation_df['supplementary_information'] = violation_df.apply(extract_supplementary_info, axis=1)
# violation_df.to_csv("/workspace/FullPipeline/Extended_havingAllSupplimentary.csv", index=False)
# print(violation_df.head())
# print("=====EXTRA SUPPLEMENTARY COMPLETED===")
