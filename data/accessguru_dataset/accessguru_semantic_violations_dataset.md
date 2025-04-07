# Semantic Accessibility Violations Dataset

This table presents 55 semantic accessibility violations along with associated HTML and image context where applicable.

| # | Violation Type | Impact | Description | Affected HTML | Preview of the Web Page with Accessibility Violation |
|---|------------------|--------|-------------|-----------------------------|------------|
| 1 | `image-alt-not-descriptive` | Critical | Inaccurate or misleading alternative text that fails to describe the purpose of the image. | `<html lang="en"/> <img alt="ERCIM logo" src="/WAI/content-assets/wcag-act-rules/test-assets/shared/w3c-logo.png" /> </html/> <img alt="logo" src="/WAI/content-assets/wcag-act-rules/test-assets/shared/w3c-logo.png" />` | ![Img](https://www.w3.org/WAI/content-assets/wcag-act-rules/test-assets/shared/w3c-logo.png) |
| 2 | `image-alt-not-descriptive` | Critical | Inaccurate or misleading alternative text that fails to describe the purpose of the image. | `<html lang="en">      <svg aria-label="W3C" role="img" viewbox="0 0 512 512">      <path d="M108.4 0h23v22.8h21.2V0h23v69h-23V46h-21v23h-23.2M206 23h-20.3V0h63.7v23H229v46h-23M259.5 0h24.1l14.8 24.3L313.2 0h24.1v69h-23V34.8l-16.1 24.8l-16.1-24.8v34.2h-22.6M348.7 0h23v46.2h32.6V69h-55.6">   </path>      <path d="M107.6 471l-33-370.4h362.8l-33 370.2L255.7 512" fill="#e44d26">   </path>      <path d="M256 480.5V131H404.3L376 447" fill="#f16529">   </path>      <path d="M142 176.3h114v45.4h-64.2l4.2 46.5h60v45.3H154.4M156.4 336.3H202l3.2 36.3 50.8 13.6v47.4l-93.2-26" fill="#ebebeb">   </path>      <path d="M369.6 176.3H255.8v45.4h109.6M361.3 268.2H255.8v45.4h56l-5.3 59-50.7 13.6v47.2l93-25.8" fill="#fff">   </path>      </svg>      </html>` | ![Img](https://i.ibb.co/mFYM2Ft/image.png) |
| 3 | `image-alt-not-descriptive` | Critical | Inaccurate or misleading alternative text that fails to describe the purpose of the image. | `<!DOCTYPE html>          <html lang="en">          <head>          <meta charset="UTF-8">          <!-- Accessibility Violation Starts Here --">       <title> Canvas Image Example   </title>          </head>          <body>          <canvas aria-label="HTML 5 logo" height="48" id="logo" width="72">         </canvas>          <script>       const img = new Image(); img.src = &#x27;/WAI/content-assets/wcag-act-rules/test-assets/shared/w3c-logo.png&#x27;; img.onload = function() { const ctx = document.querySelector(&#x27;#logo&#x27;).getContext(&#x27;2d&#x27;); ctx.drawImage(img, 0, 0, 72, 48); }    </script>          </body>          </html> 
` | ![Img](https://i.ibb.co/BPkxx7z/screenshot.png) |
| 4 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `` | *(none)* |
| 5 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `` | *(none)* |
| 6 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `` | *(none)* |
| 7 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `` | *(none)* |
| 8 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `` | *(none)* |
| 9 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `` | *(none)* |
| 10 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `` | *(none)* |
| 11 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `` | *(none)* |
| 12 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `` | *(none)* |
| 13 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `` | *(none)* |
| 14 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `` | *(none)* |
| 15 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `` | *(none)* |
| 16 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `` | *(none)* |
| 17 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | `` | *(none)* |
| 18 | `missing-lang-tag` | Serious | Sections in different languages lack appropriate lang attributes. | `` | *(none)* |
| 19 | `missing-lang-tag` | Serious | Sections in different languages lack appropriate lang attributes. | `` | *(none)* |
| 20 | `missing-lang-tag` | Serious | Sections in different languages lack appropriate lang attributes. | `` | *(none)* |
| 21 | `missing-lang-tag` | Serious | Sections in different languages lack appropriate lang attributes. | `` | *(none)* |
| 22 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | `` | *(none)* |
| 23 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | `` | *(none)* |
| 24 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | `` | *(none)* |
| 25 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | `` | *(none)* |
| 26 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | `` | *(none)* |
| 27 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | `` | *(none)* |
| 28 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | `` | *(none)* |
| 29 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | `` | *(none)* |
| 30 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | `` | *(none)* |
| 31 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | `` | *(none)* |
| 32 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | `` | *(none)* |
| 33 | `form-label-mismatch` | Critical | Forms elements have unclear or incorrect labels. | `` | *(none)* |
| 34 | `form-label-mismatch` | Critical | Forms elements have unclear or incorrect labels. | `` | *(none)* |
| 35 | `form-label-mismatch` | Critical | Forms elements have unclear or incorrect labels. | `` | *(none)* |
| 36 | `form-label-mismatch` | Critical | Forms elements have unclear or incorrect labels. | `` | *(none)* |
| 37 | `form-label-mismatch` | Critical | Forms elements have unclear or incorrect labels. | `` | *(none)* |
| 38 | `ambiguous-heading` | Moderate | Headings are vague, repetitive, or fail to describe the content. | `` | *(none)* |
| 39 | `ambiguous-heading` | Moderate | Headings are vague, repetitive, or fail to describe the content. | `` | *(none)* |
| 40 | `ambiguous-heading` | Moderate | Headings are vague, repetitive, or fail to describe the content. | `` | *(none)* |
| 41 | `ambiguous-heading` | Moderate | Headings are vague, repetitive, or fail to describe the content. | `` | *(none)* |
| 42 | `page-title-not-descriptive` | Serious | Page title fails to describe the content or purpose of the page, making navigation difficult. | `` | *(none)* |
| 43 | `page-title-not-descriptive` | Serious | Page title fails to describe the content or purpose of the page, making navigation difficult. | `` | *(none)* |
| 44 | `page-title-not-descriptive` | Serious | Page title fails to describe the content or purpose of the page, making navigation difficult. | `` | *(none)* |
| 45 | `button-label-mismatch` | Critical | Buttons labels are unclear or fail to specify their purpose. | `` | ![Img](https://www.w3.org/WAI/content-assets/wcag-act-rules/test-assets/shared/search-icon.svg) |
| 46 | `button-label-mismatch` | Critical | Buttons labels are unclear or fail to specify their purpose. | `` | ![Img](https://www.w3.org/WAI/content-assets/wcag-act-rules/test-assets/shared/search-icon.svg) |
| 47 | `button-label-mismatch` | Critical | Buttons labels are unclear or fail to specify their purpose. | `` | ![Img](https://www.w3.org/WAI/content-assets/wcag-act-rules/test-assets/shared/search-icon.svg) |
| 48 | `button-label-mismatch` | Critical | Buttons labels are unclear or fail to specify their purpose. | `` | ![Img](https://www.w3.org/WAI/content-assets/wcag-act-rules/test-assets/shared/search-icon.svg) |
| 49 | `button-label-mismatch` | Critical | Buttons labels are unclear or fail to specify their purpose. | `` | *(none)* |
| 50 | `image-alt-not-descriptive` | Critical | Inaccurate or misleading alternative text that fails to describe the purpose of the image. | `` | ![Img](https://www.climaterealityproject.org/sites/default/files/graphblog-1.png) |
| 51 | `image-alt-not-descriptive` | Critical | Inaccurate or misleading alternative text that fails to describe the purpose of the image. | `` | ![Img](https://images.stockcake.com/public/b/7/a/b7a38663-0207-4222-932a-d25a576f5dd7_large/solar-power-generation-stockcake.jpg) |
| 52 | `image-alt-not-descriptive` | Critical | Inaccurate or misleading alternative text that fails to describe the purpose of the image. | `` | ![Img](https://thumbs.dreamstime.com/b/mental-health-infographic-diagram-chart-illustration-banner-presentation-has-managing-stress-meaning-purpose-staying-active-315756097.jpg) |
| 53 | `button-label-mismatch` | Critical | Buttons labels are unclear or fail to specify their purpose. | `` | *(none)* |
| 54 | `button-label-mismatch` | Critical | Buttons labels are unclear or fail to specify their purpose. | `` | *(none)* |
| 55 | `button-label-mismatch` | Critical | Buttons labels are unclear or fail to specify their purpose. | `` | *(none)* |
