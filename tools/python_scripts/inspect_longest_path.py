import json
import networkx as nx

with open('data/corpus/music_industry_corpus.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

G = nx.Graph()
for n in data['nodes']:
    G.add_node(n['id'], **n)
for e in data['edges']:
    G.add_edge(e['source'], e['target'], **e)

components = [G.subgraph(c).copy() for c in nx.connected_components(G)]
largest_cc = max(components, key=len)
print(f"Total Nodes: {len(G.nodes)} | Edges: {len(G.edges)}")
print(f"Largest Connected Component Nodes: {len(largest_cc.nodes)}")

# Compute diameter and longest shortest path
length_dict = dict(nx.all_pairs_shortest_path_length(largest_cc))
max_dist = 0
longest_pair = (None, None)
for u in length_dict:
    for v in length_dict[u]:
        if length_dict[u][v] > max_dist:
            max_dist = length_dict[u][v]
            longest_pair = (u, v)

path = nx.shortest_path(largest_cc, longest_pair[0], longest_pair[1])
print(f"\n============================================================")
print(f"  MAXIMUM GRAPH DIAMETER: {max_dist} HOPS")
print(f"  START: {longest_pair[0]} -> TARGET: {longest_pair[1]}")
print(f"============================================================")
for idx, nid in enumerate(path):
    n = largest_cc.nodes[nid]
    name = n.get('name', nid)
    etype = n.get('entity_type', 'node')
    edge_str = ""
    if idx > 0:
        prev = path[idx - 1]
        ed = G.get_edge_data(prev, nid)
        edge_str = f" <-- [{ed.get('rel_type', ed.get('relationship', 'CONNECTED'))}] -- "
    print(f"Hop {idx:2d}: {edge_str}[{etype}] {name} ({nid})")

# Also find transatlantic / transcontinental deep paths:
# e.g., Anjunadeep Goa -> Basic Channel Berlin -> Electric Lady NYC
print(f"\n============================================================")
print(f"  EMERGING CROSS-CONTINENTAL LINEAGE PATHWAYS")
print(f"============================================================")
pairs = [
    ("cur_anjuna_goa_sunset", "art_bjork"),
    ("ven_hilltop_goa", "ven_station_mines"),
    ("art_divine", "art_aphex"),
    ("std_yrf_mumbai", "std_abbeyroad"),
    ("subg_amapiano", "subg_jungle_dnb"),
]

for src, tgt in pairs:
    if src in G and tgt in G and nx.has_path(G, src, tgt):
        p = nx.shortest_path(G, src, tgt)
        print(f"\nPath: {G.nodes[src].get('name')} -> {G.nodes[tgt].get('name')} ({len(p)-1} hops):")
        for i, node_id in enumerate(p):
            n = G.nodes[node_id]
            print(f"  {i}: [{n.get('entity_type', '')}] {n.get('name', node_id)}")
