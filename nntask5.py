import ast
import sys

def read(input_file, neurons_file):
    try:
        input = open(input_file).readlines()
        samples = []
        for line in input:
            line = line.replace("\n", "")
            mass = line.split("->")
            ver = []
            for neuron in mass:
                neuron = neuron[1:-1].split(" ")
                ver.append(neuron)
            samples.append(ver)
        for x in range(len(samples)):
            for y in range(len(samples[x])):
                for z in range(len(samples[x][y])):
                    samples[x][y][z] = float("".join(samples[x][y][z]))
        neurons = open(neurons_file).read()
        neurons = ast.literal_eval(neurons)
        return samples, neurons
    except:
        print("Ошибка в входном файле")
        sys.exit(1)


class Selection:
    def __init__(self, parameters, neurons, samples):
        self.parameters = parameters
        self.values = neurons
        self.samples = samples
        self.functions = []
        self.weights = []
        for i in range(len(neurons)):
            self.functions.append([])
            self.weights.append([])

    def check(self, input):
        result = []
        result.extend(input)
        for j in range(len(self.values)):
            resultSize = len(result)
            for k in range(len(self.values[j])):
                if resultSize != len(self.values[j][k]):
                    print("Число нейронов не совпадает с длиной массива весов")
                    sys.exit(1)
                summa = 0.0
                for i in range(len(self.values[j][k])):
                    summa += result[i] * self.values[j][k][i]
                self.weights[j].append(summa)
                summa = summa / (1 + abs(summa))
                self.functions[j].append(summa)
                result.append(summa)
            if resultSize > 0:
                result[:resultSize] = []
        return result

    def educ_neuron(self, output):
        eps = self.parameters[1]
        n = self.parameters[0]
        resString = []
        step = 3
        for sample in range(len(self.samples)):
            resString.append([])
        for sample in range(step):
            for count in range(n + 1):
                input = self.samples[sample][0]
                expected = self.samples[sample][1]
                resOfPerceptron = self.check(input)
                if count != 0:
                    resString[sample].append("Ошибка на итерации" + " " + str(count) + " - " + str(expected[0] - resOfPerceptron[0])+ "\n")
                sigma = []
                for x in range(len(self.values)):
                    sigma.append([])
                for i in range(len(resOfPerceptron)):
                    sigma[len(self.values) - 1] = [expected[i] - resOfPerceptron[i]]
                for i in range(len(self.values) - 1, 0, -1):
                    for j in range(len(self.values[i][i - 1])):
                        sum = 0.0
                        for z in range(len(sigma[i])):
                            sum += abs(sigma[i][z]) * self.values[i][z][j]
                        sigma[i - 1].append([sum])
                for i in range(1, len(self.values)):
                    for j in range(len(self.values[i])):
                        for weight in range(len(self.values[i][j])):
                            der = 1 / pow((1 + abs(self.weights[i][j])), 2)
                            deltaWeight = sigma[i][j] * der * self.functions[i-1][weight] * eps
                            self.values[i][j][weight] = self.values[i][j][weight] + deltaWeight
        with open(output, 'w') as file:
            for line in resString:
                for x in line:
                        file.write(x)


def main():
    values, layers = read('input.txt', 'neurons.txt')
    n = int(777)
    epsil = float(0.1)
    x = Selection([n, epsil], [layers[0]], values)
    x.educ_neuron('output.txt')


main()