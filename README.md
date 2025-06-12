# Web Application Vulnerability Scanner

A lightweight Python-based tool that scans websites for common vulnerabilities like **XSS (Cross-Site Scripting)** and **SQL Injection**.

---

## 🔎 Features
- Recursively crawls URLs within the target domain
- Detects input fields and forms
- Injects common XSS and SQLi payloads
- Analyzes server response for reflection or error messages
- Flask-based web UI for easy scan management
- Logs all findings with timestamps

---

## 🛠️ Tools & Technologies
- Python 3
- Requests
- BeautifulSoup
- Flask
- Linux Terminal

---

## 📁 Project Structure
```bash
web-vulnerability-scanner/
├── scanner.py                 # Main scanner script
├── payloads/
│   ├── xss.txt               # XSS payloads
│   └── sqli.txt              # SQLi payloads
├── logs/
│   ├── vuln_log.txt          # Raw scan log
│   └── scan_report.txt       # Cleaned summary report
├── ui_flask_app/
│   ├── app.py                # Flask UI app
│   └── templates/
│       └── index.html        # Web UI form
```

---

## 🚀 Getting Started
### 1. Clone the repository
```bash
git clone https://github.com/yourusername/web-vulnerability-scanner.git
cd web-vulnerability-scanner
```

### 2. Install required packages
```bash
pip install requests beautifulsoup4 flask
```

### 3. Add Payloads
Edit `payloads/xss.txt` and `payloads/sqli.txt` with the desired test payloads.

### 4. Run the Scanner from Terminal
```bash
python3 scanner.py
```

### 5. Or Use the Flask UI
```bash
cd ui_flask_app
python3 app.py
```
Then visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 📓 Sample Output (scan_report.txt)
```
[XSS] http://testphp.vulnweb.com/cart.php - Payload: <script>alert(1)</script>
[SQLi] http://testphp.vulnweb.com/login.php - Payload: ' OR 1=1 --
```
