import argparse
import json
import os
from bandit.core import manager

from ai_advisor import analyze_with_ai

def run_bandit(absolute_path):
    bandit_mgr = manager.BanditManager()
    bandit_mgr.discover_files([absolute_path])
    bandit_mgr.run_tests()

    results = bandit_mgr.get_issue_list()
    return results

def run_security_scan(target_path, ai_platform):
    print(f"🚀 Initializing security scanning in {target_path}...")
    absolute_path = os.path.abspath(target_path)

    if not os.path.exists(absolute_path):
        print(f"❌ {absolute_path} path doesn't exist.")
        return
    
    print(f"🔍 Scanning started at: {absolute_path} using {ai_platform}")

    results = run_bandit(absolute_path)
    
    # Bandit returns 1 if it finds vulnerabilities
    
    if results:
        print(f"⚠️ Found {len(results)} vulnerabilities.")
        vuln_data = [results.to_dict() for result in results]

        report = analyze_with_ai(vuln_data, ai_platform)
        print("\n--- AI Security Report ---\n")
        print(report)

        # Write to GitHub Step Summary if running in a CI
        if os.getenv('GITHUB_STEP_SUMMARY'):
            with open(os.getenv('GITHUB_STEP_SUMMARY'), 'a') as summary:
                summary.write(f"## 🛡️ PyGuardIA Analysis\n{report}")
    else:
        print("✅ No vulnerabilities found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default="./src", help="Path to scan for vulnerabilities (default: './src')")
    parser.add_argument("--ai_platform", default="gemini", choices=["gemini", "openai"], help="AI Platform to use ('gemini', 'openai')")
    args = parser.parse_args()
    run_security_scan(args.path, args.ai_platform)