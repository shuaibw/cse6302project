# Semantic Accessibility Violations Dataset

This table presents 55 semantic accessibility violations along with associated HTML and image context where applicable.

| # | Violation Type | Impact | Description | Affected HTML | Preview of the Web Page with Accessibility Violation |
|---|------------------|--------|-------------|-----------------------------|------------|
| 1 | `image-alt-not-descriptive` | Critical | Inaccurate or misleading alternative text that fails to describe the purpose of the image. |   <pre><code><html lang="en"/>&#10;<img alt="ERCIM logo" src="w3c-logo.png" />&#10;</html/></code></pre>   | ![Img](https://www.w3.org/WAI/content-assets/wcag-act-rules/test-assets/shared/w3c-logo.png) |
| 2 | `image-alt-not-descriptive` | Critical | Inaccurate or misleading alternative text that fails to describe the purpose of the image. |  ` <html lang="en"> &#10; <svg aria-label="W3C" role="img" viewbox="0 0 512 512"> &#10; <path d="M108.4 0h23v22.8h21.2V0h23v69h-23V46h-21v23h-23.2M206 23h-20.3V0h63.7v23H229v46h-23M259.5 0h24.1l14.8 24.3L313.2 0h24.1v69h-23V34.8l-16.1 24.8l-16.1-24.8v34.2h-22.6M348.7 0h23v46.2h32.6V69h-55.6"></path> &#10; <path d="M107.6 471l-33-370.4h362.8l-33 370.2L255.7 512" fill="#e44d26"></path> &#10; <path d="M256 480.5V131H404.3L376 447" fill="#f16529"></path> &#10; <path d="M142 176.3h114v45.4h-64.2l4.2 46.5h60v45.3H154.4M156.4 336.3H202l3.2 36.3 50.8 13.6v47.4l-93.2-26" fill="#ebebeb"></path> &#10; <path d="M369.6 176.3H255.8v45.4h109.6M361.3 268.2H255.8v45.4h56l-5.3 59-50.7 13.6v47.2l93-25.8" fill="#fff"></path> &#10; </svg> &#10; </html>` | ![Img](https://i.ibb.co/mFYM2Ft/image.png) |
| 3 | `image-alt-not-descriptive` | Critical | Inaccurate or misleading alternative text that fails to describe the purpose of the image. | <pre><code> <!DOCTYPE html>  &#10;  &#10; <html lang="en"> &#10;  &#10;  <head> &#10;  &#10;  <meta charset="UTF-8">  &#10;  &#10; <!-- Accessibility Violation Starts Here --">  &#10; <title> Canvas Image Example</title>  &#10;  &#10; </head>  &#10;  &#10; <body>  &#10;  &#10; <canvas aria-label="HTML 5 logo" height="48" id="logo" width="72"> &#10;  &#10; </canvas>  &#10;  &#10; <script>  &#10;  &#10; const img = new Image(); img.src = &#x27;/WAI/content-assets/wcag-act-rules/test-assets/shared/w3c-logo.png&#x27;; img.onload = function() { const ctx = document.querySelector(&#x27;#logo&#x27;).getContext(&#x27;2d&#x27;); ctx.drawImage(img, 0, 0, 72, 48); } </script>  &#10;  &#10; </body>  &#10;  &#10; </html> 
        </code></pre> | ![Img](https://i.ibb.co/BPkxx7z/screenshot.png) |
| 4 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | <pre><code><!-- Accessibility Violation Starts Here --">  &#10; <html lang="da"> &#10; <head> &#10; <title>ACT Rules Format 1.0 - Abstract</title> &#10; </head> &#10; <body> &#10; <p> &#10; The Accessibility Conformance Testing (ACT) Rules Format 1.0 defines a format for writing accessibility test &#10; rules. These test rules can be used for developing automated testing tools and manual testing methodologies. It &#10; provides a common format that allows any party involved in accessibility testing to document and share their &#10; testing procedures in a robust and understandable manner. This enables transparency and harmonization of testing &#10; methods, including methods implemented by accessibility test tools. &#10; </p> &#10; </body> &#10; </html>

    
    </code></pre> | *(none)* |
| 5 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | <pre><code>   <!-- Accessibility Violation Starts Here --">             &#10; <html lang="en"> &#10; <head> &#10; <title>Met de kippen op stok</title> &#10; </head> &#10; <body> &#10; <blockquote> &#10; <p>"Hij ging met de kippen op stok"</p> &#10; </blockquote> &#10; <p lang="en"> &#10; This Dutch phrase literally translates into " &#10; He went to roost with the chickens", but it means  &#10; that he went to bed early. &#10; </p> &#10; </body> &#10; </html>
    </code></pre>
       <!-- Accessibility Violation Starts Here --">                 &#10; <html lang="nl"> &#10; <head> &#10; <title>Happy</title> &#10; </head> &#10; <body> &#10;  &#10; <p>The Dutch word  &#10;  <!-- Accessibility Violation Starts Here --">  &#10; "gelukkig" has no equivalent in English.</p> &#10; </body> &#10; </html>

    </code></pre> | *(none)* |
| 6 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | <pre><code> <!-- Accessibility Violation Starts Here --">                 &#10; <html lang="nl"> &#10; <head> &#10; <title>Happy</title> &#10; </head> &#10; <body> &#10;  &#10; <p>The Dutch word  &#10;  <!-- Accessibility Violation Starts Here --">  &#10; "gelukkig" has no equivalent in English.</p> &#10; </body> &#10; </html>
    </code></pre> | *(none)* |
| 7 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | <pre><code><!-- Accessibility Violation Starts Here --">   &#10; <html lang="nl"> &#10; <head> &#10; <title>Fireworks over Paris</title> &#10; </head> &#10; <body> &#10; <img alt="Fireworks over Paris"  &#10; src="/WAI/content-assets/wcag-act-rules/test-assets/shared/fireworks.jpg"/> &#10; <p lang="nl"> &#10; Gelukkig nieuwjaar! &#10; </p> &#10; </body> &#10; </html> &#10; 

    </code></pre>
 | *(none)* |
| 8 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | <pre><code><!-- Accessibility Violation Starts Here --">  &#10; <html lang="nl"> &#10; <head> &#10; <title>Paris</title> &#10; </head> &#10; <body> &#10; <img aria-labelledby="caption" src="https://www.bvjhostelparis.com/wp-content/uploads/2017/07/PARIS-FIRE-WORKS.jpg"/> &#10; <p hidden="" id="caption" lang="en"> &#10; Fireworks over Paris! &#10; </p> &#10; </body> &#10; </html>

    </code></pre>
 | *(none)* |
| 9 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | <pre><code><!-- Accessibility Violation Starts Here --">   &#10; <html lang="es"> &#10; <head> &#10; <title> Stranddorp </title> &#10; </head> &#10; <body> &#10; <article lang="dutch"> &#10; Zij liepen een vreemde Tiki bar binnen, aan de rand van een dorpje aan het strand. &#10; </article> &#10; </body> &#10; </html>

    </code></pre>
 | *(none)* |
| 10 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | <pre><code><html lang="en"> &#10; <body> &#10; <!-- Accessibility Violation Starts Here --">  &#10; <article lang="#!"> &#10; They wandered into a strange Tiki bar on the edge of the  &#10; small beach town. &#10; </article> &#10; </body> &#10; </html>

    </code></pre>
 | *(none)* |
| 11 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | <pre><code> | *(none)* |
| 12 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | <pre><code> | *(none)* |
| 13 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | <pre><code> | *(none)* |
| 14 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | <pre><code> | *(none)* |
| 15 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | <pre><code> | *(none)* |
| 16 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | <pre><code> | *(none)* |
| 17 | `lang-mismatch` | Serious | Page language attribute does not match the actual language of the content. | <pre><code> | *(none)* |
| 18 | `missing-lang-tag` | Serious | Sections in different languages lack appropriate lang attributes. | <pre><code> | *(none)* |
| 19 | `missing-lang-tag` | Serious | Sections in different languages lack appropriate lang attributes. | <pre><code> | *(none)* |
| 20 | `missing-lang-tag` | Serious | Sections in different languages lack appropriate lang attributes. | <pre><code> | *(none)* |
| 21 | `missing-lang-tag` | Serious | Sections in different languages lack appropriate lang attributes. | <pre><code> | *(none)* |
| 22 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | <pre><code> | *(none)* |
| 23 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | <pre><code> | *(none)* |
| 24 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | <pre><code> | *(none)* |
| 25 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | <pre><code> | *(none)* |
| 26 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | <pre><code> | *(none)* |
| 27 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | <pre><code> | *(none)* |
| 28 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | <pre><code> | *(none)* |
| 29 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | <pre><code> | *(none)* |
| 30 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | <pre><code> | *(none)* |
| 31 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | <pre><code> | *(none)* |
| 32 | `link-text-mismatch` | Serious | Links fail to convey their purpose or are ambiguous. | <pre><code> | *(none)* |
| 33 | `form-label-mismatch` | Critical | Forms elements have unclear or incorrect labels. | <pre><code> | *(none)* |
| 34 | `form-label-mismatch` | Critical | Forms elements have unclear or incorrect labels. | <pre><code> | *(none)* |
| 35 | `form-label-mismatch` | Critical | Forms elements have unclear or incorrect labels. | <pre><code> | *(none)* |
| 36 | `form-label-mismatch` | Critical | Forms elements have unclear or incorrect labels. | <pre><code> | *(none)* |
| 37 | `form-label-mismatch` | Critical | Forms elements have unclear or incorrect labels. | <pre><code> | *(none)* |
| 38 | `ambiguous-heading` | Moderate | Headings are vague, repetitive, or fail to describe the content. | <pre><code> | *(none)* |
| 39 | `ambiguous-heading` | Moderate | Headings are vague, repetitive, or fail to describe the content. | <pre><code> | *(none)* |
| 40 | `ambiguous-heading` | Moderate | Headings are vague, repetitive, or fail to describe the content. | <pre><code> | *(none)* |
| 41 | `ambiguous-heading` | Moderate | Headings are vague, repetitive, or fail to describe the content. | <pre><code> | *(none)* |
| 42 | `page-title-not-descriptive` | Serious | Page title fails to describe the content or purpose of the page, making navigation difficult. | <pre><code> | *(none)* |
| 43 | `page-title-not-descriptive` | Serious | Page title fails to describe the content or purpose of the page, making navigation difficult. | <pre><code> | *(none)* |
| 44 | `page-title-not-descriptive` | Serious | Page title fails to describe the content or purpose of the page, making navigation difficult. | <pre><code> | *(none)* |
| 45 | `button-label-mismatch` | Critical | Buttons labels are unclear or fail to specify their purpose. | <pre><code> | ![Img](https://www.w3.org/WAI/content-assets/wcag-act-rules/test-assets/shared/search-icon.svg) |
| 46 | `button-label-mismatch` | Critical | Buttons labels are unclear or fail to specify their purpose. | <pre><code> | ![Img](https://www.w3.org/WAI/content-assets/wcag-act-rules/test-assets/shared/search-icon.svg) |
| 47 | `button-label-mismatch` | Critical | Buttons labels are unclear or fail to specify their purpose. | <pre><code> | ![Img](https://www.w3.org/WAI/content-assets/wcag-act-rules/test-assets/shared/search-icon.svg) |
| 48 | `button-label-mismatch` | Critical | Buttons labels are unclear or fail to specify their purpose. | <pre><code> | ![Img](https://www.w3.org/WAI/content-assets/wcag-act-rules/test-assets/shared/search-icon.svg) |
| 49 | `button-label-mismatch` | Critical | Buttons labels are unclear or fail to specify their purpose. | <pre><code> | *(none)* |
| 50 | `image-alt-not-descriptive` | Critical | Inaccurate or misleading alternative text that fails to describe the purpose of the image. | <pre><code> | ![Img](https://www.climaterealityproject.org/sites/default/files/graphblog-1.png) |
| 51 | `image-alt-not-descriptive` | Critical | Inaccurate or misleading alternative text that fails to describe the purpose of the image. | <pre><code> | ![Img](https://images.stockcake.com/public/b/7/a/b7a38663-0207-4222-932a-d25a576f5dd7_large/solar-power-generation-stockcake.jpg) |
| 52 | `image-alt-not-descriptive` | Critical | Inaccurate or misleading alternative text that fails to describe the purpose of the image. | <pre><code> | ![Img](https://thumbs.dreamstime.com/b/mental-health-infographic-diagram-chart-illustration-banner-presentation-has-managing-stress-meaning-purpose-staying-active-315756097.jpg) |
| 53 | `button-label-mismatch` | Critical | Buttons labels are unclear or fail to specify their purpose. | <pre><code> | *(none)* |
| 54 | `button-label-mismatch` | Critical | Buttons labels are unclear or fail to specify their purpose. | <pre><code> | *(none)* |
| 55 | `button-label-mismatch` | Critical | Buttons labels are unclear or fail to specify their purpose. | <pre><code> | *(none)* |
