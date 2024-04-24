import whois
import socket
import ssl
import os
import re
import requests
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from pathlib import Path

def sanitize_filename(name):
    """Remove problematic characters from filenames."""
    return re.sub(r'[\\/*?:"<>|]', "", name)

def create_output_directory(path):
    """Ensure the output directory exists."""
    try:
        os.makedirs(path, exist_ok=True)
        print(f"Output directory created: {path}")
    except Exception as e:
        print(f"Error creating output directory '{path}': {str(e)}")

def save_to_file(filename, data):
    """Save data to a file."""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(data)
        print(f"Data saved to file: {filename}")
    except Exception as e:
        print(f"Error saving data to file '{filename}': {str(e)}")

def read_hostnames_from_file(file_path):
    """Read and parse hostnames from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        hostnames = set(re.split(r'[\s,\n]+', content.strip()))
        print(f"Hostnames read from file: {hostnames}")
        return hostnames
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return set()
    except Exception as e:
        print(f"Error reading file '{file_path}': {str(e)}")
        return set()

def check_host_reachability(hostname):
    """Check if the host is reachable and not returning 404."""
    try:
        response = requests.head(f"https://{hostname}", allow_redirects=True)
        if response.status_code == 404:
            print(f"Host '{hostname}' returned 404 Not Found.")
            return False
        response.raise_for_status()  # raises an HTTPError for bad responses
        print(f"Host '{hostname}' is reachable.")
        return True
    except requests.exceptions.HTTPError as e:
        print(f"Host '{hostname}' is unreachable: HTTP error: {e}")
        return False
    except Exception as e:
        print(f"Host '{hostname}' is unreachable: {str(e)}")
        return False

def get_ssl_details(hostname):
    """Retrieve SSL certificate details."""
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                return ssl.DER_cert_to_PEM_cert(cert)
    except Exception as e:
        return f"Failed to retrieve SSL certificate: {str(e)}"

def get_http_headers(url):
    """Fetch HTTP headers from a URL if not 404."""
    try:
        response = requests.get(url)
        if response.status_code == 404:
            print(f"URL '{url}' returned 404 Not Found.")
            return "404 Not Found"
        response.raise_for_status()
        headers = response.headers
        return '\n'.join(f"{k}: {v}" for k, v in headers.items())
    except Exception as e:
        return f"Failed to retrieve HTTP headers: {str(e)}"

def get_whois_info(domain):
    """Retrieve WHOIS information for a given domain."""
    try:
        w = whois.whois(domain)
        info = f"Domain Name: {w.domain_name}\n"
        if w.registrar:
            info += f"Registrar: {w.registrar}\n"
        if w.whois_server:
            info += f"WHOIS Server: {w.whois_server}\n"
        if w.creation_date:
            info += f"Creation Date: {w.creation_date}\n"
        if w.expiration_date:
            info += f"Expiration Date: {w.expiration_date}\n"
        if w.status:
            info += f"Status: {w.status}\n"
        if w.emails:
            info += f"Emails: {', '.join(w.emails)}\n"
        return info
    except Exception as e:
        return f"Failed to get whois information for {domain}: {str(e)}"

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

def process_hostnames(hostnames, output_file, reachable_output_file):
    """Process each hostname and store results in a single text file."""
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            with open(reachable_output_file, 'w', encoding='utf-8') as reachable_file:
                for hostname in sorted(hostnames):
                    reachable = check_host_reachability(hostname)
                    file.write(f"Hostname: {hostname}\n")
                    file.write(f"Reachable: {'Yes' if reachable else 'No'}\n")
                    if reachable:
                        reachable_file.write(f"{hostname}\n")
                        domain_info = get_whois_info(hostname)
                        file.write(f"\nWHOIS Information:\n{domain_info}\n")
                        ssl_details = get_ssl_details(hostname)
                        file.write(f"\nSSL Details:\n{ssl_details}\n")
                        http_headers = get_http_headers(f"https://{hostname}")
                        file.write(f"\nHTTP Headers:\n{http_headers}\n")
                        screenshot_path = output_file.parent / f"{sanitize_filename(hostname)}.png"
                        take_screenshot(f"https://{hostname}", screenshot_path)
                        file.write(f"\nScreenshot saved: {screenshot_path}\n\n")
                    else:
                        file.write("\n\n")
        print(f"Results saved to file: {output_file}")
        print(f"Reachable hostnames saved to file: {reachable_output_file}")
    except Exception as e:
        print(f"Error processing hostnames: {str(e)}")

output_dir = Path('output')
create_output_directory(output_dir)
hostnames_file_path = Path('hostnames.txt')
hostnames = read_hostnames_from_file(hostnames_file_path)
output_file = output_dir / 'results.txt'
reachable_output_file = output_dir / 'reachable_hostnames.txt'
process_hostnames(hostnames, output_file, reachable_output_file)
