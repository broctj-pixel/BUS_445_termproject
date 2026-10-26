import zipfile
import networkx as nx
import numpy as np
import pandas as pd

# 1. Define paths based on your VS Code workspace structure
zip_filename = 'Krackhardt-High-Tech-main.zip'

# Correct paths pointing directly to the nodes and multiplex edges inside the zip
nodes_file_path = 'Krackhardt-High-Tech-main/Dataset/Krackhardt-High-Tech_nodes.txt'
edges_file_path = 'Krackhardt-High-Tech-main/Dataset/Krackhardt-High-Tech_multiplex.edges'

print("Loading dataset directly from the zip file...")

# 2. Open the zip file and read nodes and edges in-memory
with zipfile.ZipFile(zip_filename, 'r') as z:
    # Read Nodes
    with z.open(nodes_file_path) as f:
        nodes_df = pd.read_csv(f, sep='\t')
        
    # Read Multiplex Edges
    with z.open(edges_file_path) as f:
        # The multiplex edges file typically uses space or tab separation
        edges_df = pd.read_csv(f, sep=r'\s+', header=None, names=['source', 'target', 'layer'])

print(f"Successfully loaded {len(nodes_df)} nodes and {len(edges_df)} edge records.")

# 3. Clean and Prepare Node Attributes & Simulate AI Adoption
np.random.seed(42) # Set seed for reproducible simulation

if 'department' not in nodes_df.columns:
    nodes_df['department'] = np.random.choice([1, 2, 3, 4], size=len(nodes_df))
if 'level' not in nodes_df.columns:
    nodes_df['level'] = np.random.choice([1, 2, 3], size=len(nodes_df), p=[0.1, 0.2, 0.7])

# Simulate AI Adoption Score (1 = Resistant, 5 = EnthusiasticChampion)
base_scores = nodes_df['department'].map({1: 4.0, 2: 3.5, 3: 2.5, 4: 3.0}).fillna(3.0)
noise = np.random.normal(0, 0.6, size=len(nodes_df))
nodes_df['ai_sentiment_score'] = np.clip(np.round(base_scores + noise), 1, 5)

def categorize_adoption(score):
    if score >= 4:
        return 'Champion'
    elif score >= 3:
        return 'Trial User'
    else:
        return 'Non-Adopter'

nodes_df['ai_status'] = nodes_df['ai_sentiment_score'].apply(categorize_adoption)

# 4. Build NetworkX Graph with explicit type consistency (casting to string)
G = nx.DiGraph()

node_id_col = nodes_df.columns[0]

# Add nodes with attributes (casting ID to string to ensure matches)
for _, row in nodes_df.iterrows():
    node_id = str(row[node_id_col]).strip()
    G.add_node(
        node_id, 
        department=row['department'], 
        ai_score=row['ai_sentiment_score'], 
        status=row['ai_status']
    )

# Filter for the 'advice' layer (or use all if layer column is absent)
if 'layer' in edges_df.columns:
    advice_edges = edges_df[edges_df['layer'].astype(str).str.contains('advice', case=False, na=False)]
    if len(advice_edges) == 0:
        advice_edges = edges_df
else:
    advice_edges = edges_df

# Add edges (casting source and target to string to match nodes)
for _, row in advice_edges.iterrows():
    source = str(row['source']).strip()
    target = str(row['target']).strip()
    G.add_edge(source, target)

# Print graph stats to verify it's connected properly
print(f"Graph successfully built with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

# 5. Calculate Social Network Analysis (SNA) Metrics directly on G
deg_cent = nx.degree_centrality(G)
bet_cent = nx.betweenness_centrality(G)

# Instead of mapping by a separate ID column, let's assign metrics 
# by matching the dataframe's row index or casting cleanly:
nodes_df['degree_centrality'] = nodes_df.index.astype(str).map(deg_cent)
nodes_df['betweenness_centrality'] = nodes_df.index.astype(str).map(bet_cent)

# Fallback if the graph uses 1-based or direct ID matching
if nodes_df['degree_centrality'].isna().all():
    nodes_df['degree_centrality'] = nodes_df[node_id_col].astype(str).map(deg_cent).fillna(0)
    nodes_df['betweenness_centrality'] = nodes_df[node_id_col].astype(str).map(bet_cent).fillna(0)
else:
    nodes_df['degree_centrality'] = nodes_df['degree_centrality'].fillna(0)
    nodes_df['betweenness_centrality'] = nodes_df['betweenness_centrality'].fillna(0)

print("\n--- Network Analysis & Simulated AI Adoption Summary ---")
print(nodes_df[[node_id_col, 'department', 'ai_sentiment_score', 'ai_status', 'degree_centrality', 'betweenness_centrality']].head(10))