
# The following set of functions are defined to show data distribution and well log behaviour of the FORCE 2020 ML Challenge 
# Both of them were created by Felix Gallo, and they were used for demostration in the 
# Workshop day-3 of the E-challenge ML edition from the SPE Ecuador Section

# The original plot function from which I was inspired belongs to Alessandro Amato del Monte's work: 
# https://github.com/aadm/geophysical_notes/blob/master/seismic_petrophysics.ipynb

################################### Plot Distributions/Bar charts##################################################
"""
Basic concept: if a column contains continuous values, then it will have good quantity of Unique Values. 
"""



def distr_plotter(df,numeric=False,categorical=False):

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from matplotlib.legend_handler import HandlerBase  
    from matplotlib.text import Text
    from matplotlib.font_manager import FontProperties
    from matplotlib.legend_handler import HandlerBase
    
  # Drop ID Column since it's not relevant for our prediction
    
    for i in df.keys():
      if i == 'WELL':
        df = df.drop('WELL',axis=1)
      else:
        pass

    continuos = [feature for feature in df.keys() if len(df[feature].unique())>100]
    discretes = df.keys().drop(continuos).to_list()

    if numeric == True:    
   
      fig, axs = plt.subplots(nrows=3, ncols=8, figsize=(25, 10))

      df = df.drop(discretes,axis=1)
      axs = axs.ravel()
      cols = df.keys()

      for ax, i in zip(axs, cols):

        ax = sns.distplot(df[i], ax=ax) 
        ax.set_yticks([])
        ax.set_ylabel('')

    elif categorical == True:

      class TextHandler(HandlerBase):
          def create_artists(self, legend, tup ,xdescent, ydescent,
                              width, height, fontsize,trans):
              tx = Text(width/2.,height/2,tup[0], fontsize=fontsize,
                        ha="center", va="center", color=tup[1], fontweight="bold")
              return [tx]        

      fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(30, 20))

      df['FORMATION_CAT'] = df['FORMATION'].astype('category')
      df['FORMATION_CAT'] = df['FORMATION_CAT'].cat.codes
      df['FORMATION_CAT_str'] = [str(i) for i in df['FORMATION_CAT']]

      formation_codes = dict(zip(np.delete(df['FORMATION'].unique(),0), np.delete(df['FORMATION_CAT'].unique(),0)))
      labeldic = dict(zip(np.delete(df['FORMATION_CAT_str'].unique(),0),np.delete(df['FORMATION'].unique(),0)))
      lithofacies = {30000:'Sandstone', 65030:'Sandstone/Shale', 65000:'Shale', 80000:'Marl', 74000:'Dolomite', 70000:'Limestone', 
                      70032:'Chalk', 88000:'Halite', 86000:'Anhydrite', 99000:'Tuff', 90000:'Coal', 93000:'Basement'}   

      del df['FORMATION_CAT']
      del df['FORMATION_CAT_str'] 

      df = df.replace({'FORMATION':formation_codes, 'LL':lithofacies})

      df = df.drop(continuos,axis=1)
      axs = axs.ravel()
      cols = df.keys()

      for ax, i in zip(axs, cols):

        ax = sns.countplot(df[i], ax=ax)  
        ax.set_title(df[i].name+str(':'),loc='left',fontdict={'fontsize': 13,'fontweight': 'bold'})
        ax.set_xlabel(' ')
        ax.set_xticklabels(df[i].unique(),fontproperties=FontProperties(weight='bold',size=12))     
        ax.set_yticks([])
        ax.set_ylabel('')   

        if i == 'FORMATION':
          ax.set_xticklabels(map(str, np.arange(0,69)))
          t = ax.get_xticklabels()
          labels = [labeldic[h.get_text()]  for h in t]
          handles = [(h.get_text(),c.get_fc()) for h,c in zip(t,ax.patches)]
          ax.legend(handles, labels, ncol=11, handler_map={tuple : TextHandler()},prop=dict(size=11.5),loc=0) 
        elif i == 'LL':
          ax.set_title('LITHOLOGY:',loc='left',fontdict={'fontsize': 13,'fontweight': 'bold'})


########################## Class to plot Logs ########################################

class skylog:

  def __init__(self,data):

    import numpy as np
    import pandas as pd

    # Set parameters to be used along the class
    self.data = data

    #-------------------------------- Colours -------------------------------------#            
    self.facies_colors = ['#F4D03F','#F5B041','#DC7633','#6E2C00','#e0301e','#2E86C1','#1B4F72','#f7347a','#AED6F1','#A569BD','#196F3D','#17bebb']    
    self.group_colors = ['#ffff00', '#00ffff','#75ad0a','#000099', '#9fb6cd', '#ff5a1d','#b2071d','#f3bd9d','#a020f0', 
                    '#00a79d','#ff00ff','#000000', '#33ff00',  '#ff9900', '#ffffff']
    self.formation_colors =  ['#ffffff', '#5A37FB', '#E81EFE', '#FD74AC', '#FF2373', '#F74084', '#AC920F', '#B72B78', '#5D47C9', '#F3A495', '#09133E',
                        '#A9CA7A', '#593A00', '#733514', '#A1FB69', '#AF6742', '#D66C50', '#F4617E', '#9928F8', '#84D22F', '#7C1EA8', '#BADCEF',
                        '#774DF9', '#A21FD0', '#6C9AE6', '#5002EC', '#D7C695', '#184ED3', '#FB1F5D', '#DB9085', '#6FEF8D', '#57D10D', '#0E66D1',
                        '#C8D867', '#1547A0', '#4E528A', '#228DE7', '#D807C0', '#91D71A', '#3AFDDF', '#AC128C', '#3898C1', '#8EFA42', '#C9192D',
                        '#D234E7', '#D4AAD5', '#080DC1', '#BE6D32', '#0A8FCA', '#BC7BF1', '#194D6B', '#743B74', '#CA99CA', '#DF9FD5', '#61AA89',
                        '#2C4374', '#8BC4E0', '#45BA49', '#16CB90', '#EF4EE3', '#AB25E9', '#F8D076', '#580282', '#AD0B4C', '#02A49F', '#7308F8',
                        '#34DDCB', '#BDA775', '#368FC6', '#85C1CC']
    #------------------------------- Labels ---------------------------------------#
    self.facies_labels = ['Ss', 'SSh', 'Sh', 'Marl', 'Dol', 'Ls', 'Ch','Hal', 'Anhy','Tuff','Coal','Bsm']
    self.group_labels = ['NORDLAND', 'HORDALAND', 'ROGALAND', 'SHETLAND','CROMER KNOLL','VIKING','VESTLAND',
                    'ZECHSTEIN','HEGRE', 'ROTLIEGENDES', 'TYNE', 'BOKNFJORD','DUNLIN', 'BAAT', 'NaN']      

    #---------------------------- Lithology Codes ---------------------------------#
    self.litho_keys = {30000: 0, 65030: 1, 65000: 2, 80000: 3, 74000: 4, 70000: 5, 70032: 6, 88000: 7, 86000: 8, 99000: 9, 90000: 10, 93000: 11}

    self.lithofacies = {30000:'Sandstone', 65030:'Sandstone/Shale', 65000:'Shale', 80000:'Marl', 
                    74000:'Dolomite', 70000:'Limestone', 70032:'Chalk', 88000:'Halite', 
                    86000:'Anhydrite', 99000:'Tuff', 90000:'Coal', 93000:'Basement'}  

    #----------------------------- Groups Codes -----------------------------------#
    self.group_codes = {'NORDLAND GP.': 0, 'HORDALAND GP.': 1, 'ROGALAND GP.': 2, 'SHETLAND GP.': 3, 'CROMER KNOLL GP.': 4, 'VIKING GP.': 5, 'VESTLAND GP.': 6,
                  'ZECHSTEIN GP.': 7, 'HEGRE GP.': 8, 'ROTLIEGENDES GP.': 9, 'TYNE GP.': 10, 'BOKNFJORD GP.': 11, 'DUNLIN GP.': 12, 'BAAT GP.': 13,
                  self.data['GROUP'].unique()[-1]:14}     

    #---------------------------- Formation Codes ---------------------------------#
    formations = [] 
    for i in self.data['FORMATION'].unique():
      formations.append(i)
    formation_codes = {}
    for i in range(70):
      formation_codes[formations[i]] = i
    
    self.formation_codes = formation_codes

    formation_labels = []
    for i in np.delete(self.data['FORMATION'].unique(),0):
      formation_labels.append(i.rstrip(' Fm.'))

    formation_labels[31] = 'Draupne Sst'
    formation_labels[39] = 'Balder Sst'
    formation_labels[53] = 'Heather Sst'
    formation_labels.insert(0,'NaN')    

    self.formation_labels = formation_labels                                                     

  def encoder(self):

    import numpy as np
    import pandas as pd
	
    # This method will created the columns to be plotted, assinging numerical encoding for each categorical value and returning a copy of the data
    # Since we don't want to modify the original input

    df = self.data.copy()

    #--------------------------- Replace Categoricals -----------------------------#

    df['Facies'] = df['LL'].replace(self.litho_keys)
    df['Groups'] = df['GROUP'].replace(self.group_codes)
    df['Formations'] = df['FORMATION'].replace(self.formation_codes)

    return df

  #-------------------------------- Log Colors ----------------------------------#
  #------------------- Method to assign a random color to Logs-------------------#
  def hex_list(self,num):
    import random      

    hex_codes = ['#000000', '#00a260', '#00a79d', '#000033', '#000066', '#000099', '#0000cc',
                '#e0301e', '#003300', '#003366', '#003399', '#0033cc', '#006600', '#0066ff', 
                '#0066cc', '#009900', '#330000', '#330033', '#330066', '#330099', '#3300cc', 
                '#3333ff', '#339900', '#660000', '#660033', '#660066', '#660099', '#663300', 
                '#663333', '#663399', '#990000', '#990033', '#993300', '#cc0000', '#cc0033', 
                '#cc0066', '#cc3300', '#cc3333', '#ff0000', '#ff3300', '#ff3333', '#ff6633',
                '#ff9933', '#ffcc33'] 
    color = [hex_codes[random.randrange(len(hex_codes))] for i in range(num)]
    return color  


  def draw(self,well,params):

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib.legend_handler import HandlerBase  
    from matplotlib.text import Text
    from matplotlib.font_manager import FontProperties
    from matplotlib.legend_handler import HandlerBase

    import matplotlib.colors as colors
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    import matplotlib.patches as mpatches
    import matplotlib.gridspec as gridspec    

    df = skylog(self.data).encoder() # Create Numerical Columns for Formation, Group and Lithology 

    df = df.loc[df['WELL']==well]    
    df = df.sort_values(by='DEPTH_MD')
    ztop = df.DEPTH_MD.min(); zbot=df.DEPTH_MD.max()

    group_colors = np.asarray(self.group_colors)
    group_labels = np.asarray(self.group_labels)
    formation_colors = np.asarray(self.formation_colors)
    formation_labels = np.asarray(self.formation_labels)      
    
    #-------------Facies Color Map--------------#
    cmap_facies = colors.ListedColormap(self.facies_colors[0:len(self.facies_colors)], 'indexed')        
    cluster = np.repeat(np.expand_dims(df['Facies'].values,1), 100, 1)

    #------------Formation Color Map------------#
    f_unique_values, formation_new_values = np.unique(df['Formations'], return_inverse=True)
    cmap_formations = colors.ListedColormap(formation_colors[f_unique_values], 'indexed')
    cluster_f = formation_new_values.reshape(-1, 1) 

    #-------------Groups Color Map--------------#
    g_unique_values, group_new_values = np.unique(df['Groups'], return_inverse=True)
    cmap_groups = colors.ListedColormap(group_colors[g_unique_values], 'indexed')
    cluster_g = group_new_values.reshape(-1, 1)
    g_width = 0.03
    g_space = 0.77

    if len(params)<10:
      figsize = (30,10)    
      wspace = 0.15
      right=0.8  
    elif len(params)<11:
      figsize = (30,10) 
      wspace = 0.16 
      right=0.8  
    elif len(params)<15:
      figsize = (30,10) 
      wspace = 0.17 
      right=0.8
      g_width = 0.023
      g_space = 0.7782    
   
    
    colours = skylog(self.data).hex_list(len(params))
    fig, ax = plt.subplots(nrows=1, ncols=len(params), figsize=figsize, constrained_layout=True)
    lw=0.6
    
    for i in range(0,len(params)-3):

      ax[i].plot(df[params[i]], df.DEPTH_MD, colours[i], label=df[params[i]].name) 
      ax[i].set_ylim(ztop,zbot)
      ax[i].invert_yaxis()  
      ax[i].grid(True)     
      ax[i].locator_params(axis='x', nbins=4)
      ax[i].set_xlabel(df[params[i]].name, fontdict={'fontsize': 13,'fontweight': 'bold'})
      if i+1 < len(params)-3:
        ax[i+1].set_yticklabels([]);      
      if df[params[i]].isna().sum() < len(df[params[i]]):
        ax[i].set_xlim(df[params[i]].min(),df[params[i]].max())
      elif df[params[i]].isna().sum() == len(df[params[i]]):
        pass

    im = ax[len(params)-3].imshow(cluster, interpolation='none', aspect='auto', cmap = cmap_facies, vmin=0, vmax=11)
    ax[len(params)-3].set_xlabel('Facies', fontdict={'fontsize': 13,'fontweight': 'bold'})
    ax[len(params)-3].set_xticklabels([])
    ax[len(params)-3].set_yticklabels([]);    

    im_f = ax[len(params)-2].imshow(cluster_f, extent=[0, 1, zbot, ztop],
                    interpolation='none', aspect='auto', cmap=cmap_formations, vmin=0, vmax=len(f_unique_values)-1)
    ax[len(params)-2].set_xlabel('FORMATION', fontdict={'fontsize': 13,'fontweight': 'bold'})
    ax[len(params)-2].set_xticklabels([]) 
    ax[len(params)-2].set_yticklabels([]);    

    im_g = ax[len(params)-1].imshow(cluster_g, extent=[0, 1, zbot, ztop],
                    interpolation='none', aspect='auto', cmap=cmap_groups, vmin=0, vmax=len(g_unique_values)-1)  
    ax[len(params)-1].set_xlabel('GROUP', fontdict={'fontsize': 13,'fontweight': 'bold'})
    ax[len(params)-1].set_xticklabels([])
    ax[len(params)-1].set_yticklabels([]);        
        
    divider = make_axes_locatable(ax[len(params)-3])
    cax = divider.append_axes("right", size="15%", pad=0.04)
    cbar=plt.colorbar(im, cax=cax)
    cbar.set_label((9*' ').join([' SS ', ' SSh ', 'Sh', ' Marl', 'Dol', '  Ls','  Ch','  Hal', 'Anhy','Tuff','Coal','Bsm']))
    cbar.ax.get_yaxis().labelpad = -3.7
    cbar.set_ticks(range(0,1)); cbar.set_ticklabels('')

    divider_f = make_axes_locatable(ax[len(params)-2])
    cax_f = divider_f.append_axes("right", size="15%", pad=0.05)
    cbar_f = plt.colorbar(im_f, cax=cax_f)
    cbar_f.set_ticks(np.linspace(0, len(f_unique_values)-1, 2*len(f_unique_values)+1)[1::2])
    cbar_f.set_ticklabels(formation_labels[f_unique_values])    

    divider_f = make_axes_locatable(ax[len(params)-1])
    cax_g = divider_f.append_axes("right", size="20%", pad=0.05)    
    cbar_g = plt.colorbar(im_g, cax=cax_g)
    cbar_g.set_ticks(np.linspace(0, len(g_unique_values)-1, 2*len(g_unique_values)+1)[1::2])
    cbar_g.set_ticklabels(group_labels[g_unique_values])    
                  
    fig.suptitle('WELL: %s'%df.iloc[0]['WELL'], fontsize=18,y=0.935,x=0.225)

    plt.subplots_adjust(left=0.2, 
                    bottom=0.1,  
                    right=right,  
                    top=0.9,  
                    wspace=wspace,  
                    hspace=0.4)    
    
    ax[len(params)-1].set_position([g_space,0.10,g_width,0.8]) 