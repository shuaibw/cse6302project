# AccessGuru: Leveraging LLMs to Detect and Correct Web Accessibility Violations in HTML Code


## Overview

**AccessGuru** is a novel system that combines large language models (LLMs) and accessibility testing tools to **automatically detect and correct web accessibility violations** in HTML code.

🔬 Contributions:

-  A taxonomy categorizing Web accessibility violations into **Syntactic**, **Semantic**, and **Layout** violations
-  A benchmark dataset of **3,500 real-world violations** across **112 types**
-  A modular pipeline:
  - `AccessGuruDetect`: Detect violations (Axe-Playwright + LLM)
  - `AccessGuruCorrect`: Generate corrections using LLM prompting strategies

<p align="center">
  <img src="data/accessguru_dataset/accessguru_semantic_violations_sampled_dataset_supp_material/detect.png" alt="Overview of the AccessGuru Detection Module. Given a raw HTML document (left), the detection module applies two detectors: (1) a syntax and layout detector based on the Axe-Playwright accessibility testing engine and (2) an LLM-based semantic detector. The module outputs a set of detected accessibility violations (right)." width="700"/>
</p>

<p align="center"><b>Figure 1:</b> Overview of the AccessGuru Detection Module. Given a raw HTML document (left), the detection module applies two detectors: (1) a syntax and layout detector based on the Axe-Playwright accessibility testing engine and (2) an LLM-based semantic detector. The module outputs a set of detected accessibility violations (right).</p>

<p align="center">
  <img src="data/accessguru_dataset/accessguru_semantic_violations_sampled_dataset_supp_material/fig1.png" alt="Overview of AccessGuru's correction module: For each Web accessibility violation $v$ detected by \method \emph{Detect}, the LLM is prompted to generate the corrected code. The generated code is assigned a violation score; if the violation score remains above zero, corrective re-prompting is applied to improve the response further." width="700"/>
</p>

<p align="center"><b>Figure 2:</b> Overview of AccessGuru's correction module: For each Web accessibility violation detected by AccessGuru Detection Module, the LLM is prompted to generate the corrected code. The generated code is assigned a violation score; if the violation score remains above zero, corrective re-prompting is applied to improve the response further.</p>

## 📁 Repository Structure



## 📊 Dataset
- 3,500 annotated HTML violations
- 112 distinct types
- Sourced from 448 real-world web pages across domains (health, news, e-commerce, etc.)

### Dataset Summary
### Dataset Access
### Dataset Structure 

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

| Method                          | Model          | Avg. Violation Score Decrease (Our Dataset, Size=250) | # Corrected Violations (Our Dataset, Size=250) | Avg. Violation Score Decrease (Huang et al. Dataset, Size=171) | # Corrected Violations (Huang et al. Dataset, Size=171) |
| ------------------------------- | -------------- | ------------------- | -------------- | --------------------------- | ---------------------- |
| Contextual Prompting            | GPT-4          | 0.46                | 123            | 0.42                        | 86                     |
| ReAct Prompting                 | GPT-4          | 0.50                | 141            | 0.48                        | 91                     |
| Zero-shot Prompting             | GPT-4          | 0.19                | 43             | 0.12                        | 19                     |
| **AccessGuru (w/o reprompting)** | GPT-4          | *0.72*              | *184*          | *0.67*                      | *119*                  |
| **AccessGuru (Ours)**           | **GPT-4**      | **0.84**            | **204**        | **0.83**                    | **141**                |
| Contextual Prompting            | Mistral-7B     | 0.12                | 44             | 0.27                        | 62                     |
| ReAct Prompting                 | Mistral-7B     | 0.13                | 45             | 0.26                        | 48                     |
| Zero-shot Prompting             | Mistral-7B     | 0.05                | 10             | 0.002                       | 2                      |
| **AccessGuru (w/o reprompting)** | Mistral-7B     | *0.50*              | *162*          | *0.51*                      | *110*                  |
| **AccessGuru (Ours)**           | **Mistral-7B** | **0.82**            | **200**        | **0.79**                    | **147**                |
| Contextual Prompting            | Qwen2.5        | 0.41                | 121            | 0.39                        | 77                     |
| ReAct Prompting                 | Qwen2.5        | 0.44                | 130            | 0.37                        | 71                     |
| Zero-shot Prompting             | Qwen2.5        | 0.14                | 54             | 0.19                        | 49                     |
| **AccessGuru (no reprompting)** | Qwen2.5        | *0.49*              | *153*          | *0.52*                      | *103*                  |
| **AccessGuru (Ours)**           | **Qwen2.5**    | **0.74**            | **183**        | **0.75**                    | **126**                |

<p align="center"><b>Table 1:</b> Comparison of the decrease in violation score and the number of corrected accessibility violations for syntax & layout violations on our dataset and the dataset from Huang et al. Dataset</p>


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

