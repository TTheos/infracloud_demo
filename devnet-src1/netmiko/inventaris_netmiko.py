import datetime
import pandas as pd
from netmiko import ConnectHandler

print("=== DEVICE INVENTARIS ===")
print("Timestamp:", datetime.datetime.now())

device = {
    "device_type": "cisco_ios",
    "host": "devnetsandboxiosxec8k.cisco.com",
    "port": "22",
    "username": "theos.tungunkonda",
    "password": "Mw1G-Nepsr5-78"
}

ssh = ConnectHandler(**device)
print("\n[+] Verbonden via SSH...")

# Commando’s
commands = {
    "show_version": "show version",
    "show_ip_br": "show ip interface brief",
    "show_ip_route": "show ip route",
    "show_ip_proto": "show ip protocols",
    "show_cdp": "show cdp neighbors"
}

raw = {}
for key, cmd in commands.items():
    print(f"[+] Executing: {cmd}")
    raw[key] = ssh.send_command(cmd)

ssh.disconnect()

# -------------------------
# PARSING
# -------------------------
info = {}
output = raw["show_version"]

for line in output.splitlines():
    if "Cisco IOS Software" in line:
        info["IOS Version"] = line.strip()
    if "uptime" in line:
        info["Hostname"] = line.split()[0]
        info["Uptime"] = line.strip()

# Interfaces → DataFrame
interfaces = []
for line in raw["show_ip_br"].splitlines():
    if "Interface" in line or "-----" in line:
        continue
    parts = line.split()
    if len(parts) >= 6:
        interfaces.append({
            "Interface": parts[0],
            "IP": parts[1],
            "OK": parts[2],
            "Method": parts[3],
            "Status": parts[4],
            "Protocol": parts[5]
        })

df_interfaces = pd.DataFrame(interfaces)

# Routing Table (raw)
df_route = pd.DataFrame(raw["show_ip_route"].splitlines(), columns=["Routing"])

# CDP
df_cdp = pd.DataFrame(raw["show_cdp"].splitlines(), columns=["CDP"])

# Device Info
df_info = pd.DataFrame([info])

# EXCEL EXPORTS
with pd.ExcelWriter("device_inventory.xlsx", engine="openpyxl") as writer:
    df_info.to_excel(writer, sheet_name="Device Info", index=False)
    df_interfaces.to_excel(writer, sheet_name="Interfaces", index=False)
    df_route.to_excel(writer, sheet_name="Routing", index=False)
    df_cdp.to_excel(writer, sheet_name="CDP", index=False)

print("\nInventaris klaar → opgeslagen als: device_inventory.xlsx")
