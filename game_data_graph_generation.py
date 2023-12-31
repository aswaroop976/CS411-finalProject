# -*- coding: utf-8 -*-
"""Game data Graph Generation

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sFYxcjeVD6q6f0Lv2sMw96RCdot4U8bH

## **Imports**
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go


# fig = plt.figure()
# print(type(fig))
# fig = plt.figure(figsize=(6, 4), facecolor='green')
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import stopwords
import collections
from nltk import ngrams

"""##**Interactive Graph**
Create Interactive Graphs based on the genre of the game:
"""

# create interactive plot

def genreSelection():
  df = pd.read_csv('games-features.csv').set_index('ResponseID')
  # print(df.head(5))
  genres = ['GenreIsIndie', 'GenreIsAction',\
            'GenreIsAdventure','GenreIsCasual', 'GenreIsStrategy', \
            'GenreIsRPG', 'GenreIsSimulation',\
            'GenreIsEarlyAccess', 'GenreIsFreeToPlay', 'GenreIsSports',\
            'GenreIsRacing', 'GenreIsMassivelyMultiplayer']
  df = df[['Metacritic']+genres]
  data = []
  fig = go.Figure()
  for g in genres:

    primarymask = (df[g] == True) & (df['Metacritic'] > 0)
    tempDf = df[primarymask]
    genreData = []
    for f in genres:
      secondarymask = (tempDf[f] == True)
      metacritic = tempDf[secondarymask]['Metacritic'].agg('mean')
      genreData.append(metacritic)

    data.append(genreData)

  label = ['Indie', 'Action',\
            'Adventure','Casual', 'Strategy', \
            'RPG', 'Simulation',\
            'EarlyAccess', 'Free', 'Sports',\
            'Racing', 'Multiplayer']
  fig = px.imshow(data,
                labels=dict(x="Second Genre", y="First Genre",\
                            color="Average Metacritic Score"),
                x=label,
                y=label
               )
  fig.update_layout(title_text='Fig.1 MetaCritic Score Heatmap by Game Genre'
  )

  fig.show()
  fig.write_html("Genreinteractive.html")


genreSelection()

# create interactive plot

def sales(t):
  df = pd.read_csv('games-features.csv')
  primarymask = (df[t] == True)
  # print(df.head(5))
  df = df[primarymask].set_index('ResponseID')
  genres = ['GenreIsNonGame', 'GenreIsIndie', 'GenreIsAction',\
            'GenreIsAdventure','GenreIsCasual', 'GenreIsStrategy', \
            'GenreIsRPG', 'GenreIsSimulation',\
            'GenreIsEarlyAccess', 'GenreIsFreeToPlay', 'GenreIsSports',\
            'GenreIsRacing', 'GenreIsMassivelyMultiplayer']
  inter = pd.DataFrame()
  for g in genres:
    if(g == t):
      continue

    mask = (df[g] == True) & ((df['PriceInitial'] > 0) | (df['PriceFinal'] > 0))
    tempDf = df[mask][['SteamSpyOwners', 'PriceInitial', 'PriceFinal']]
    tempDf['TotalSales'] = (0.5 * tempDf['SteamSpyOwners'] * tempDf['PriceInitial'] +\
                      0.5 * tempDf['SteamSpyOwners'] * tempDf['PriceFinal']) / 1000000
    tempDf['Type'] = t[7:] + " + " + g[7:]
    inter = pd.concat([inter, tempDf[['TotalSales', 'Type']]])

  grp = inter.groupby(['Type'])
  r1 = grp.agg(['mean'])
  r1 = r1.rename(columns={'mean': 'Average Sales Numbers (M$)'})
  display(r1)

  fig = go.Figure()
  fig = px.box(inter, x="Type", y="TotalSales", log_y=True)
  fig.update_layout(title_text='Fig.2 Total Sales Numbers for ' + t[7:] + ' games\
 categorized by secondary Genre', # title of plot
    yaxis_title_text='Total Sales (M$)', # xaxis label
    xaxis_title_text='Game Genre (Primary + Secondary)',

  )

  fig.show()
  fig.write_html(t[7:] + "Sales.html")


sales('GenreIsAction')

from collections import Counter

def keywords(t):
  df = pd.read_csv('games-features.csv').set_index('ResponseID')
  primarymask = (df[t] == True) & ((df['PriceInitial'] > 0) | (df['PriceFinal'] > 0))
  # print(df.head(5))
  # genres = ['GenreIsNonGame', 'GenreIsIndie', 'GenreIsAction',\
  #           'GenreIsAdventure','GenreIsCasual', 'GenreIsStrategy', \
  #           'GenreIsRPG', 'GenreIsSimulation',\
  #           'GenreIsEarlyAccess', 'GenreIsFreeToPlay', 'GenreIsSports',\
  #           'GenreIsRacing', 'GenreIsMassivelyMultiplayer']

  tempDf = df[primarymask][['SteamSpyOwners', 'PriceInitial', 'PriceFinal', 'AboutText']]
  tempDf['TotalSales'] = 0.5 * tempDf['SteamSpyOwners'] * tempDf['PriceInitial'] +\
                      0.5 * tempDf['SteamSpyOwners'] * tempDf['PriceFinal']
  tempDf['Type'] = t[7:]
  tempDf.sort_values(by=['TotalSales'], ascending=False)

  inter = tempDf.iloc[0:100]
  word_list = []
  stopwordList = stopwords.words()
  stopwordList.extend(['gameplay', 'player', 'play', 'tm'])

  for index, row in inter.iterrows():
    for sent in nltk.sent_tokenize(row['AboutText']):
      tokens = nltk.word_tokenize(sent)
      tokens_without_stp = [word for word in tokens if not word in stopwordList]
      tagged = nltk.pos_tag(tokens_without_stp)
      for key in tagged:
        if ((key[1] == 'NN' or key[1] == 'JJ') and key[0].lower() != 'game' \
            and key[0].lower() != t[7:].lower()):
          word_list.append(key[0].lower())

  counter = Counter(word_list)
  keywords = counter.most_common(15)
  # print(keywords)
  count = [count for tag, count in keywords]
  word = [tag for tag, count in keywords]
  fig = go.Figure(data=[
    go.Bar(x=word, y=count),
  ])
  fig.update_layout(title_text='Fig. 4 Keyword distribution for top 100 '\
                    + t[7:] + ' games in sales', # title of plot
    yaxis_title_text='Number of appearances', # xaxis label
    xaxis_title_text='Keyword (lowercase)',
  )
  fig.show()
  fig.write_html(t[7:] + "Keywords.html")

keywords("GenreIsAction")

def cod():
  df = pd.read_csv('games-features.csv').set_index('ResponseID')
  primarymask  = (df['ResponseName'].str.contains('Call of Duty:', case = False)) | (df['ResponseName'].str.contains('Call of Duty\(r\):', case = False))
  # print(df.head(5))
  inter = df[primarymask][['ResponseName', 'RecommendationCount']]
  inter = inter.rename(columns=lambda x: 'Title' if x == 'ResponseName' else x)
  final = inter.groupby(['Title']).mean().reset_index()
  fig = px.bar(final, x='Title', y="RecommendationCount", text_auto='.3s')
  fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
  fig.update_layout(title_text='Fig.3 Recommendations for Titles in the \
Call Of Duty Series', # title of plot
    yaxis_title_text='Recommendations', # xaxis label
    xaxis_title_text='Game title',

  )

  fig.show()
  fig.write_html("CallOfDuty.html")


cod()