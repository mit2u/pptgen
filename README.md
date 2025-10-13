<p align="center">
    <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" align="center" width="30%">
</p>
<p align="center"><h1 align="center">PPTGEN</h1></p>
<p align="center">
	<em><code>❯ REPLACE-ME</code></em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/mit2u/pptgen?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/mit2u/pptgen?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/mit2u/pptgen?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/mit2u/pptgen?style=default&color=0080ff" alt="repo-language-count">
</p>
<p align="center"><!-- default option, no dependency badges. -->
</p>
<p align="center">
	<!-- default option, no dependency badges. -->
</p>
<br>

##  Table of Contents


- [ Project Structure](#-project-structure)
  - [ Project Index](#-project-index)
- [ Getting Started](#-getting-started)
  - [ Prerequisites](#-prerequisites)
  - [ Installation](#-installation)
  - [ Usage](#-usage)
  - [ Testing](#-testing)

---


##  Project Structure

```sh
└── pptgen/
    ├── 1.pptx
    ├── 16.pptx
    ├── 23.pptx
    ├── 25.pptx
    ├── Dockerfile
    ├── README.Docker.md
    ├── compose.yaml
    ├── core
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── decorators.py
    │   ├── migrations
    │   ├── models.py
    │   ├── nlp_models.py
    │   ├── rest.py
    │   ├── routers.py
    │   ├── serializers.py
    │   ├── settings.py
    │   ├── urls.py
    │   ├── utils.py
    │   └── wsgi.py
    ├── manage.py
    └── requirements.txt
```



##  Getting Started

###  Prerequisites

Before getting started with pptgen, ensure your runtime environment meets the following requirements:

- **Programming Language:** Python
- **Package Manager:** Pip
- **Container Runtime:** Docker

### Usage

Add GEMINI_API_KEY=XXXXX in .env file
Modify Models in settings.py

Login through http://domain/api-auth/login/?next=/

Later use http://domain/topic-submit/ for submitting the topic

Previous Templates can be found in http://domain/slides/

###  Installation

Install pptgen using one of the following methods:



**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ pip install -r requirements.txt
```


**Using `docker`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Docker-2CA5E0.svg?style={badge_style}&logo=docker&logoColor=white" />](https://www.docker.com/)

```sh
❯ docker build -t mit2u/pptgen .
```




###  Usage
Run pptgen using the following command:
**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ python {entrypoint}
```


**Using `docker`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Docker-2CA5E0.svg?style={badge_style}&logo=docker&logoColor=white" />](https://www.docker.com/)

```sh
❯ docker run -it {image_name}
```





<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://github.com{/mit2u/pptgen/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=mit2u/pptgen">
   </a>
</p>
</details>


