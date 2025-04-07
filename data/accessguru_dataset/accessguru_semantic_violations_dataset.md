# Semantic Accessibility Violations Dataset

This table presents 55 semantic accessibility violations along with associated HTML and image context where applicable.

| # | Violation Type | Impact | Description | Affected HTML | Preview of the Web Page with Accessibility Violation |
|---|------------------|--------|-------------|-----------------------------|------------|
| 1 | `image-alt-not-descriptive` | Critical | Inaccurate or misleading alternative text that fails to describe the purpose of the image. | `<html lang="en"> <img alt="ERCIM logo" src="https://image.png" width="170" height="100"/> </html>` | ![Img](https://www.w3.org/WAI/content-assets/wcag-act-rules/test-assets/shared/w3c-logo.png) |
| 2 | `image-alt-not-descriptive` | Critical | Inaccurate or misleading alternative text that fails to describe the purpose of the image. | `<html lang="en"> <svg aria-label="W3C" r...` | ![Img](https://i.ibb.co/mFYM2Ft/image.png) |
| 3 | `image-alt-not-descriptive` | Critical | Inaccurate or misleading alternative text that fails to describe the purpose of the image. | `<html lang="en"> <canvas aria-label="HTM...` | ![Img](https://i.ibb.co/BPkxx7z/screenshot.png) |
| 4 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `<html lang="da"> <head> <title>ACT Rules...` | *(none)* |
| 5 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `<html lang="nl"> <head> <title>Gelukkig<...` | *(none)* |
| 6 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `<html lang="en"> <head> <title>Met de ki...` | *(none)* |
| 7 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `<html lang="nl"> <head> <title>Fireworks...` | *(none)* |
| 8 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `<html lang="nl"> <head> <title>Paris</ti...` | *(none)* |
| 9 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `<html lang="es"> <body> <article lang="d...` | *(none)* |
| 10 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `<html lang="en"> <body> <article lang="#...` | *(none)* |
| 11 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `<html lang="fr"> <body> <article lang=" ...` | *(none)* |
| 12 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `<html lang="es"> <body> <article lang="e...` | *(none)* |
| 13 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `<html lang="fr"> <body> <article lang="E...` | *(none)* |
| 14 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `<html lang="es"> <body> <article lang="e...` | *(none)* |
| 15 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `<html lang="en"> <body> <div lang="inval...` | *(none)* |
| 16 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `<html lang="en"> <body> <p lang="eng">I ...` | *(none)* |
| 17 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `<html lang="lb"> <body> <p lang="i-lux">...` | *(none)* |
| 18 | `missing-lang-tag` | Serious | Sections in different languages lack appropriate lang attributes. | `<html lang="en"> <head> <title>Dutch idi...` | *(none)* |
| 19 | `missing-lang-tag` | Serious | Sections in different languages lack appropriate lang attributes. | `<html lang="nl"> <head> <title>Met de ki...` | *(none)* |
| 20 | `missing-lang-tag` | Serious | Sections in different languages lack appropriate lang attributes. | `<html lang="fr"> <head> <title>Feu d'art...` | *(none)* |
| 21 | `missing-lang-tag` | Serious | Sections in different languages lack appropriate lang attributes. | `<html lang="fr"> <head> <title>Feu d'art...` | *(none)* |
| 22 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | `<html lang="en"> <head> <title>Failed Ex...` | *(none)* |
| 23 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | `<html lang="en"> <head> <title>Failed Ex...` | *(none)* |
| 24 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | `<html lang="en"> <head> <title>Failed Ex...` | *(none)* |
| 25 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | `<html lang="en"> <head> <title>Failed Ex...` | *(none)* |
| 26 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | `<html lang="en"> <head> <title>Failed Ex...` | *(none)* |
| 27 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | `<html lang="en"> <head> <title>Failed Ex...` | *(none)* |
| 28 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | `<html lang="en"> <head> <title>Failed Ex...` | *(none)* |
| 29 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | `<html lang="en"> <head> <title>Failed Ex...` | *(none)* |
| 30 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | `<html lang="en"> <head> <title>Failed Ex...` | *(none)* |
| 31 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | `<html lang="en"> <head> <title>Failed Ex...` | *(none)* |
| 32 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | `<html lang="en"> <head> <title>Failed Ex...` | *(none)* |
| 33 | `form-label-mismatch` | Critical | Forms elements have unclear or incorrect labels. | `<html lang="en"> <label>Menu<input id="f...` | *(none)* |
| 34 | `form-label-mismatch` | Critical | Forms elements have unclear or incorrect labels. | `<html lang="en"> <label for="fname">Menu...` | *(none)* |
| 35 | `form-label-mismatch` | Critical | Forms elements have unclear or incorrect labels. | `<html lang="en"> <p id="label_fname">Men...` | *(none)* |
| 36 | `form-label-mismatch` | Critical | Forms elements have unclear or incorrect labels. | `<html lang="en"> <fieldset> <h2 style="p...` | *(none)* |
| 37 | `form-label-mismatch` | Critical | Forms elements have unclear or incorrect labels. | `<html lang="en"> <span id="search" style...` | *(none)* |
| 38 | `ambiguous-heading` | Moderate | Headings are vague, repetitive, or fail to describe the content. | `<html lang="en"> <h1>Weather</h1> <p>We ...` | *(none)* |
| 39 | `ambiguous-heading` | Moderate | Headings are vague, repetitive, or fail to describe the content. | `<html lang="en"> <span aria-level="1" ro...` | *(none)* |
| 40 | `ambiguous-heading` | Moderate | Headings are vague, repetitive, or fail to describe the content. | `<html lang="en"> <span aria-level="1" ro...` | *(none)* |
| 41 | `ambiguous-heading` | Moderate | Headings are vague, repetitive, or fail to describe the content. | `<html lang="en"> <h1>Weather</h1> <p>We ...` | *(none)* |
| 42 | `page-title-not-descriptive` | Serious | Page title fails to describe the content or purpose of the page, making navigation difficult. | `<html lang="en"> <head> <title>Apple har...` | *(none)* |
| 43 | `page-title-not-descriptive` | Serious | Page title fails to describe the content or purpose of the page, making navigation difficult. | `<html lang="en"> <head> <title>First tit...` | *(none)* |
| 44 | `page-title-not-descriptive` | Serious | Page title fails to describe the content or purpose of the page, making navigation difficult. | `<html lang="en"> <head> <title>Universit...` | *(none)* |
| 45 | `button-label-mismatch` | Critical | Buttons labels are unclear or fail to specify their purpose. | `<html lang="en"> <head> <title>Passed Ex...` | ![Img](https://www.w3.org/WAI/content-assets/wcag-act-rules/test-assets/shared/search-icon.svg) |
| 46 | `button-label-mismatch` | Critical | Buttons labels are unclear or fail to specify their purpose. | `<html lang="en"> <head> <title>Passed Ex...` | ![Img](https://www.w3.org/WAI/content-assets/wcag-act-rules/test-assets/shared/search-icon.svg) |
| 47 | `button-label-mismatch` | Critical | Buttons labels are unclear or fail to specify their purpose. | `<html lang="en"> <head> <title>Passed Ex...` | ![Img](https://www.w3.org/WAI/content-assets/wcag-act-rules/test-assets/shared/search-icon.svg) |
| 48 | `button-label-mismatch` | Critical | Buttons labels are unclear or fail to specify their purpose. | `<html lang="en"> <head> <title>Passed Ex...` | ![Img](https://www.w3.org/WAI/content-assets/wcag-act-rules/test-assets/shared/search-icon.svg) |
| 49 | `button-label-mismatch` | Critical | Buttons labels are unclear or fail to specify their purpose. | `<button id="voiceSearchButton" class="se...` | *(none)* |
| 50 | `image-alt-not-descriptive` | Critical | Inaccurate or misleading alternative text that fails to describe the purpose of the image. | `<!DOCTYPE html> <html lang="en"> <head> ...` | ![Img](https://www.climaterealityproject.org/sites/default/files/graphblog-1.png) |
| 51 | `image-alt-not-descriptive` | Critical | Inaccurate or misleading alternative text that fails to describe the purpose of the image. | `<!DOCTYPE html> <html lang="en"> <head> ...` | ![Img](https://images.stockcake.com/public/b/7/a/b7a38663-0207-4222-932a-d25a576f5dd7_large/solar-power-generation-stockcake.jpg) |
| 52 | `image-alt-not-descriptive` | Critical | Inaccurate or misleading alternative text that fails to describe the purpose of the image. | `<!DOCTYPE html> <html lang="en"> <head> ...` | ![Img](https://thumbs.dreamstime.com/b/mental-health-infographic-diagram-chart-illustration-banner-presentation-has-managing-stress-meaning-purpose-staying-active-315756097.jpg) |
| 53 | `button-label-mismatch` | Critical | Buttons labels are unclear or fail to specify their purpose. | `<!DOCTYPE html> <html lang="en"> <head> ...` | *(none)* |
| 54 | `button-label-mismatch` | Critical | Buttons labels are unclear or fail to specify their purpose. | `<!DOCTYPE html> <html lang="en"> <head> ...` | *(none)* |
| 55 | `button-label-mismatch` | Critical | Buttons labels are unclear or fail to specify their purpose. | `<!DOCTYPE html> <html lang="en"> <head> ...` | *(none)* |
