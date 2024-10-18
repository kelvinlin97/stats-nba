import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox)

from scipy import stats

# Function to fetch player stats
def fetch_player_stats(url):
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

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_name = f'player_stats_{timestamp}.csv'
            df.to_csv(file_name, index=False)
            return file_name
        else:
            return None
    else:
        return None

# Function to analyze defensive rating
def analyze_defensive_rating(file_name):
    fg_pct_yrs, pts, asts, rebs, stls, blks = [], [], [], [], [], []

    with open(file_name, newline='') as csvfile:
        csvreader = pd.read_csv(csvfile)
        for idx, row in csvreader.iterrows():
            if pd.notna(row['FG%']):
                fg_pct_yrs.append(float(row['FG%']))
            if pd.notna(row['PTS']):
                pts.append(float(row['PTS']))
            if pd.notna(row['TRB']):
                rebs.append(float(row['TRB']))
            if pd.notna(row['AST']):
                asts.append(float(row['AST']))
            if pd.notna(row['STL']):
                stls.append(float(row['STL']))
            if pd.notna(row['BLK']):
                blks.append(float(row['BLK']))

    effective_pts = [a * b for a, b in zip(fg_pct_yrs, pts)]
    offense = [a + b + c for a, b, c in zip(rebs, effective_pts, asts)]
    defense = [a + b for a, b in zip(stls, blks)]

    # Linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(offense, defense)

    # Plot
    plt.scatter(offense, defense, color='blue', label='Data points')
    regression_line = [slope * x + intercept for x in offense]
    plt.plot(offense, regression_line, color='red', label='Regression line')
    plt.xlabel('Offense')
    plt.ylabel('Defense')
    plt.title(f'Offense vs Defense (r={r_value:.2f})')
    plt.legend()
    plt.show()

# PyQt5 GUI Application
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'NBA Stats Analyzer'
        self.initUI()

    def initUI(self):
        # Window settings
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 400, 200)

        # Layout
        layout = QVBoxLayout()

        # Label
        self.label = QLabel('Enter the player URL from basketball-reference.com:', self)
        layout.addWidget(self.label)

        # Input field for URL
        self.url_input = QLineEdit(self)
        layout.addWidget(self.url_input)

        # Button to Fetch and Analyze
        self.button = QPushButton('Fetch Stats and Analyze', self)
        self.button.clicked.connect(self.on_click)
        layout.addWidget(self.button)

        # Set layout
        self.setLayout(layout)

    def on_click(self):
        url = self.url_input.text()
        if url:
            file_name = fetch_player_stats(url)
            if file_name:
                QMessageBox.information(self, 'Success', f'Data saved to {file_name}')
                analyze_defensive_rating(file_name)
            else:
                QMessageBox.critical(self, 'Error', 'Failed to retrieve stats. Please check the URL.')
        else:
            QMessageBox.warning(self, 'Input Required', 'Please enter a player URL.')

# Main function to run the PyQt5 application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
