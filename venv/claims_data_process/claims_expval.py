import collections
import claims_preprocess

Dict1 = collections.defaultdict(list)
for key in Dict.keys():
    if (key not in continuous) and (key!=dependant_var):
        for value in Dict[key]:
            counts_sum=0
            for i in range(1,10000):
                counts_i = 0
                rdf = dataset.sample(1000)
                counts_i = rdf.loc[(rdf[key]==value) & (rdf[dependant_var]==1)].shape[0]
                counts_i += rdf.loc[(rdf[key]!=value) & (rdf[dependant_var]==0)].shape[0]
                counts_sum+= counts_i
            counts_sum = counts_sum/10000
            Dict1[key].append([value,counts_sum])


#calculating expected counts for continuous variables

Dict2 = collections.defaultdict(list)
for variable in continuous:
    counts_sum=0
    for i in range(1,10000):
        counts_i = 0
        rdf = dataset.sample(1000)
        counts_i = rdf.loc[(rdf[variable]>=dataset[variable].mean()) & (rdf[dependant_var]==1)].shape[0]
        counts_i += rdf.loc[(rdf[variable]<dataset[variable].mean()) & (rdf[dependant_var]==0)].shape[0]
        counts_sum+= counts_i
    counts_sum = counts_sum/10000
    Dict2[variable].append(['>=average',counts_sum])

    counts_sum=0
    for i in range(1,10000):
        counts_i = 0
        rdf = dataset.sample(1000)
        counts_i = rdf.loc[(rdf[variable]<dataset[variable].mean()) & (rdf[dependant_var]==1)].shape[0]
        counts_i += rdf.loc[(rdf[variable]>=dataset[variable].mean()) & (rdf[dependant_var]==0)].shape[0]
        counts_sum+= counts_i
    counts_sum = counts_sum/10000
    Dict2[variable].append(['<average',counts_sum])

#obtained dict for all expected counts
expected_counts = {'AGE': [['65+', 526.8779], ['16-25', 774.5352], ['26-39', 586.821], ['40-64', 484.8584]],
            'GENDER': [['female', 449.9874], ['male', 550.0471]], 'RACE': [['majority', 347.8425], ['minority', 652.1557]],
            'DRIVING_EXPERIENCE': [['0-9y', 776.9952], ['10-19y', 514.0672], ['20-29y', 496.6342], ['30y+', 585.514]],
            'EDUCATION': [['high school', 539.5346], ['none', 675.7131], ['university', 471.0634]],
            'INCOME': [['upper class', 368.9461], ['poverty', 742.4658], ['working class', 670.6671], ['middle class', 591.123]],
            'VEHICLE_OWNERSHIP': [[1.0, 264.942], [0.0, 735.033]], 'VEHICLE_YEAR': [['after 2015', 447.7823], ['before 2015', 551.808]],
            'MARRIED': [[0.0, 620.7437], [1.0, 379.0589]], 'CHILDREN': [[1.0, 329.4385], [0.0, 670.5332]],
            'POSTAL_CODE': [[10238, 369.8532], [32765, 626.2568], [92101, 678.2905], [21217, 698.6685]],
            'VEHICLE_TYPE': [['sedan', 329.8434], ['sports car', 669.7558]], 'CREDIT_SCORE': [['>=average', 352.3756], ['<average', 647.4396]],
            'ANNUAL_MILEAGE': [['>=average', 537.9271], ['<average', 461.7684]],
            'SPEEDING_VIOLATIONS': [['>=average', 427.3318], ['<average', 572.8016]],
            'DUIS': [['>=average', 542.2536], ['<average', 457.8742]],
            'PAST_ACCIDENTS': [['>=average', 471.7471], ['<average', 528.0528]]}

#remove values with expected count<500 (i.e. 50%)
for key,values in expected_counts.items():
    for value in values:
        if value[1]<500:
            values.remove(value)
