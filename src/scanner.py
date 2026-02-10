import argparse
import json
import os
import sys
from bandit.core import manager
from bandit.core import config as b_config

from ai_advisor import analyze_with_ai

def run_bandit(absolute_path):
    cfg = b_config.BanditConfig()
    bandit_mgr = manager.BanditManager(cfg, agg_type='grouped')
    bandit_mgr.discover_files([absolute_path], recursive=True)
    bandit_mgr.run_tests()
    # Get the list of Issue objects found by Bandit
    issues = bandit_mgr.get_issue_list()
    return issues

def run_security_scan(target_path, ai_platform):
    print(f"🚀 Initializing security scanning in {target_path}...")
    absolute_path = os.path.abspath(target_path)

    if not os.path.exists(absolute_path):
        print(f"❌ {absolute_path} path doesn't exist.")
        sys.exit(1)
    
    print(f"🔍 Scanning started at: {absolute_path} using {ai_platform}")

    results = run_bandit(absolute_path)
    
    # Bandit returns 1 if it finds vulnerabilities
    
    if results:
        print(f"⚠️ Found {len(results)} vulnerabilities.")
        vuln_data = [result.as_dict() for result in results]
        json_vuln_data = json.dumps(vuln_data, indent=2)
        print(f"Analyzing vulnerabilities with AI platform: {ai_platform}...")
        report = analyze_with_ai(json_vuln_data, ai_platform)
        print("\n--- AI Security Report ---\n")
        print(report)

        # Write to GitHub Step Summary if running in a CI
        summary_path = os.getenv('GITHUB_STEP_SUMMARY')
        if summary_path:
            try:
                with open(summary_path, 'a', encoding='utf-8') as f:
                    f.write(f"## 🛡️ PyGuardIA Analysis\n{report}")
                print(f"✅ PyGuardIA report written to Github Step Summary.")
            except Exception as e:
                print(f"❌ Error writing to Github Step Summary: {e}")
        else:
            print("⚠️ GITHUB_STEP_SUMMARY environment variable not set, skipping visual report.")
    else:
        print("✅ No vulnerabilities found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default="./src", help="Path to scan for vulnerabilities (default: './src')")
    parser.add_argument("--ai_platform", default="gemini", choices=["gemini", "openai"], help="AI Platform to use ('gemini', 'openai')")
    args = parser.parse_args()
    run_security_scan(args.path, args.ai_platform)