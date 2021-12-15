import networkx as nx



def isbelong(list1, list2):
    x = 0
    for i in list1:
        for j in list2:
            if i == j:
                x = 1
    return x



def isexist(x, list1):
    k = 0
    for i in list1:
        if x == i:
            k = 1
    return k



def intra_wo(dict_graph_wo, partition):
    dict_node_partition_wo = dict()
    for i in dict_graph_wo: 
        dict_node_partition_wo[i] = [] 
        for j in partition:  
            for k in partition[j]:
                if i == k:
                    dict_node_partition_wo[i].append(j)

    d_copy = dict_graph_wo.copy()
    dict_g_intra_wo = dict()
    for i in d_copy:
        dict_g_intra_wo[i] = []
        for j in d_copy[i]:
            k = isbelong(dict_node_partition_wo[i], dict_node_partition_wo[j])  
            if k == 1:
                dict_g_intra_wo[i].append(j)

    graph_intra_wo = nx.Graph()
    for i in dict_g_intra_wo:
        graph_intra_wo.add_node(i)

    for i in dict_g_intra_wo:
        for j in dict_g_intra_wo[i]:
            graph_intra_wo.add_edges_from([(i, j)])

    return dict_g_intra_wo, graph_intra_wo


def intra_o(g, partition, lo):

    dict_node_partition = dict ()
    for i in g:  
        dict_node_partition[i] = [] 
        for j in partition: 
            for k in partition[j]:  
                if i == k:  
                    dict_node_partition[i].append(j)


    s = set()
    for i in lo:
        for j in dict_node_partition[i]:
            s.add(j) 
    s_sup = set()
    for i in partition:
        s_sup.add(i)  

    for i in s: 
        s_sup.remove(i) 

 
    g_copy = g.copy()
    for i in s_sup:
        for j in partition[i]:
            g_copy.remove_node(j)


    dict_g_intra_o = dict()
    for i in g_copy:
        dict_g_intra_o[i] =[]
        for j in g[i]:
            k = isbelong(dict_node_partition[i], dict_node_partition[j])  # Do they share any community? If so, append
            if k == 1:
                dict_g_intra_o[i].append(j)


    graph_intra_o = nx.Graph()
    for i in dict_g_intra_o:
        graph_intra_o.add_node(i)

    for i in dict_g_intra_o:
        for j in dict_g_intra_o[i]:
            graph_intra_o.add_edges_from([(i, j)])

    return dict_g_intra_o, graph_intra_o


def inter_wo_o(g, partition):

    dict_node_partition = dict()
    for i in g:
        dict_node_partition[i] = []
        for j in partition:
            for k in partition[j]:
                if i == k:
                    dict_node_partition[i].append(j)

    dict_g_inter = dict()
    for i in g:
        dict_g_inter[i] = []
        for j in g[i]:
            k = isbelong(dict_node_partition[i], dict_node_partition[j])
            if k == 0:
                dict_g_inter[i].append(j)


    graph_inter = nx.Graph()
    for i in dict_g_inter:
        graph_inter.add_node(i)

    for i in dict_g_inter:
        for j in dict_g_inter[i]:
            graph_inter.add_edges_from([(i, j)])

    return dict_g_inter, graph_inter

