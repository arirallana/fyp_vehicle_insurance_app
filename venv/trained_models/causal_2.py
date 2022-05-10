import dowhy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import econml

dataset = pd.read_csv('Car_Insurance_Claim.csv')

# Replacing missing values with column average
dataset.isnull().sum()
dataset['CREDIT_SCORE'].fillna((dataset['CREDIT_SCORE'].mean()), inplace=True)
dataset['ANNUAL_MILEAGE'].fillna((dataset['ANNUAL_MILEAGE'].mean()), inplace=True)
dataset = dataset.drop(['ID', 'RACE', 'MARRIED', 'CHILDREN', 'POSTAL_CODE', 'VEHICLE_YEAR'], axis=1)

# state causal relations
rel_str = """VEHICLE_OWNERSHIP->DRIVING_EXPERIENCE; DRIVING_EXPERIENCE->SPEEDING_VIOLATIONS; 
DRIVING_EXPERIENCE->DUIS; DRIVING_EXPERIENCE->PAST_ACCIDENTS; VEHICLE_OWNERSHIP->CREDIT_SCORE; 
SPEEDING_VIOLATIONS->CREDIT_SCORE; SPEEDING_VIOLATIONS->PAST_ACCIDENTS; DUIS->CREDIT_SCORE; 
DUIS->SPEEDING_VIOLATIONS; DUIS->PAST_ACCIDENTS;PAST_ACCIDENTS->CREDIT_SCORE; VEHICLE_OWNERSHIP->OUTCOME; 
DRIVING_EXPERIENCE->OUTCOME; SPEEDING_VIOLATIONS->OUTCOME; DUIS->OUTCOME; PAST_ACCIDENTS->OUTCOME; 
VEHICLE_OWNERSHIP->OUTCOME; CREDIT_SCORE->OUTCOME; VEHICLE_TYPE->ANNUAL_MILEAGE; ANNUAL_MILEAGE->CREDIT_SCORE; 
VEHICLE_TYPE->CREDIT_SCORE; AGE->DRIVING_EXPERIENCE; AGE->EDUCATION; AGE->INCOME; AGE->VEHICLE_OWNERSHIP; 
GENDER->EDUCATION; GENDER->INCOME; GENDER->VEHICLE_TYPE; EDUCATION->INCOME; INCOME->VEHICLE_OWNERSHIP; 
INCOME->VEHICLE_TYPE; AGE->SPEEDING_VIOLATIONS; AGE->DUIS; AGE->PAST_ACCIDENTS; AGE->CREDIT_SCORE;
EDUCATION->CREDIT_SCORE; INCOME->CREDIT_SCORE;"""

# create causal graph
import pygraphviz

causal_graph = """digraph {
VEHICLE_OWNERSHIP[label="VEHICLE_OWNED"];
OUTCOME[label="CLAIM FILED"];
AGE;
GENDER;
DRIVING_EXPERIENCE;
EDUCATION;
INCOME;
CREDIT_SCORE;
ANNUAL_MILEAGE;
VEHICLE_TYPE;
SPEEDING_VIOLATIONS;
DUIS;
PAST_ACCIDENTS;
""" + rel_str + """
}"""

print(dataset.head())

rel_str_selective = """VEHICLE_OWNERSHIP_1->DRIVING_EXPERIENCE_0_9y;DRIVING_EXPERIENCE_0_9y->SPEEDING_VIOLATIONS;DRIVING_EXPERIENCE_0_9y->DUIS;DRIVING_EXPERIENCE_0_9y->PAST_ACCIDENTS;VEHICLE_OWNERSHIP_1->CREDIT_SCORE;SPEEDING_VIOLATIONS->CREDIT_SCORE;SPEEDING_VIOLATIONS->PAST_ACCIDENTS;DUIS->CREDIT_SCORE;DUIS->SPEEDING_VIOLATIONS;DUIS->PAST_ACCIDENTS;PAST_ACCIDENTS->CREDIT_SCORE;VEHICLE_OWNERSHIP_1->OUTCOME;DRIVING_EXPERIENCE_0_9y->OUTCOME;SPEEDING_VIOLATIONS->OUTCOME;DUIS->OUTCOME;PAST_ACCIDENTS->OUTCOME;VEHICLE_OWNERSHIP_1->OUTCOME;CREDIT_SCORE->OUTCOME;VEHICLE_TYPE_sedan->ANNUAL_MILEAGE;ANNUAL_MILEAGE->CREDIT_SCORE;VEHICLE_TYPE_sedan->CREDIT_SCORE;AGE_26_39->DRIVING_EXPERIENCE_0_9y;AGE_26_39->EDUCATION_high_school;AGE_26_39->INCOME_upper_class;AGE_26_39->VEHICLE_OWNERSHIP_1;GENDER_female->EDUCATION_high_school;GENDER_female->INCOME_upper_class;GENDER_female->VEHICLE_TYPE_sedan;EDUCATION_high_school->INCOME_upper_class;INCOME_upper_class->VEHICLE_OWNERSHIP_1;INCOME_upper_class->VEHICLE_TYPE_sedan;AGE_26_39->SPEEDING_VIOLATIONS;AGE_26_39->DUIS;AGE_26_39->PAST_ACCIDENTS;AGE_26_39->CREDIT_SCORE;EDUCATION_high_school->CREDIT_SCORE;INCOME_upper_class->CREDIT_SCORE;"""

causal_graph_selective = """digraph {
VEHICLE_TYPE_sedan;
VEHICLE_OWNERSHIP_1;
GENDER_female;
EDUCATION_high_school; 
INCOME_upper_class;
DRIVING_EXPERIENCE_0_9y;
AGE_26_39; 
CREDIT_SCORE;
ANNUAL_MILEAGE;
SPEEDING_VIOLATIONS;
DUIS;
PAST_ACCIDENTS;
OUTCOME;
""" + rel_str_selective + """
}"""

confounders_continuous = [
    'CREDIT_SCORE',
    'SPEEDING_VIOLATIONS',
    'ANNUAL_MILEAGE',
    'DUIS',
    'PAST_ACCIDENTS',
]

confounders_categorical = [
    'VEHICLE_TYPE',
    'GENDER',
    'VEHICLE_OWNERSHIP',
    'EDUCATION',
    'INCOME',
    'DRIVING_EXPERIENCE',
    'AGE']

one_hot_encoded_data = pd.get_dummies(dataset, columns=confounders_categorical)
one_hot_encoded_data = one_hot_encoded_data.sample(n=10)

one_hot_encoded_data = one_hot_encoded_data.rename(columns={'VEHICLE_TYPE_sports car': 'VEHICLE_TYPE_sports_car',
                                                            'EDUCATION_high school': 'EDUCATION_high_school',
                                                            'INCOME_middle class': 'INCOME_middle_class',
                                                            'INCOME_upper class': 'INCOME_upper_class',
                                                            'INCOME_working class': 'INCOME_working_class',
                                                            'DRIVING_EXPERIENCE_0-9y': 'DRIVING_EXPERIENCE_0_9y',
                                                            'DRIVING_EXPERIENCE_10-19y': 'DRIVING_EXPERIENCE_10_19y',
                                                            'DRIVING_EXPERIENCE_20-29y': 'DRIVING_EXPERIENCE_20_29y',
                                                            'DRIVING_EXPERIENCE_30y+': 'DRIVING_EXPERIENCE_30y',
                                                            'AGE_16-25': 'AGE_16_25',
                                                            'AGE_26-39': 'AGE_26_39',
                                                            'AGE_40-64': 'AGE_40_64',
                                                            'AGE_65+': 'AGE_65'})

one_hot_encoded_data = one_hot_encoded_data.drop(['VEHICLE_TYPE_sports_car', 'GENDER_male',
                                                  'VEHICLE_OWNERSHIP_0', 'EDUCATION_none', 'EDUCATION_university',
                                                  'INCOME_middle_class',
                                                  'INCOME_poverty', 'INCOME_working_class', 'DRIVING_EXPERIENCE_10_19y',
                                                  'DRIVING_EXPERIENCE_20_29y', 'DRIVING_EXPERIENCE_30y', 'AGE_16_25',
                                                  'AGE_40_64', 'AGE_65'], axis=1)

from IPython.display import Image, display

display(Image(filename="causal_model_selective.png"))

print(one_hot_encoded_data)

print(one_hot_encoded_data.columns)

effects = {}
for i in one_hot_encoded_data.columns:
    model = dowhy.CausalModel(data=one_hot_encoded_data, graph=causal_graph_selective.replace("\n", " "), treatment=i,
                              outcome='OUTCOME')

    # from IPython.display import Image, display
    # display(Image(filename="causal_model.png"))

    print("\n")
    print(i)
    identified_estimand_experiment = model.identify_effect(proceed_when_unidentifiable=True)
    causal_estimate_reg = model.estimate_effect(identified_estimand_experiment,
                                                method_name="backdoor.linear_regression",
                                                test_significance=True)
    print(causal_estimate_reg)
    effects[i] = causal_estimate_reg.value

print("\n")
print(effects)
