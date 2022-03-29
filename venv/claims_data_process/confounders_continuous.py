import claims_preprocess
import claims_expval
import confounders_discrete

# find confounders in continuous variables
expected_counts_continuous = {x: expected_counts[x] for x in continuous}
list2 = []
for key in Dict.keys():
    if key != dependant_var:
        for value in Dict[key]:
            for key1 in expected_counts_continuous.keys():
                if key1 != key:
                    for value1 in expected_counts_continuous[key1]:
                        try:
                            if value1[0] == '>=average':
                                sum1 = 0
                                for i in range(1, 250):
                                    counts_i = 0
                                    rdf = dataset[dataset[key] == value].sample(25)
                                    counts_i = \
                                    rdf.loc[(rdf[key1] >= dataset[key1].mean()) & (rdf[dependant_var] == 1)].shape[0]
                                    counts_i += \
                                    rdf.loc[(rdf[key1] < dataset[key1].mean()) & (rdf[dependant_var] == 0)].shape[0]
                                    sum1 += counts_i
                                sum1 = sum1 / 6.25

                                sum2 = 0
                                for i in range(1, 250):
                                    counts_i = 0
                                    rdf = dataset[dataset[key] != value].sample(25)
                                    counts_i = \
                                    rdf.loc[(rdf[key1] >= dataset[key1].mean()) & (rdf[dependant_var] == 1)].shape[0]
                                    counts_i += \
                                    rdf.loc[(rdf[key1] < dataset[key1].mean()) & (rdf[dependant_var] == 0)].shape[0]
                                    sum2 += counts_i
                                sum2 = sum2 / 6.25

                            if value1[0] == '<average':
                                sum1 = 0
                                for i in range(1, 250):
                                    counts_i = 0
                                    rdf = dataset[dataset[key] == value].sample(25)
                                    counts_i = \
                                    rdf.loc[(rdf[key1] < dataset[key1].mean()) & (rdf[dependant_var] == 1)].shape[0]
                                    counts_i += \
                                    rdf.loc[(rdf[key1] >= dataset[key1].mean()) & (rdf[dependant_var] == 0)].shape[0]
                                    sum1 += counts_i
                                sum1 = sum1 / 6.25

                                sum2 = 0
                                for i in range(1, 250):
                                    counts_i = 0
                                    rdf = dataset[dataset[key] != value].sample(25)
                                    counts_i = \
                                    rdf.loc[(rdf[key1] < dataset[key1].mean()) & (rdf[dependant_var] == 1)].shape[0]
                                    counts_i += \
                                    rdf.loc[(rdf[key1] >= dataset[key1].mean()) & (rdf[dependant_var] == 0)].shape[0]
                                    sum2 += counts_i
                                sum2 = sum2 / 6.25

                            if (sum1 > float(value1[1]) and sum2 < float(value1[1])) or (
                                    sum1 < float(value1[1]) and sum2 > float(value1[1])):
                                list2.append([key, key1, value, value1, sum1, sum2])

                        except ValueError:
                            pass

