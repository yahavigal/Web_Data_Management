import networkx as nx
import matplotlib.pyplot as plt
import crawler

def PageRank(G):
    N = G.number_of_nodes()
    d = 0.3
    iters = 60

    if (N == 0):
        return

    result = {node: [1/N, 1/N] for node in G.nodes()}

    for node in G.nodes():
        if G.out_degree(node) == 0:
            G.add_edge(node, node)

    for i in range(iters):
        for node in G.nodes():
            result[node][i%2] = d*(1/N) + (1-d)*sum([result[prev][(i-1)%2]/G.out_degree(prev) for prev in G.predecessors(node)])


    return {k: v[0] for k,v in result.items()}


G = crawler.crawl()
print('\n')
result = PageRank(G)
sorted_result =  sorted(result.items(), key=lambda x: x[1], reverse=True)
for url, rank in sorted_result:
    print(str(url)  + ": " + str(rank))
