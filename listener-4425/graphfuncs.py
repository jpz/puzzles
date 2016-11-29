# A small collection of graph traversal functions


def add_connection(connections, parent, child):
    if parent == child:
        return
    if connections.get(parent) is None:
        connections[parent] = set()
    connections[parent].add(child)


def is_node_in_subgraph(connections, node, target):
    if target in connections[node]:
        return True
    for subgraph in connections[node]:
        if is_node_in_subgraph(connections, subgraph, target):
            return True
    return False


def prune_redundant_links(connections):
    direct_connections = {}
    for node in connections:
        direct_connections[node] = set()
        for target in connections[node]:
            add = True
            for subgraph in connections[node]:
                if subgraph != target:
                    if is_node_in_subgraph(connections, subgraph, target):
                        add = False
            if add:
                direct_connections[node].add(target)
    return direct_connections


def is_child_node_of(connections, child, possible_parent):
    """Is Child Node, i.e. there is a greater-than node that points directly or indirectly to the child"""
    if child in connections[possible_parent]:
        return True
    for ppchild in connections[possible_parent]:
        if is_child_node_of(connections, child, ppchild):
            return True
    return False


def populate_indirect_links(connections):
    indirect_connections = {}
    for parent in connections:
        indirect_connections[parent] = set()
        for child in connections:
            if parent != child:
                if is_child_node_of(connections, child, parent):
                    indirect_connections[parent].add(child)
    return indirect_connections


def invert_graph(connections):
    inv = dict((n, set()) for n in connections)
    for a in connections:
        for b in connections[a]:
            inv[b].add(a)
    return inv

