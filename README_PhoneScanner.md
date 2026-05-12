<div align="center">

# 🛡️ PriVi Elite Phone Scanner: Developed by PriViSecurity

![PriVi Elite Phone Scanner](PriVi-Phone-Scanner.PNG)

</div>

### Advanced Phone Number OSINT & Intelligence Suite
**Developed by Prince Ubebe | [PriViSecurity](https://github.com/Privis40)**

---

## ⚠️ Legal Notice

> **This tool is intended ONLY for lawful OSINT investigations on numbers you have authorization to research.**
> Unauthorized surveillance or investigation of individuals without their consent or a lawful basis may be illegal under privacy laws, the Computer Misuse Act, NDPR (Nigeria Data Protection Regulation), GDPR, and equivalent laws worldwide.
> **PriViSecurity accepts no liability for unauthorized or malicious use of this tool.**

Legitimate use cases include: corporate due diligence, fraud investigation, HR verification, authorized journalism, and law enforcement support.

---

## What It Does

PriVi Elite Phone Scanner is a phone number OSINT and intelligence tool. It validates phone numbers, identifies carriers (with a specialized Nigerian mobile network database), detects timezone, generates investigative social media search links, builds targeted Google dorks for leak and forum searches, and produces a regional geospatial HTML map — all in a single workflow.

It is designed for:
- Corporate investigators and fraud analysts conducting due diligence
- HR and compliance teams performing authorized background verification
- Journalists conducting source verification for investigative reporting
- Security researchers and investigators in authorized OSINT engagements

---

## Features

| Feature | Description |
|---|---|
| ✅ Number Validation | Validates international format using the phonenumbers library |
| 📡 Carrier Detection | Identifies carrier via phonenumbers + custom Nigerian prefix database |
| 🇳🇬 Nigerian Network Intelligence | Custom prefix database for MTN, Airtel, Glo, and 9mobile (234 prefix) |
| 🌍 Timezone Detection | Identifies the number's timezone region |
| 🔗 Social Media Links | Generates clickable investigation links for TrueCaller, WhatsApp, Telegram, LinkedIn, Facebook, Instagram |
| 🔎 Google Dork Generator | Builds targeted search strings for leak databases, forums, and paste sites |
| 🗺️ Regional HTML Map | Generates a Folium HTML map pinpointing the number's regional location |
| 📋 Clean Terminal Output | Structured Rich-style output for fast field use |

---

## Requirements

```bash
pip install phonenumbers folium colorama
```

---

## Installation

```bash
git clone https://github.com/Privis40/PriVi_Elite_Phone.No_Scanner.git
cd "PriVi_Elite_Phone.No_Scanner"
pip install -r requirements.txt
```

---

## Usage

```bash
python3 priviphone.py
```

Enter the target phone number in international format when prompted:

```
Enter phone number (international format): +2348031234567
```

### Example Output

```
  Number:      +2348031234567
  Valid:        Yes
  Country:      Nigeria
  Carrier:      MTN Nigeria  (custom database match)
  Timezone:     Africa/Lagos
  Number Type:  Mobile

  Social Investigation Links:
    TrueCaller:   https://www.truecaller.com/search/ng/08031234567
    WhatsApp:     https://wa.me/2348031234567
    Telegram:     https://t.me/+2348031234567
    LinkedIn:     https://www.linkedin.com/search/results/all/?keywords=+2348031234567
    Facebook:     https://www.facebook.com/search/top/?q=2348031234567
    Instagram:    https://www.instagram.com/explore/tags/2348031234567/

  Google Dork:
    "2348031234567" site:pastebin.com OR site:ghostbin.com OR site:raidforums.com

  [*] Regional map saved: privi_recon_map.html
```

---

## Nigerian Carrier Database

PriViSpecter includes a custom prefix-to-carrier mapping for Nigerian mobile numbers — a feature missing from the standard `phonenumbers` library for many local prefixes.

Supported carriers and prefixes:

| Carrier | Prefixes |
|---|---|
| MTN Nigeria | 803, 806, 903, 906, 913, 916 |
| Airtel Nigeria | 901, 902, 904, 907, 911, 912 |
| Globacom | 705, 805, 905, 915 |
| 9mobile | 809, 817, 908, 909 |

Numbers matching these prefixes will show the correct carrier even where the standard library returns generic results.

---

## Output Files

| File | Contents |
|---|---|
| `privi_recon_map.html` | Interactive Folium HTML map with regional pin |

Open the HTML file in any browser to view the interactive map.

---

## What This Tool Does NOT Do

- ❌ Does **not** track real-time location of any device
- ❌ Does **not** intercept calls or messages
- ❌ Does **not** access any carrier database directly
- ❌ Does **not** perform any active network contact with the target number

All intelligence is derived from publicly available number metadata and open-source search links only.

---

## Tested On

- Kali Linux 2024+
- Ubuntu 22.04 / 24.04
- Windows 10/11 (Python 3.10+)
- Python 3.10+

---

## Author & Brand

**Prince Ubebe**
Cybersecurity Analyst | Security Automation Engineer | Founder, PriViSecurity

- GitHub: [github.com/Privis40](https://github.com/Privis40)
- LinkedIn: [linkedin.com/in/prince-ubebe-291573321](https://www.linkedin.com/in/prince-ubebe-291573321)
- YouTube: [@princeubebecyber](https://youtube.com/@princeubebecyber)
- HackerOne / Bugcrowd: Active researcher

---

## License

This tool is released for **authorized security research and professional use only.**
Redistribution or modification for malicious purposes is strictly prohibited.

© 2026 PriViSecurity. All rights reserved.
