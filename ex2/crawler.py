import requests
import lxml.html
import networkx as nx

DEBUG = False
MAX_DEPTH = 3
MAX_LINKS = 10

kiril_url = "/wiki/Kirill_Nababkin"
prefix = "https://en.wikipedia.org"


def crawl_rec(url, g, depth, visited):
    if depth > MAX_DEPTH or url in visited:
        return
    visited.add(url)
    urls = set()
    r = requests.get(prefix + url)
    doc = lxml.html.fromstring(r.content)
    if DEBUG:
        print("\n")
        print(url)
    for node in doc.xpath("//a[contains(@href,'/wiki/') and not(contains(@href,':'))]/@href"):
        if DEBUG:
            print("---" + str(node))

        if node in urls:
            continue

        urls.add(node)

        if depth == MAX_DEPTH:
            if node in visited:
                g.add_edge(url, node)
        else:
            if not g.has_node(node):
                g.add_node(node)
            g.add_edge(url, node)

        if len(urls) == MAX_LINKS:
            break

    depth += 1
    for link in urls:
        crawl_rec(link, g, depth, visited)


def crawl():              
    graph = nx.DiGraph()
    graph.add_node(kiril_url)
    crawl_rec(kiril_url, graph, 0, set())
    for node in graph.nodes():
        print(node + " = {" + ", ".join(graph[node]) + "}")
    return graph


