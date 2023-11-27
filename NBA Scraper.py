import requests
import pandas as pd
from bs4 import BeautifulSoup

# Scraping data from the first URL
url1 = "https://www.basketball-reference.com/leagues/NBA_2024_per_game.html"
r1 = requests.get(url1)
soup1 = BeautifulSoup(r1.text, "html.parser")
rows1 = soup1.find("table", {"id": "per_game_stats"}).find("tbody").findAll("tr")

player_data = []
for row in rows1:
    if row.find("td"):
        dic = {}
        dic["Name"] = row.findAll("td")[0].text
        dic["Position"] = row.findAll("td")[1].text
        dic["Age"] = int(row.findAll("td")[2].text)
        dic["team"] = row.findAll("td")[3].text
        dic["Games played"] = int(row.findAll("td")[4].text)
        dic["Games started"] = int(row.findAll("td")[5].text)
        dic["Minutes per game"] = float(row.findAll("td")[6].text)
        dic["Assists per game"] = float(row.findAll("td")[23].text)
        dic["Steals per game"] = float(row.findAll("td")[24].text)
        dic["Blocks per game"] = float(row.findAll("td")[25].text)
        dic["Points per game"] = float(row.findAll("td")[28].text)
        player_data.append(dic)

df = pd.DataFrame(player_data)

# Scraping data from the second URL
url2 = "https://www.basketball-reference.com/leagues/NBA_2024_advanced.html"
r2 = requests.get(url2)
soup2 = BeautifulSoup(r2.text, "html.parser")
rows2 = soup2.find("table", {"id": "advanced_stats"}).find("tbody").findAll("tr")

player_data2 = []
for row in rows2:
    if row.find("td"):
        dic = {}
        dic["Name"] = row.findAll("td")[0].text
        dic["Minutes played"] = row.findAll("td")[5].text
        dic["PER"] = row.findAll("td")[6].text
        dic["TS%"] = row.findAll("td")[7].text
        dic["AST%"] = row.findAll("td")[13].text
        dic["STL%"] = row.findAll("td")[14].text
        dic["BLK%"] = row.findAll("td")[15].text
        dic["TO%"] = row.findAll("td")[16].text
        dic["USG%"] = row.findAll("td")[17].text
        dic["OWS"] = row.findAll("td")[19].text
        dic["DWS"] = row.findAll("td")[20].text
        dic["WS"] = row.findAll("td")[21].text
        dic["WS/48"] = row.findAll("td")[22].text
        dic["VORP"] = row.findAll("td")[27].text
        player_data2.append(dic)

df2 = pd.DataFrame(player_data2)

# Scraping data from the third URL
url3 = "https://www.basketball-reference.com/contracts/players.html"
r3 = requests.get(url3)
soup3 = BeautifulSoup(r3.text, "html.parser")

rows3 = soup3.find("table", {"id": "player-contracts"}).find("tbody").findAll("tr")

player_salaries = []
for row in rows3:
    if row.find("td"):
        dic = {}
        dic["Name"] = row.findAll("td")[0].text
        dic["Salary"] = row.findAll("td")[2].text
        player_salaries.append(dic)

df3 = pd.DataFrame(player_salaries)

# Convert the percentage column to decimal format
df2['AST%'] = pd.to_numeric(df2['AST%']) / 100
df2['STL%'] = pd.to_numeric(df2['STL%']) / 100
df2['BLK%'] = pd.to_numeric(df2['BLK%']) / 100
df2['TO%'] = pd.to_numeric(df2['TO%']) / 100
df2['USG%'] = pd.to_numeric(df2['USG%']) / 100

# Merge DataFrames based on the "Name" column using inner join & Save the merged DataFrame to a new CSV file
merged_df = pd.merge(df, df2, on="Name", how="inner")
merged_df = pd.merge(merged_df, df3, on="Name", how="inner")
merged_df.to_csv("merged_data.csv", index=False)