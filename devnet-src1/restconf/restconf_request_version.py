import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

# ======= DEVICE INFO INVULLEN =======
host = "devnetsandboxiosxec8k.cisco.com"    # <-- jouw URL hier
username = "theos.tungunkonda"                           # standaard DevNet credentials
password = "9__AMkZ6xdM49o!"                       # standaard DevNet credentials

# Volledige RESTCONF URL
url = f"https://{host}:443/restconf/data/ietf-interfaces:interfaces"

# ======= HEADERS =======
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

# ======= SSL WARNING UIT =======
requests.packages.urllib3.disable_warnings()
verify_ssl = False

print(f"→ Verbinden naar RESTCONF: {url}")

# ======= RESTCONF REQUEST =======
response = requests.get(
    url,
    headers=headers,
    auth=HTTPBasicAuth(username, password),
    verify=verify_ssl
)

print("Status code:", response.status_code)

# Als JSON mislukt → tekst printen
try:
    data = response.json()
except:
    print("\nGeen JSON ontvangen:")
    print(response.text)
    exit()

print("\nRESTCONF Interface JSON ontvangen.")
print(data)

# ======= PARSING VOOR EXCEL =======
interfaces = data.get("ietf-interfaces:interfaces", {}).get("interface", [])

rows = []
for intf in interfaces:
    rows.append({
        "Name": intf.get("name"),
        "Enabled": intf.get("enabled"),
        "Type": intf.get("type"),
        "IPv4": str(intf.get("ietf-ip:ipv4")),
        "IPv6": str(intf.get("ietf-ip:ipv6"))
    })

df = pd.DataFrame(rows)

# ======= EXCEL EXPORT =======
excel_file = "restconf_inventory.xlsx"

with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Interfaces", index=False)

print(f"\nExcel bestand gemaakt: {excel_file}")
