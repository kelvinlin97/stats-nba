import os
import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, 
                             QScrollArea, QGridLayout, QMessageBox, QMainWindow, QFrame)
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt
from scipy import stats

# Function to fetch player stats and save to a folder
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

            if not os.path.exists('player_stats'):
                os.makedirs('player_stats')

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_name = f'player_stats/player_stats_{timestamp}.csv'
            df.to_csv(file_name, index=False)
            return file_name
        else:
            return None
    else:
        return None

# Function to analyze player rating
def analyze_player_rating(file_name):
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

    slope, intercept, r_value, p_value, std_err = stats.linregress(offense, defense)

    plt.scatter(offense, defense, color='blue', label='Data points')
    regression_line = [slope * x + intercept for x in offense]
    plt.plot(offense, regression_line, color='red', label='Regression line')
    plt.xlabel('Offense')
    plt.ylabel('Defense')
    plt.title(f'Offense vs Defense (r={r_value:.2f})')
    plt.legend()
    plt.show()

# Clickable QLabel for Images
class ClickableLabel(QLabel):
    def __init__(self, parent=None, url=None):
        super().__init__(parent)
        self.url = url

    def mousePressEvent(self, event):
        if self.url:
            file_name = fetch_player_stats(self.url)
            if file_name:
                QMessageBox.information(self, 'Success', f'Data saved to {file_name}')
                analyze_player_rating(file_name)
            else:
                QMessageBox.critical(self, 'Error', 'Failed to retrieve stats. Please check the URL.')

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'NBA Stats Analyzer'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 600, 600)

        # Set background image
        self.set_background_image('public/background.jpg')

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        container_widget = QWidget()
        scroll.setWidget(container_widget)

        layout = QVBoxLayout(container_widget)

        grid_frame = QFrame()
        grid_layout = QGridLayout()

        label = QLabel('Click on a player image to fetch stats:', self)
        layout.addWidget(label)

        pixmap1 = QPixmap('public/cp3.jpg')
        image1 = ClickableLabel(self, url='https://www.basketball-reference.com/players/p/paulch01.html')
        image1.setPixmap(pixmap1)
        image1.setScaledContents(True)
        image1.setFixedSize(150, 150)
        grid_layout.addWidget(image1, 0, 0)

        pixmap2 = QPixmap('public/kd.jpg')
        image2 = ClickableLabel(self, url='https://www.basketball-reference.com/players/d/duranke01.html')
        image2.setPixmap(pixmap2)
        image2.setScaledContents(True)
        image2.setFixedSize(150, 150)
        grid_layout.addWidget(image2, 0, 1)

        pixmap3 = QPixmap('public/lebron.jpg')
        image3 = ClickableLabel(self, url='https://www.basketball-reference.com/players/j/jamesle01.html')
        image3.setPixmap(pixmap3)
        image3.setScaledContents(True)
        image3.setFixedSize(150, 150)
        grid_layout.addWidget(image3, 0, 2)

        pixmap4 = QPixmap('public/jamesharden.jpg')
        image4 = ClickableLabel(self, url='https://www.basketball-reference.com/players/h/hardeja01.html')
        image4.setPixmap(pixmap4)
        image4.setScaledContents(True)
        image4.setFixedSize(150, 150)
        grid_layout.addWidget(image4, 1, 0)

        pixmap5 = QPixmap('public/jokic.jpg')
        image5 = ClickableLabel(self, url='https://www.basketball-reference.com/players/j/jokicni01.html')
        image5.setPixmap(pixmap5)
        image5.setScaledContents(True)
        image5.setFixedSize(150, 150)
        grid_layout.addWidget(image5, 1, 1)

        pixmap6 = QPixmap('public/lamelo.jpg')
        image6 = ClickableLabel(self, url='https://www.basketball-reference.com/players/b/ballla01.html')
        image6.setPixmap(pixmap6)
        image6.setScaledContents(True)
        image6.setFixedSize(150, 150)
        grid_layout.addWidget(image6, 1, 2)

        pixmap7 = QPixmap('public/jrueholiday.jpg')
        image7 = ClickableLabel(self, url='https://www.basketball-reference.com/players/h/holidjr01.html')
        image7.setPixmap(pixmap7)
        image7.setScaledContents(True)
        image7.setFixedSize(150, 150)
        grid_layout.addWidget(image7, 2, 0)

        pixmap8 = QPixmap('public/zion.jpg')
        image8 = ClickableLabel(self, url='https://www.basketball-reference.com/players/w/willizi01.html')
        image8.setPixmap(pixmap8)
        image8.setScaledContents(True)
        image8.setFixedSize(150, 150)
        grid_layout.addWidget(image8, 2, 1)

        pixmap9 = QPixmap('public/embiid.jpg')
        image9 = ClickableLabel(self, url='https://www.basketball-reference.com/players/e/embiijo01.html')
        image9.setPixmap(pixmap9)
        image9.setScaledContents(True)
        image9.setFixedSize(150, 150)
        grid_layout.addWidget(image9, 2, 2)

        pixmap10 = QPixmap('public/alleniverson.jpg')
        image10 = ClickableLabel(self, url='https://www.basketball-reference.com/players/i/iversal01.html')
        image10.setPixmap(pixmap10)
        image10.setScaledContents(True)
        image10.setFixedSize(150, 150)
        grid_layout.addWidget(image10, 3, 0)

        pixmap11 = QPixmap('public/jaylenbrown.jpg')
        image11 = ClickableLabel(self, url='https://www.basketball-reference.com/players/b/brownja02.html')
        image11.setPixmap(pixmap11)
        image11.setScaledContents(True)
        image11.setFixedSize(150, 150)
        grid_layout.addWidget(image11, 3, 1)

        pixmap12 = QPixmap('public/yaoming.jpg')
        image12 = ClickableLabel(self, url='https://www.basketball-reference.com/players/m/mingya01.html')
        image12.setPixmap(pixmap12)
        image12.setScaledContents(True)
        image12.setFixedSize(150, 150)
        grid_layout.addWidget(image12, 3, 2)

        grid_frame.setLayout(grid_layout)
        layout.addWidget(grid_frame)

        self.setCentralWidget(scroll)

    def set_background_image(self, image_path):
        o_image = QPixmap(image_path)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(o_image.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        self.setPalette(palette)

    def resizeEvent(self, event):
        self.set_background_image('public/basketball.jpg')
        super().resizeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
