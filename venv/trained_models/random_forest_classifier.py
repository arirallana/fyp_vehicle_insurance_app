import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


dataset = pd.read_csv('frauds.csv')
dataset = dataset.drop(columns=['policy_number', 'policy_bind_date',
                                'policy_state','policy_csl','insured_zip',
                                'insured_hobbies','insured_relationship',
                                'incident_date', 'incident_state', 'incident_city',
                                'incident_location','auto_make','auto_model','months_as_customer',
                                'umbrella_limit','insured_occupation','capital-gains',
                                'capital-loss','incident_hour_of_the_day','property_damage', 'bodily_injuries',
                                'witnesses','injury_claim', 'property_claim', 'vehicle_claim'])
dataset=dataset.replace('?',np.nan).dropna(axis = 0, how = 'any')




#Encoding categorical data
from sklearn.preprocessing import LabelEncoder


continuous_cols = ['age', 'policy_deductable', 'policy_annual_premium',
       'number_of_vehicles_involved', 'total_claim_amount', 'auto_year']

categorical_cols = ["insured_sex" , "incident_type", "insured_education_level",
                    "collision_type","incident_severity", "authorities_contacted","police_report_available"]


X_continuous = dataset[continuous_cols]
X_categorical = dataset[categorical_cols]
X_encoded_data = pd.get_dummies(X_categorical)

X=pd.concat([X_encoded_data,X_continuous],axis=1)

print(len(X.columns))

X = X.values
y = dataset.iloc[:, 13].values

labelencoder_y = LabelEncoder()
y = labelencoder_y.fit_transform(y)

#Training and Testing Data (divide the data into two part)
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test =train_test_split(X,y,test_size=0.25, random_state=0)


from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

from sklearn.ensemble import RandomForestClassifier

# Create a Random forest Classifier
clf = RandomForestClassifier(n_estimators=60, criterion='entropy',random_state = 0)

# Train the model using the training sets
clf.fit(X_train, y_train)

y_pred= clf.predict(X_test)

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

from sklearn.metrics import accuracy_score
import seaborn as sns

accuracy_score(y_test,y_pred)

# Making the Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
cmd = ConfusionMatrixDisplay(cm, display_labels=['Y','N'])
cmd.plot()
cmd.ax_.set(xlabel='Predicted', ylabel='True')


from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
acc_score = accuracy_score(y_pred,y_test)
print('accuracy score = '+str(acc_score))


#Evaluation
from sklearn import metrics

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

print('Precision: %.3f' % precision_score(y_test, y_pred))
print('Recall: %.3f' % recall_score(y_test, y_pred))
print('F1 Score: %.3f' % f1_score(y_test, y_pred))

#Predict for one case

insured_sex_FEMALE = 0
insured_sex_MALE = 1
incident_type_Multi_vehicle_Collision = 0
incident_type_Single_Vehicle_Collision = 1
insured_education_level_Associate = 0
insured_education_level_College = 0
insured_education_level_High_School = 0
insured_education_level_JD = 0
insured_education_level_MD = 1
insured_education_level_Masters= 0
insured_education_level_PhD = 0
collision_type_Front_Collision = 0
collision_type_Rear_Collision = 0
collision_type_Side_Collision = 1
incident_severity_Major_Damage = 1
incident_severity_Minor_Damage = 0
incident_severity_Total_Loss = 0
authorities_contacted_Ambulance = 0
authorities_contacted_Fire = 0
authorities_contacted_Other = 0
authorities_contacted_Police = 1
police_report_available_NO = 0
police_report_available_YES = 1
age = 48
policy_deductable = 1000
policy_annual_premium = 1406.91
number_of_vehicles_involved = 1
total_claim_amount = 71610
auto_year = 2004


prediction = clf.predict([[
insured_sex_FEMALE,
insured_sex_MALE,
incident_type_Multi_vehicle_Collision,
incident_type_Single_Vehicle_Collision,
insured_education_level_Associate,
insured_education_level_College,
insured_education_level_High_School,
insured_education_level_JD,
insured_education_level_MD,
insured_education_level_Masters,
insured_education_level_PhD,
collision_type_Front_Collision,
collision_type_Rear_Collision,
collision_type_Side_Collision,
incident_severity_Major_Damage,
incident_severity_Minor_Damage,
incident_severity_Total_Loss,
authorities_contacted_Ambulance,
authorities_contacted_Fire,
authorities_contacted_Other,
authorities_contacted_Police,
police_report_available_NO,
police_report_available_YES,
age,
policy_deductable,
policy_annual_premium,
number_of_vehicles_involved,
total_claim_amount,
auto_year
]])

print(labelencoder_y.inverse_transform(prediction))

import pickle

# create an iterator object with write permission - model.pkl
with open('random_forest_classifier_pkl.pickle', 'wb') as files:
    pickle.dump(clf, files)

# load saved model
with open('random_forest_classifier_pkl.pickle' , 'rb') as f:
    lr = pickle.load(f)