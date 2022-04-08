import numpy as np
import pandas as pd
import itertools
from random import random
import collections
from Modules import latexAPI as latexAPI

# This is the probability functions
def p_plus(w):
    """Calculates the value for this function for populating Transistion Matrices

    Args:
        w (Float): Take in the W value

    Returns:
        Float: The result of the Formula
    """
    return (np.exp(w)) / (np.exp(-w) + np.exp(w))


def p_minus(w):
    """Calculates the value for this function for populating Transistion Matrices

    Args:
        w (Float): Take in the W value

    Returns:
        Float: The result of the Formula
    """
    return (np.exp(-w)) / (np.exp(-w) + np.exp(w))


def getDimensions(k):
    """Get the dimension for a K qubit system

    Args:
        k (int): K qubit system

    Returns:
        int: Dimension for a K qubit system
    """
    return 2**k


def getInputs(k):
    """Gets all possible permutations for a K qubit system. I dont believe it is used anymore. It was slow.

    Args:
        k (int): [description]

    Returns:
        [type]: [description]
    """
    lst = list(map(list, itertools.product([0, 1], repeat=k)))
    firsthalf = []
    secondhalf = []
    for i in lst:
        if i[k - 1] == 0:
            firsthalf.append(i)
        else:
            secondhalf.append(i)
    for i in secondhalf:
        firsthalf.append(i)
    return np.array(firsthalf)


def getInputFeaturesIndex(inputfeatures, numOfBits=8):
    """Gives the index of the input features

    Args:
        inputfeatures ([type]): [description]
        numOfBits (int, optional): [description]. Defaults to 8.

    Returns:
        [type]: [description]
    """
    temp = []
    for x in inputfeatures:
        inputs = getInputs(numOfBits)
        inputfeature = x
        dec = int(inputfeature, 2)
        # print(dec)
        # even
        if dec % 2 == 0:
            index = int((dec / 2))
        else:
            index = int(dec / 2) + (int(2 ** (len(inputfeature)) / 2))
        temp.append(index)
    return temp


def getData(path, numOfInputBits=None):
    """This gets the data from a file and returns the input features and the output features. These are the just strings of the numbers.
    For the inputfeature it removes the last char of the total dataset and replaces it with a 0.

    Args:
        path (str): The path of the file that contains the data
        numOfInputBits (int, optional): This is the number of bits in the system. Defaults to None.

    Returns:
        tuple: two strings that are input and output.
    """
    if numOfInputBits is None:
        numOfInputBits = 8
    inputfeatures = []
    outputfeatures = []
    f = open(path, "r")

    with open(path) as f:
        lines = f.readlines()

    for i in lines:
        x = i.replace(" ", "").replace("\n", "")
        # This line takes the parsed input string and removes the last char, and sets it to 0.
        # This means that an input of 1  1  1  1  and 1  1  1  0  will both give the same input
        # feature only differing by output feature which is correct.
        inputfeatures.append(x[0 : numOfInputBits - 1] + "0")
        outputfeatures.append(x[-1:])
    # print(outputfeatures)
    # print(inputfeatures)
    return inputfeatures, outputfeatures


def getInputsandOutputs(path, numOfInputBits=8):
    """This takes in a dataSet and creates an Input and Output that can be understood by the circuit compiler.
    Args:
            path (string): path to the data. It must be formatted first n bits are the input feature and the last bit is the output feature.
    """

    # This inputfeature is the binary part. Our inputs look like this converted to the index.
    inputfeatures, outputfeatures = getData(path, numOfInputBits)
    inputfeaturesindexed = getInputFeaturesIndex(inputfeatures)
    return inputfeaturesindexed, outputfeatures


def getDatasets(path, numOfBits=8, head=None):
    """This takes in a dataSet and creates the DataSet that can be understood by the circuit compiler. It is a list with each element being a tuple of inputfeature and outputfeature
    Args:
            path (string): path to the data. It must be formatted first n bits are the input feature and the last bit is the output feature.
            numOfBits(int): this Defaults to 8. This num tells us how many digits are in the input feature.
            head(int): this picks the first n datapoints from the file.
    """

    inputfeatures, outputfeatures = getInputsandOutputs(path, numOfBits)
    DataSet = []
    if head == None:
        head = len(inputfeatures)
    for x, y in zip(inputfeatures[:head], outputfeatures[:head]):
        DataSet.append((x, y))
    return DataSet


def generateDataSet(
    numofInputBits, probOfEachInput, probofOutput, filename, numOfSamples=100
):
    """
    This generates a dataset to be trained on, where the we give the probability of each input bit being a 1. And then the probability of the final output bit being a 1. It will return in it the format that the normal machine takes in data.
    Args:
        numofInputBits - INT - The number of input bits.
        probOfEachInput - DECIMAL - The probability of the inputs being 1.
        probofOutput - DECIMAL - The probability of it being 1 each run
        numOfSamples - DECIMAL - Number of samples of this to be generated. Defualt is 100
    Return:
        It returns a file that is in the same format as the geonomic data.
    """
    listofDatapoints = []
    for x in range(numOfSamples):
        datapoint = []
        for x in range(0, numofInputBits):
            # If it is less than it will be 1
            if probOfEachInput < random():
                datapoint.append(1)
            else:
                datapoint.append(0)
            # If it is less than it will be 1 this will add the output bit as the last bit.
        if probofOutput < random():
            datapoint.append(1)
        else:
            datapoint.append(0)

        listofDatapoints.append(datapoint)
        # At this point this list is the contains the correct data it just needs to be converted into the correct format to be read by the system.
        outputfile = ""
    for x in listofDatapoints:
        for y in x:
            outputfile += str(y) + "  "
        outputfile += "\n"

    # It is formatted correctly but it is not outputed to file.
    with open(filename, "w") as f:
        f.write(outputfile)


def generateDataSetAlternative(
    numofInputBits, probOfEachInput, filename, numOfSamples=100
):
    """
    This generates a dataset in which the outputbit probability is equal to the probability of input bits that were 1.
    Args:
        numofInputBits - INT - The number of input bits.
        probOfEachInput - DECIMAL - The probability of the inputs being 1.
        numOfSamples - DECIMAL - Number of samples of this to be generated. Defualt is 100
    Return:
        It returns a file that is in the same format as the geonomic data.
    """
    listofDatapoints = []
    for x in range(numOfSamples):
        datapoint = []
        for x in range(0, numofInputBits):
            # If it is less than it will be 1
            if probOfEachInput > random():
                datapoint.append(1)
            else:
                datapoint.append(0)
            # If it is less than it will be 1 this will add the output bit as the last bit.

        # This adds the Last bit. The last bit will be whatever the majority is.
        freq = collections.Counter(datapoint)
        # Should it be less than or equal not important but may skew data very very slightly if there is ever the same number
        if freq[0] > freq[1]:
            datapoint.append(0)
        else:
            datapoint.append(1)
        listofDatapoints.append(datapoint)
        # At this point this list is the contains the correct data it just needs to be converted into the correct format to be read by the system.
        outputfile = ""
    for x in listofDatapoints:
        for y in x:
            outputfile += str(y) + "  "
        outputfile += "\n"

    # It is formatted correctly but it is not outputed to file.
    with open(filename, "w") as f:
        f.write(outputfile)


def printTransistionMatrices(circuit, epoch=None, latex=None):
    data = []
    for index, x in enumerate(circuit.circuits[0].TransistionLayers):
        print(
            f"Epoch {epoch} - Transistion Matrix {index +1} - Type: {circuit.circuits[0].LayerNames[index]}"
        )
        if latex == True:
            print("It got in herer")
            data.append([epoch, index + 1, circuit.circuits[0].LayerNames[index], x])
        print(x)
    if latex == True:
        latexAPI.printAllMatrices(data)


def printAllGates(circuit):
    print("================================================================")
    print(f"The input state is:\n{circuit.InputState.A}")
    print("================================================================")
    for index, x in enumerate(circuit.TransistionLayers):
        print(f"Transistion Matrix {index +1}")
        print(x)
    print("================================================================")
    print(f"The Ouput state is:\n{circuit.OutputState.A}")
    print("================================================================")


def generateAND_DataSet(numofInputBits, probOfEachInput, filename, numOfSamples=100):
    """
    This generates a dataset where the output is an AND.
    Args:
        numofInputBits - INT - The number of input bits.
        probOfEachInput - DECIMAL - The probability of the inputs being 1.
        numOfSamples - DECIMAL - Number of samples of this to be generated. Defualt is 100
    Return:
        It returns a file that is in the same format as the geonomic data.
    """
    # Not Implemented


def generateXOR_DataSet(numofInputBits, probOfEachInput, filename, numOfSamples=100):
    """
    This generates a dataset where the output is an AND.
    Args:
        numofInputBits - INT - The number of input bits.
        probOfEachInput - DECIMAL - The probability of the inputs being 1.
        numOfSamples - DECIMAL - Number of samples of this to be generated. Defualt is 100
    Return:
        It returns a file that is in the same format as the geonomic data.
    """
    # Not Implemented
