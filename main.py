import networkx as nx
import matplotlib.pyplot as plt

def set_initial_attributes():
    attrs = {}
    for i in range(0,10):
        attrs[i] = {
            "state":-1,
            "leader":-1,
            "messageCount":0,
            "algoCount":0
        }
    return attrs

def add_edges(graph:nx.Graph):
    graph.add_edge(len(graph.nodes),0)
    for i in range(0,len(graph.nodes)-1):
        graph.add_edge(i,i+1)

def create_graph():
    graph = nx.Graph()
    for i in range(0,10):
        graph.add_node(i)
    attrs = set_initial_attributes()
    nx.set_node_attributes(graph, attrs)
    add_edges(graph)
    return graph

def display_graph(graph: nx.Graph):
    pos = nx.spring_layout(graph,seed=3068)
    nx.draw(graph, pos=pos, with_labels=True)
    plt.show()


algo_graph = create_graph()
print(algo_graph.edges)
display_graph(algo_graph)
