"""
Based on the article: Guimera, R., & Amaral, L. A. N. (2005). Functional cartography of complex metabolic networks. nature, 433(7028), 895-900.
"""


# ---------------------------------------------- Helper functions -----------------------------------------------------
def degree_method(g):
    list_nodes = g.nodes ()  # list of nodes
    dict_degree = dict ()  # nodes and their degree centrality

    for i in list_nodes:
        dict_degree[i] = g.degree(i)

    return dict_degree


# ---------------------------------------------- Main functions -----------------------------------------------------
def getPCExternal(g, communities):
    # community is a dictionary of key as nodes and value as their community
    
    #community = communities[2] # get the community of node i
    #neighbors_of_node = dict_graph[2]
    #total_degree_of_node = dict_degree[2]
    #dict_pc_external = 0
    
    # Get the total degree for each node
    dict_degree = degree_method(g)

    list = g.nodes()
    dict_graph = dict ()  # nodes in the key and their neighbors
    for i in list:
        dict_graph[i] = []
    for i in list:
        iteri = g.neighbors (i)
        for j in iteri:
            dict_graph[i].append (j)
    
    dict_pc_external = {}
    temp = 0
    
    for i in communities: # for each node
        dict_pc_external[i]=0
        community = communities[i] # get its community and put it in a variable
        neighbors_of_node = dict_graph[i]
        total_degree_of_node = dict_degree[i]
        for j in neighbors_of_node: # get the neighbors of node i 
            #print("neighbor of node 2: ",j)
            x = j
            if communities[x] != community: # check if community of node i is not the same
                #print("External neighbor of node 2: ", x)
                #print("Neighbors of external neighbor",x, "are: ", dict_graph[x])
                #print()
                temp = 1 # set temp = 1, but if neighbors are in the same community, increase temp
                neighbor_of_neighbor_list = dict_graph[x] # get the neighbors of the neighbor
                for neighbor_of_neighbor in neighbor_of_neighbor_list:
                    if communities[x] == communities[neighbor_of_neighbor]: # and check if they are in the same comm
                        if neighbor_of_neighbor in neighbors_of_node: # but make sure they are also neighbors of i 
                            temp = temp + 1
                            #print(x, neighbor_of_neighbor, temp)
                            neighbors_of_node.remove(neighbor_of_neighbor) # in order not to count the link twice
                working_on_temp = (temp/total_degree_of_node)**2
                #print(working_on_temp, "on neighbor node: ", x)
                dict_pc_external[i] =  dict_pc_external[i] + working_on_temp
                working_on_temp = 0
                temp = 0

    #community = communities[2] # get the community of node i
    #neighbors_of_node = dict_graph
    #total_degree_of_node = dict_degree[2]
    
  
    return dict_pc_external


def getPCInternal(g, communities):  
    # Get the total degree for each node
    dict_degree = degree_method(g)

    list = g.nodes()
    dict_graph = dict ()  # nodes in the key and their neighbors
    for i in list:
        dict_graph[i] = []
    for i in list:
        iteri = g.neighbors (i)
        for j in iteri:
            dict_graph[i].append (j)
    
    dict_pc_internal = {}
    temp = 0
    for i in communities: # for each node
        community = communities[i] # get its community and put it in a variable
        neighbors_of_node = dict_graph[i]
        total_degree_of_node = dict_degree[i] 
        for j in neighbors_of_node: # get the neighbors of node i 
            #print("neighbor of node 5: ",j)
            x = j
            if communities[x] == community: # check if community of node i are the same
                temp = temp + 1
            dict_pc_internal[i] = (temp/total_degree_of_node)**2
        temp = 0
    
    return dict_pc_internal
	
def getPCFinal(g, communities):
    dict_pc_internal = getPCInternal(g, communities) # Outer call 1
    dict_pc_external = getPCExternal(g, communities) # Outer call 2
    
    # Add up PC internal and PC external 
    dict_pc_final = {}
    for i in communities:
        dict_pc_final[i] = 1 - (dict_pc_internal[i] + dict_pc_external[i])
        
    return dict_pc_final