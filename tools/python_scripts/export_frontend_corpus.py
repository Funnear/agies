import json
from pathlib import Path

with open('data/corpus/music_industry_corpus.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

nodes = corpus.get('nodes', [])
edges = corpus.get('edges', [])

conn_map = {}
for e in edges:
    src = e.get('source')
    tgt = e.get('target')
    if src not in conn_map:
        conn_map[src] = []
    if tgt not in conn_map:
        conn_map[tgt] = []
    conn_map[src].append(tgt)
    conn_map[tgt].append(src)

category_colors = {
    'city': '#00f0ff',
    'artist': '#c084fc',
    'venue': '#eab308',
    'studio': '#38bdf8',
    'record_label': '#f43f5e',
    'agency': '#f97316',
    'producer': '#ec4899',
    'festival': '#fb7185',
    'gear': '#84cc16',
    'genre': '#a855f7'
}

out_nodes = []
for n in nodes:
    nid = n['id']
    raw_type = str(n.get('entity_type', 'entity')).lower()
    cat = 'artist'
    if 'city' in nid or 'country' in raw_type or 'district' in nid or 'geo_' in nid or 'state_' in nid:
        cat = 'city'
    elif 'ven_' in nid or 'venue' in raw_type or 'club' in str(n.get('name','')).lower():
        cat = 'venue'
    elif 'std_' in nid or 'studio' in raw_type:
        cat = 'studio'
    elif 'lbl_' in nid or 'label' in raw_type:
        cat = 'record_label'
    elif 'gear_' in nid:
        cat = 'gear'
    elif 'subg_' in nid or 'genre' in raw_type:
        cat = 'genre'
    elif 'cur_' in nid or 'fest_' in nid:
        cat = 'festival'
    elif 'art_' in nid or 'artist' in raw_type:
        cat = 'artist'
    elif 'prd_' in nid or 'producer' in raw_type:
        cat = 'producer'
    elif 'agency' in raw_type or 'coll_' in nid:
        cat = 'agency'

    color = category_colors.get(cat, '#00f0ff')
    radius = 20 if cat in ['city', 'genre'] else (15 if cat in ['venue', 'artist', 'festival'] else 13)
    desc = n.get('description') or f"{n.get('name', nid)} is a premier music ecosystem entity."

    out_nodes.append({
        'id': nid,
        'name': n.get('name', nid),
        'category': cat,
        'country': n.get('country', ''),
        'color': color,
        'radius': radius,
        'description': desc[:160],
        'connections': list(set(conn_map.get(nid, [])))[:6],
        'bpm': n.get('attributes', {}).get('bpm', None),
        'genre': n.get('genres', [None])[0] if n.get('genres') else None,
        'soundSystem': n.get('attributes', {}).get('sound_system', None)
    })

out_dir = Path('frontend-next/public/data')
out_dir.mkdir(parents=True, exist_ok=True)
with open(out_dir / 'authentic_graph_nodes.json', 'w', encoding='utf-8') as f:
    json.dump(out_nodes, f, indent=2)

print(f"Exported {len(out_nodes)} authentic real-world nodes to frontend-next/public/data/authentic_graph_nodes.json!")
