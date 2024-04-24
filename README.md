# Website Analysis Toolkit

This repository contains a collection of Python scripts designed for conducting detailed analysis and reconnaissance on websites and subdomains. These tools facilitate a range of activities including reachability checks, WHOIS lookups, SSL certificate retrieval, subdomain enumeration, and more.

## Scripts Included

### 1. Site Checker (`site_checker.py`)

The `site_checker.py` script offers a suite of features for analyzing individual hostnames:

- **Reading Hostnames**: Extracts a list of hostnames from `hostnames.txt`, each on a separate line.
- **Checking Host Reachability**: Attempts to connect via HTTPS (port 443) to check if the host is reachable.
- **WHOIS Information Retrieval**: Gathers WHOIS data for reachable hosts, detailing registrar, registration dates, status, etc.
- **SSL Certificate Fetching**: Retrieves SSL details for each hostname using the SSL context.
- **HTTP Headers Capture**: Collects HTTP headers to identify server configuration and policies.
- **Screenshot Capturing**: Utilizes Selenium with headless Firefox to take screenshots of reachable websites.
- **Results Compilation**: All collected data is compiled into a `results.txt` file, including paths to saved screenshots.
- **Output Directory Management**: Ensures all outputs are neatly stored in an `output` directory.
- **Error Handling**: Provides robust error management to handle unreachable hosts or failures in data retrieval.

#### Prerequisites
- Python 3.x
- Packages: `whois`, `requests`, `selenium`
- Geckodriver (for Selenium)

#### Usage
To run the script:
```bash
python site_checker.py
```
Prepare a `hostnames.txt` file with each target hostname on a new line.

### 2. Subdomain Enumerator (`subdomain_enumerator.py`)

This script performs exhaustive subdomain discovery using dictionary-based attacks.

- **Dictionary File Selection**: Users can select a dictionary file from the `lists` folder.
- **Subdomain Discovery**: Checks each subdomain for availability and captures relevant data.
- **Comprehensive Outputs**: Saves detailed information and screenshots for each found subdomain.

#### Prerequisites
- Python 3.x
- Packages: `requests`, `selenium`, `whois`
- Geckodriver / Firefox driver

#### Usage
Run the script with a target domain:
```bash
python subdomain_enumerator.py example.com
```
Choose a dictionary file when prompted.

### 3. Domain Analysis (`domain_analysis.py`)

Analyzes a list of domains to provide DNS, WHOIS, and NSLOOKUP insights.

- **Domain Processing**: Reads domains from a provided list and performs multiple checks.
- **Detailed Reporting**: Outputs results into `list-output.txt`.

#### Prerequisites
- Python 3.x
- Packages: `argparse`, `subprocess`, `re`

#### Usage
Execute the script with an input list:
```bash
python domain_analysis.py list.txt
```
Replace `list.txt` with your file containing domains.

## Legal Disclaimer

These tools are intended for educational and testing purposes only. Any use of these scripts must comply with applicable laws, and consent must be obtained from target entities. The authors are not liable for misuse or damage derived from using these scripts.

## Contributing

Contributions are welcome. Please ensure your pull requests or issues adhere to coding standards and provide meaningful enhancements or fixes.