#!/usr/bin/env python3
import re
import sys
import os

# Define patterns for sensitive information (API keys, passwords, tokens, etc.)
SECRET_PATTERNS = [
    # Match key-value pairs with optional quotes and special characters in values
    r"(?i)(apikey|token|password|secret|bearer|access_key|private_key|client_secret|auth_token|credential)\s*[:=]\s*['\"]?([A-Za-z0-9\-_$@!%*?&]{8,})['\"]?",
    # Match specific known keys (e.g., AWS, GitHub, Slack tokens)
    r"(?i)(AWS_ACCESS_KEY_ID|API_KEY|AWS_SECRET_ACCESS_KEY|GITHUB_TOKEN|GITLAB_TOKEN|SLACK_TOKEN|TWILIO_AUTH_TOKEN|GOOGLE_API_KEY|OPENAI_API_KEY)\s*=\s*['\"]?([A-Za-z0-9\-_$@!%*?&]{8,})['\"]?"
]

# Function to mask detected secrets while keeping the key visible
def mask_secrets(file_content):
    def mask_match(match):
        try:
            key_name = match.group(1)  # Capture the key (e.g., "password", "apikey")
            secret_value = match.group(2)  # Capture the actual secret value

            masked_secret = '*' * len(secret_value)  # Replace value with stars

            # Preserve the original format (quotes or no quotes)
            if "'" in match.group(0) or '"' in match.group(0):
                return f"{key_name} = \"{masked_secret}\""
            else:
                return f"{key_name} = {masked_secret}"
        except IndexError:
            # If the regex pattern does not have the expected groups, return the original match
            return match.group(0)

    for pattern in SECRET_PATTERNS:
        file_content = re.sub(pattern, mask_match, file_content)
    return file_content

# Function to process a given file and mask secrets in place
def process_file(file_path):
    if not os.path.exists(file_path):
        print(f"❌ Error: File '{file_path}' does not exist.")
        return

    try:
        # Read the file
        with open(file_path, "r") as f:
            content = f.read()

        # Mask sensitive credentials
        masked_content = mask_secrets(content)

        # Overwrite the original file with the masked content
        with open(file_path, "w") as f:
            f.write(masked_content)

        print(f"🔒 Masked secrets saved in the original file: {file_path}")

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")

# Main execution
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 mask_secrets.py <filename>")
        sys.exit(1)

    # Read the list of files from the log file
    log_file = "api_keys_log.txt"
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            files_to_process = f.read().splitlines()
    else:
        print(f"❌ Error: Log file '{log_file}' does not exist.")
        sys.exit(1)

    # Process each file listed in the log file
    for file_to_process in files_to_process:
        process_file(file_to_process)