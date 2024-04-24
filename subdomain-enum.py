import sys
import re
import requests
import time
import os
import socket
import ssl
import whois
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from pathlib import Path

def sanitize_filename(name):
    """Remove problematic characters from filenames."""
    return re.sub(r'[\\/*?:"<>|]', "", name)

def create_output_directory(path):
    """Ensure the output directory exists."""
    os.makedirs(path, exist_ok=True)
    print(f"Output directory created: {path}")

def check_host_reachability(hostname):
    """Check if the host is reachable."""
    try:
        response = requests.head(f"https://{hostname}")
        if response.status_code == 404:
            print(f"{hostname} returned 404 Not Found.")
            return False
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"{hostname} is unreachable: {e}")
        return False

def get_whois_info(domain):
    """Retrieve WHOIS information for a domain."""
    try:
        w = whois.whois(domain)
        info = f"Domain Name: {w.domain_name}\nRegistrar: {w.registrar}\n"
        return info
    except Exception as e:
        print(f"Failed to get WHOIS information for {domain}: {e}")
        return "Failed to retrieve WHOIS info"

def get_ssl_details(hostname):
    """Retrieve SSL certificate details."""
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                return ssl.DER_cert_to_PEM_cert(cert)
    except Exception as e:
        return f"Failed to retrieve SSL certificate: {e}"

def take_screenshot(url, output_path):
    """Take a screenshot of the website after a delay, if not 404."""
    try:
        response = requests.head(url)
        if response.status_code == 404:
            print(f"URL '{url}' returned 404 Not Found. No screenshot taken.")
            return
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        time.sleep(10)
        driver.save_screenshot(output_path)
        driver.quit()
        print(f"Screenshot saved: {output_path}")
    except Exception as e:
        print(f"Failed to take screenshot: {str(e)}")
        
def choose_dictionary():
    """Choose a dictionary file from the 'lists' folder."""
    lists_dir = Path('lists')
    if not lists_dir.exists():
        print("Lists directory not found.")
        return ""
    files = [f for f in lists_dir.iterdir() if f.is_file()]
    if not files:
        print("No dictionary files found in the 'lists' directory.")
        return ""
    print("Choose a dictionary file:")
    for i, file in enumerate(files):
        print(f"{i + 1}. {file.name}")
    while True:
        try:
            choice = int(input("Enter the number of the dictionary file: "))
            if 1 <= choice <= len(files):
                return str(files[choice - 1])
            else:
                print("Invalid choice. Please enter a number between 1 and", len(files))
        except ValueError:
            print("Invalid input. Please enter a number.")

def process_subdomains(subdomains, domain, output_dir):
    """Process each subdomain and store results."""
    for sub in subdomains:
        hostname = f"{sub}.{domain}"
        if check_host_reachability(hostname):
            whois_info = get_whois_info(hostname)
            ssl_details = get_ssl_details(hostname)
            screenshot_path = output_dir / f"{sanitize_filename(hostname)}.png"
            take_screenshot(f"https://{hostname}", str(screenshot_path))
            with open(output_dir / f"{sanitize_filename(hostname)}.txt", 'w') as f:
                f.write(f"WHOIS info:\n{whois_info}\n\nSSL details:\n{ssl_details}\n")
                print(f"Details saved for {hostname}")

def main(domain):
    output_dir = Path.cwd() / 'subdomain_results'
    create_output_directory(output_dir)
    subdomain_file = choose_dictionary()
    if not subdomain_file:
        print("No dictionary selected, exiting.")
        return
    with open(subdomain_file, 'r') as file:
        subdomains = {line.strip() for line in file if line.strip()}
    process_subdomains(subdomains, domain, output_dir)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <domain>")
        sys.exit(1)
    domain = sys.argv[1]
    main(domain)
