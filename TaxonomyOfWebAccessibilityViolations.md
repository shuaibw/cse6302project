# Taxonomy of Web Accessibility Violations

Each violation includes a **Rule ID**, **Description**, the corresponding **WCAG Guidelines** it violates, and **Impact**.

- **Syntactic Violations:** These occur when HTML code lacks proper structural elements or attributes required by accessibility standards. Examples include missing alt attributes for images or improperly structured tables, which hinder compliance with accessibility guidelines.
- **Layout Violations:** These relate to visual design and organization that do not meet accessibility standards, such as insufficient color contrast between text and background. These issues affect readability and usability for users, especially those with visual impairments.
- **Semantic Violations: We define semantic violations as the violations that involve the misuse or absence of meaningful content or attributes that provide contextual understanding. For instance, using nonsensical or placeholder text in alt attributes fails to convey the intended information to assistive technologies.**

## Semantic Violations Table

| **Category**           | **Rule ID**           | **Description**                                                                                       | **Guidelines**    | **Impact** | **Additional Context Needed**|
|-------------------------|-----------------------|-------------------------------------------------------------------------------------------------------|-------------------|-------------------|------------------|
| Semantic      | `image-alt-not-descriptive`      | Inaccurate or misleading alternative text that fails to describe the purpose of the image.            | 1.1.1             |  Critical | Image  |
| Semantic      | `video-captions-not-descriptive`    | Inaccurate video captions.                                 | 1.2.1, 1.2.3      | Critical  |  Video |
| Semantic      | `lang-mismatch`      | Page language attribute does not match the actual language of the content.                            | 3.1.1             | Serious  |   |
| Semantic      | `missing-lang-tag`   | Sections in different languages lack appropriate `lang` attributes.                                   | 3.1.2             |  Serious |   |
| Semantic      | `link-text-mismatch`  | Links fail to convey their purpose or are ambiguous.                                                  | 2.4.4, 2.4.9      | Serious  |   |
| Semantic      | `button-label-mismatch`       | Buttons labels are unclear or fail to specify their purpose.                                            | 2.5.3             |  Critical  |  |
| Semantic      | `form-label-mismatch`         | Forms elements have unclear or incorrect labels.                                                 | 3.3.2             |   Critical |Form context (e.g., surrounding text, instructions)|
| Semantic      | `ambiguous-heading`  | Headings are vague, repetitive, or fail to describe the content.                                      | 2.4.6, 2.4.10     |  Moderate  |   |
| Semantic      | `incorrect-semantic-tag`    | A non-semantic tag (e.g., `div` or `span`) is used instead of a proper semantic element (e.g., `header`, `nav`, `main`).                                      | 1.3.1             | Serious  |  Document structure (other headings, section context) |
| Semantic      | `landmark-structural-violation`    |  Landmarks or ARIA roles are misused, such as having multiple `main` elements, nesting landmarks, or failing to label multiple `nav` regions properly.                                         | 1.3.6           | Serious  |  |
| Semantic      | `landmark-purpose-mismatch` | A landmark or ARIA role does not match its actual purpose or placement, such as labeling a <nav> in the header as "Footer navigation."                                          | 1.3.6             | Serious  |  Document structure and context around the landmark  |
| Semantic      | `page-title-not-descriptive`      | Page title fails to describe the content or purpose of the page, making navigation difficult.           | 2.4.2             |  Serious | Page content and purpose  |

---


<!-- This is commented out.| Semantic      | `sensory-instructions`| Instructions rely on sensory characteristics without alternatives.                                    | 1.3.3             |  Serious |   |
| Semantic      | `error-messages`     | Errors are not clearly described, leaving users unable to fix them.                                   | 3.3.1             | Serious  |  Error context (e.g., input validation rules) |
| Semantic      | `error-correction`   | No accessible suggestions for correcting input errors.                                                | 3.3.3             | Serious  |  Error context and input requirements  |
| Semantic      | `error-consistency`  | Error messages lack consistency or clarity across interactions.                                       | 3.3.4             | Serious  |  All error messages on the page |
| Semantic      | `status-updates`     | Status changes are not announced to assistive technologies.                                           | 4.1.3             | Serious  |   |
| Semantic      | `hover-focus`        | Content triggered by hover or focus is inaccessible or non-dismissible.                               | 1.4.13            | Serious |   |
 -->
