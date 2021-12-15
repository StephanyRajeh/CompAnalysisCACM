import sys
import time
from os import listdir
from os.path import isfile, join
import networkx as nx
from igraph import *
import igraph as ix
import matplotlib.pyplot as plt
import scipy.io as spio
import pandas as pd
#from utils import *


colorlist = {0:"red", 1:"orange", 2:"green",3:"yellow", 4:"pink",5:"blue", 6:"azure",7:"cyan",8:"magenta",9:"purple",10:"white",\
    11:"peru",12:"sienna",13:"navy",14:"tomato",15:"violet",16:"plum",17:"thistle",18:"orchid",19:"beige",20:"tan",\
    21:"orchid",22:"lavender",23:"goldenrod",24:"khaki",25:"grey",26:"ivory",27:"salmon",28:"royalblue",29:"limegreen",30:"seagreen",\
    31:"burlywood",32:"coral",33:"black",34:"sandybrown",35:"firebrick"\
    }

def triangles(G,nodes=None):
    if nodes is None:
        nodes_nbrs = G.adj.items()
    else:
        nodes_nbrs= ( (n,G[n]) for n in G.nbunch_iter(nodes) )
    for v,v_nbrs in nodes_nbrs:
        vs=set(v_nbrs) -set([v])
        ntriangles=0
        for w in vs:
            ws=set(G[w])-set([w])
            ntriangles+=len(vs.intersection(ws))
        yield (v,len(vs),ntriangles)

def edge_support(G):
    neighbors=G.neighborhood()    #neighbors_iter
    nbrs=dict((v.index,set(neighbors[v.index])) for v in G.vs)
    support = {}
    for e in G.es:
        nod1,nod2 = e.source, e.target
        nod1_nbrs = set(nbrs[nod1])-set([nod1])
        nod2_nbrs = set(nbrs[nod2])-set([nod2])
        sup = len(nod1_nbrs.intersection(nod2_nbrs))
        #G[nod1][nod2]['support'] = sup
        support[(nod1,nod2)] = sup
    #print 'support :', support
    return support

def ktruss(G):
    #G = G.simplify()    #assume graph is simple
    #G.to_undirected(mode=False)
    support = edge_support(G)
    edges=sorted(support,key=support.get)
    bin_boundaries=[0]
    curr_support=0
    for i,e in enumerate(edges):
        if support[e]>curr_support:
            bin_boundaries.extend([i]*(support[e]-curr_support))
            curr_support=support[e]

    edge_pos = dict((e,pos) for pos,e in enumerate(edges))
    #print 'edge-pos:',edge_pos
    truss={}         ## initial guesses for truss is support
    neighbors=G.neighborhood()    #neighbors_iter
    #print 'neighbors:', neighbors
    nbrs=dict((v.index,(set(neighbors[v.index])-set([v.index]))) for v in G.vs)
    #nbrs=dict((v.index,set(neighbors[v.index])) for v in G.vs)
    #print 'nbrs:', nbrs
    for e in edges:
      #print 'processing edge : ', e, 'support :', support[e], 'pos:', edge_pos[e]
      u,v =e[0], e[1]
      if not(u == v) :
        common_nbrs = set(nbrs[u]).intersection(nbrs[v])
        #print u,v,'common_nbrs',common_nbrs
        for w in common_nbrs:
            if (u,w) in support :
               e1 = (u,w)
            else :
               e1 = (w,u)
            if (v,w) in support :
               e2 = (v,w)
            else:
               e2 = (w,v)
            pos=edge_pos[e1]
            if support[e1] > support[e] :
               bin_start=bin_boundaries[support[e1]]
               edge_pos[e1]=bin_start
               edge_pos[edges[bin_start]]=pos
               edges[bin_start],edges[pos]=edges[pos],edges[bin_start]
               bin_boundaries[support[e1]]+=1
            #print 'e1',e1,'support:',support[e1], 'pos:', pos, 'new pos:', edge_pos[e1]

            pos=edge_pos[e2]
            if support[e2] > support[e] :
               bin_start=bin_boundaries[support[e2]]
               edge_pos[e2]=bin_start
               edge_pos[edges[bin_start]]=pos
               edges[bin_start],edges[pos]=edges[pos],edges[bin_start]
               bin_boundaries[support[e2]]+=1
            #print 'e2',e2,'support:',support[e2], 'pos:', pos, 'new pos:', edge_pos[e2]

            support[e1] =  max(support[e], support[e1]-1)
            support[e2] =  max(support[e], support[e2]-1)

        truss[e] = support[e] + 2
        nbrs[u].remove(v)
        nbrs[v].remove(u)
    #print 'Truss: ', truss
    #print 'Sorted Truss: ', sorted(truss,key=truss.get)
    return truss


def get_ktrussProbs(g, name):
    print ("Extracting KTruss features: %s" % name)
    trussness = ktruss(g).values()
    n = len(trussness)
    d = {n:trussness.count(n) for n in range(2,max(trussness)+1)}
    ktrussprobability = [d[key] / (n * 1.0) for key in sorted(d)]
    return (ktrussprobability)

def getnodetrussness(graph):
    # Me
    dict_node_truss = {}
    n = graph.vcount()
    ktrussdict = ktruss(graph)
    nodetruss = [0] * n
    for edge in graph.es:
      source = edge.source
      target = edge.target
      if not (source == target) :
         t = ktrussdict[(source,target)]
      else:
         t = 0
      nodetruss[source] = max(nodetruss[source], t)
      nodetruss[target] = max(nodetruss[target], t)
      
    

    return nodetruss
	
def getnodetrussnessdict(graph):
    sr_node_ktruss_dict = {} 
    n = graph.vcount()
    ktrussdict = ktruss(graph)
    nodetruss = [0] * n
    for edge in graph.es:
        source = edge.source
        target = edge.target
        if not (source == target) :
            t = ktrussdict[(source,target)]
        else:
            t = 0
        nodetruss[source] = max(nodetruss[source], t)
        nodetruss[target] = max(nodetruss[target], t)
    d = {}
    node_index = 0
    node_truss_value = 0
    while (node_index<len(nodetruss)):
        d[node_index] = nodetruss[node_truss_value]
        node_truss_value = node_truss_value+1
        node_index = node_index+1
    return d

def mappingAndRelabeling(g):
    # Mapping
    g_nx=g.copy()
    l_nodes = g_nx.nodes ()
    taille=len(l_nodes)
    dict_graph = dict ()  # nodes in the key and themselves
    for i in l_nodes:
        dict_graph[i] = [i]
    index = 0
    for i in dict_graph:
        for j in dict_graph[i]:
            dict_graph[i] = index
            index = index + 1
            
    # Relabling: Construct a new graph with those mappings now
    mapping = dict_graph
    g_relabled = nx.relabel_nodes(g, mapping, copy=True)
    
    return g_relabled


