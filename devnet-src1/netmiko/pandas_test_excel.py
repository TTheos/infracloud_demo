import pandas as pd

data = {
    "Hostname": ["Cat8K"],
    "IOS Version": ["17.9.2a"],
    "Uptime": ["2h56m"],
    "Interfaces": [3]
}

df = pd.DataFrame(data)
df.to_excel("device_report.xlsx", index=False)

print("Excel bestand gemaakt!")
