from matplotlib import pyplot as plt
from itertools import cycle

cycol = cycle('brgcmk')


class Data:
    def __init__(self, x, y, label=None, color=None):
        self.x = x
        self.y = y
        self.label = label
        self.color = next(cycol)
        if color is not None:
            self.color = color


def read_csv(filename, label=None, color=None):
    with open(filename, 'r') as file:
        x = []
        y = []
        for line in file:
            line = line.strip('\n')
            line = line.split(', ')
            x.append(float(line[0]))
            y.append(float(line[1]))

        # plotList.append(Data(x, y, label))
        return Data(x, y, label, color)


def plot(plotList_, xlabel=None, ylabel=None, title=None, grid=None, legend=None):
    for data in plotList_:
        plt.plot(data.x, data.y, label=data.label, color=data.color)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(grid)
    if legend:
        plt.legend()
    plt.show()

if __name__ == '__main__':
    read_csv('./data/sem tlcd.csv', 'sem tlcd')
    read_csv('./data/com tlcd.csv', 'com tlcd')
    plot(plotList, 'x', 'y', 'title', True, True)