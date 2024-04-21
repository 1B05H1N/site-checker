# Site Checker

The Site Checker script is a Python tool designed to gather various information about a list of hostnames provided in a text file. It performs the following tasks:

1. **Reading Hostnames**: Reads a list of hostnames from a file named `hostnames.txt`, with each hostname listed on a separate line.

2. **Checking Host Reachability**: Checks if each hostname is reachable by attempting to establish a connection on port 443 (HTTPS) using the `socket` module.

3. **Retrieving WHOIS Information**: For reachable hostnames, retrieves WHOIS information using the `whois` library, including details such as the domain name, registrar, creation date, expiration date, status, and contact emails.

4. **Fetching SSL Details**: Retrieves SSL certificate details for reachable hostnames using the `ssl` module, including the certificate in PEM format.

5. **Capturing HTTP Headers**: Fetches HTTP headers from the hostnames using the `requests` library, providing information such as the server type, content type, and cache control directives.

6. **Taking Screenshots**: For reachable hostnames, uses Selenium WebDriver to open the website in a headless Firefox browser and capture a screenshot after waiting for the page to fully load.

7. **Outputting Results**: The gathered information for each hostname is saved into a single text file named `results.txt`, including details such as WHOIS information, SSL details, HTTP headers, and paths to screenshots.

8. **Creating Output Directory**: Before saving the results, the script creates an output directory named `output` if it doesn't already exist.

9. **Handling Errors**: Includes error handling to manage cases where hostnames cannot be reached or where information retrieval fails.

## Prerequisites

- Python 3.x
- Required Python packages: `whois`, `requests`, `selenium`
- Geckodriver executable (geckodriver.exe)

Ensure that you have the required dependencies installed and that Geckodriver is available in your PATH environment variable before running the script. You also need to provide a `hostnames.txt` file containing the list of hostnames to be analyzed.

## Usage

1. **Prepare Hostname List**: Create a text file named `hostnames.txt` containing the list of hostnames you want to analyze. Each hostname should be on a separate line.

2. **Run the Script**: Execute the script by running the following command:

   ```bash
   python site_checker.py
   ```

3. **Output**: The script will create an `output` directory if it doesn't exist and store the results in the `results.txt` file within that directory.

## Customization

You can customize the behavior of the script by modifying the source code directly or passing arguments to the script when executing it.

## Disclaimer

This script is provided for educational and informational purposes only. Use it responsibly and ensure compliance with applicable laws and regulations.
