import pandas as pd
import numpy as np
import networkx as nx
import openpyxl as op

class Comparator:

    comorbidities = ['cancer', 'renalfailure', 'pulmonarydisease', 'cardiacdisease', 'obesity', 'pregnancy', 'smoke', 'sot', 'diabetes', 'cbvsc', 'hypertension', 'hivaids', 'liverdisease', 'neuro ', 'paralysis', 'hypothyroid', 'rheum', 'coag', 'danemia ', 'dabuse', 'psychoses', 'depression']

    def get_data_dict(this):
        race_data = []
        cmbdts = this.comorbidities
        dataframe = pd.read_csv('test/Phi.csv', header=None)
        dataframe_dist = dataframe.to_dict('records')
        for i, data in enumerate(dataframe_dist):
            for key in data:
                race_data.append({
                    "Source": cmbdts[i],
                    "Target": cmbdts[key],
                    "Value": data[key],
                })
        print(race_data)
        wb = op.Workbook()
        ws = wb.active
            