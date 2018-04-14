import requests
import lxml.html
import networkx as nx
import matplotlib.pyplot as plt

DEBUG = True
MAX_DEPTH = 3
MAX_LINKS = 10

robot_url = "https://en.wikipedia.org/wiki/Robot"
prefix = "https://en.wikipedia.org"

def crawl_rec(url, g, depth, visited):
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
                crawl_rec(link, g, depth, visited)

def crawl():              
    graph = nx.DiGraph()
    graph.add_node(robot_url)
    return crawl_rec(robot_url, graph, 0, set())
