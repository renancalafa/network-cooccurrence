import pandas as pd

header_colums = ['inp_readm30', 'cancer', 'renalfailure', 'pulmonarydisease', 'cardiacdisease', 'obesity', 'pregnancy', 'sickle', 'smoke', 'sot', 'diabetes', 'cbvsc', 'hypertension', 'hivaids', 'liverdisease', 'neuro', 'thalass', 'paralysis', 'hypothyroid', 'peptic', 'rheum', 'coag', 'wtloss', 'fluelec', 'blanemia', 'danemia', 'alcabuse', 'dabuse', 'psychoses', 'depression', 'mv']

races = ['Hispanic or Latino', 'Asian', 'White', 'Black or African American']
race_abv = ['hisp', 'asian', 'white', 'black']

c_all = pd.read_csv('covid.csv', usecols=[0] + list(range(220,254)))
# c_all = pd.read_csv('covid.csv', usecols=[0,221,222,223])
c_all_matrix = c_all.iloc[:,1:32]
c_all_matrix.to_csv('network_oc-all.csv', header=0, index=0)
co = list(range(1,10))
print(co)

# c_all_matrix.to_csv('network_oc-all.csv', header=0, index=0)

# for i, race in enumerate(races):
    
#     c_race = c_all[c_all.race_new == race].iloc[:,1:32]
#     print(race_abv[i], c_race.shape[0])
#     c_race.to_csv('network_oc-' + race_abv[i] + '.csv', header=0, index=0)
