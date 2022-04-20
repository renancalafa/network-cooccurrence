import sys
import numpy as np
import networkx as nx
import pandas as pd
from dataframes import DataframeCreator
from network_cooccurrence import NetworkCoOccurrence


def main(path_occurrence_network, min_subjects, min_occurrences, race):
    occurrences = np.genfromtxt(path_occurrence_network, delimiter=',')
    metadata = pd.read_csv('network-metadata.csv')

    labels = np.asarray(metadata['label'].values)

    component = NetworkCoOccurrence()

    C, CC, RR_graph, RR_dist, G_rr, Phi_graph, Phi_dist, G_phi = component.get_network(labels,occurrences, min_subjects,
                                                                                       min_occurrences)

    nx.write_graphml(G_phi, 'graphs/G_phi-' + race +'.graphml')
    # nx.write_graphml(G_rr, 'G_RR-all.graphml')


if __name__ == '__main__':

    dataframe = DataframeCreator()
    dataframe.create_dataframe_occurrence()

    race_abv = ['black']
    # race_abv = ['all', 'hisp', 'asian', 'white', 'black']
    for race in race_abv:

        path_occurrence_network = 'dataframes/network_oc-' + race + '.csv'
        min_subjects = 1
        min_occurrences = 1

        if len(sys.argv) > 1:
            path_occurrence_network = sys.argv[1]

        if len(sys.argv) > 2:
            min_subjects = sys.argv[1]
        if len(sys.argv) > 3:
            min_occurrences = sys.argv[1]

        main(path_occurrence_network, min_subjects, min_occurrences, race)