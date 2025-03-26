import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load co-occurrence data
cooc_df = pd.read_csv("data/sentiment_data/intent_cooccurrence_matrix.csv")

# Filter strong relationships
threshold = 0.5  # only show edges with strength >= 0.4
filtered_df = cooc_df[cooc_df["score"] >= threshold]

# Create graph
G = nx.Graph()

for _, row in filtered_df.iterrows():
    intent = row["intent"]
    related_intent = row["related_intent"]
    weight = row["score"]
    G.add_edge(intent, related_intent, weight=weight)

# Draw the graph
plt.figure(figsize=(14, 10))
pos = nx.spring_layout(G, k=0.5, seed=42)

edges = G.edges(data=True)
weights = [d['weight'] * 4 for (_, _, d) in edges]  # scale for visibility

nx.draw_networkx_nodes(G, pos, node_size=1200, node_color="skyblue")
nx.draw_networkx_edges(G, pos, width=weights, alpha=0.6)
nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")

plt.title("Intent Co-occurrence Network (Threshold ≥ 0.5)", fontsize=14)
plt.axis("off")
plt.tight_layout()
plt.savefig("intent_network_graph.png")
plt.show()
