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
import time
from selenium.webdriver.firefox.service import Service
import os

def clean_domains(domains):
    cleaned_domains = set()
    for domain in domains:
        domain = domain.strip()
        if re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', domain):
            cleaned_domains.add(domain)
    return sorted(cleaned_domains)

def perform_banner_grab(ip):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(10)
            sock.connect((ip, 80))
            sock.send(b"GET / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
            return sock.recv(1024).decode(errors='ignore')
    except Exception as e:
        return f"Banner grab failed: {str(e)}\n"

def perform_dig(domain):
    try:
        result = subprocess.run(['dig', '+short', domain], capture_output=True, text=True)
        return result.stdout.strip() if result.stdout else "No records found.\n"
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

def main(input_file):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    output_folder = os.path.join(os.path.dirname(input_file), os.path.splitext(os.path.basename(input_file))[0] + f"+cleaned+{timestamp}")
    os.makedirs(output_folder, exist_ok=True)

    with open(input_file, 'r') as f:
        domains = f.read().splitlines()
        cleaned_domains = clean_domains(domains)

    print("Cleaned and sorted domains:")
    for domain in cleaned_domains:
        print(domain)
    
    print("Available checks: \n1. DIG\n2. WHOIS\n3. NSLOOKUP\n4. DNS Recon\n5. SSL Details\n6. Take Screenshot\n7. Banner Grab")
    checks = input("Enter the numbers of the checks you want to perform, or 'exit' to quit (e.g., 1,2,4,5,6,7): ")
    if checks.lower() == 'exit':
        print("Exiting...")
        return
    checks = [int(x.strip()) for x in checks.split(',')]
    
    for domain in cleaned_domains:
        output_file = os.path.join(output_folder, f"{domain}_results.txt")
        with open(output_file, 'w') as f_out:
            f_out.write(f"Domain: {domain}\n\n")
            if 1 in checks:
                ip = perform_dig(domain)
                f_out.write(f"DIG Results:\nIP Address: {ip}\n")
            if 2 in checks:
                f_out.write("WHOIS Information:\n" + get_whois_info(domain) + '\n')
            if 3 in checks:
                f_out.write("NSLOOKUP Results:\n" + nslookup(domain) + '\n')
            if 4 in checks:
                f_out.write("DNS Recon Results:\n" + dns_recon(domain) + '\n')
            if 5 in checks:
                f_out.write("SSL Details:\n" + get_ssl_details(domain) + '\n')
            if 6 in checks:
                screenshot_path = os.path.join(output_folder, f"{domain}.png")
                take_screenshot(f"https://{domain}", screenshot_path)
                f_out.write(f"Screenshot taken and saved as {screenshot_path}\n")
            if 7 in checks:
                if 'ip' in locals():
                    banner = perform_banner_grab(ip)
                    f_out.write(f"Banner Grab Results:\n{banner}\n")
            f_out.write("-" * 80 + "\n\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform domain checks including DIG, WHOIS, NSLOOKUP, DNS Recon, SSL Details, take screenshots, and perform banner grabs.")
    parser.add_argument("input_file", help="Path to the input file containing a list of domains.")
    args = parser.parse_args()
    main(args.input_file)
