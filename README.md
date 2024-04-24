# Site checker

This toolkit includes several Python scripts designed for analyzing and gathering information from websites and subdomains. Each script serves a specific purpose, helping users with a range of tasks from basic site reachability checks to detailed subdomain enumeration with screenshot capturing.

## 1. Site Checker

The `site_checker.py` script performs the following tasks:

- **Reading Hostnames**: Reads a list of hostnames from a file named `hostnames.txt`, with each hostname listed on a separate line.
- **Checking Host Reachability**: Checks if each hostname is reachable by attempting to establish a connection on port 443 (HTTPS) using the `socket` module.
- **Retrieving WHOIS Information**: For reachable hostnames, retrieves WHOIS information using the `whois` library, including details such as the domain name, registrar, creation date, expiration date, status, and contact emails.
- **Fetching SSL Details**: Retrieves SSL certificate details for reachable hostnames using the `ssl` module, including the certificate in PEM format.
- **Capturing HTTP Headers**: Fetches HTTP headers from the hostnames using the `requests` library, providing information such as the server type, content type, and cache control directives.
- **Taking Screenshots**: For reachable hostnames, uses Selenium WebDriver to open the website in a headless Firefox browser and capture a screenshot after waiting for the page to fully load.
- **Outputting Results**: The gathered information for each hostname is saved into a single text file named `results.txt`, including details such as WHOIS information, SSL details, HTTP headers, and paths to screenshots.
- **Creating Output Directory**: Before saving the results, the script creates an output directory named `output` if it doesn't already exist.
- **Handling Errors**: Includes error handling to manage cases where hostnames cannot be reached or where information retrieval fails.

### Prerequisites

- Python 3.x
- Required Python packages: `whois`, `requests`, `selenium`
- Geckodriver executable (geckodriver.exe)

### Usage

1. **Prepare Hostname List**: Create a text file named `hostnames.txt` containing the list of hostnames you want to analyze. Each hostname should be on a separate line.
2. **Run the Script**: Execute the script by running the following command:
   ```bash
   python site_checker.py
   ```

## 2. Subdomain Enumerator

The `subdomain_enumerator.py` script enumerates subdomains for a given domain by leveraging a dictionary attack approach. It performs the following tasks:

- **Choosing a Dictionary File**: Allows the user to select a dictionary file from the `lists` directory containing potential subdomains.
- **Reading Subdomains**: Reads subdomains from the selected dictionary file.
- **Processing Subdomains**: Checks reachability of each subdomain, retrieves WHOIS information, SSL details, and takes screenshots of reachable subdomains.
- **Outputting Results**: Saves the gathered information for each subdomain into separate text files and screenshots into the `subdomain_results` directory.

### Prerequisites

- Python 3.x
- Required Python packages: `requests`, `selenium`, `whois`
- Geckodriver executable (geckodriver.exe)

### Usage

1. **Prepare Domain and Dictionary**: Run the script with the target domain as a command-line argument, e.g.:
   ```bash
   python subdomain_enumerator.py example.com
   ```
   The script will prompt you to choose a dictionary file from the `lists` directory.

## 3. Domain Analysis

The `domain_analysis.py` script takes in a list of domains from an input file and performs DNS reconnaissance, WHOIS lookup, and NSLOOKUP for each domain. It then writes the output to a new file called `list-output.txt`.

### Prerequisites

- Python 3.x
- Required Python packages: `argparse`, `subprocess`, `re`

### Usage

Run the script with the input file containing the list of domains as a command-line argument, e.g.:
   ```bash
   python domain_analysis.py list.txt
   ```
   Replace `list.txt` with the path to your input file containing the list of domains.

## Legal Disclaimer
The scripts provided in this repository are for educational purposes only. Using these scripts to attack targets without prior mutual consent is illegal. It is the end user’s responsibility to obey all applicable local, state, and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by these programs.

## Contributing
Contributions to this repository are welcome. Please ensure that any pull requests or issues adhere to the existing coding standards and fulfill a purposeful enhancement or bug fix.