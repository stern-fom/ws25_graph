import sys

import graphviz

graph = {
    "a": ["b", "e"],
    "b": ["a", "c", "f"],
    "c": ["b", "d"],
    "d": ["c", "g", "j", "s", "z"],
    "e": ["a", "f", "h"],
    "f": ["b", "e", "g", "h"],
    "g": ["f", "d", "j"],
    "h": ["e", "f", "i"],
    "i": ["h", "j", "k", "q"],
    "j": ["d", "g", "i", "q"],
    "k": ["i", "l"],
    "l": ["k", "q"],
    "n": ["r", "t", "u"],
    "q": ["i", "j", "l", "r"],
    "r": ["n", "q", "s"],
    "s": ["r", "d", "u", "z"],
    "t": ["v", "n"],
    "u": ["n", "s", "w"],
    "v": ["x", "t"],
    "w": ["u", "x", "z"],
    "x": ["w", "v", "y"],
    "y": ["z", "x"],
    "z": ["d", "s", "w", "y"],
}

dfs_visited = set()
dfs_list = []

def depth_first_search(graph_param, node):
    if node in dfs_visited:
        return
    dfs_list.append(node)
    print(node, end=", ")
    adjacents = graph_param[node]
    for adjacent in adjacents:
        dfs_visited.add(node)
        depth_first_search(graph_param, adjacent)

bfs_list = []

def breadth_first_search(graph_param, start_node):
    current_nodes = [start_node]
    next_nodes = []
    output = set()
    distance = 0
    if start_node not in output:
        output.add(start_node)
        print(start_node, end=", ")
        bfs_list.append((start_node, distance))
    while len(current_nodes):
        distance += 1
        for node in current_nodes:
            for adjacent in graph_param[node]:
                if adjacent not in output:
                    output.add(adjacent)
                    bfs_list.append((adjacent, distance))
                    print(adjacent, end=", ")
                    next_nodes.append(adjacent)
        current_nodes = next_nodes
        next_nodes = []

if __name__ == '__main__':
    depth_first_search(graph, "a")

    dot = graphviz.Graph(engine="neato")
    dot.attr('node', shape='circle', style='filled')

    for node in graph:
        dot.node(node, label=node)

    edges_known = []

    for node in graph:
        adjacents = graph[node]
        for adjacent in adjacents:
            a, b = node, adjacent
            if a > b:
                a, b = b, a
            if (a, b) in edges_known:
                # Wenn die Edge schon bekannt ist, nicht erneut zeichnen
                continue
            edges_known.append((a, b))  # Edge als gezeichnet merken
            dot.edge(node, adjacent)

    dot.render(filename='out\\graph.dot', format='pdf', view=False)

    for i, visited in enumerate(dfs_list):
        dot.node(visited, label=visited, color='red', fillcolor="white")
        print(f"Make node \"{visited}\" red.")
        dot.render(filename=f'out\\graph_{i:02d}', format='png', view=False)


    breadth_first_search(graph, "a")

    maximum_steps = max([t[1] for t in bfs_list])
    color_table = ["#ffffff"]
    for i in range(1, maximum_steps + 1):
        # Nichtlineare Interpolation (quadratisch) für Grün und Blau
        factor = (i / maximum_steps) ** 2
        green_blue = int(255 * (1 - factor))
        color_hex = f"#ff{green_blue:02x}{green_blue:02x}"
        color_table.append(color_hex)

    for i, visited in enumerate(bfs_list):
        distance = visited[1]
        color_string = color_table[distance]
        dot.node(visited[0], fillcolor=color_string)
        print(f"Fill node \"{visited}\" with color \"{color_string}\".")
        dot.render(filename=f'out_bfs\\graph_{i:02d}', format='png', view=False)