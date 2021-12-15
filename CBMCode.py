import math

def degree_method(g):
    list_nodes = g.nodes ()  # list of nodes
    dict_degree = dict ()  # nodes and their degree centrality

    for i in list_nodes:
        dict_degree[i] = g.degree(i)

    return dict_degree

def CBM(g,partition):
    #partition=dict(node:community)

    l_nodes = g.nodes ()
    dict_graph = dict ()  # nodes in the key and their neighbors
    for i in l_nodes:
        dict_graph[i] = []
    for i in l_nodes:
        dict_graph[i] = g.neighbors (i)
        #dict_graph[i] = [n for n in g_relabled.neighbors(i)]
        

    d = degree_method (g)
    total_degree=sum(list(d.values()))

    list_community = []
    for i in partition:
        list_community.append (partition[i])

    #rho_in=dict(node: its inner density)
    rho_in=dict()
    for i in l_nodes:
        sum_indeg=0
        for j in dict_graph[i]:
            if partition[i]==partition[j]:
                sum_indeg=sum_indeg+1
        rho_in[i]=float(sum_indeg/d[i])

    #rho_out=dict(node: its extern density)
    rho_out=dict()
    for i in l_nodes:
        sum_outdeg=0
        for j in dict_graph[i]:
            if partition[i]!=partition[j]:
                sum_outdeg=sum_outdeg+1
        rho_out[i]=float(sum_outdeg/d[i])

    #entropy=dict(node: its entropy)
    entropy=dict()

    cbm=dict()

    for i in l_nodes:
        if (rho_in[i]!=0) and (rho_out[i]!=0):
            entropy[i]=-(rho_in[i]*math.log(rho_in[i]))-(rho_out[i]*math.log(rho_out[i]))
        elif (rho_in[i]!=0) and (rho_out[i]==0):
            entropy[i]=-(rho_in[i]*math.log(rho_in[i]))
        elif (rho_in[i]==0) and (rho_out[i]!=0):
            entropy[i]=-(rho_out[i]*math.log(rho_out[i]))
        else:
            entropy[i]=0

        cbm[i]=entropy[i]*(d[i]/total_degree)

    d = cbm
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

    dict_cbm = dict ()
    for i in l:
        dict_cbm[i] = d[i]

    return dict_cbm