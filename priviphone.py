#!/usr/bin/env python3
"""
PriViSecurity | ELITE RECON v1.0
Advanced OSINT & Social Intelligence Suite
"""

import os
import urllib.parse
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from phonenumbers.phonenumberutil import NumberParseException
from colorama import Fore, Style, init
import folium

# Initialize colorama for terminal styling
init(autoreset=True)

# Manual Override Database for Nigerian Mobile Blocks (Prefixed with 234)
NG_CARRIERS = {
    "911": "Airtel Nigeria", "912": "Airtel Nigeria", "901": "Airtel Nigeria", 
    "902": "Airtel Nigeria", "904": "Airtel Nigeria", "907": "Airtel Nigeria",
    "913": "MTN Nigeria", "916": "MTN Nigeria", "903": "MTN Nigeria", 
    "906": "MTN Nigeria", "803": "MTN Nigeria", "806": "MTN Nigeria",
    "909": "9mobile", "908": "9mobile", "809": "9mobile", "817": "9mobile",
    "905": "Globacom", "915": "Globacom", "805": "Globacom", "705": "Globacom"
}

class PriViElitePro:
    def __init__(self):
        self.banner = (
            f"\n{Fore.CYAN}  ██████╗ ██████╗ ██╗██╗   ██╗██╗███████╗███████╗ ██████╗\n"
            f"{Fore.CYAN}  ██╔══██╗██╔══██╗██║██║   ██║██║██╔════╝██╔════╝██╔════╝\n"
            f"{Fore.CYAN}  ██████╔╝██████╔╝██║██║   ██║██║███████╗█████╗  ██║     \n"
            f"{Fore.CYAN}  ██╔═══╝ ██╔══██╗██║╚██╗ ██╔╝ ██║╚════██║██╔══╝  ██║     \n"
            f"{Fore.CYAN}  ██║     ██║  ██║██║ ╚████╔╝  ██║███████║███████╗╚██████╗\n"
            f"{Fore.RED}  PriViSecurity 🛡️ | SOCIAL RECON v1.0 | OSINT Suite 2026\n"
            f"{Fore.YELLOW}  {'=' * 65}\n"
        )

    def generate_intel_map(self, location_name, number):
        """Generates a regional map without triggering 403 Forbidden errors."""
        print(f"{Fore.YELLOW}[*] Syncing Geospatial Intel...")
        try:
            # Regional Coordinates (Defaults to center of Nigeria)
            coords = [9.0820, 8.6753]
            
            loc_lower = location_name.lower()
            if "lagos" in loc_lower: coords = [6.5244, 3.3792]
            elif "abuja" in loc_lower: coords = [9.0765, 7.3986]
            
            # Using 'cartodbdark_matter' to bypass OpenStreetMap's local file block
            m = folium.Map(location=coords, zoom_start=10, control_scale=True, tiles="cartodbdark_matter")
            folium.Marker(
                coords, 
                popup=f"Target: {number}<br>Region: {location_name}", 
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
            
            map_name = "privi_recon_map.html"
            m.save(map_name)
            print(f"{Fore.GREEN}[+] Map File Generated: {os.path.abspath(map_name)}")
        except Exception as e:
            print(f"{Fore.RED}[!] Mapping Error: {e}")

    def scan(self, phone_number):
        try:
            # Step 1: Parse and Validate
            parsed = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(parsed):
                print(f"{Fore.RED}[!] Validation Failed: Target number is not active or invalid.")
                return

            clean = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            raw = clean.replace("+", "")
            
            print(self.banner)
            print(f"{Fore.GREEN}[+] SOCIAL RECON INITIALIZED: {phone_number}")
            print(f"{Fore.CYAN}{'=' * 45}")

            # Step 2: Network Carrier Intelligence
            provider = carrier.name_for_number(parsed, "en")
            if not provider and parsed.country_code == 234:
                prefix = str(parsed.national_number)[:3]
                provider = NG_CARRIERS.get(prefix, "Private/Internal Node")

            print(f"{Fore.WHITE}[-] Service Provider : {Fore.YELLOW}{provider}")
            
            tz_tuple = timezone.time_zones_for_number(parsed)
            print(f"{Fore.WHITE}[-] Local Timezone   : {Fore.YELLOW}{', '.join(tz_tuple)}")

            # Step 3: Social & Digital Footprint (THE CORE)
            print(f"\n{Fore.CYAN}[*] SOCIAL IDENTITY SEARCH (Click to Investigate):")
            socials = {
                "TrueCaller ID": f"https://www.truecaller.com/search/global/{raw}",
                "WhatsApp Profile": f"https://wa.me/{raw}",
                "Telegram Account": f"https://t.me/+{raw}",
                "LinkedIn Recon": f"https://www.linkedin.com/search/results/all/?keywords=%2B{raw}",
                "Facebook Graph": f"https://www.facebook.com/search/top/?q=%2B{raw}",
                "Instagram Search": f"https://www.instagram.com/search/?q={raw}"
            }
            for site, url in socials.items():
                print(f"{Fore.WHITE}{site.ljust(18)}: {Fore.BLUE}{url}")

            # Step 4: Advanced Web Dorking (Forum Leak Search)
            print(f"\n{Fore.RED}[!] FORUM & LEAK ARCHIVE SEARCH:")
            # These dorks look for the number in common Nigerian marketplaces and forums
            dork_query = f"site:nairaland.com OR site:jiji.ng OR site:facebook.com \"{raw}\""
            dork_url = f"https://www.google.com/search?q={urllib.parse.quote(dork_query)}"
            print(f"{Fore.WHITE}Identity Dork      : {Fore.YELLOW}{dork_url}")

            # Step 5: Regional Mapping
            location = geocoder.description_for_number(parsed, "en")
            self.generate_intel_map(location if location else "Nigeria", phone_number)

            print(f"\n{Fore.MAGENTA}[!] RECON COMPLETE")
            print(f"{Fore.WHITE}Manual Tip: Check WhatsApp for a profile photo; use Google Lens to reverse-search it.")

        except NumberParseException:
            print(f"{Fore.RED}[!] Format Error: Provide the number in international format (e.g., +234...)")
        except Exception as e:
            print(f"{Fore.RED}[!] System Crash: {e}")

def main():
    scanner = PriViElitePro()
    try:
        target = input(f"{Fore.WHITE}Enter Target Number (e.g. +234...): ").strip()
        if target:
            scanner.scan(target)
        else:
            print(f"{Fore.RED}[!] No target specified.")
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Session Terminated.")

if __name__ == "__main__":
    main()
