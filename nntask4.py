import sys
import math
import argparse
import xml.etree.cElementTree as ET
from xml.dom import minidom


def read(textfile, input):
    vector = open(textfile).read().split(" ")
    vector = [int(x) for x in vector]
    matrix = []
    in_file = open(input).readlines()
    indx = 0
    length = len(vector)
    for line in in_file:
        indx += 1
        line = line.replace("[", " ")
        line = line.replace("]", " ")
        line = line[1:-2]
        line = line.split("   ")
        tmp = []
        for x in line:
            x = x.split(" ")
            try:
                x = [int(i) for i in x]
                tmp.append(x)
            except ValueError:
                print("Ошибка в строке " + str(indx))
                sys.exit(1)
            if len(x) != length:
                print("Не совпадает число компонент нейронов в слoях " + str(indx - 1) + " - " + str(indx))
                sys.exit(1)
        length = len(line)
        matrix.append([tmp])
    return matrix, vector


def evaluate(matrix, vector):
    new_matrix = []
    for layer in matrix:
        tmp = []
        for x in layer:
            for neuron in x:
                value = 0
                for i in range(len(vector)):
                    value += neuron[i] * vector[i]
                value = value / (1 + abs(value))
                tmp.append(value)
            new_matrix.append(tmp)
            vector = tmp
    return new_matrix


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True, help='input.txt')
    parser.add_argument('-v', required=True, help='vector.txt')
    parser.add_argument('-o', required=True, help='output.txt')
    args = parser.parse_args()
    matrix, vector = read(args.v, args.i)
    new_matrix = evaluate(matrix, vector)
    with open(args.o, 'w') as output:
        for x in new_matrix[-1]:
            output.write(str(x) + " ")
    root = ET.Element("network")
    for layer in matrix:
        tmp = ""
        for x in layer:
            for y in x:
                tmp += str(y) + " "
            break
        tmp = tmp[:-1]
        ET.SubElement(root, "layer").text = tmp
    d = minidom.parseString(ET.tostring(root))
    tree = d.toprettyxml(indent='\t')
    with open("output.xml", 'w') as file:
        file.write(tree)


if __name__ == "__main__":
    main()