# Site Checker

## Disclaimer

This script is provided for educational and informational purposes only. By using this script, you agree that:

- The author of this script is not responsible for any misuse or damage caused by the use of this tool.
- You are solely responsible for ensuring compliance with applicable laws and regulations in your jurisdiction.
- Usage of this script may involve making requests to external websites, which could result in access restrictions or legal consequences.
- Use this script at your own risk.

## Prerequisites

Before using this script, ensure you have the following dependencies installed:

- Python 3.x
- Required Python packages: `whois`, `requests`, `selenium`

You can install the required packages using pip:

```
pip install whois requests selenium
```

Additionally, make sure you have the latest version of Mozilla Firefox installed, as the script utilizes the Firefox WebDriver for taking screenshots.

**Geckodriver**: You also need to download Geckodriver, which is a requirement for Selenium to interact with Firefox. Ensure that Geckodriver is downloaded and placed in the same directory as the script. You can download Geckodriver from the [official Mozilla repository](https://github.com/mozilla/geckodriver/releases).

## Usage

1. **Prepare Hostname List**: Create a text file named `hostnames.txt` containing the list of hostnames you want to analyze. Each hostname should be on a separate line.

2. **Run the Script**: Execute the script by running the following command:

```
python site_checker.py
```

3. **Output**: The script will create an `output` directory if it doesn't exist and store the results in the following files:

- `results.txt`: Contains detailed information for each hostname, including WHOIS information, SSL details, HTTP headers, and screenshots (if reachable).
- `reachable_hostnames.txt`: Lists only the reachable hostnames for further analysis.

## Customization

You can customize the behavior of the script by modifying the source code directly or passing arguments to the script when executing it.