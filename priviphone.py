#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║       PriVi Elite Phone Scanner v2.0                             ║
║       Advanced Phone Number OSINT & Intelligence Suite           ║
║       Developed by Prince Ubebe | PriViSecurity                  ║
╚══════════════════════════════════════════════════════════════════╝

LEGAL NOTICE:
  This tool is intended ONLY for lawful OSINT investigations on
  numbers you have authorization to research. Unauthorized
  surveillance or investigation of individuals without consent or
  a lawful basis may be illegal under privacy laws, NDPR, GDPR,
  and equivalent laws worldwide.
  PriViSecurity accepts no liability for unauthorized use.
"""

import os
import sys
import urllib.parse
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from phonenumbers.phonenumberutil import NumberParseException
import folium
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()

AUTHOR  = "Prince Ubebe"
BRAND   = "PriViSecurity"
VERSION = "2.0"
TOOL    = "PriVi Elite Phone Scanner"

# ── NIGERIAN CARRIER DATABASE ─────────────────────────────────────────────────
# Custom prefix-to-carrier mapping for Nigerian mobile numbers.
# The standard phonenumbers library returns incomplete results for many
# Nigerian prefixes — this database fills that gap.

NG_CARRIERS = {
    # Airtel Nigeria
    "901": "Airtel Nigeria", "902": "Airtel Nigeria", "904": "Airtel Nigeria",
    "907": "Airtel Nigeria", "911": "Airtel Nigeria", "912": "Airtel Nigeria",
    # MTN Nigeria
    "803": "MTN Nigeria",    "806": "MTN Nigeria",    "903": "MTN Nigeria",
    "906": "MTN Nigeria",    "913": "MTN Nigeria",    "916": "MTN Nigeria",
    # 9mobile
    "809": "9mobile",        "817": "9mobile",        "908": "9mobile",
    "909": "9mobile",
    # Globacom
    "705": "Globacom",       "805": "Globacom",       "905": "Globacom",
    "915": "Globacom",
}


# ── HEADER ────────────────────────────────────────────────────────────────────

def print_header():
    os.system("clear")
    header = Text()
    header.append(
        "\n"
        "  ██████╗ ██╗  ██╗ ██████╗ ███╗   ██╗███████╗\n"
        "  ██╔══██╗██║  ██║██╔═══██╗████╗  ██║██╔════╝\n"
        "  ██████╔╝███████║██║   ██║██╔██╗ ██║█████╗\n"
        "  ██╔═══╝ ██╔══██║██║   ██║██║╚██╗██║██╔══╝\n"
        "  ██║     ██║  ██║╚██████╔╝██║ ╚████║███████╗\n"
        "  ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝\n",
        style="bold cyan"
    )
    header.append(
        f"  {BRAND}  |  {TOOL} v{VERSION}  |  Phone Number OSINT & Intelligence Suite\n",
        style="dim white"
    )
    header.append(f"  Developer: {AUTHOR}  |  Authorized Use Only\n", style="dim red")
    console.print(Panel(header, border_style="blue"))


# ── MAP GENERATOR ─────────────────────────────────────────────────────────────

def generate_intel_map(location_name: str, number: str):
    console.print("\n[bold yellow][*] Syncing geospatial intel...[/bold yellow]")
    try:
        # Regional coordinates — defaults to center of Nigeria
        coords = [9.0820, 8.6753]
        loc_lower = location_name.lower()
        if "lagos"  in loc_lower: coords = [6.5244, 3.3792]
        elif "abuja" in loc_lower: coords = [9.0765, 7.3986]
        elif "kano"  in loc_lower: coords = [12.0022, 8.5920]
        elif "ph"    in loc_lower or "port harcourt" in loc_lower:
            coords = [4.8156, 7.0498]
        elif "ibadan" in loc_lower: coords = [7.3775, 3.9470]

        m = folium.Map(
            location=coords, zoom_start=10,
            control_scale=True, tiles="cartodbdark_matter"
        )
        folium.Marker(
            coords,
            popup=f"Target: {number}<br>Region: {location_name}",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)

        map_name = "privi_recon_map.html"
        m.save(map_name)
        console.print(
            f"[bold green][+] Map saved:[/bold green] [cyan]{os.path.abspath(map_name)}[/cyan]"
        )
    except Exception as e:
        console.print(f"[bold red][!] Mapping error: {e}[/bold red]")


# ── SCANNER ───────────────────────────────────────────────────────────────────

class PriViPhoneScanner:

    def scan(self, phone_number: str):
        try:
            # ── Step 1: Parse & validate ──────────────────────────────────────
            parsed = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(parsed):
                console.print(
                    "[bold red][!] Validation failed: number is invalid or inactive.[/bold red]"
                )
                return

            clean = phonenumbers.format_number(
                parsed, phonenumbers.PhoneNumberFormat.E164
            )
            raw = clean.replace("+", "")

            # ── Step 2: Carrier intelligence ──────────────────────────────────
            provider = carrier.name_for_number(parsed, "en")

            # Custom Nigerian prefix lookup if standard library returns empty
            if not provider and parsed.country_code == 234:
                prefix   = str(parsed.national_number)[:3]
                provider = NG_CARRIERS.get(prefix, "Private/Internal Node")

            # ── Step 3: Timezone & location ───────────────────────────────────
            tz_list  = timezone.time_zones_for_number(parsed)
            location = geocoder.description_for_number(parsed, "en")
            num_type = phonenumbers.number_type(parsed)
            type_map = {
                phonenumbers.PhoneNumberType.MOBILE:        "Mobile",
                phonenumbers.PhoneNumberType.FIXED_LINE:    "Fixed Line",
                phonenumbers.PhoneNumberType.VOIP:          "VoIP",
                phonenumbers.PhoneNumberType.TOLL_FREE:     "Toll-Free",
                phonenumbers.PhoneNumberType.PREMIUM_RATE:  "Premium Rate",
            }
            num_type_str = type_map.get(num_type, "Unknown")

            # ── Display target intelligence ───────────────────────────────────
            intel = Table(
                title="[bold cyan]Phone Number Intelligence[/bold cyan]",
                border_style="blue", show_lines=True
            )
            intel.add_column("Field",  style="bold white", width=20)
            intel.add_column("Value",  style="cyan")

            intel.add_row("Number (E.164)", clean)
            intel.add_row("Valid",          "[bold green]Yes[/bold green]")
            intel.add_row("Country",
                phonenumbers.region_code_for_number(parsed) or "Unknown")
            intel.add_row("Location",   location or "Unknown")
            intel.add_row("Carrier",    provider or "Unknown")
            intel.add_row("Timezone",   ", ".join(tz_list) if tz_list else "Unknown")
            intel.add_row("Number Type", num_type_str)

            console.print(intel)

            # ── Social investigation links ─────────────────────────────────────
            socials = {
                "TrueCaller":  f"https://www.truecaller.com/search/global/{raw}",
                "WhatsApp":    f"https://wa.me/{raw}",
                "Telegram":    f"https://t.me/+{raw}",
                "LinkedIn":    f"https://www.linkedin.com/search/results/all/?keywords=%2B{raw}",
                "Facebook":    f"https://www.facebook.com/search/top/?q=%2B{raw}",
                "Instagram":   f"https://www.instagram.com/search/?q={raw}",
            }

            social_table = Table(
                title="[bold cyan]Social Investigation Links[/bold cyan]",
                border_style="blue", show_lines=True
            )
            social_table.add_column("Platform", style="bold white", width=14)
            social_table.add_column("Investigation URL", style="blue")
            for platform, url in socials.items():
                social_table.add_row(platform, url)
            console.print(social_table)

            # ── Google dork ───────────────────────────────────────────────────
            dork_query = (
                f'"{raw}" site:pastebin.com OR site:ghostbin.com OR '
                f'site:raidforums.com OR site:nairaland.com OR site:jiji.ng'
            )
            dork_url = f"https://www.google.com/search?q={urllib.parse.quote(dork_query)}"

            dork_text = Text()
            dork_text.append("Forum & Leak Archive Dork\n\n", style="bold white")
            dork_text.append(f"  {dork_url}\n", style="yellow")
            console.print(Panel(dork_text, border_style="red",
                                title="[bold red]Google Dork[/bold red]"))

            # ── Map generation ────────────────────────────────────────────────
            generate_intel_map(location or "Nigeria", phone_number)

            console.print(
                "\n[bold green][✔] Recon complete. PriViSecurity standing by.[/bold green]"
            )
            console.print(
                "[dim]Tip: Check WhatsApp for a profile photo — "
                "use Google Lens to reverse-search it.[/dim]\n"
            )

        except NumberParseException:
            console.print(
                "[bold red][!] Format error: provide the number in international format "
                "(e.g. +2348031234567)[/bold red]"
            )
        except Exception as e:
            console.print(f"[bold red][!] Error: {e}[/bold red]")


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    print_header()
    try:
        target = console.input(
            "[bold cyan]Enter target number[/bold cyan] "
            "[dim](international format, e.g. +2348031234567)[/dim]: "
        ).strip()
        if not target:
            console.print("[bold red][!] No number entered.[/bold red]")
            sys.exit(0)
        scanner = PriViPhoneScanner()
        scanner.scan(target)
    except KeyboardInterrupt:
        console.print("\n[bold yellow][!] Session terminated.[/bold yellow]")
        sys.exit(0)


if __name__ == "__main__":
    main()
