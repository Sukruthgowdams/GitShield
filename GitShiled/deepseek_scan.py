import os
import re
from mistralai.client import MistralClient

# Get API key from environment variable
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("❌ MISTRAL_API_KEY is not set! Please export it before running.")

# Initialize Mistral AI Client
client = MistralClient(api_key=api_key)

# Regex pattern to detect API keys (adjust as needed)
API_KEY_PATTERNS = [
    r'(?i)(API_KEY|AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY|password)\s*=\s*[\'"]([^\'"]+)[\'"]',
    r'(?i)(ghp_[a-zA-Z0-9]{36})',  # GitHub Personal Access Tokens
    r'(?i)(sk-[a-zA-Z0-9]{32,})',  # OpenAI API keys
    r'(?i)(AKIA[0-9A-Z]{16})',     # AWS Access Key IDs
    r'(?i)([0-9a-zA-Z+/]{40})',    # Generic 40-character keys (e.g., some API keys)
    r'(?i)(password|passwd|pwd)\s*=\s*[\'"]([^\'"]+)[\'"]'  # Passwords
]

def mask_api_keys(code):
    """Mask detected API keys in the code before processing."""
    for pattern in API_KEY_PATTERNS:
        code = re.sub(pattern, lambda match: f"{match.group(1)} = \"********\"", code)
    return code

def scan_code(file_path):
    """Analyzes code for security vulnerabilities using Mistral AI."""
    with open(file_path, "r", encoding="utf-8") as f:
        code_lines = f.readlines()

    masked_code = mask_api_keys("".join(code_lines))  # Mask API keys

    # AI Security Analysis Prompt
    prompt = f"""
    You are a cybersecurity AI assistant. Analyze the following code for security vulnerabilities.
    
    CODE:
    {masked_code[:400]}  # Only process the first 400 characters

    Provide output in this format:
    ---
    DETECTED ISSUES:
    [List security vulnerabilities]

    RECOMMENDED FIXES:
    [Suggest fixes]
    ---
    """

    response = client.chat(
        model="mistral-large-latest",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content.strip()

def check_repo_for_vulnerabilities():
    """Scans all code files in the repo before Git push."""
    issues_found = []
    api_keys_detected = False  # Flag to track if API keys are detected
    files_with_api_keys = []   # List to store files with API keys

    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith((".py", ".js", ".ts", ".java", ".cpp", ".c", ".go" , ".txt", ".json")):
                file_path = os.path.join(root, file)

                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                result = scan_code(file_path)

                if "DETECTED ISSUES" in result:
                    issue_details = []
                    for i, line in enumerate(lines, start=1):
                        if "eval(" in line:
                            issue_details.append(f"❌ **Line {i}**: Insecure `eval()` usage.")
                        if "input(" in line:
                            issue_details.append(f"❌ **Line {i}**: Unvalidated user input.")

                        # Check for API keys & Mask them
                        for pattern in API_KEY_PATTERNS:
                            if re.search(pattern, line):
                                issue_details.append(f"⚠️ **Line {i}**: API key detected and masked.")
                                api_keys_detected = True
                                files_with_api_keys.append(file_path)  # Add file to the list

                    issues_found.append((file, issue_details, result))

    # Write files with API keys to a log file
    if api_keys_detected:
        with open("api_keys_log.txt", "w") as log_file:
            for file_path in files_with_api_keys:
                log_file.write(f"{file_path}\n")

    return issues_found, api_keys_detected, files_with_api_keys

if __name__ == "__main__":
    vulnerabilities, api_keys_detected, files_with_api_keys = check_repo_for_vulnerabilities()

    if vulnerabilities:
        print("🚨 AI Security Scan Found Issues! Fix before pushing.")
        for file, issue_details, ai_response in vulnerabilities:
            print(f"🔍 **File: {file}")
            for issue in issue_details:
                print(issue)
            print("\n🔹 **AI Recommendations:**")
            print(ai_response)
        exit(1)  # Block push if vulnerabilities exist
    else:
        print("✅ No security issues found. Proceeding with push.")
        if api_keys_detected:
            print("🔒 API keys detected in the following files:")
            for file in files_with_api_keys:
                print(f"- {file}")
            exit(2)  # Signal to pre-push script to run mask.py
        else:
            exit(0)  # No issues, proceed with push