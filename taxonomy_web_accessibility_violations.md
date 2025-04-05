# Taxonomy of Web Accessibility Violations

Each violation includes a **Rule ID**, **Description**, the corresponding **WCAG Guidelines** it violates, **Impact**, and **Supplementary Information**.

- **Syntactic Violations:** These occur when HTML code lacks proper structural elements or attributes required by accessibility standards. Examples include missing alt attributes for images or improperly structured tables, which hinder compliance with accessibility guidelines. (HTML code expertise only)
- **Layout Violations:** These relate to visual design and organization that do not meet accessibility standards, such as insufficient color contrast between text and background. These issues affect readability and usability for users, especially those with visual impairments. (Familiar with web design principles, make sure it is not distorted for normal users)
- **Semantic Violations:** We define semantic violations as the violations that involve the misuse or absence of meaningful content or attributes that provide contextual understanding. For instance, using nonsensical or placeholder text in alt attributes fails to convey the intended information to assistive technologies.



| **Category**           | **Rule ID**           | **Description**                                                                                       | **Guidelines**    | **Impact** | **Supplementary Information**|
|-------------------------|-----------------------|-------------------------------------------------------------------------------------------------------|-------------------|-------------------|------------------|
| Semantic      | `image-alt-not-descriptive`      | Inaccurate or misleading alternative text that fails to describe the purpose of the image.            | 1.1.1             |  Critical | Image  |
| Semantic      | `video-captions-not-descriptive`    | Inaccurate video captions.                                 | 1.2.1, 1.2.3      | Critical  |  Video |
| Semantic      | `lang-mismatch`      | Page language attribute does not match the actual language of the content.                            | 3.1.1             | Serious  |   |
| Semantic      | `missing-lang-tag`   | Sections in different languages lack appropriate `lang` attributes.                                   | 3.1.2             |  Serious |   |
| Semantic      | `link-text-mismatch`  | Links fail to convey their purpose or are ambiguous.                                                  | 2.4.4, 2.4.9      | Serious  |   |
| Semantic      | `button-label-mismatch`       | Buttons labels are unclear or fail to specify their purpose.                                            | 4.1.2, 2.5.3             |  Critical  |  |
| Semantic      | `form-label-mismatch`         | Forms elements have unclear or incorrect labels.                                                 | 3.3.2             |   Critical |Form context (e.g., surrounding text, instructions)|
| Semantic      | `ambiguous-heading`  | Headings are vague, repetitive, or fail to describe the content.                                      | 2.4.6, 2.4.10     |  Moderate  |   |
| Semantic      | `incorrect-semantic-tag`    | A non-semantic tag (e.g., `div` or `span`) is used instead of a proper semantic element (e.g., `header`, `nav`, `main`).                                      | 1.3.1             | Serious  |  Document structure (other headings, section context) |
| Semantic      | `landmark-structural-violation`    |  Landmarks or ARIA roles are misused, such as having multiple `main` elements, nesting landmarks, or failing to label multiple `nav` regions properly.                                         | 1.3.6           | Serious  |  |
| Semantic      | `landmark-purpose-mismatch` | A landmark or ARIA role does not match its actual purpose or placement, such as labeling a `<nav>` in the header as "Footer navigation."                                          | 1.3.6             | Serious  |  Document structure and context around the landmark  |
| Semantic      | `page-title-not-descriptive`      | Page title fails to describe the content or purpose of the page, making navigation difficult.           | 2.4.2             |  Serious | Page content and purpose  |

---



| **Category**           | **Rule ID**           | **Description**                                                                                       | **Guidelines**    | **Impact** | **Supplementary Information**|
|-------------------------|-----------------------|-------------------------------------------------------------------------------------------------------|-------------------|-------------------|------------------|
| Layout      | `meta-viewport`      | Ensure `<meta name="viewport">` does not disable text scaling and zooming            |             |  Critical | |

| Layout      | `meta-viewport-large`      |  Ensure `<meta name="viewport">` can scale a significant amount           |             |  Minor | |


---


| **Category**           | **Rule ID**           | **Description**                                                                                       | **Guidelines**    | **Impact** | 
|-------------------------|-----------------------|-------------------------------------------------------------------------------------------------------|-------------------|-------------------|
| Syntax      | `blink`      |      	Ensure `<blink>` elements are not used       |             | Serious  |
| Syntax      | `scope-attr-valid`      |       Ensure the scope attribute is used correctly on tables      |             |  Moderate |
| Syntax      | `aria-allowed-attr`      |    Ensure an element's role supports its ARIA attributes         |             | Critical  |
| Syntax      | `aria-allowed-role`      |   Ensure role attribute has an appropriate value for the element          |             |  Minor |
| Syntax      | `aria-valid-attr`      |   Ensure attributes that begin with aria- are valid ARIA attributes          |             |  Critical |
| Syntax      | `aria-valid-attr-value`      |   Ensure all ARIA attributes have valid values          |             |  Critical |
| Syntax      | `autocomplete-valid`      |   Ensure the autocomplete attribute is correct and suitable for the form field          |             |  Serious |
| Syntax      | `role-img-alt`      |   Ensure [role="img"] elements have alternative text          |             | Serious  |
| Syntax      | `td-headers-attr`      | Ensure that each cell in a table that uses the headers attribute refers only to other `<th>` elements in that table  |    |  Serious |
| Syntax      | `area-alt`      |    Ensure `<area>` elements of image maps have alternative text         |             |  Critical |
| Syntax      | `object-alt`      |      Ensure `<object>` elements have alternative text       |             |  Serious |
| Syntax      | `svg-img-alt`      |   Ensure `<svg>` elements with an img, graphics-document or graphics-symbol role have an accessible text          |             |  Serious |
| Syntax      | `input-image-alt`      |    Ensure `<input type="image">` elements have alternative text         |             |  Critical |
| Syntax      | `image-alt`      |    Ensure `<img>` elements have alternative text or a role of none or presentation         |             |  Critical |
| Syntax      | `html-lang-valid`      |      Ensure the lang attribute of the `<html>` element has a valid value       |             |  Serious |
| Syntax      | `html-xml-lang-mismatch`      |      Ensure that HTML elements with both valid lang and xml:lang attributes agree on the base language of the page       |             | Moderate  |
| Syntax      | `duplicate-id-aria`      |       Ensure every id attribute value used in ARIA and in labels is unique      |             |  Critical |
| Syntax      | `tabindex`      |       Ensure tabindex attribute values are not greater than 0      |             |  Serious |
| Syntax      | `valid-lang`      |       Ensure lang attributes have valid values      |             |  Serious |
| Syntax      | `aria-required-attr`      |      Ensure elements with ARIA roles have all required ARIA attributes       |             |  Critical |
| Syntax      | `aria-required-parent`      |     Ensure elements with an ARIA role that require parent roles are contained by them        |             | Critical  |
| Syntax      | `aria-required-children`      |      Ensure elements with an ARIA role that require child roles contain them       |             |  Critical |
| Syntax      | `aria-deprecated-role`      |       Ensure elements do not use deprecated roles      |             |  Minor |
| Syntax      | `presentation-role-conflict`      |      Ensure elements marked as presentational do not have global ARIA or tabindex so that all screen readers ignore them       |             | Minor  |
| Syntax      | `aria-prohibited-attr`      |       Ensure ARIA attributes are not prohibited for an element's role      |             |  Serious |
| Syntax      | `list`      |        Ensure that lists are structured correctly     |             |  Serious |
| Syntax      | `frame-focusable-content`      |    Ensure `<frame>` and `<iframe>` elements with focusable content do not have tabindex=-1         |             |  Serious |
| Syntax      | `meta-refresh`      |       Ensure `<meta http-equiv="refresh">` is not used for delayed refresh      |             | Critical  |
| Syntax      | `marquee`      |         Ensure `<marquee>` elements are not used    |             |  Serious |
| Syntax      | `skip-link`      |     Ensure all skip links have a focusable target        |             |  Moderate |
| Syntax      | `landmark-no-duplicate-contentinfo`      |      Ensure the document has at most one contentinfo landmark       |             | Moderate  |
| Syntax      | `landmark-contentinfo-is-top-level`      |  Ensure the contentinfo landmark is at top level           |             | Moderate  |
| Syntax      | `landmark-one-main`      |     Ensure the document has a main landmark        |             |  Moderate |
| Syntax      | `landmark-unique`      |      Ensure landmarks are unique       |             |  Moderate |
| Syntax      | `landmark-banner-is-top-level`      |    Ensure the banner landmark is at top level         |             |  Moderate |
| Syntax      | `landmark-complementary-is-top-level`      |      Ensure the complementary landmark or aside is at top level       |             |  Moderate |
| Syntax      | `landmark-main-is-top-level`      |    Ensure the main landmark is at top level         |             |  Moderate |
| Syntax      | `landmark-no-duplicate-main`      |    Ensure the document has at most one main landmark         |             |  Moderate |
| Syntax      | `landmark-no-duplicate-banner`      |    Ensure the document has at most one banner landmark         |             | Moderate  |
| Syntax      | `document-title`      |     Ensure each HTML document contains a non-empty `<title>` element        |             | Serious  |
| Syntax      | `label`      |         Ensure every form element has a label    |             | Critical  |
| Syntax      | `label-title-only`      |   Ensure that every form element has a visible label and is not solely labeled using hidden labels, or the title or aria-describedby attributes          |             |  Serious |
| Syntax      | `summary-name`      |    Ensure summary elements have discernible text         |             |  Serious |
| Syntax      | `definition-list`      |   Ensure `<dl>` elements are structured correctly          |             | Serious  |
| Syntax      | `dlitem`      |       Ensure `<dt>` and `<dd>` elements are contained by a `<dl>`     |             | Serious  |
| Syntax      | `th-has-data-cells`      |     Ensure that `<th>` elements and elements with role=columnheader/rowheader have data cells they describe    |             |  Serious |
| Syntax      | `empty-table-header`      | Ensure table headers have discernible text            |             |  Minor |
| Syntax      | `empty-heading`      |  Ensure headings have discernible text           |             | Minor  |
| Syntax      | `listitem`      |       Ensure `<li>` elements are used semantically      |             |  Serious |
| Syntax      | `image-redundant-alt`      |    Ensure image alternative is not repeated as text         |             | Minor  |
| Syntax      | `link-name`      |     Ensure links have discernible text        |             | Serious  |
| Syntax      | `link-in-text-block`      |  Ensure links are distinguished from surrounding text in a way that does not rely on color           |             | Serious  |
| Syntax      | `input-button-name`      |   Ensure input buttons have discernible text          |             |  Critical |
| Syntax      | `aria-text`      |       Ensure role="text" is used on elements with no focusable descendants      |             | Serious  |
| Syntax      | `aria-tooltip-name`      |   Ensure every ARIA tooltip node has an accessible name          |             | Serious  |
| Syntax      | `aria-command-name`      |    Ensure every ARIA button, link and menuitem has an accessible name         |             |  Serious |
| Syntax      | `aria-input-field-name`      |   Ensure every ARIA input field has an accessible name          |             |  Serious |
| Syntax      | `aria-meter-name`      |     Ensure every ARIA meter node has an accessible name        |             | Serious  |
| Syntax      | `aria-progressbar-name`      |     Ensure every ARIA progressbar node has an accessible name        |             |  Serious |
| Syntax      | `aria-dialog-name`      |    Ensure every ARIA dialog and alertdialog node has an accessible name         |             |  Serious |
| Syntax      | `aria-toggle-field-name`      |   Ensure every ARIA toggle field has an accessible name          |             |  Serious |
| Syntax      | `aria-hidden-body`      |       Ensure aria-hidden="true" is not present on the document body      |             | Critical  |
| Syntax      | `aria-hidden-focus`      |   Ensure aria-hidden elements are not focusable nor contain focusable elements          |             | Serious  |
| Syntax      | `nested-interactive`      |     Ensure interactive controls are not nested as they are not always announced by screen readers or can cause focus problems for assistive technologies        |             |  Serious |
| Syntax      | `scrollable-region-focusable`      |    Ensure elements that have scrollable content are accessible by keyboard         |             |  Serious |
| Syntax      | `no-autoplay-audio`      |   Ensure `<video>` or `<audio>` elements do not autoplay audio for more than 3 seconds without a control mechanism to stop or mute the audio          |             |  Moderate |
| Syntax      | `region`      |             |             |   |
| Syntax      | `frame-tested`      |             |             |   |
| Syntax      | `frame-title`      |      Ensure `<iframe>` and `<frame>` elements have an accessible name       |             | Serious  | 
| Syntax      | `frame-title-unique`      |    Ensure all page content is contained by landmarks         |             |  Moderate |
| Syntax      | `video-caption`      |    Ensure `<video>` elements have captions         |             | Critical  |
| Syntax      | `heading-order`      |      Ensure the order of headings is semantically correct       |             | Moderate  |
| Syntax      | `accesskeys`      |      Ensure every accesskey attribute value is unique       |             |  Serious |
| Syntax      | `page-has-heading-one`      |   Ensure that the page, or at least one of its frames contains a level-one heading          |             |  Moderate |
| Syntax      | `bypass`      |        Ensure each page has at least one mechanism for a user to bypass navigation and jump straight to the content     |             |  Serious |
| Syntax      | `server-side-image-map`      |       Ensure that server-side image maps are not used      |             | Minor  |
| Syntax      | `button-name`      |      Ensure buttons have discernible text       |             | Critical  |
| Syntax      | `aria-roledescription`      |  Ensure aria-roledescription is only used on elements with an implicit or explicit role           |             |  Serious |
| Syntax      | `aria-roles`      |   Ensure all elements with a role attribute use a valid value          |             | Critical  |
| Syntax      | `duplicate-id`      |      Ensure every id attribute value is unique       |             |  Minor |
| Syntax      | `duplicate-id-active`      |  Ensure every id attribute value of active elements is unique           |             | Serious   |
| Syntax      | `html-has-lang`      |    Ensure every HTML document has a lang attribute         |             |  Serious |
| Syntax      | `select-name`      |      Ensure select element has an accessible name       |             |  Critical |

<!-- This is commented out.| Semantic      | `sensory-instructions`| Instructions rely on sensory characteristics without alternatives.                                    | 1.3.3             |  Serious |   |
| Semantic      | `error-messages`     | Errors are not clearly described, leaving users unable to fix them.                                   | 3.3.1             | Serious  |  Error context (e.g., input validation rules) |
| Semantic      | `error-correction`   | No accessible suggestions for correcting input errors.                                                | 3.3.3             | Serious  |  Error context and input requirements  |
| Semantic      | `error-consistency`  | Error messages lack consistency or clarity across interactions.                                       | 3.3.4             | Serious  |  All error messages on the page |
| Semantic      | `status-updates`     | Status changes are not announced to assistive technologies.                                           | 4.1.3             | Serious  |   |
| Semantic      | `hover-focus`        | Content triggered by hover or focus is inaccessible or non-dismissible.                               | 1.4.13            | Serious |   |
 -->
