# 🛡️ VY-OSINTFramework

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Security](https://img.shields.io/badge/Security-Strict-success.svg)
![Zero Leak](https://img.shields.io/badge/Zero_Leak-Verified-success.svg)
![Telemetry](https://img.shields.io/badge/Telemetry-None-critical.svg)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

A modern, privacy-first Open Source Intelligence (OSINT) framework designed for DevSecOps engineers, penetration testers, and security researchers. Built entirely in Python using `customtkinter` for a seamless, fatigue-free graphical interface.

## ⚙️ Security & Privacy Philosophy (Secure by Design)

As a core engineering standard, this project is strictly built on **Privacy-First** principles:

* **Zero Telemetry:** The application does not collect, log, or transmit any user hardware data, IP addresses, search queries, or network configurations to third parties.
* **100% Passive Reconnaissance:** The framework interacts with targets strictly through intermediary APIs and public datasets. Direct interaction (active scanning, pinging, or port scanning) that could trigger target WAFs or IDS/IPS systems is strictly prohibited by design.
* **Safe API Routing:** Prioritizes APIs from privacy-respecting jurisdictions. All necessary API keys are handled securely via local `.env` environments and are never hardcoded.

## 🚀 Core Modules (In Development)

* **[1] Infrastructure & Network Intelligence:** Passive resolution of domain IPs, geolocation, ISP analysis, and non-intrusive HTTP header grabbing via intermediary services.
* **[2] Digital Footprint Hunter:** Rapid username enumeration across various social media platforms and forums without triggering rate limits. *(Coming Soon)*
* **[3] Media Forensics:** Offline EXIF and metadata extraction for images and documents to uncover hidden GPS coordinates, camera models, and software versions. *(Coming Soon)*

## 🛠️ Installation & Setup

We recommend running the framework within an isolated Python Virtual Environment.

```bash
# Clone the repository
git clone [https://github.com/VolkanYildirim/VY-OSINTFramework.git](https://github.com/VolkanYildirim/VY-OSINTFramework.git)

# Navigate to the directory
cd VY-OSINTFramework

# Install dependencies
pip install -r requirements.txt

# Run the framework
python main.py
