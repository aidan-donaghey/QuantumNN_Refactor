import numpy as np
import itertools


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
