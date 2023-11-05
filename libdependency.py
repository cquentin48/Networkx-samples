import argparse
import requests
import networkx as nx
import matplotlib.pyplot as plt
"""
pos = None
annot = None
ax = None
nodes = None
"""

def display_graph(graph: nx.Graph):
    global pos
    global annot
    global ax
    global nodes
    global fig
    fig, ax = plt.subplots()
    annot = ax.annotate(
        "",
        xy=(0,0),
        xytext=(20,20),
        textcoords="offset points",
        bbox=dict(boxstyle="round", fc="w"),
        arrowprops=dict(arrowstyle="->")
    )
    pos = nx.spring_layout(graph,seed=3068)
    nodes = nx.draw_networkx_nodes(graph, pos=pos, ax=ax)
    nx.draw_networkx_labels(graph, pos=pos)
    nx.draw_networkx_edges(graph, pos, ax=ax)
    fig.canvas.mpl_connect("motion_notify_event", hover)
    plt.show()

def update_annot(ind):
    node = ind["ind"][0]
    xy = pos[node]
    annot.xy = xy
    node_attr = {'node' : node}
    node_attr.update(graph.nodes[node])
    text = '\n'.join(f'{k} : {v}' for k, v in node_attr.items())
    annot.set_text(text)

def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = nodes.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

def fetch_raw_data(package: str) ->[str]:
    """Fetch the first dependencies of package

    Args:
        num_depedencies (int): number of depedencies shown into a graph

    Returns:
        array : raw depedencies
    """
    url = 'https://pypi.org/pypi/{}/json'

    json = requests.get(url.format(package)).json()
    return json

def return_lib_attributes(name, version):
    """Node attribute for the library fetched

    Args:
        name (str): Library name
        version (str): Library version

    Returns:
        {str, str}: Node attribute with the following form :
        ```python
        {
            name,
            version
        }
        ```
    """
    return {
            'name':name,
            'version':version
        }

def return_data_dependency(single_dependency:str) -> {str,str}:
    """Build data attributes for a single dependency

    Args:
        single_dependency (str): single dependency string data

    Returns:
        {str,str}: dependency attribute for a node with the following form:
        ```python
        {
            name,
            version
        }
        ```
    """
    attrs = single_dependency.split('>=')
    return {
        'name': attrs[0],
        'version': attrs[1]
    }

def build_attributes(raw_list: list, number_of_neighbors:int) -> [str]:
    """Build attribute list based on the list fetched from
    Pypi website and 

    Args:
        raw_list (list): list fetched from Pypi API
        number_of_neighbors (int): Number of first neighbors from
        a list to be displayed

    Returns:
        [str]: _description_
    """
    lib_attribute = return_lib_attributes(
        raw_list['info']['name'],
        raw_list['info']['version']
    )
    attrs = {
        0:lib_attribute
    }
    for i in range(0,number_of_neighbors):
        single_dependency = raw_list['info']['requires_dist'][i].split('; ')[0]
        attrs[i] = return_data_dependency(single_dependency)
    return attrs

def build_graph(lib_name:str, dependencies_count:int) -> nx.DiGraph:
    """Build a directed graph based on dependencies
    of a library on Pypi with a limit amount of dependencies

    Args:
        lib_name (str): library on Pypi
        dependencies_count (int): number of dependencies to be displayed
        on a graph (first one)

    Returns:
        nx.DiGraph: newly created directed graph
    """
    #raw_list = fetch_raw_data('pandas')
    raw_list = fetch_raw_data(lib_name)
    #attrs = build_attributes(raw_list,30)
    attrs = build_attributes(raw_list,dependencies_count)
    graph = nx.DiGraph()
    #for i in range(0,31):
    for i in range(0,dependencies_count+1):
        graph.add_node(i)
        if i >= 1:
            graph.add_edge(0,i)
    nx.set_node_attributes(graph, attrs)
    return graph

def parse_args():
    parser = argparse.ArgumentParser(
        prog='Python dependency graph visualiser',
        description='Display in a graph the dependencies of a pypi'+\
            ' libraries published on this website'
    )
    parser.add_argument(
        '-l',
        '--library',
        type=str,
        help='library',
        default='pandas'
    )
    parser.add_argument(
        '-n',
        '--number',
        type=int,
        help='number of dependencies to be shown',
        default=30
    )
    args = parser.parse_args()
    return(args.library, args.number)

(library_name, dep_numbers) = parse_args()
graph = build_graph(library_name, dep_numbers)
print(graph)
display_graph(graph)
