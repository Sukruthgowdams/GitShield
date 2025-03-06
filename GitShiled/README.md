# GitShield

GitShield is a pre-push Git hook designed to enhance the security of your codebase by automatically scanning for and masking sensitive information, such as API keys, passwords, and tokens, before pushing code to a remote repository. It integrates with AI-powered security analysis to detect vulnerabilities and ensures that sensitive data is not accidentally exposed.

---

## Features

- **Automated Security Scanning**: Scans your codebase for security vulnerabilities using AI-powered analysis.
- **API Key Detection**: Detects and logs files containing API keys or other sensitive information.
- **Automatic Masking**: Masks detected API keys in the logged files to prevent accidental exposure.
- **Pre-Push Hook**: Integrates with Git's pre-push hook to enforce security checks before code is pushed to a remote repository.
- **Customizable Patterns**: Supports customizable regex patterns for detecting sensitive information.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/gitshield.git
   cd gitshield
   ```

2. **Set Up the Pre-Push Hook**:
   Copy the `pre-push` script to your `.git/hooks/` directory:
   ```bash
   cp pre-push .git/hooks/
   chmod +x .git/hooks/pre-push
   ```

3. **Install Dependencies**:
   Ensure you have Python 3 installed, and install the required dependencies:
   ```bash
   pip install mistralai
   ```

4. **Set the `MISTRAL_API_KEY`**:
   Export your Mistral AI API key as an environment variable:
   ```bash
   export MISTRAL_API_KEY="your-api-key-here"
   ```

---

## Workflow

GitShield operates in two phases:

1. **Scan and Log**:
   - The `scan_and_log.py` script scans the repository for API keys and logs the files containing them to `api_keys_log.txt`.

2. **Mask Logged Files**:
   - The `mask_logged_files.py` script reads `api_keys_log.txt` and masks the API keys in the listed files.

---

## Scripts

### `scan_and_log.py`
Scans the repository for API keys and logs the files containing them to `api_keys_log.txt`.

#### Usage:
```bash
python scan_and_log.py
```

#### Exit Codes:
- **0**: No API keys detected.
- **2**: API keys detected and logged.

---

### `mask_logged_files.py`
Reads `api_keys_log.txt` and masks the API keys in the listed files.

#### Usage:
```bash
python mask_logged_files.py
```

#### Exit Codes:
- **0**: Masking completed successfully.
- **1**: Error during masking.

---

### `pre-push`
A Git pre-push hook script that orchestrates the scanning and masking workflow.

#### Usage:
Automatically runs when you attempt to push code to a remote repository.

#### Exit Codes:
- **0**: No security issues found. Proceed with push.
- **1**: Security vulnerabilities detected. Block push.
- **2**: API keys detected. Masking required.

---

## Configuration

### Customizing Detection Patterns
You can customize the regex patterns used to detect sensitive information by modifying the `API_KEY_PATTERNS` list in `scan_and_log.py` and `SECRET_PATTERNS` in `mask_logged_files.py`.

---

## Example Workflow

1. **Make Changes**:
   Modify your code and stage the changes:
   ```bash
   git add .
   ```

2. **Attempt to Push**:
   When you push your changes, GitShield will automatically run:
   ```bash
   git push origin main
   ```

3. **Scan and Log**:
   - If API keys are detected, they will be logged to `api_keys_log.txt`.

4. **Mask Logged Files**:
   - If API keys are detected, the pre-push hook will trigger `mask_logged_files.py` to mask the keys.

5. **Push**:
   - If no security issues are found, the push will proceed. Otherwise, the push will be blocked until the issues are resolved.

---

## Troubleshooting

### API Keys Not Masked
- Ensure `api_keys_log.txt` contains the correct file paths.
- Verify that `mask_logged_files.py` has the necessary permissions to overwrite the files.

### Pre-Push Hook Not Running
- Ensure the `pre-push` script is executable:
  ```bash
  chmod +x .git/hooks/pre-push
  ```

### AI Analysis Failing
- Ensure the `MISTRAL_API_KEY` environment variable is set correctly.
- Check your internet connection and API key validity.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

---

## License

GitShield is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgments

- **Mistral AI**: For providing the AI-powered security analysis.
- **Git**: For the pre-push hook mechanism.

---

## Contact

For questions or feedback, please open an issue on GitHub or contact the maintainers directly.

---

**GitShield**: Protecting your code, one push at a time. 🛡️