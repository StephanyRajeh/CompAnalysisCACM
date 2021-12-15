"""""""""""""""""""""""""""" Community Hub-Bridge """""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def degree_method(g):
    list_nodes = g.nodes ()  # list of nodes
    dict_degree = dict ()  # nodes and their degree centrality

    for i in list_nodes:
        dict_degree[i] = g.degree(i)

    return dict_degree


def inout_degree(g, best):
    list = g.nodes ()
    dict_graph = dict ()  # nodes in the key and their neighbors
    for i in list:
        dict_graph[i] = []
    for i in list:
        iteri = g.neighbors (i)
        for j in iteri:
            dict_graph[i].append (j)

    dict_in = dict ()
    dict_out = dict ()
    d = degree_method (g)

    for i in list:
        community = best[i]
        nbr_in = 0
        for j in dict_graph[i]:
            if best[j] == community:
                nbr_in = nbr_in + 1 # intra links, since node's community (best[i]) is in the same as j's (best[j])
        idegree = d[i]
        nbr_out = idegree - nbr_in # inter links
        dict_in[i] = nbr_in
        dict_out[i] = nbr_out

    return dict_in,dict_out




def NNC(g,partition):

    #g: the network
    #partition: dict(node: its community)

    #returns: dict(node: number of neighboring communities with which it is connected)

    list_nodes = g.nodes ()

    dict_graph = dict ()  # nodes in the key and their neighbors
    for i in list_nodes:
        dict_graph[i] = []
    for i in list_nodes:
        iteri = g.neighbors(i)
        for j in iteri:
            dict_graph[i].append (j)

    dict_nnc=dict()



    for i in dict_graph:
        ens_community = set () # Will only contain unique communities
        for j in dict_graph[i]:
            ens_community.add(partition[j]) # add node j's (neighbor of i that can be reached in 1 hop) community to ens_comm 
        nbr=len(ens_community)
        dict_nnc[i]=nbr

    # Ce bloc de code permet d'ordonner les noeuds selon leurs comm centrality
    d = dict_nnc
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

    dict_nnc=dict_tri



    dict_nnc2=dict()
    dict_in,dict_out=inout_degree(g,partition)
    dict_degree=degree_method(g)

    e=set()
    for i in partition:
        e.add(partition[i])
    nbr_partition=len(e) # total number of partitions

    for i in dict_graph:
        dict_nnc2[i]=float(dict_nnc[i]/nbr_partition)*float(dict_out[i]/dict_degree[i]) # Steph: bridge influence

    # Ce bloc de code permet d'ordonner les noeuds selon leurs comm centrality
    d = dict_nnc2
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

    dict_nnc2=dict_tri


    return dict_nnc,dict_nnc2

def community_Hub_Bridge(g,partition):
    #g: network
    #partition: dict(node: its community)

    l_nodes = g.nodes ()
    taille=len(l_nodes)

    dict_size_community=dict() #dict(node: the size of its community)
    for i in partition:
        size_community=0
        icommunity=partition[i]
        for j in partition:
            if partition[j]==icommunity:
                size_community=size_community+1
        dict_size_community[i]=float(size_community/taille)

    dict_nnc, dict_nnc2 =NNC(g,partition) #dict_nnc2 will not directy be used, just do let the function work else we have an error
    dict_in,dict_out=inout_degree(g,partition)
    dict_degree=degree_method(g)

    e=set()
    for i in partition:
        e.add(partition[i])
    nbr_partition=len(e) # total number of partitions

    d_CHB=dict()
    for i in l_nodes:
        d_CHB[i]=dict_size_community[i]*float(dict_in[i]/dict_degree[i])+float(dict_nnc[i]/nbr_partition)*float(dict_out[i]/dict_degree[i])


    # Ce bloc de code permet d'ordonner les noeuds selon leurs comm centrality
    d = d_CHB
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

    d_CHB=dict_tri

    return d_CHB