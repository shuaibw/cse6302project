# Taxonomy of Web Accessibility Violations

Each violation includes a **Rule ID**, **Description**, the corresponding **WCAG Guidelines** it violates, and **Impact**.

- **Syntactic Violations:**
- **Layout Violations:**
- **Semantic Violations:** These violations require manual review and are not reliably detected by automated tools like Wave or Playwright. 

## Semantic Violations Table

| **Category**           | **Rule ID**           | **Description**                                                                                       | **Guidelines**    |  
|-------------------------|-----------------------|-------------------------------------------------------------------------------------------------------|-------------------|
| Semantic      | `image-alt-not-descriptive`      | Inaccurate or misleading alternative text that fails to describe the purpose of the image.            | 1.1.1             |
| Semantic      | `multimedia-desc`    | Multimedia content lacks detailed transcripts or audio descriptions.                                  | 1.2.1, 1.2.3      |
| Semantic      | `lang-mismatch`      | Page language attribute does not match the actual language of the content.                            | 3.1.1             |
| Semantic      | `missing-lang-tag`   | Sections in different languages lack appropriate `lang` attributes.                                   | 3.1.2             |
| Semantic      | `unclear-link-text`  | Links fail to convey their purpose or are ambiguous.                                                  | 2.4.4, 2.4.9      |
| Semantic      | `button-label-not-clear`       | Buttons with unclear labels fail to specify their purpose.                                            | 2.5.3             |
| Semantic      | `form-label-not-meaningful`         | Forms have unclear or missing labels or instructions.                                                 | 3.3.2           
| Semantic Violations     | `ambiguous-heading`  | Headings are vague, repetitive, or fail to describe the content.                                      | 2.4.6, 2.4.10     |
| Semantic      | `incorrect-semantic-tag`    | Incorrect use of semantic elements like headings or regions.                                          | 1.3.1             |
| Semantic      | `landmark-structural-violation`    | Incorrect or ineffective use of ARIA landmarks or regions.                                            | 1.3.6           |
| Semantic      | `landmark-purpose-mismatch` | Content purpose does not align with its intended function.                                            | 1.3.6             |
| Semantic      | `sensory-instructions`| Instructions rely on sensory characteristics without alternatives.                                    | 1.3.3             |
| Semantic      | `error-messages`     | Errors are not clearly described, leaving users unable to fix them.                                   | 3.3.1             |
| Semantic      | `error-correction`   | No accessible suggestions for correcting input errors.                                                | 3.3.3             |
| Semantic      | `error-consistency`  | Error messages lack consistency or clarity across interactions.                                       | 3.3.4             |
| Semantic      | `status-updates`     | Status changes are not announced to assistive technologies.                                           | 4.1.3             |
| Semantic      | `hover-focus`        | Content triggered by hover or focus is inaccessible or non-dismissible.                               | 1.4.13            |

---

