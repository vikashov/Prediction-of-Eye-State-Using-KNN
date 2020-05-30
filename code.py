# -*- coding: utf-8 -*-
"""Myimp.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uZfMiZbPQyoBv3GCMMgXr50XtDbkVkMK
"""

from google.colab import files
uploaded = files.upload()

import pandas as pd    # for dataframe
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split # for splitiing data frame into testa and train dataframe
from sklearn.neighbors import KNeighborsClassifier   # To use KNN model
from sklearn.metrics import confusion_matrix          # To get confusion matrix
from sklearn.metrics import classification_report     # To get accuracy, precision, F score and all
from sklearn.metrics import accuracy_score
import sklearn.metrics as met
from numpy import array   
import io
import numpy as np
import seaborn as sn

# Uploading data using pandas dataframe
data = pd.read_csv(io.BytesIO(uploaded['eye movement.csv']))
data.head()

# Splitting dataset into two data frames X and Y
values = data.values
X = values[:,:-1]
Y = values[:, -1]

# splitting dataset
train_X, test_X, train_Y, test_Y = train_test_split(X, Y, test_size = 0.1, shuffle = False, random_state = 1)

# walk-forward validation
NewX = [i for i in train_X]
NewY = [j for j in train_Y]

pred = list()

for i in range(len(test_Y)):
  KNN = KNeighborsClassifier(n_neighbors=3)
  # fit model on subset of data
  subX = array(NewX)[-10:,:]
  subY = array(NewY)[-10:]
  KNN.fit(subX, subY)

  # Now forcasting for next step
  Ynew = KNN.predict([test_X[i,:]])[0]

  # storing prediction in pred list
  pred.append(Ynew)

  NewX.append(test_X[i, :])
  NewY.append(test_Y[i])

# evaluate prediction
print(accuracy_score(test_Y, pred))

cm = confusion_matrix(test_Y, pred)
print(cm)
sn.heatmap(cm, annot=True)
plt.show()

print(classification_report(test_Y, pred))

prob_Y = KNN.predict_proba(test_X)
#print(prob_Y)
preds = prob_Y[:1]

fpr, tpr, threshold = met.roc_curve(test_Y, pred)
#print(fpr, tpr, threshold)
# plot ROC curve
plt.title("ROC curve")
plt.plot(fpr, tpr, label ="auc = " + str(auc))
plt.legend(loc = 4)
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.show()
auc = met.auc(fpr, tpr)
#print(auc)