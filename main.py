import sys
import numpy as np
import networkx as nx
import pandas as pd
from dataframes import DataframeCreator
from network_cooccurrence import NetworkCoOccurrence
from comparator import Comparator

    
def main(path_occurrence_network, min_subjects, min_occurrences, race):
    occurrences = np.genfromtxt(path_occurrence_network, delimiter=',')
    metadata = pd.read_csv('network-metadata.csv')

    labels = np.asarray(metadata['label'].values)

    component = NetworkCoOccurrence()

    C, CC, RR_graph, RR_dist, G_rr, Phi_graph, Phi_dist, G_phi = component.get_network(race, labels,occurrences, min_subjects,
                                                                                       min_occurrences)

    nx.write_graphml(G_phi, 'graphs/' + race["race_abv"] + '/G_phi-' + race["path"] + '.graphml')
    # nx.write_graphml(G_rr, 'G_RR-all.graphml')


if __name__ == '__main__':
    

    races_test = [{
        "race_full":"Black or African American",
        "race_abv":"black",
    }]
    races = [
        {
            "race_full":"Hispanic or Latino",
            "race_abv":"hisp",
        },
        {
            "race_full":"Black or African American",
            "race_abv":"black",
        },
        {
            "race_full":"Asian",
            "race_abv":"asian",
        },
        {
            "race_full":"White",
            "race_abv":"white",
        },

    ]

    dataframe = DataframeCreator()
        

    # for i, race in enumerate(races):
    for i, race in enumerate(races):

        # dataframe.create_dataframe_occurrence(race)
        composite_sufix = ['_all','_c','_nc']

        for sufix in composite_sufix:
            race["path"] = race["race_abv"] + sufix
            path_occurrence_network = 'dataframes/' + race["race_abv"] + '/network_oc_' + race["path"] + '.csv'
            min_subjects = 1
            min_occurrences = 1

            if len(sys.argv) > 1:
                path_occurrence_network = sys.argv[1]

            if len(sys.argv) > 2:
                min_subjects = sys.argv[1]
            if len(sys.argv) > 3:
                min_occurrences = sys.argv[1]

            # main(path_occurrence_network, min_subjects, min_occurrences, race)
        
    Comparator().create_sheets(races)