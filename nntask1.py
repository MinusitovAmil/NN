import xml.etree.ElementTree as xml
from re import split


def write_file(edges, v):
    graph = xml.Element("graph")
    for i in v:
        vertex = xml.SubElement(graph, "vertex")
        vertex.text = 'v' + str(i)
    for i in edges:
        arc = xml.SubElement(graph, "arc")
        fromx = xml.SubElement(arc, "from")
        fromx.text = 'v' + i[0]
        to = xml.SubElement(arc, "to")
        to.text = 'v' + i[2]
        order = xml.SubElement(arc, "order")
        order.text = i[4]
    tree = xml.ElementTree(graph)
    tree.write('graph1.xml')


def read_graph():
    with open('graph.txt', 'r') as input_graph:
        j = 0
        for line in input_graph:
            j += 1
    edges = split('\),\(', line)
    n = len(edges)
    for i in range(n):
        edges[i] = edges[i].replace('(', '')
        edges[i] = edges[i].replace(')', '')

    for i in range(n - 1):
        a = edges[i]
        # print(edge1)
        for j in range(1, n):
            b = edges[j]
            # print(edge2)
            if a != b:
                if a[2] == b[2] and a[4] == b[4]:
                    print('В строке № {} входных данных ошибка введенных данных'.format(str(j)))
                    exit()
                if a[0] == b[0] and a[2] == b[2]:
                    print('В строке № {} входных данных ошибка введенных данных'.format(str(j)))
                    exit()
    edges.sort(key=lambda i: (i[0], i[2]))
    c = edges
    k = []
    for i in range(n):
        k.append(([int(edges[i][0]), int(edges[i][2]), int(edges[i][4])]))
    edges = k
    # print(edges)
    v = []
    for i in range(n):
        v.append(edges[i][0])
        v.append(edges[i][1])
    v.sort()
    vertex = []
    for x in v:
        if x not in vertex:
            vertex.append(x)
    return c, vertex

if __name__ == '__main__':
    c, vertex = read_graph()
    write_file(c, vertex)


