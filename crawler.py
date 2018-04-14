import requests
import lxml.html
import networkx as nx
import matplotlib.pyplot as plt

DEBUG = True
MAX_DEPTH = 3
MAX_LINKS = 10

print('Starting...')
robot_url = "https://en.wikipedia.org/wiki/Robot"
prefix = "https://en.wikipedia.org"

def crawl(url, g, depth, visited):
    if depth > MAX_DEPTH:
        return
    visited.add(url)
    urls = []
    r = requests.get(url)
    doc = lxml.html.fromstring(r.content)
    i = 0
    if DEBUG:
        print("\n")
        print(url)
    for t in doc.xpath("//a[contains(@href,'/wiki/') and not(contains(@href,':'))]/@href"):
        if DEBUG:
            print("---" + str(t))
        node = prefix + t
        urls.append(node)
        g.add_node(node)
        g.add_edge(url, node)
        i += 1
        if i == MAX_LINKS:
            break
    depth += 1
    if len(urls) > 0:
        for link in urls:
            if link not in visited:
                crawl(link, g, depth, visited)


depth = 0
visited = set()
g = nx.DiGraph()
g.add_node(robot_url)
crawl(robot_url, g, depth, visited)
print('number of nodes: ' + str(g.number_of_nodes()))
print('number of edges: ' + str(g.number_of_edges()))
nx.draw(g, with_labels=True)
plt.show()