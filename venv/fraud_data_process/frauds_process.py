import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Importing the dataset
dataset = pd.read_csv('frauds.csv')
X = dataset.iloc[:, [0,37]].values
y = dataset.iloc[:, 38].values

#Training and Testing Data (divide the data into two part)
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test =train_test_split(X,y,test_size=0.20, random_state=0)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

from sklearn.ensemble import RandomForestClassifier

# Create a Random forest Classifier
clf = RandomForestClassifier(n_estimators=60)

# Train the model using the training sets
clf.fit(X_train, y_train)

y_pred= clf.predict(X_test)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test,y_pred)

from sklearn.metrics import accuracy_score
accuracy_score(y_test,y_pred)

# Making the Confusion Matrix
cm = confusion_matrix(y_pred, y_test)
sns.heatmap(cm,annot=True)
plt.savefig('dt.png')
print(cm)

from sklearn.metrics import accuracy_score
acc_score = accuracy_score(y_pred,y_test)
print(acc_score)

#saveas pickle object
##import pickle
##with open('clf.pickle', 'wb') as f:
##    pickle.dump(clf, f)
