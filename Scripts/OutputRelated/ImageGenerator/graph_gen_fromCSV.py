#
# This Python File generates the graphs with the solutions from the raw output files
#
# Run it with "python3 graph_gen_fromCSV.py Time Input/Merged/merged_cleaned.csv".
#

import os
import re
from pathlib import Path
import sys
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import functools
import csv



if __name__ == '__main__':

    plotting_val = (sys.argv[1])
    csv_file = (sys.argv[2])

    print(f"Plotting value is \"{plotting_val}\"")
    print(f"Plotting file is \"{csv_file}\"")


    plt.rcParams["figure.figsize"] = [14.00, 8.00]
    plt.rcParams["figure.autolayout"] = True
    # Make a list of columns

   # mydata = ["Fast Downward",'SOFAIxPlansformers','SOFAIxPlanning', 'Jaccard']



    with open(csv_file) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                headers = row
                break

    mydata = []
    suffixes = []
    for elem in headers:
        if re.match(rf"{plotting_val}-.+", elem):
            mydata.append(elem)
            suffixes.append(re.sub(rf"{plotting_val}-(.+)", r"\1", elem))

    columns = mydata
    styles = ['o', 'x', 'h' , '^', 'D']

    df = pd.read_csv(csv_file, usecols=columns)

    if plotting_val == "Time":
        df[columns] = df[columns] / 1000

    # Plot the lines
    df.plot(y=columns, style=styles, figsize=(12,4),color=['black','limegreen','tab:blue','tab:orange','tab:red'])
    #plt.title(plotting_val + " comparsion between Fast and Slow Arch. and FD", weight='bold')
    # label the x and y axes
    plt.xlabel('Instances', weight='bold', size='large')
    if plotting_val == "Time":
        plt.ylabel(plotting_val + (" (s)"), weight='bold', size='large')
    else:
        plt.ylabel(plotting_val, weight='bold', size='large')
    #plt.legend(['Jac','Plf','SOFAIxPlanning','FD'])

    #n_inst = 100
    #plt.axvspan(0, 99, color='red', alpha=0.2)
    #plt.axvspan(100, 199, color='green', alpha=0.2)
    #plt.axvspan(200, 299, color='yellow', alpha=0.2)
    #plt.axvspan(300, 399, color='blue', alpha=0.2)
    #plt.axvspan(400, 499, color='orange', alpha=0.2)

    plt.legend(prop={'size': 18})
    plt.legend(labels=suffixes)
    #plt.xlim(1, 240)
    #plt.ylim(1, 900000)

    #plt.yscale('log')
    Path("Output").mkdir(parents=True,exist_ok=True)
    plt.savefig("Output/"+plotting_val+"-Plot.png")



