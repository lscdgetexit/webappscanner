import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

visited = set()

def is_valid_url(url, domain):
    parsed = urlparse(url)
    return domain in parsed.netloc and parsed.scheme in ['http', 'https']

def extract_forms(soup):
    return soup.find_all("form")

def get_form_details(form):
    details = {
        "action": form.get("action"),
        "method": form.get("method", "get").lower(),
        "inputs": []
    }
    for input_tag in form.find_all("input"):
        input_type = input_tag.get("type", "text")
        name = input_tag.get("name")
        value = input_tag.get("value", "")
        details["inputs"].append({"type": input_type, "name": name, "value": value})
    return details

def submit_form(form_details, url, payload):
    target_url = urljoin(url, form_details["action"])
    data = {}

    for input_field in form_details["inputs"]:
        if input_field["name"]:
            data[input_field["name"]] = payload

    try:
        if form_details["method"] == "post":
            return requests.post(target_url, data=data)
        else:
            return requests.get(target_url, params=data)
    except:
        return None

def scan_xss(forms, url):
    with open("../payloads/xss.txt") as f:
        payloads = f.read().splitlines()

    for form in forms:
        form_details = get_form_details(form)
        for payload in payloads:
            response = submit_form(form_details, url, payload)
            if response and payload in response.text:
                print(f"[!!!] XSS vulnerability detected at {url}")
                print(f"      Payload: {payload}")
                log_vulnerability("XSS", url, payload)

def scan_sqli(forms, url):
    with open("../payloads/sqli.txt") as f:
        payloads = f.read().splitlines()

    for form in forms:
        form_details = get_form_details(form)
        for payload in payloads:
            response = submit_form(form_details, url, payload)
            if response and any(error in response.text.lower() for error in ["sql", "syntax", "warning", "error"]):
                print(f"[!!!] SQLi vulnerability detected at {url}")
                print(f"      Payload: {payload}")
                log_vulnerability("SQLi", url, payload)

def log_vulnerability(vuln_type, url, payload):
    with open("../logs/vuln_log.txt", "a") as log:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{timestamp}] {vuln_type} at {url} using payload: {payload}\n")

def crawl(url, domain):
    if url in visited:
        return
    visited.add(url)

    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        print(f"[+] Crawling: {url}")

        forms = extract_forms(soup)
        print(f"    [*] Found {len(forms)} forms.")

        if forms:
            scan_xss(forms, url)
            scan_sqli(forms, url)

        for link in soup.find_all("a"):
            href = link.get("href")
            if not href:
                continue
            full_url = urljoin(url, href)
            if is_valid_url(full_url, domain):
                crawl(full_url, domain)

    except requests.exceptions.RequestException as e:
        print(f"[-] Error crawling {url} - {e}")

if __name__ == "__main__":
    target = input("Enter the target URL (e.g., http://testphp.vulnweb.com): ").strip()
    domain = urlparse(target).netloc
    print("[*] Starting crawl + scan...")
    start = time.time()
    crawl(target, domain)
    print(f"\n[*] Scan complete. Total pages visited: {len(visited)}")
    print(f"[*] Time taken: {round(time.time() - start, 2)} seconds")
