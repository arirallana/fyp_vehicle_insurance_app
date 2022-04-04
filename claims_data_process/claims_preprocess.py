# Config dict to set the logging level
import logging.config

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        '': {
            'level': 'INFO',
        },
    }
}
logging.config.dictConfig(DEFAULT_LOGGING)

# Disabling warnings output
import warnings
from sklearn.exceptions import DataConversionWarning, ConvergenceWarning

warnings.filterwarnings(action='ignore', category=DataConversionWarning)
warnings.filterwarnings(action='ignore', category=ConvergenceWarning)
warnings.filterwarnings(action='ignore', category=UserWarning)

# import libraries
import dowhy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dataset = pd.read_csv('Car_Insurance_Claim.csv')
dataset.head()
dataset.columns

# Replacing missing values with column average
dataset.isnull().sum()
dataset['CREDIT_SCORE'].fillna((dataset['CREDIT_SCORE'].mean()), inplace=True)
dataset['ANNUAL_MILEAGE'].fillna((dataset['ANNUAL_MILEAGE'].mean()), inplace=True)
dataset = dataset.drop(['ID'], axis=1)

# create dict of unique col values
Dict = {}
for col in dataset.columns:
    Dict[col] = dataset[col].unique().tolist()

###calculating expected counts for discrete varuables
continuous = ['CREDIT_SCORE', 'ANNUAL_MILEAGE', 'SPEEDING_VIOLATIONS', 'DUIS',
              'PAST_ACCIDENTS']  # variables with continuous values
dependant_var = 'OUTCOME'