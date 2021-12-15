import random

def degree_method(g):
    list_nodes = g.nodes ()  # list of nodes
    dict_degree = dict ()  # nodes and their degree centrality

    for i in list_nodes:
        dict_degree[i] = g.degree(i)

    return dict_degree
	
def fraction_outerconnections(g,best):
    dict_fraction_outerconnections=dict()
    list = g.nodes ()

    #best = c.best_partition (g)
    list_community = []
    for i in best:
        list_community.append(best[i])
    list_community.sort ()
    list_community = set(list_community)
    l = []
    for i in list_community:
        l.append (i)
    list_community = l  # all communities in a list [0, 1, .... x]

    degree = degree_method (g)
    degree_in,degree_out=inout_degree(g,best)

    for i in list_community: # for each community
        µ=0
        couter=0
        for j in list: # for each node
            if best[j]==i: # if the community of node j is in community i
                couter=couter+1 # increment counter
                kout=degree_out[j] # get the outer degrees of this node
                k=degree[j] # get the total degrees of this node
                µ=µ+float(kout/k) # add it to u
        dict_fraction_outerconnections[i]=float(µ/couter)
    return dict_fraction_outerconnections

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


def max_inout(g,partition):
    #partition: dict(node: its community)

    max_in = dict ()
    max_out = dict ()
    list = g.nodes ()

    list_community = []
    for i in partition:
        list_community.append (partition[i])
    list_community.sort ()
    list_community = set (list_community)
    l=[]
    for i in list_community:
        l.append(i)
    list_community=l

    degree_in, degree_out = inout_degree (g,partition)

    for i in list_community:
        inmax=outmax=0
        for j in list:
            if partition[j]==i:
                if inmax<degree_in[j]:
                    inmax=degree_in[j]
                if outmax<degree_out[j]:
                    outmax=degree_out[j]
        max_in[i]=inmax
        max_out[i] = outmax

    return max_in,max_out


def comm_centreality(g,partition):
    #partition: dict(node: its community)

    list = g.nodes ()
    dict_comm=dict()

    max_in,max_out=max_inout(g,partition)
    dict_fraction_outerconnections=fraction_outerconnections(g,partition)
    dict_in,dict_out=inout_degree(g,partition)
    R=random.randint(1,50)
    """print(R)
    print(dict_fraction_outerconnections)
    print(max_in)
    print(max_out)
    print(dict_in)
    print(dict_out)"""
    for i in list:
        community=partition[i]
        µc=dict_fraction_outerconnections[community]
        maxkin=max_in[community]
        maxkout=max_out[community]
        #print('maxkin',maxkin)
        #print('maxkout',maxkout)

        kin=dict_in[i]
        kout=dict_out[i]


        if maxkout==0:
            dict_comm[i] = (1 + µc) * (float (kin / maxkin) * R) + (1 - µc) * (float (kout) * R) * (
            float (kout) * R)
        else:
            try:
                dict_comm[i] = (1 + µc) * (float (kin / maxkin) * R) + (1 - µc) * (float (kout / maxkout) * R) * (
                float (kout / maxkout) * R)
            except:
                pass
   
    d = dict_comm
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

    return dict_tri