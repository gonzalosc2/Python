####################################
# author: Gonzalo Salazar
# course: Python for Data Science and Machine Learning Bootcamp
# purpose: lecture notes
# description: Section 17 - Logistic Regression
# datasets: (i) Titanic: Machine Learning from Disaster (source: Kaggle), 
#           (ii) Advertising data: fake data.
####################################

### LOGISTIC REGRESSION ###
# We use it as a method for CLASSIFICATION since we are trying to predict discrete categories.
# For instance: (i) spam vs. ham emails; (ii) loan default (yes/no); or (iii) disease diagnosis
# Linear regression does not return good results when we are working with categories as dependent
# variables (e.g., a binary case) because it predicts results outside the scope of the categories
# (e.g., probabilities below 0 and above 1)

# Sigmoid (aka Logistic) Function takes any value and outpus it to be between 0 and 1.
#   \phi(z) = 1/(1+e^{-z}), where z = b_0 + b_1 x (i.e., the linear model)

#%%
import os
#from numpy.lib.function_base import corrcoef
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import cufflinks as cf
cf.go_offline()
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

#%matplotlib inline
os.chdir('/Users/gsalazar/Documents/C_Codes/Learning-Python/Udemy_Py_DataScience_ML/logr_data')

#%%
train = pd.read_csv('titanic_train.csv')
test = pd.read_csv('titanic_test.csv')

# %%
# Brief descriptive statistics from the data
train.info()
train.describe()

# %%
train.head()

# %%
## Explanatory data analysis
# Checking for missing data
sns.heatmap(train.isnull(),yticklabels = False, cbar = False, cmap = 'Greens')
# Comment: we are missing some age info as well as a lot of cabin info. With the first
#          we can fill in values taking into account other passengers with similar 
#          characteristics. In regard to cabin, it is not possible to fill in values, instead
#          we might drop it or transform it to a binary variable (have cabin = 1, no cabin = 0)

# %%
# Describing the data we'll work with
sns.set_style('whitegrid')
sns.countplot(x = 'Survived', hue = 'Sex', data = train, palette = 'Greens')
# Comment: there is a tendency, more men tended not to survived compared to women

# %%
sns.countplot(x = 'Survived', hue = 'Pclass', data = train)
# Comment: mostly all who did not survived, belonged to the lowest class. Among the survivors,
#          passengers from the highest class appear to have better chance to survive.

# %%
sns.displot(train['Age'].dropna(), kde = False, bins = 30, alpha = .4)
#train['Age'].plot.hist(bins = 30)
# Comment: bi-modal distribution. Skewed to the left, there is a minor concentration of young
#          people 5-15 yo. and then the rest is concentrated, mostly, between 20 and 35 yo.

# %%
sns.countplot(x = 'SibSp', data = train)
# Comment: mostly all people in the Titanic were young or have 1 sibling or spouse (more probably)

# %%
sns.histplot(train['Fare'], bins = 40)
#train['Fare'].iplot(kind='hist',bins=30)
# Comment: related to the previous point. Smallest fares correspond to lower classes.

# %%
## Cleaning data: age will be imputed according to the average age on each Pclass
plt.figure(figsize = (10,7))
sns.boxplot(x = 'Pclass', y = 'Age', data=train)

mean_age = train.groupby('Pclass').mean()['Age']

def impute_age(cols):
    Age = cols[0]
    Pclass = cols[1]

    if pd.isnull(Age):
        if Pclass == 1:
            return mean_age[1]
        elif Pclass == 2:
            return mean_age[2]
        else:
            return mean_age[3]
    else:
        return Age

train['Age'] = train[['Age','Pclass']].apply(impute_age,axis = 1)  # axis tells we to apply 
                                                                   # it across the columns

# %%
# Checking Age after imputation
sns.heatmap(train.isnull(),yticklabels = False, cbar = False, cmap = 'Greens')                                                                   

# Dropping cabin column
train.drop('Cabin', axis = 1,inplace=True)

# %%
# Checking any remaining missing value and deleting it (in case these are just a few)
plt.figure(figsize=(10,10))
sns.heatmap(train.isnull(),yticklabels = False, cbar = False, cmap = 'Greens')                                                                   
train.dropna(inplace=True)

#%%
# Encoding categorical values
sex = pd.get_dummies(train['Sex'],drop_first=True)  # drop_first will drop one of the columns
                                                    # to avoid having perfect collinearity
embark = pd.get_dummies(train['Embarked'],drop_first=True)
pclass = pd.get_dummies(train['Pclass'],drop_first=True)  # it is actually a categorical value
train = pd.concat([train,sex,embark,pclass],axis=1)                                               

train.head()

#%%
# Dropping columns that we're not going to use
train.drop(['Sex','Name','Embarked','Ticket','PassengerId','Pclass'],axis=1,inplace=True)
train.head()

# %%
## Training and using the model (NOTICE: train dataset is used as it were the complete dataset)
# Establishing the data we'll work with as well as defining training and testing samples
X = train.drop('Survived', axis = 1)
y = train['Survived']

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.3, random_state = 101)

# Instantiating a linear regression model and training it
logm = LogisticRegression()
logm.fit(X_train,y_train)

#%%
# Predicting probability of surviving
predic = logm.predict(X_test)  

# Checking performance 
print('Classification Report')
print(classification_report(y_test,predic))
print('\nConfusion Matrix')
print(confusion_matrix(y_test,predic))
# Comment: performance can be increased by using the whole training.csv data as just training data.
#          Also consider that more can be done by using NLP algorithms to extract information about
#          names (i.e., Dr., Mr., etc.) or ticket info that could lead us to specific location on the
#          the Titanic.

del y, X, X_test, X_train, y_train, y_test, logm, predic

####################################################################################
# PROJECT EXERCISE - Advertisement

# This data set contains the following features:
    # 'Daily Time Spent on Site': consumer time on site in minutes
    # 'Age': cutomer age in years
    # 'Area Income': Avg. Income of geographical area of consumer
    # 'Daily Internet Usage': Avg. minutes a day consumer is on the internet
    # 'Ad Topic Line': Headline of the advertisement
    # 'City': City of consumer
    # 'Male': Whether or not consumer was male
    # 'Country': Country of consumer
    # 'Timestamp': Time at which consumer clicked on Ad or closed window
    # 'Clicked on Ad': 0 or 1 indicated clicking on Ad

# %%
# Reading in the Ecommerce Customers csv file as a DataFrame called customers
ad_data = pd.read_csv('Advertising.csv')

# Checking the head of customers
ad_data.head()

# %%
# Checking out its info() and describe() methods
ad_data.info()
ad_data.describe()

# %%
## EXPLORATORY DATA ANALYSIS
sns.axes_style('whitegrid')
# Checking users' age
sns.histplot(ad_data['Age'],bins=30, alpha=.4)
# Comment: people is mostly 30 to 40 yo.

# %%
# Displaying relationship between Age and Area Income
sns.jointplot(y='Area Income', x='Age', data = ad_data,kind='reg',color='g')
# Comment: it appears that younger people are concentrated in a geographical
#          area with higher avg. income

# %%
# Displaying relationship between Daily Time Spent on Site and Age
sns.jointplot(y='Daily Time Spent on Site', x='Age', data = ad_data,kind='kde',color='g', fill=True)
# Comment: young people spend more time on site than old people

# %%
# Displaying relationship between Daily Time Spent on Site and Daily Internet Usage
sns.jointplot(y='Daily Time Spent on Site', x='Daily Internet Usage', data = ad_data,kind='reg',color='g')
# Comment: there seems to be two groups. (i) high daily internet usage is associated with
#          high daily time spent on site, and viceversa.

# %%
# Checking all the possible relationships among variables
sns.pairplot(data=ad_data,hue='Clicked on Ad',kind='hist',diag_kind='auto',corner=True)
# Comment: people who click on ad uses internet less compared to those who do not click on ad,
#          regardless of age, time spent on site or area income. 
#          Those who click on ad use fewer internet than those who do not click (the same happens
#          when we check the time spent on site). The latter also seems to be younger than the
#          former, on average.

# %%
## TRAINING AND TESTING THE MODEL
# Establishing the data we'll work with as well as defining training and testing samples
X = ad_data.drop(['Clicked on Ad','Ad Topic Line','City','Country','Timestamp'],axis = 1)
y = ad_data['Clicked on Ad']
# NOTICE: I did not consider City or Country because I did not have enough representation for
#         each of these categories (i.e., just 4/5 people from each country)

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.3)

# Instantiating a linear regression model and training it
logm = LogisticRegression()
logm.fit(X_train,y_train)

#%%
# Predicting probability of surviving
predic = logm.predict(X_test)  

# Checking performance 
print('Classification Report')
print(classification_report(y_test,predic))
print('\nConfusion Matrix')
print(confusion_matrix(y_test,predic))
