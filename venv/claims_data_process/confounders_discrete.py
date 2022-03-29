import claims_preprocess
import claims_expval

# find confounders in discrete variables
list1 = []
for key in Dict.keys():
    if (key not in continuous) and (key != dependant_var):
        for value in Dict[key]:
            for key1 in expected_counts.keys():
                if key1 != key and (key1 not in continuous):
                    for value1 in expected_counts[key1]:
                        sum1 = 0
                        for i in range(1, 250):
                            counts_i = 0
                            rdf = dataset[dataset[key] == value].sample(25)
                            counts_i = rdf.loc[(rdf[key1] == value) & (rdf[dependant_var] == 1)].shape[0]
                            counts_i += rdf.loc[(rdf[key1] != value) & (rdf[dependant_var] == 0)].shape[0]
                            sum1 += counts_i
                        sum1 = sum1 / 6.25

                        sum2 = 0
                        for i in range(1, 250):
                            counts_i = 0
                            rdf = dataset[dataset[key] != value].sample(25)
                            counts_i = rdf.loc[(rdf[key1] == value) & (rdf[dependant_var] == 1)].shape[0]
                            counts_i += rdf.loc[(rdf[key1] != value) & (rdf[dependant_var] == 0)].shape[0]
                            sum2 += counts_i
                        sum2 = sum2 / 6.25

                        if (sum1 > float(value1[1]) and sum2 < float(value1[1])) or (
                                sum1 < float(value1[1]) and sum2 > float(value1[1])):
                            list1.append([key, key1, value, value1, sum1, sum2])

