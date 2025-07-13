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

Delnevo et al. "On the Interaction with Large Language Models for Web Accessibility: Implications and Challenges" (2024)
- **Contextual prompting**

 Othman et al. "Fostering websites accessibility: A case study on the use of the Large Language Models ChatGPT for automatic remediation" (2023)
- **ReAct prompting**

Huang et al. "ACCESS: Prompt Engineering for Automated Web Accessibility Violation Corrections" (2024)

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

``` @inproceedings{fathallah2025accessguru,
  title={AccessGuru: Leveraging LLMs to Detect and Correct Web Accessibility Violations in HTML Code},
  author={Fathallah, Nadeen and Hernández, Daniel and Staab, Steffen},
  booktitle={Proceedings of the 27th International ACM SIGACCESS Conference on Computers and Accessibility},
  year={2025},
  publisher={ACM}
}

---
## 📚 References

```bibtex
@inproceedings{DBLP:conf/ccnc/DelnevoAM24,
  author       = {Giovanni Delnevo and
                  Manuel Andruccioli and
                  Silvia Mirri},
  title        = {On the Interaction with Large Language Models for Web Accessibility:
                  Implications and Challenges},
  booktitle    = {21st {IEEE} Consumer Communications {\&} Networking Conference,
                  {CCNC} 2024, Las Vegas, NV, USA, January 6-9, 2024},
  pages        = {1--6},
  publisher    = {{IEEE}},
  year         = {2024},
  url          = {https://doi.org/10.1109/CCNC51664.2024.10454680},
  doi          = {10.1109/CCNC51664.2024.10454680},
  timestamp    = {Tue, 26 Mar 2024 22:14:36 +0100},
  biburl       = {https://dblp.org/rec/conf/ccnc/DelnevoAM24.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}

@inproceedings{DBLP:conf/petra/OthmanDJ23,
  author       = {Achraf Othman and
                  Amira Dhouib and
                  Aljazi Nasser Al Jabor},
  title        = {Fostering websites accessibility: {A} case study on the use of the
                  Large Language Models ChatGPT for automatic remediation},
  booktitle    = {Proceedings of the 16th International Conference on PErvasive Technologies
                  Related to Assistive Environments, {PETRA} 2023, Corfu, Greece, July
                  5-7, 2023},
  pages        = {707--713},
  publisher    = {{ACM}},
  year         = {2023},
  url          = {https://doi.org/10.1145/3594806.3596542},
  doi          = {10.1145/3594806.3596542},
  timestamp    = {Fri, 18 Aug 2023 08:45:12 +0200},
  biburl       = {https://dblp.org/rec/conf/petra/OthmanDJ23.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}

@article{DBLP:journals/corr/abs-2401-16450,
  author       = {Calista Huang and
                  Alyssa Ma and
                  Suchir Vyasamudri and
                  Eugenie Puype and
                  Sayem Kamal and
                  Juan Belza Garcia and
                  Salar Cheema and
                  Michael Lutz},
  title        = {{ACCESS:} Prompt Engineering for Automated Web Accessibility Violation
                  Corrections},
  journal      = {CoRR},
  volume       = {abs/2401.16450},
  year         = {2024},
  url          = {https://doi.org/10.48550/arXiv.2401.16450},
  doi          = {10.48550/ARXIV.2401.16450},
  eprinttype    = {arXiv},
  eprint       = {2401.16450},
  timestamp    = {Tue, 06 Feb 2024 14:15:49 +0100},
  biburl       = {https://dblp.org/rec/journals/corr/abs-2401-16450.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
