import argparse
import re
import subprocess
import ssl
import socket
import requests
from datetime import datetime
from pathlib import Path
import whois
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time  # Added import for time module
from selenium.webdriver.firefox.service import Service

def clean_domains(domains):
    cleaned_domains = set()
    for domain in domains:
        domain = domain.strip()
        if re.match(r'^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,}$', domain):
            cleaned_domains.add(domain.lower())
    return sorted(cleaned_domains)

def perform_dig(domain):
    try:
        result = subprocess.run(['dig', '+short', domain], capture_output=True, text=True)
        return result.stdout if result.stdout else "No records found.\n"
    except Exception as e:
        return f"An error occurred with dig: {str(e)}\n"

def get_whois_info(domain):
    try:
        w = whois.whois(domain)
        info = f"Domain Name: {w.domain_name}\nRegistrar: {w.registrar}\nWHOIS Server: {w.whois_server}\n" \
               f"Creation Date: {w.creation_date}\nExpiration Date: {w.expiration_date}\nStatus: {w.status}\n" \
               f"Emails: {', '.join(w.emails if w.emails else [])}\n"
        return info
    except Exception as e:
        return f"Failed to get whois information for {domain}: {str(e)}\n"

def nslookup(domain):
    try:
        result = subprocess.run(['nslookup', domain], capture_output=True, text=True)
        return result.stdout if result.stdout else "NSLOOKUP failed.\n"
    except Exception as e:
        return f"An error occurred with nslookup: {str(e)}\n"

def dns_recon(domain):
    try:
        result = subprocess.run(['dnsrecon', '-d', domain], capture_output=True, text=True)
        return result.stdout if result.stdout else "DNS Recon failed or no data.\n"
    except Exception as e:
        return f"An error occurred with dnsrecon: {str(e)}\n"

def get_ssl_details(hostname):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                return ssl.DER_cert_to_PEM_cert(cert)
    except Exception as e:
        return f"Failed to retrieve SSL certificate: {str(e)}\n"

def take_screenshot(url, output_path):
    """Take a screenshot of the website after a delay, if not 404."""
    try:
        response = requests.head(url)
        if response.status_code == 404:
            print(f"URL '{url}' returned 404 Not Found. No screenshot taken.")
            return
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(service=Service(executable_path='/path/to/geckodriver'), options=options)  # Replace '/path/to/geckodriver' with the actual path
        driver.get(url)
        time.sleep(10)
        driver.save_screenshot(output_path)
        driver.quit()
        print(f"Screenshot saved: {output_path}")
    except Exception as e:
        print(f"An error occurred while taking screenshot: {e}")

def main(input_file):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    output_file = f"{Path(input_file).stem}+cleaned+{timestamp}.txt"

    with open(input_file, 'r') as f:
        domains = f.read().splitlines()
        cleaned_domains = clean_domains(domains)

    print("Cleaned and sorted domains:")
    for domain in cleaned_domains:
        print(domain)
    
    save_cleaned = input("Would you like to save the cleaned domains to a file? (y/n): ")
    if save_cleaned.lower() == 'y':
        with open(f"{Path(input_file).stem}+cleaned_domains.txt", 'w') as f:
            f.writelines(f"{domain}\n" for domain in cleaned_domains)
        print("Cleaned domains saved.")

    proceed = input("Proceed with domain checks? (y/n): ")
    if proceed.lower() != 'y':
        return

    print("Available checks: \n1. DIG\n2. WHOIS\n3. NSLOOKUP\n4. DNS Recon\n5. SSL Details\n6. Take Screenshot")
    checks = input("Enter the numbers of the checks you want to perform, or 'exit' to quit (e.g., 1,2,4,5,6): ")
    if checks.lower() == 'exit':
        print("Exiting...")
        return
    checks = [int(x.strip()) for x in checks.split(',')]

    with open(output_file, 'w') as f_out:
        for domain in cleaned_domains:
            f_out.write(f"Domain: {domain}\n\n")
            if 1 in checks:
                f_out.write("DIG Results:\n" + perform_dig(domain) + '\n')
            if 2 in checks:
                f_out.write("WHOIS Information:\n" + get_whois_info(domain) + '\n')
            if 3 in checks:
                f_out.write("NSLOOKUP Results:\n" + nslookup(domain) + '\n')
            if 4 in checks:
                f_out.write("DNS Recon Results:\n" + dns_recon(domain) + '\n')
            if 5 in checks:
                f_out.write("SSL Details:\n" + get_ssl_details(domain) + '\n')
            if 6 in checks:
                screenshot_path = f"{Path(output_file).parent}/{domain}.png"
                take_screenshot(f"https://{domain}", screenshot_path)
                f_out.write(f"Screenshot taken and saved as {screenshot_path}\n")
            f_out.write("-" * 80 + "\n\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform domain checks including DIG, WHOIS, NSLOOKUP, DNS Recon, SSL Details, and take screenshots.")
    parser.add_argument("input_file", help="Path to the input file containing a list of domains.")
    args = parser.parse_args()
    main(args.input_file)
