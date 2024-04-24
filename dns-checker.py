import argparse
import re
import subprocess

def clean_domains(domains):
    cleaned_domains = []
    for domain in domains:
        # Remove leading/trailing spaces and filter out invalid domain names
        domain = domain.strip()
        if re.match(r'^[a-zA-Z0-9.-]+$', domain):
            cleaned_domains.append(domain)
    return cleaned_domains

def dns_recon(domain):
    try:
        result = subprocess.run(['dnsrecon', '-d', domain], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

def whois_lookup(domain):
    try:
        result = subprocess.run(['whois', domain], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

def nslookup(domain):
    try:
        result = subprocess.run(['nslookup', domain], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

def main(input_file):
    output_file = "list-output.txt"
    with open(input_file, 'r') as f:
        # Read the input file and clean up the domains
        domains = f.read().splitlines()
        cleaned_domains = clean_domains(domains)

    with open(output_file, 'w') as f_out:
        for domain in cleaned_domains:
            f_out.write(f"Domain: {domain}\n\n")
            f_out.write("DNS Reconnaissance:\n")
            f_out.write(dns_recon(domain) + '\n')

            f_out.write("\nWHOIS Lookup:\n")
            f_out.write(whois_lookup(domain) + '\n')

            f_out.write("\nNSLOOKUP:\n")
            f_out.write(nslookup(domain) + '\n')

            f_out.write("\n" + "-" * 50 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform DNS reconnaissance, WHOIS lookup, and NSLOOKUP for a list of domains.")
    parser.add_argument("input_file", help="Path to the input file containing a list of domains.")
    args = parser.parse_args()
    main(args.input_file)
