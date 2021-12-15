"""""""""""""""""""""""""""" K-shell with community centrality """""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import networkx as nx


def kshell_community(g,g_wo_intra,g_inter,alpha=0.5):
    #this centrality was used in networks with non-overlapping community structure
    #g: network
    # the parameter alpha gives more or less weight to the intra and inter-community links, it is set to 0.5 in their paper

    l_nodes = g.nodes ()

    #g_wo_intra: dict(node: list of its neighbors) contains only the nodes of the local network formed from the intra-community links
    g_wo_intra_converted = nx.Graph(g_wo_intra)
    dict_intra_kshell = nx.core_number(g_wo_intra_converted)

    #g_inter: dict(node: list of its neighbors) contains only the nodes of the global network formed from the inter-community links
    g_inter_converted = nx.Graph(g_inter)
    dict_inter_kshell = nx.core_number(g_inter_converted)


    d_kshell_community=dict()
    for i in l_nodes:
        d_kshell_community[i]=alpha*dict_intra_kshell[i]+((1-alpha)*(1+dict_inter_kshell[i]))

    d = d_kshell_community
    l = []
    for i in d:
        l.append (i)

    n = len (d)
    for i in range (0, n - 1):
        max = i
        for j in range (i + 1, n):
            if d[l[max]] < d[l[j]]:
                max = j
        if max != i:
            x = l[i]
            l[i] = l[max]
            l[max] = x

    dict_tri = dict ()
    for i in l:
        dict_tri[i] = d[i]

    d_kshell_community=dict_tri

    return d_kshell_community