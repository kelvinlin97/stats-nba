# defensive rating effect on wins 

import numpy as np

import matplotlib.pyplot as plt

import csv

from scipy import stats

from sklearn.linear_model import LinearRegression

import seaborn as sns

import pandas as pd

import matplotlib.pyplot as plt

rng = np.random.default_rng()

with open('player_stats.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    
    # idx 9 


    fg_pct_yrs = []
    pts = []
    asts = []
    rebs = []
    stls = []
    blks = []
    awards = []
    
    for idx, row in enumerate(csvreader):
        if len(row) > 9:
            fg_pct_by_yr = row[9]
            print(fg_pct_by_yr)
            if int(fg_pct_by_yr):
                fg_pct_yrs.append(int(fg_pct_by_yr))
        if len(row) > 21:
            reb = row[21]
            if reb.isdigit():
                rebs.append(int(reb))
        if len(row) > 22:
            ast = row[22]
            if ast.isdigit():
                asts.append(int(ast))
        if len(row) > 23:
            stl = row[23]
            if stl.isdigit():
                stls.append(int(stl))
        if len(row) > 24:
            blk = row[24]
            if blk.isdigit():
                blks.append(int(blk))
        if len(row) > 27:
            pt_by_yr = row[27]
            if pt_by_yr.isdigit():
                pts.append(int(pt_by_yr))
        if len(row) > 28:
            award = len(row[28])
             
            awards.append(int(award))

    # effect of defense vs offense vs age on awards
            
    print(fg_pct_yrs)

    effective_pts = [a * b for a, b in zip(fg_pct_yrs, pts)]
    print(effective_pts)
    offense = [a + b + c for a, b, c in zip(rebs, effective_pts, asts)]
    defense = [a + b for a,b in zip(stls, blks)]

    # category: age
    # independent variables: offense, defense
    # dependent variables: awards

    print(len(offense), len(awards))
    print(len(defense))
    plt.scatter(offense,awards[1:])
    plt.scatter(defense,awards[1:])
    plt.show()
    
    
