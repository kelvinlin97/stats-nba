# defensive rating effect on wins 

import numpy as np

import matplotlib.pyplot as plt

import csv

from scipy import stats

rng = np.random.default_rng()

with open('player_stats.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile)

    categories = csvreader[0]
    annual_off_rtg = {}
    for i in range(1, len(csvreader)):
        # offense: (pts * fg%) + 0.5(ast) + 0.5(rebounds) 
            # measure by year
        # defense: steals + blocks 
        ortg = 0
        drtg = 0
        for j in range(len(csvreader[i])):
            if categories[j] == ''
        age = csvreader[i][0]
        annual_off_rtg[age] = ortg