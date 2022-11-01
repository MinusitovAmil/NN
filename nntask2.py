from re import split


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
    return (edges, vertex)


def matr(edges, vertex):
    n = len(vertex)
    m = [[0]*n for i in range(n)]
    for a in edges:
        m[a[0]-1][a[1]-1] = 1
    return m


def stok(matr):
    n = len(matr)
    crs = []
    for r in range(n):
        for c in range(n):
            if matr[r][c] != 0:
                break
        else:
            crs.append(r + 1)
    return crs


def dfs(v, color, d):
    color[v] = 'grey'
    for y in d[v]:
        if color[y] == 'white':
            dfs(y, color, d)
        if color[y] == 'grey':
            print('Ошибка введённых данных. В графе обнаружен цикл')
            exit()
    color[v] = 'black'


def Function(x, func): # вычисление функции графа
    if len(d[x]) == 0:
        return func
    func += '('
    t = False
    for v in d[x]:
        if t == True:
            func += ','
        func += 'v' + str(v)
        t = True
        func = Function(v, func)
    func += ')'
    return func


if __name__ == '__main__':
    edges, vertex = read_graph()
    d = {}
    color = {}
    for v in vertex:
        color[v] = 'white'
        tmp = []
        for edge in edges:
            if edge[1] == v:
                tmp.append(edge[0])
            d[v] = tmp
    for v in vertex:
        dfs(v, color, d)
    crc = stok(matr(edges, vertex))
    f1 = open('graph2.txt', 'w')
    for x in crc:
        func ='v' + Function(x, str(x))
        f1.write(func + '\n')