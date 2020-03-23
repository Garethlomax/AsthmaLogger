#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 13:12:06 2020

@author: garethlomax
"""


#quick script for monitoring peak flow 

import pandas as pd 
import matplotlib.pyplot as plt
import argparse 
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()




def make_dataframe(quants = ['peakflow, spo2']):
    """Make inital dataframe for the logging program"""
    columns = ['time'] + quants
    
    df = pd.DataFrame(columns=columns, index=pd.to_datetime([]))
    
    return df

def plot(df, save = True, show = True):
    """plots health history as pdf, will accept multiple keywords for variables 
    to plot """
    
    fig, ax = plt.subplots(figsize=(10, 10))
    # Add x-axis and y-axis
    ax.set_xlim(df.index.values[0], df.index.values[-1])
    ax.scatter(df.index.values,
        df['peakflow'],
        color='purple')
    
    ax.plot(df.index.values,
        df['peakflow'],
        color='blue')

    
    if save == True:
        plt.savefig("plot.png")
    
    if show == True:
        plt.show()
    
def log(df, data, quants):
    df.loc[pd.Timestamp('now')] = pd.Series([pd.Timestamp('now')] + data, ['time'] + quants)
                                             

def deleteall(df):
    """clears content of dataframe"""
    df.drop(df.index, inplace=True)




## parsinbg stuff 
#got rid of extend as no longer in python 3.8 - will add later for backwards compatabiltiy   
parser = argparse.ArgumentParser(description = "Extract symptom data and keys from command line")
parser.add_argument('--quantities', nargs = '+', type = str)
parser.add_argument('--data', nargs = '+', type = float)
parser.add_argument('--plot', action = 'store_true')
parser.add_argument('--savep', action = 'store_true')
parser.add_argument('--csv', action = 'store_true')
parser.add_argument('--show', action = 'store_true')
parser.add_argument('--deleteall', action = 'store_true')
parser.add_argument('--confirm', action = 'store_true')

def main():
    """main scripty for saving health information"""
    args = parser.parse_args()
    print(args)
    
    df = pd.read_pickle("~/Health/AsthmaLogger/peakflow.pkl")
    
    if (args.confirm == True) and (args.deleteall == True):
        deleteall(df)
        
    if (args.data != None) and (args.quantities != None):
        log(df, args.data, args.quantities) #log the data
    
    if args.plot:
        plot(df, save = args.savep, show = args.show)
        
    if args.csv:
        df.to_csv("peakflow.csv")
        
    df.to_pickle("~/Health/AsthmaLogger/peakflow.pkl")
    

if __name__ == "__main__":
    main()
