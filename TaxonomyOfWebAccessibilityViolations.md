# Taxonomy of Web Accessibility Violations

Each violation includes a **Rule ID**, **Description**, the corresponding **WCAG Guidelines** it violates, and **Impact**.

- **Syntactic Violations:**
- **Layout Violations:**
- **Semantic Violations:** These violations require manual review and are not reliably detected by automated tools like Wave or Playwright. 

## Semantic Violations Table

| **Category**           | **Rule ID**           | **Description**                                                                                       | **Guidelines**    | **Impact** | **Additional Context Needed**|
|-------------------------|-----------------------|-------------------------------------------------------------------------------------------------------|-------------------|-------------------|------------------|
| Semantic      | `image-alt-not-descriptive`      | Inaccurate or misleading alternative text that fails to describe the purpose of the image.            | 1.1.1             |   | Image  |
| Semantic      | `video-captions-not-descriptive`    | Inaccurate video captions                                 | 1.2.1, 1.2.3      |   |  Video |
| Semantic      | `lang-mismatch`      | Page language attribute does not match the actual language of the content.                            | 3.1.1             |   |   |
| Semantic      | `missing-lang-tag`   | Sections in different languages lack appropriate `lang` attributes.                                   | 3.1.2             |   |   |
| Semantic      | `unclear-link-text`  | Links fail to convey their purpose or are ambiguous.                                                  | 2.4.4, 2.4.9      |   |   |
| Semantic      | `button-label-not-clear`       | Buttons with unclear labels fail to specify their purpose.                                            | 2.5.3             |    |  |
| Semantic      | `form-label-not-meaningful`         | Forms have unclear or missing labels or instructions.                                                 | 3.3.2             |    |Form context (e.g., surrounding text, instructions)|
| Semantic Violations     | `ambiguous-heading`  | Headings are vague, repetitive, or fail to describe the content.                                      | 2.4.6, 2.4.10     |   |   |
| Semantic      | `incorrect-semantic-tag`    | A non-semantic tag (e.g., `div` or `span`) is used instead of a proper semantic element (e.g., `header`, `nav`, `main`).                                      | 1.3.1             |   |   |
| Semantic      | `landmark-structural-violation`    |  Landmarks or ARIA roles are misused, such as having multiple `main` elements, nesting landmarks, or failing to label multiple `nav` regions properly.                                         | 1.3.6           |   |   |
| Semantic      | `landmark-purpose-mismatch` | A landmark or ARIA role does not match its actual purpose or placement, such as labeling a <nav> in the header as "Footer navigation."                                          | 1.3.6             |   |   |
| Semantic      | `sensory-instructions`| Instructions rely on sensory characteristics without alternatives.                                    | 1.3.3             |   |   |
| Semantic      | `error-messages`     | Errors are not clearly described, leaving users unable to fix them.                                   | 3.3.1             |   |   |
| Semantic      | `error-correction`   | No accessible suggestions for correcting input errors.                                                | 3.3.3             |   |   |
| Semantic      | `error-consistency`  | Error messages lack consistency or clarity across interactions.                                       | 3.3.4             |   |   |
| Semantic      | `status-updates`     | Status changes are not announced to assistive technologies.                                           | 4.1.3             |   |   |
| Semantic      | `hover-focus`        | Content triggered by hover or focus is inaccessible or non-dismissible.                               | 1.4.13            |   |   |

---

