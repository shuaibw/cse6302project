PROMPT_TEMPLATE = """ You are a web accessibility expert. Your task is to detect semantic accessibility violations in the given HTML Web page. These violations are often not detectable by standard automated tools and require interpretation of the content meaning and user context.

A semantic violation occurs when: 
- Attributes like alt text, language, or link/button labels are present but do not provide meaningful or accurate information, 
- Visual or multimedia content is not described in a way that conveys its purpose to users with disabilities. 

Use the information below to guide your analysis, you are operating on: 
- The domain of the web page: {Insert Web page Domain}
- The URL of the web page: {Insert Web page URL}

You are provided with:
- The HTML code of the web page to analyze,
- The full semantic violation taxonomy. This taxonomy defines specific types of semantic violations, their descriptions, 
- A screenshot of the rendered view of the web page.

{Semantic Violation Taxonomy}

{Insert HTML here}
{Insert Web page screenshot}


Now, review the HTML and supplementary data. List all semantic violations you detect, and for each: 
1. Identify the affected HTML element or attribute, 
2. Specify the violation type. 
