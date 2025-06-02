from math import ceil

from src.fineman.betweenness_reduction import betweenness_reduction
from src.fineman.core_functions import super_source_bfd, compute_reach, h_hop_sssp, \
    h_hop_stsp, reweight_graph
from src.fineman.elimination_by_hop_reduction import _elimination_by_hop_reduction
from src.fineman.independent_set_or_crust import find_is_or_crust


def _eliminate_1hop_IS(graph, org_neg_edges, independent_set):
    out_I = {(u,v) for u in independent_set for v in graph[u].keys()}
    graph_out_I, _ = _subgraph_of_pos_edges_and_out_set(graph, org_neg_edges, out_I)
    return super_source_bfd(graph_out_I, out_I, 1)


def _make_U_r_remote(graph, neg_edges, neg_edges_T, negative_sandwich, beta):

    (x,U,y) = negative_sandwich
    phi = [0] * len(graph)

    dists_from_x = h_hop_sssp(x, graph, neg_edges, beta)
    dists_to_y = h_hop_stsp(y, graph, neg_edges_T, beta)

    for v in graph.keys():
        phi[v] = min(0, max(dists_from_x[v], -(dists_to_y[v])))

    return phi


def _subgraph_of_pos_edges_and_out_set(graph: dict[int, dict[int, float]], org_neg_edges, out_set: set):
    new_graph = {}
    new_neg_edges = set()

    for u, edge in graph.items():
        if u not in new_graph:
            new_graph[u] = {}
        for v, w in edge.items():
            if (u,v) in out_set or (w >= 0 and (u,v) not in org_neg_edges):
                new_graph[u][v] = w
                if w < 0:
                    new_neg_edges.add((u,v))

    return new_graph, new_neg_edges


def elimination_algorithm(org_graph, org_neg_edges, seed = None):
    n = len(org_graph.keys())

    k = len(org_neg_edges)
    r = ceil(k**(1/9))

    neg_vertices = set()
    neg_edges_T = set()
    for u,v in org_neg_edges:
        neg_vertices.add(u)
        neg_edges_T.add((v,u))
    
    phi_1 = betweenness_reduction(org_graph, org_neg_edges, tau=r, beta=r+1)
    graph_phi1, _, graph_T = reweight_graph(org_graph, phi_1, with_transpose=True)

    match find_is_or_crust(graph_phi1, org_neg_edges, neg_edges_T, neg_vertices):

        case (y,U_1):
            match find_is_or_crust(graph_T, neg_edges_T, org_neg_edges, U_1):
                case (x,U_2):
                    while len(U_2) > k**(1/3):
                        U_2.pop()
                    phi_2 = _make_U_r_remote(graph_phi1, org_neg_edges, neg_edges_T, (x,U_2,y), beta=r+1)

                    graph_phi1_phi2, _ = reweight_graph(graph_phi1, phi_2)

                    if len(compute_reach(graph_phi1_phi2, org_neg_edges, U_2, r)) > n / r:
                        return elimination_algorithm(org_graph, org_neg_edges)

                    out_U_2 = {(u, v) for u in U_2 for v in org_graph[u].keys()}
                    graph_phi1_phi2_out_U_2, neg_edges = _subgraph_of_pos_edges_and_out_set(graph_phi1_phi2, org_neg_edges, out_U_2)
                    phi = _elimination_by_hop_reduction(graph_phi1_phi2_out_U_2, neg_edges, r)

                    return reweight_graph(graph_phi1_phi2, phi)

                case I:
                    phi = _eliminate_1hop_IS(graph_phi1, org_neg_edges, I)
                    return reweight_graph(graph_phi1, phi)

        case I:
            phi = _eliminate_1hop_IS(graph_phi1, org_neg_edges, I)
            return reweight_graph(graph_phi1, phi)
