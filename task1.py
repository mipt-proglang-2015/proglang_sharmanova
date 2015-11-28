__author__ = 'Mila'

import xml.dom.minidom
import time
import electro

def main():
    xmlfile = open('input.xml', 'r')

    dom = xml.dom.minidom.parse(xmlfile)
    schematicsNode = dom._get_childNodes()[0]

    maxnet = 0
    for item in schematicsNode.getElementsByTagName('diode'):
        maxnet = max(maxnet, int(item.attributes['net_from'].value))
        maxnet = max(maxnet, int(item.attributes['net_to'].value))

    for item in schematicsNode.getElementsByTagName('resistor'):
        maxnet = max(maxnet, int(item.attributes['net_from'].value))
        maxnet = max(maxnet, int(item.attributes['net_to'].value))

    for item in schematicsNode.getElementsByTagName('capactor'):
        maxnet = max(maxnet, int(item.attributes['net_from'].value))
        maxnet = max(maxnet, int(item.attributes['net_to'].value))

    matrix = [[0 for i in range(0, maxnet)] for j in range(0, maxnet)]

    for item in schematicsNode.getElementsByTagName('diode'):
        net_from = int(item.attributes['net_from'].value) - 1
        net_to = int(item.attributes['net_to'].value) - 1
        value = float(item.attributes['resistance'].value)
        rev_value = float(item.attributes['reverse_resistance'].value)
        if matrix[net_from][net_to] != 0:
            matrix[net_from][net_to] = matrix[net_from][net_to] * value / (matrix[net_from][net_to] + value)
        else:
            matrix[net_from][net_to] = value

        if matrix[net_to][net_from] != 0:
            matrix[net_to][net_from] = matrix[net_to][net_from] * rev_value / (matrix[net_to][net_from] + rev_value)
        else:
            matrix[net_to][net_from] = rev_value

    for item in schematicsNode.getElementsByTagName('resistor'):
        net_from = int(item.attributes['net_from'].value) - 1
        net_to = int(item.attributes['net_to'].value) - 1
        value = float(item.attributes['resistance'].value)
        if matrix[net_from][net_to] != 0:
            matrix[net_from][net_to] = matrix[net_from][net_to] * value / (matrix[net_from][net_to] + value)
        else:
            matrix[net_from][net_to] = value

        if matrix[net_to][net_from] != 0:
            matrix[net_to][net_from] = matrix[net_to][net_from] * value / (matrix[net_to][net_from] + value)
        else:
            matrix[net_to][net_from] = value

    for item in schematicsNode.getElementsByTagName('capactor'):
        net_from = int(item.attributes['net_from'].value) - 1
        net_to = int(item.attributes['net_to'].value) - 1
        value = float(item.attributes['resistance'].value)
        if matrix[net_from][net_to] != 0:
            matrix[net_from][net_to] = matrix[net_from][net_to] * value / (matrix[net_from][net_to] + value)
        else:
            matrix[net_from][net_to] = value

        if matrix[net_to][net_from] != 0:
            matrix[net_to][net_from] = matrix[net_to][net_from] * value / (matrix[net_to][net_from] + value)
        else:
            matrix[net_to][net_from] = value
    matrix = electro.electro_count(matrix)
    # for k in range(0, maxnet):
    #     for i in range(0, maxnet):
    #         for j in range(0, maxnet):
    #             if matrix[i][j] != 0 and (matrix[i][k] + matrix[k][j]) != 0 :
    #                 matrix[i][j] = (matrix[i][j] * (matrix[i][k] + matrix[k][j])) / (matrix[i][j] + matrix[i][k] + matrix[k][j])

    csv_out = open('out.csv', 'w')

    for line in matrix:
        csv_out.write(','.join(map(str, [line[i] for i in range(0, len(line))])))
        csv_out.write('\n')

if __name__ == "__main__":
    start = time.process_time()
    main()
    end = time.process_time()
    delta = end - start
    print("Python calculations time: {:.1f} sec".format(delta))