## 🛡️ PyGuardIA - AI-Powered SAST tool ##
PyGuardIA is a Static Application Security Testing (SAST) tool. By combining __Bandit's__ deep code analysis with __LLM intelligence__, it provides automated vulnerability explanations and code patches. 

## 🚩 Features ##
- __Native Library Integration:__ Utilizes `bandit.core` directly to perform scans, eliminating risks of shell injection associated with system calls. 
- __Multi-Platform AI Engine:__ Toggle between __OpenAI GPT__ and __Google Gemini__ (by now) for vulnerability remediation.
- __Container-First Design:__ Optimized Docker Image for easy integration into any environment without local dependency. 

## ⚡Quick Start ##
Add this to your repository at `.github/workflows/security-scan.yml` to automatically audit your code on every push.

~~~
name: PyGuardIA Audit

on:
  push:
    branches: [ "main", "develop" ]
  pull_request:
    branches: [ "main" ]

jobs:
  pyguardia-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run PyGuardIA Scanner
        # OPENAI_API_KEY if using OpenAI, otherwise use GEMINI_API_KEY=${{ secrets.GEMINI_API_KEY }} and AI_PLATFORM="gemini"
        run: |
          docker run --rm \
            -e OPENAI_API_KEY=${{ secrets.OPENAI_API_KEY }} \
            -e SCAN_PATH="/github/workspace" \
            -e AI_PLATFORM="openai" \
            -v ${{ github.workspace }}:/github/workspace \
            pleskr011/pyguardia:latest
~~~

## 🛠️ Developer Configuration ##

If you prefer to run the tool locally:

__1. Clone the repository:__
~~~
Bash

git clone https://github.com/pleskr011/PyGuardIA.git
cd PyGuardIA
~~~
__2. Install dependencies:__
~~~
Bash

pip install -r requirements.txt
~~~
__3. Usage:__ The script accepts two main arguments:

- `--path`: The directory to scan (Default: `./src`).

- `--ai_platform`: The AI engine to use (`openai` or `gemini`).

~~~
Bash

python src/scanner.py --path ./my_project --ai_platform gemini
~~~
## 🔒 Security by Design (Development experience) ##

During development, this project identified potential __CWE-78 (OS Command Injection)__ risks when using the `subprocess` module.

To ensure maximum security, the tool was refactored to interface directly with the Bandit Core API. This prevents any external shell execution, making the scanner itself as secure as the code it audits.

## 🔮 Next steps: ##
- Adding more AI platforms, like Claude, Deepseek, and others.
- Unified code interface for managing multiple AI platforms
- Give tools to the AI so it can research about the found vulnerabilities, in order to improve its results.
- Support more languages
- Create a VSCode extension (maybe?)
