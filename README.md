# AccessGuru: Leveraging LLMs to Detect and Correct Web Accessibility Violations in HTML Code


## Overview

**AccessGuru** is a novel system that combines large language models (LLMs) and accessibility testing tools to **automatically detect and correct web accessibility violations** in HTML code.

🔬 Contributions:

-  A taxonomy categorizing Web accessibility violations into **Syntactic**, **Semantic**, and **Layout** violations
-  A benchmark dataset of **3,500 real-world violations** across **112 types**
-  A modular pipeline:
  - `AccessGuruDetect`: Detect violations (Axe-Playwright + LLM)
  - `AccessGuruCorrect`: Generate corrections using LLM prompting strategies



## 📁 Repository Structure



## 📊 Dataset
- 3,500 annotated HTML violations
- 112 distinct types
- Sourced from 448 real-world web pages across domains (health, news, e-commerce, etc.)


## 📦 Baselines 
Reproducible baseline implementations:

- **Zero-shot prompting**

Delnevo, Giovanni, Manuel Andruccioli, and Silvia Mirri. "On the interaction with large language models for web accessibility: Implications and challenges." 2024 IEEE 21st Consumer Communications & Networking Conference (CCNC). IEEE, 2024.

- **Contextual prompting**

Othman, Achraf, Amira Dhouib, and Aljazi Nasser Al Jabor. "Fostering websites accessibility: A case study on the use of the Large Language Models ChatGPT for automatic remediation." Proceedings of the 16th international conference on pervasive technologies related to assistive environments. 2023.

- **ReAct prompting**

Huang, Calista, et al. "Access: Prompt engineering for automated web accessibility violation corrections." arXiv preprint arXiv:2401.16450 (2024).

## 👩‍💻 Human Evaluation
This repository includes a developer study to compare LLM-generated accessibility corrections with human-written ones. We evaluated 55 semantic violations using:
- Manual expert annotations based on WCAG 2.1
- Sentence-BERT semantic similarity with developer-generated fixes

📋 You can contribute to our ongoing evaluation study by participating in a short survey and reviewing a small set of HTML accessibility corrections. 

Participate in the Evaluation Survey
(https://surveyjs.io/published?id=c2ebd794-0b9d-4af2-a4ab-79c5ddb6c509)

Your feedback will support future benchmarking and the design of more effective accessibility correction systems.



## 🧪 Results



## 📬 Contact

For inquiries, feel free to contact:
nadeen.fathallah@ki.uni-stuttgart.de



## 📜 License

[![CC BY 4.0 License](https://licensebuttons.net/l/by/4.0/88x31.png)](https://creativecommons.org/licenses/by/4.0/)  
The AccessGuru dataset is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

 Code under this repo is licensed under a MIT License.


## 📄 Citation

If you find this work useful, please consider citing our paper:

```
@inproceedings{fathallah2025accessguru,
  title={AccessGuru: Leveraging LLMs to Detect and Correct Web Accessibility Violations in HTML Code},
  author={Fathallah, Nadeen and Hernández, Daniel and Staab, Steffen},
  booktitle={Proceedings of the 27th International ACM SIGACCESS Conference on Computers and Accessibility},
  year={2025},
  publisher={ACM}
}

