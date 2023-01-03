import ast

# Dictionaries and Lists

# Clan Dictionary
with open('files/Clans.txt', encoding="utf8") as f:
    clans_data = f.read()
Dict_Clans = ast.literal_eval(clans_data)

# Flag Dictionary
with open('files/Flags.txt') as g:
    flags_data = g.read()
Dict_Flags = ast.literal_eval(flags_data)

# Dict for Players with multiple names
with open('files/Multiple Names.txt') as m:
    names_data = m.read()
Dict_MultipleNames = ast.literal_eval(names_data)

# Skins
with open('files/Skins.txt') as s:
    skins_data = s.read()
skins = ast.literal_eval(skins_data)

# Youtube Playlist
with open('files/Videos.txt') as v:
    videos_data = v.read()
videos = ast.literal_eval(videos_data)

# Quotes
with open('files/Quotes.txt') as q:
    quotes_data = q.read()
quotes = ast.literal_eval(quotes_data)

# Clan Skins
with open('files/Clan Skins.txt') as c:
    clan_skins_data = c.read()
clan_skins = ast.literal_eval(clan_skins_data)

# Duplicate Names
with open('files/Duplicates.txt') as d:
    duplicates_data = d.read()
duplicates = ast.literal_eval(duplicates_data)

# Supporters
with open('files/Supporters.txt') as d:
    supporters_data = d.read()
supporters = ast.literal_eval(supporters_data)

# Clan Leaderboard
with open('files/Leaderboard.txt') as d:
    leaderboard_data = d.read()
leaderboard = ast.literal_eval(supporters_data)
