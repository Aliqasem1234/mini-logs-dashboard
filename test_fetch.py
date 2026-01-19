# test_fetch.py
from fetch_logs import hamta_loggar

df = hamta_loggar(10)
print(df)          # skriv ut i terminalen
print("––––––––––")
print(df.info())   # kolumninfo