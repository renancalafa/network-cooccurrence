from msilib.schema import Class
from os import remove
import pandas as pd

class DataframeCreator:

    @staticmethod
    def create_dataframe_occurrence():
        header_colums = ['inp_readm30', 'cancer', 'renalfailure', 'pulmonarydisease', 'cardiacdisease', 'obesity', 'pregnancy', 'sickle', 'smoke', 'sot', 'diabetes', 'cbvsc', 'hypertension', 'hivaids', 'liverdisease', 'neuro', 'thalass', 'paralysis', 'hypothyroid', 'peptic', 'rheum', 'coag', 'wtloss', 'fluelec', 'blanemia', 'danemia', 'alcabuse', 'dabuse', 'psychoses', 'depression', 'mv']

        races = ['Hispanic or Latino', 'Asian', 'White', 'Black or African American']
        race_abv = ['hisp', 'asian', 'white', 'black']

        colums=list(range(221,254))
        colums_exclude=[227, 236, 239, 242, 243, 244, 246, 250, 251, 252]

        for num in colums_exclude:
            colums.remove(num)

        c_all = pd.read_csv('covid.csv', usecols=[] + colums)
        c_all_matrix = c_all.iloc[:,:22]
        c_all_matrix.to_csv('dataframes/network_oc-all.csv', header=0, index=0)
        co = list(range(1,10))


        c_all_matrix.to_csv('dataframes/network_oc-all.csv', header=0, index=0)

        for i, race in enumerate(races):
            
            c_race = c_all[c_all.race_new == race].iloc[:,:22]
            print(race_abv[i], c_race.shape[0])
            c_race.to_csv('dataframes/network_oc-' + race_abv[i] + '.csv', header=0, index=0)
        
        