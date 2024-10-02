import requests
from bs4 import BeautifulSoup
import pandas as pd

"""
This tool grabs a players career statistics - when prompted, enter the url for the player's basketball reference page and we'll 
"""

# URL for the player's stats
url = 'https://www.basketball-reference.com/players/a/abdulka01.html'

# Set headers to mimic a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
}

# Send a GET request to the page with headers
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing the player's stats
    table = soup.find('table', {'id': 'per_game'})  # Adjust 'id' for different stat categories

    # Extract table headers
    headers = [th.text for th in table.find('thead').find_all('th')][1:]  # Skip the first empty 'th'

    # Extract the player stats from the table rows
    rows = table.find('tbody').find_all('tr')

    # Prepare list to store player data
    player_stats = []

    # Loop through rows to extract player stats
    for row in rows:
        season_stats = [td.text for td in row.find_all('td')]
        if season_stats:
            player_stats.append(season_stats)

    # Convert data into a DataFrame for easier analysis
    df = pd.DataFrame(player_stats, columns=headers)

    # Display the DataFrame
    print(df)

    # Optionally, save the DataFrame to a CSV file
    df.to_csv('player_stats.csv', index=False)
else:
    print(f"Failed to retrieve data: {response.status_code}")
