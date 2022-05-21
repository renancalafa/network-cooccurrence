from msilib.schema import Class
from os import remove
import pandas as pd

class DataframeCreator:

    @staticmethod
    def create_dataframe_occurrence(race):
        # header_colums = ['inp_readm30', 'cancer', 'renalfailure', 'pulmonarydisease', 'cardiacdisease', 'obesity', 'pregnancy', 'sickle', 'smoke', 'sot', 'diabetes', 'cbvsc', 'hypertension', 'hivaids', 'liverdisease', 'neuro', 'thalass', 'paralysis', 'hypothyroid', 'peptic', 'rheum', 'coag', 'wtloss', 'fluelec', 'blanemia', 'danemia', 'alcabuse', 'dabuse', 'psychoses', 'depression', 'mv']

        colums=list(range(221,254))
        colums.append(7) #ICU
        colums.append(13) #DEATH
        colums_exclude=[227, 236, 239, 242, 243, 244, 246, 250, 251, 252]

        for num in colums_exclude:
            colums.remove(num)

        c_all = pd.read_csv('covid.csv', usecols=[] + colums)
        c_race = c_all[c_all.race_new == race["race_full"]].iloc[:,:24]
        c_race_all = c_race.iloc[:,2:24]
        c_race_comp = c_race[(c_race.ICU == 1) | (c_race.Death == 1)].iloc[:,2:24]
        c_race_ncomp = c_race[(c_race.ICU == 0) & (c_race.Death == 0)].iloc[:,2:24]
        print(race["race_abv"], c_race.shape[0])
        print('composite = ', c_race_comp.shape[0])
        print('non composite = ', c_race_ncomp.shape[0])
        c_race_all.to_csv('dataframes/' + race["race_abv"] + '/network_oc_' + race["race_abv"] + '_all.csv', header=0, index=0)
        c_race_comp.to_csv('dataframes/' + race["race_abv"] + '/network_oc_' + race["race_abv"] + '_c.csv', header=0, index=0)
        c_race_ncomp.to_csv('dataframes/' + race["race_abv"] + '/network_oc_' + race["race_abv"] + '_nc.csv', header=0, index=0)
        
        