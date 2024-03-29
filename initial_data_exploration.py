# -*- coding: utf-8 -*-
"""initial_data_exploration.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19yqBALmoKbQI5Plm_KOer27PWuo0Rdtq

**PREDICTING RAIN IN AUSTRILIA**
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2
from sklearn import preprocessing
import matplotlib.pyplot as plt
import seaborn as sns

data=pd.read_csv('https://raw.githubusercontent.com/tjkyner/australian-rain-prediction/main/weatherAUS.csv')

"""##Print first 5 rows of dataset"""

data.head()

data.columns

"""##information of each column"""

data.info()

"""## Print number of rows and column in our dataset"""

data.shape

"""

---
## Describing mean, median,standard deviation in data 
"""

data.describe()

print(data.dtypes)

"""## printing values of categorical column"""

data.dtypes[data.dtypes == 'object'].index.unique()

"""##Checking for missing values"""

data.isnull().sum()

array = data.values
X = array[:,0:22]
Y = array[:,22]

# List of features that will be changed
winds = ['WindGustDir', 'WindDir3pm', 'WindDir9am']
    
# Doing the transformation with "get_dummies"
df = pd.get_dummies(data, columns=winds)

# Cheking the new shape
df.shape

"""## Dropping unwanted column from our dataset"""

df = df.drop(['WindGustDir_WSW', 'WindDir3pm_SSW', 'WindDir9am_NNE','Location','Date', 'Evaporation', 'Sunshine', 'Cloud9am', 'Cloud3pm'], axis =1)
df.shape

df['RainToday'].replace({'No': 0, 'Yes': 1},inplace = True)
df['RainTomorrow'].replace({'No': 0, 'Yes': 1},inplace = True)

df.RainToday.value_counts()

df.RainTomorrow.value_counts()

"""## Droping Null values rows"""

df.dropna(inplace=True)

"""## Doing the escalation using "MinMaxScale" model

"""

scaler = preprocessing.MinMaxScaler()
# Training the model
scaler.fit(df)
# Changing data 
df = pd.DataFrame(scaler.transform(df), index=df.index, columns=df.columns)
# Returning the data frama after the escalation
df.head()

"""## Finding the best features in our dataset"""

X = df.loc[:,df.columns!='RainTomorrow']
y = df[['RainTomorrow']]
# Using função SelectKBest and determining the parameters numbers of features, K = 58
selector = SelectKBest(chi2, k=58)
# Traning
selector.fit(X, y)
# Returning scores
scores = selector.scores_
# Creating a list for features names
lista = df.columns
lista = [x for x in lista if x != 'RainTomorrow']
# Creationg a dictionaty with the features name list and scores  
unsorted_pairs = zip(lista, scores)
sorted_pairs = list(reversed(sorted(unsorted_pairs, key=lambda x: x[1])))
k_best_features = dict(sorted_pairs[:58])

"""##  Plotting graph for K_best score"""

# Ploting the graphic area
plt.figure(figsize=(20,7),facecolor = 'w',edgecolor = 'w')
# Ploting the bar graphic
p = plt.bar(range(len(k_best_features)), list(k_best_features.values()), align='center')
plt.xticks(range(len(k_best_features)), list(k_best_features.keys()))
# Editing the names
plt.xticks(rotation='90')
plt.title('K best features scores')
plt.xlabel('Features')
plt.ylabel('Score')
plt.show()

"""Now we can see that RainToday is the most important feature for the models. The features about wind direction don't have high scores. I will use just features that have scores above 1% (71 points) RainToday score (7136 points).


"""

sns.boxplot(x=df['MinTemp'])
plt.show()

sns.boxplot(x=df['MaxTemp'])
plt.show()

sns.boxplot(x=df['WindGustSpeed'])
plt.show()

sns.boxplot(x=df['Rainfall'])
plt.show()

sns.boxplot(x=df['WindSpeed9am'])
plt.show()

sns.boxplot(x=df['Humidity9am'])
plt.show()

"""An exemple of outliers can be observed in the Humidity9am graph. There as some values of 0 and 100 about Humidity, this values are unreals to be found in a open space.

To remove outliers we can use the Z-score technic. 
"""

import seaborn as sns

data['RainTomorrow'].value_counts().plot(kind='pie')

