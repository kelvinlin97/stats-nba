import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy import stats

def fetch_player_stats():
    """
    This tool grabs a player's career statistics from basketball-reference.com.
    You will be prompted to enter the URL for the player's basketball reference page.
    """

    url = input("Enter the URL for the player's basketball-reference page: ")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table', {'id': 'per_game'})  

        if table:
            headers = [th.text for th in table.find('thead').find_all('th')][1:]  

            rows = table.find('tbody').find_all('tr')

            player_stats = []

            for row in rows:
                season_stats = [td.text for td in row.find_all('td')]
                if season_stats:
                    player_stats.append(season_stats)
            df = pd.DataFrame(player_stats, columns=headers)

            print(df)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_name = f'player_stats_{timestamp}.csv'

            df.to_csv(file_name, index=False)
            print(f"Data saved to {file_name}")
            return file_name
        else:
            print("Could not find the stats table. Please check the URL.")
            return None
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None


def analyze_player_rating(file_name):
    """
    Analyzes the player's offensive and defensive statistics based on the fetched data.
    """
    fg_pct_yrs = []
    pts = []
    asts = []
    rebs = []
    stls = []
    blks = []
    awards = []
    
    with open(file_name, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for idx, row in enumerate(csvreader):
            if len(row) > 9:
                fg_pct_by_yr = row[9]
                if fg_pct_by_yr == 'FG%':
                    continue
                if float(fg_pct_by_yr):
                    fg_pct_yrs.append(float(fg_pct_by_yr))
            if len(row) > 21:
                reb = row[21]
                if fg_pct_by_yr == 'TRB':
                    continue
                if reb and float(reb):
                    rebs.append(float(reb))
            if len(row) > 22:
                ast = row[22]
                if float(ast):
                    asts.append(float(ast))
            if len(row) > 23:
                stl = row[23]
                if float(stl) and stl:
                    stls.append(float(stl))
            if len(row) > 24:
                blk = row[24]
                if blk and float(blk):
                    blks.append(float(blk))
            if len(row) > 28:
                pt_by_yr = row[28]
                if float(pt_by_yr):
                    pts.append(float(pt_by_yr))
            if len(row) > 29:
                award = len(row[29])
                awards.append(int(award))

    effective_pts = [a * b for a, b in zip(fg_pct_yrs, pts)]
    offense = [a + b + c for a, b, c in zip(rebs, effective_pts, asts)]
    defense = [a + b for a, b in zip(stls, blks)]

    slope, intercept, r, p, std_err = stats.linregress(offense, defense)
    print(f"Correlation coefficient (r): {r}")

    plt.scatter(offense, defense, color='blue', label='Data points')
    
    regression_line = [slope * x + intercept for x in offense]
    
    plt.plot(offense, regression_line, color='red', label='Regression line')
    plt.xlabel('Offense')
    plt.ylabel('Defense')
    plt.title(f'Offense vs Defense (r={r})')
    plt.show()

file_name = fetch_player_stats()
if file_name:
    analyze_player_rating(file_name)
