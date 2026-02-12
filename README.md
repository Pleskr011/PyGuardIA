## 🛡️ PyGuardIA - AI-Powered SAST tool ##
PyGuardIA is a Static Application Security Testing (SAST) tool. By combining __Bandit's__ deep code analysis with __LLM intelligence__, it provides automated vulnerability explanations and code patches. 

## 🚩 Features ##
- __Native Library Integration:__ Utilizes `bandit.core` directly to perform scans, eliminating risks of shell injection associated with system calls. 
- __Multi-Platform AI Engine:__ Toggle between __OpenAI GPT__ and __Google Gemini__ (by now) for vulnerability remediation.
- __Container-First Design:__ Optimized Docker Image for easy integration into any environment without local dependency. 
- __Markdown Summary in Github Actions:__ Creates a Markdown report (in the Actions tab -> Workflow Run) with explained vulnerabilities and a Secure Code Patch alternative.

## ⚡Quick Start ##
Add this to your repository at `.github/workflows/security-scan.yml` to automatically audit your code on every push or pull request.

~~~ YAML
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
      #AI_PLATFORM must be "gemini" or "openai"
        run: |
          chmod 666 ${{ github.step_summary }}
          docker run --rm \
            -e AI_API_KEY=${{ secrets.YOUR_API_KEY }} \
            -e SCAN_PATH="/github/workspace" \
            -e AI_PLATFORM="openai" \
            -e GITHUB_STEP_SUMMARY="/github/workflow/summary.md" \
            -v ${{ github.workspace }}:/github/workspace \
            -v ${{ github.step_summary }}:/github/workflow/summary.md \
            pleskr011/pyguardia:latest
~~~

## 🛠️ Developer Configuration ##

If you prefer to run the tool locally:

__1. Clone the repository:__
~~~Bash
git clone https://github.com/pleskr011/PyGuardIA.git
cd PyGuardIA
~~~
__2. Install dependencies:__
~~~Bash
pip install -r requirements.txt
~~~
__3. Add environment secrets:__ Create a .env file with your `AI_API_KEY` inside.

__4. Usage:__ The script accepts two main arguments:

- `--path`: The directory to scan (Default: `./src`).

- `--ai_platform`: The AI engine to use (`openai` or `gemini`).

~~~Bash
python src/scanner.py --path ./my_project --ai_platform gemini
~~~
## 🔒 Security by Design (Development experience) ##

During development, this project identified potential __CWE-78 (OS Command Injection)__ risks when using the `subprocess` module.

To ensure maximum security, the tool was refactored to interface directly with the Bandit Core API. This prevents any external shell execution, making the scanner itself as secure as the code it audits.

## 🔮 Next steps: ##
- Adding more AI platforms.
- Unified code interface for managing multiple AI platforms
- Support more languages
- Option to scan commits instead of all the repository with every push. 
