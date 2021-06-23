"""
This script was created for the E-Challenge Machine Learning Workshop on June 22.
The origial job belongs to a Git-Hub repository owned by Andy McDonald: 
https://github.com/andymcdgeo/Petrophysics-Python-Series/blob/master/07%20-%20Working%20With%20LASIO.ipynb


This function takes as parameter the entire dataset and uses the length of the columns to iterate through the features instead of 
declaring repeated code for each axes.

Author: Felix Gallo
"""

"""Numpy, pandas and matplotlib.pyplot are needed to run this function.
"""   

def log_view(df):
    
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd 


    params = df.keys().drop('DEPT')
    f, ax = plt.subplots(nrows=1, ncols=len(params), figsize=(15,10))
    
    ax[0] = plt.subplot2grid((1,5), (0,0)) 
    ax[1] = plt.subplot2grid((1,5), (0,1)) 
    ax[2] = plt.subplot2grid((1,5), (0,2)) 
    ax[3] = plt.subplot2grid((1,5), (0,3)) 
    ax[4] = ax[3].twiny()
    ax[5] = plt.subplot2grid((1,5), (0,4))  
    ax[6] = ax[5].twiny()  
    
    for i in range(0,len(params)):
    
        name = df[params[i]].name  
        
        if name == 'GR':
          i = 0
          color = 'green'
          label = 'Gamma'
          min,max = 0, 200
          xticks = np.round(np.linspace(min,max,5),0)    
        
        if name == 'CALI':
          i = 1
          color = 'black'
          label = 'Caliper'
          min,max = 6, 16
          xticks = np.round(np.linspace(min,max,5),0)    
        
        if name == 'AC':
          i = 2
          color = 'purple'
          label = 'Sonic'
          min,max = 40, 140   
          xticks = np.round(np.linspace(min,max,5),0)
        
        if name == 'DEN':
          i = 3
          color = 'red'
          label = 'Density'
          min,max = 1, 3
          xticks = np.round(np.linspace(min,max,5),0)
        
        if name == 'NEU':
          i = 4
          color = 'blue'
          label = 'Porosity'
          min,max = 45, -15
          xticks = np.round(np.linspace(min,max,5),0)
        
        if name == 'RDEP':
          i = 5
          color = 'black'
          label = 'Deep RT'
          min,max = 0,2000
          xticks = [0.1, 1, 10, 100, 1000]
        
        if name == 'RMED':
          i = 6
          color = '#79f44a'
          label = 'Med RT'
          min,max = 0,2000
          xticks = [0.1, 1, 10, 100, 1000]
        
        ax[i].plot(df[name], df.DEPT, color=color, lw=0.7)
        if i== 5 or i==6:
          ax[i].semilogx()
        
        ax[i].set_xlabel(label,fontsize=14) 
        ax[i].set_xlim(min, max)       
        ax[i].xaxis.label.set_color(color)    
        ax[i].tick_params(axis='x', colors=color)
        ax[i].set_xticks(xticks)
        ax[i].xaxis.set_ticks_position('top')
        ax[i].xaxis.set_label_position('top')  
        
        ax[i].set_ylim(df.DEPT.min(),4500)
        ax[i].invert_yaxis()
        ax[i].grid(True,linewidth=0.4)
        
        
        ax[i].spines['top'].set_position(('outward', 10))
        ax[i].spines["top"].set_visible(True)
        ax[i].spines["top"].set_edgecolor(color)
        
        if i == 3 or i == 5:
          ax[i].spines["bottom"].set_position(("axes", -0.02))
          ax[i].spines["bottom"].set_edgecolor(color)
          ax[i].xaxis.set_ticks_position('bottom')
          ax[i].xaxis.set_label_position('bottom')
        
        if i+1<len(params):
          ax[i+1].set_yticklabels([])  