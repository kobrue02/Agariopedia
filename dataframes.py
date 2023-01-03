import pandas as pd

# Respective DataFrames for each field

# Spreadsheet Players
sheet_id = '1Uy0-I4236Vl8sd7v20dq4hrL7oO_Cbfj6hsr72XTpx8'
player_data = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv", on_bad_lines='skip')

# Spreadsheet Clans
sheet_clans_id = '1RDbzc5zDkGC9RP-mfDmbNPwPN_cy6-ypdG_1ZVzfr44'
clan_data = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_clans_id}/export?format=csv")

# Spreadsheet Tournaments
sheet_tourneys_id = '1vzJbjbPCHw18NN8prvcNSFQr5lLpmpOWv2kCrzFwUnY'
tourney_data = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_tourneys_id}/export?format=csv")
