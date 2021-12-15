"""
Based on the article: Zhao, Z., Wang, X., Zhang, W., & Zhu, Z. (2015). A community-based approach to identifying influential spreaders. Entropy, 17(4), 2228-2252.
"""


# ---------------------------------------------- Helper functions -----------------------------------------------------
# Input: dictionary of keys as nodes and values as community number
# Output: dictionary of keys as community number and values as nodes in that community
def flip_nodes_and_communities(dict_nodes_communities):
    # Step 1: initialize communities as keys
    new_dict = {}
    for k, v in dict_nodes_communities.items():
        new_dict[v]=[]
    
    # Step 2: Fill in nodes
    for kk,vv in new_dict.items():
        for k,v in dict_nodes_communities.items():
            if dict_nodes_communities[k] == kk: # If the community number (value) in `best` is the same as new_dict key (key), append the node (key) in `best`
            #print(k,v)
                new_dict[kk].append(k)
    
    return new_dict



# ---------------------------------------------- Main functions -----------------------------------------------------

def commmunityBasedCentrality(g, communities):
	# communities: dictionary of node: community number
    
    # Get the size of each community
    communities_flipped = flip_nodes_and_communities(communities) # call outer function
    community_size_dict = {}
    for i in communities_flipped:
        community_size_dict[i]=len(communities_flipped[i])
        
    # Get total nodes
    total_nodes = len(g)

    
    # Keep track of the link type a.k.a to which community the node externally links to
    list = g.nodes()
    dict_graph = dict ()  # nodes in the key and their neighbors
    for i in list:
        dict_graph[i] = []
    for i in list:
        iteri = g.neighbors (i)
        for j in iteri:
            dict_graph[i].append (j)

    dict_external_communities_and_sizes = {} # node: tup(external community, size)

    for i in communities: # for each node
        community = communities[i] # get its community and put it in a variable
        dict_external_communities_and_sizes[i]=[]
        for j in dict_graph[i]: # get neighbors of node i 
            if communities[j] != community: # check if the communities of the neighbors are not the same as node i
                tup = ()
                tup = (communities[j], community_size_dict[communities[j]], j) # external community, its size, the neighbor of node i in that external community
                dict_external_communities_and_sizes[i].append(tup)
    
    # Get external CBC for each node
    dict_cbc_external = {}
    for index1 in dict_external_communities_and_sizes: #for each node
        dict_cbc_external[index1] = 0
        for index2 in dict_external_communities_and_sizes[index1]: # index2 contains the tuple of each node, we can now access it
            #print(index2)
            #print(index2[0]) # Community number
            #print(index2[1]) # Community size
            #print(index2[2]) # Node in that community
            community_size = index2[1]
            temp = (community_size*1)/total_nodes
            dict_cbc_external[index1] = dict_cbc_external[index1] + temp
    
    dict_internal_communities_and_sizes = {} # node: tup(internal community, size)

    for i in communities: # for each node
        community = communities[i] # get its community and put it in a variable
        dict_internal_communities_and_sizes[i]=[]
        for j in dict_graph[i]: # get neighbors of node i 
            if communities[j] == community: # check if the communities of the neighbors are the SAME as node i
                tup = ()
                tup = (communities[j], community_size_dict[communities[j]], j) # internal community, its size, the neighbor of node i in that external community
                dict_internal_communities_and_sizes[i].append(tup)
    
    # Get internal CBC for each node
    dict_cbc_internal = {}
    for index1 in dict_internal_communities_and_sizes: #for each node
        dict_cbc_internal[index1] = 0
        for index2 in dict_internal_communities_and_sizes[index1]: # index2 contains the tuple of each node, we can now access it
            #print(index2)
            #print(index2[0]) # Community number
            #print(index2[1]) # Community size
            #print(index2[2]) # Node in that community
            community_size = index2[1]
            temp = (community_size*1)/total_nodes
            dict_cbc_internal[index1] = dict_cbc_internal[index1] + temp
            
    # Add up CBC internal and CBC external 
    dict_cbc_final = {}
    for i in dict_cbc_internal:
        dict_cbc_final[i] = dict_cbc_internal[i] + dict_cbc_external[i]
        
    return dict_cbc_final