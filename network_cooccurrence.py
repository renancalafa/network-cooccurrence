import numpy as np
import networkx as nx
from comparator import Comparator


class NetworkCoOccurrence:

    def get_network(self, race, L, C, min_subjects=0, min_occurences=1, net_type=None):
        C = C.copy()
        C, CC = self.get_cooccurrence(C, min_subjects, min_occurences)
        np.savetxt('test/' + race["race_abv"] + '_CC.csv', np.asarray(CC), delimiter = ',', fmt='%.2f')
        N = C.shape[0]

        RR, RR_l, RR_u = self.get_risk_ratio(CC, N)
        RR_graph, RR_dist = self.get_graph_sig(RR, RR_l, RR_u)

        if net_type != 'all':
            if net_type == 'high':
                RR_graph[RR_graph <= 1] = 0
                RR_dist = RR_dist[RR_dist > 1]
            if net_type == 'less':
                RR_graph[RR_graph >= 1] = 0
                RR_graph = 1 / RR_graph
                RR_graph[~np.isfinite(RR_graph)] = 0
                RR_dist = RR_dist[RR_dist < 1]

        P = np.diag(CC)
        G_rr = self.create_graph(RR_graph, P, L)

        Phi, t = self.get_phi(CC, N)
        np.savetxt('test/' + race["race_abv"] + '_t.csv', np.asarray(t), delimiter = ',', fmt='%f')
        np.savetxt('test/' + race["race_abv"] + '_Phi.csv', np.asarray(Phi), delimiter = ',', fmt='%f')
        Phi_graph, Phi_dist = self.get_graph_phi(Phi, t)

        if net_type != 'all':
            if net_type == 'high':
                Phi_graph[Phi_graph <= 0] = 0
                Phi_dist = Phi_dist[Phi_dist > 0]
            if net_type == 'less':
                Phi_graph[Phi_graph >= 0] = 0
                Phi_graph = Phi_graph * -1
                Phi_dist = Phi_dist[Phi_dist < 0]

        G_phi = self.create_graph(Phi_graph, P, L)

        Comparator().create_main_sheet(Phi, t, race)

        return C, CC, RR_graph, RR_dist, G_rr, Phi_graph, Phi_dist, G_phi

    def product_matrix(self, V):
        return np.float64(np.dot(np.array(([V] * len(V))).T, np.diag(V)))

    def get_cooccurrence(self, occurence, min_subjects=5, min_occurences=2):
        # remove not statistically significant segments
        C = occurence.copy()
        C[:, np.sum(C, axis=0) <= min_subjects] = 0
        # remove sponsors with less than two different subsidies
        C = C[np.sum(C, axis=1) >= min_occurences, :]
        ### Co-Ocurrence
        CC = C.T.dot(C) * 1.
        return C, CC

    def get_risk_ratio(self, CC, N):
        ### Prevalence
        P = np.diagonal(CC)
        ### Total
        # N = len(units) * 1.
        PP = self.product_matrix(P)

        RR = N * CC * 1 / PP
        RR[~np.isfinite(RR)] = 0

        SIG = (1 / CC) + (1 / PP)
        if N == 0:
            SIG = SIG * np.inf
        else:
            SIG = SIG - 1 / N - 1 / (N ** 2)

        SIG[~np.isfinite(SIG)] = 0
        RR_l = RR * np.exp(-2.56 * SIG)
        RR_u = RR * np.exp(+2.56 * SIG)

        return RR, RR_l, RR_u

    def get_coprevalence(self, P):
        P_cooccurence = np.zeros((len(P), len(P)))
        for i in range(len(P)):
            for j in range(len(P)):
                #         if(j > i):
                P_cooccurence[i, j] = max(P[i], P[j])

        return P_cooccurence

    def get_phi(self, CC, N):
        # N = len(units) * 1.
        P = np.diagonal(CC)

        PP = self.product_matrix(P)
        NP = self.product_matrix(N - P)

        Phi_num = N * CC - PP
        Phi_dem = np.sqrt(PP * NP)
        Phi = Phi_num / (Phi_dem)

        sample_size = self.get_coprevalence(P)

        t_num = Phi * np.sqrt(sample_size - 2)
        t_den = np.sqrt(1 - (Phi ** 2))
        t = t_num / t_den

        Phi[~np.isfinite(Phi)] = 0
        t[~np.isfinite(t)] = 0
        return Phi, t

    def get_graph_sig(self, RR, RR_l, RR_u):
        RR_dist1 = np.copy(RR)
        RR_dist2 = np.copy(RR)
        # remove not significant
        is_sig = (RR_l > 1) | (RR_u < 1)
        RR_dist1[~is_sig] = 1
        # remove self-edges
        RR_graph = RR_dist1 - np.diag(np.diagonal(RR_dist1))
        # remove zeroes
        # RR_dist = np.trim_zeros(np.sort(RR_dist.ravel()))
        # RR_dist = RR_dist2[is_sig]
        RR_dist = RR_dist2.ravel()
        return RR_graph, RR_dist

    def get_graph_phi(self, Phi, t):
        Phi_dist1 = np.copy(Phi)
        Phi_dist2 = np.copy(Phi)
        # remove not significant
        is_sig = (t <= -1.96) | (t >= 1.96)
        Phi_dist1[~is_sig] = 0
        # remove self-edges
        Phi_graph = Phi_dist1 - np.diag(np.diagonal(Phi_dist1))

        # Phi_dist = Phi_dist2[is_sig]
        Phi_dist = Phi_dist2.ravel()
        return Phi_graph, Phi_dist

    def put_attributes(self, G, P, L, metric):
        for i in G.nodes:
            G.nodes[i]['prevalence'] = int(P[i])
            G.nodes[i]['sum_metric'] = float(np.sum(metric[i, :]))
            G.nodes[i]['label'] = L[i]

    def create_graph(self, matrix, P, L):
        G = nx.from_numpy_matrix(matrix)
        self.put_attributes(G, P, L, matrix)
        return G
