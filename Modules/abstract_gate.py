"""This is all of the Gates"""

from abc import ABC, abstractmethod
import numpy as np
from scipy.sparse import coo_matrix
import scipy.sparse as sp
from Modules import utils
from Modules import helperfunctions as hf


class Gate(ABC):
    """This is an abstract Gate"""

    def __init__(self, number_of_bits, linked_qubit, theta=1):
        if linked_qubit >= number_of_bits - 1:
            raise IndexError(
                (
                    f"Linked qubit is out of range. It is zero indexed and the last bit can not be linked to itself so it must be less or equal than number_of_bits - 2.\n\n"
                    f"For this specific case linked_qubit must be less than {number_of_bits - 1}\n"
                )
            )
        self.__name__ = "Abstract_Gate"
        self.number_of_bits = number_of_bits
        self.linked_qubit = linked_qubit
        self.theta = theta
        self.inputs = utils.getInputs(self.number_of_bits)
        self.matrix = None
        self.zk_matrix = None
        self.set_matrix()

    @abstractmethod
    def set_matrix(self):
        """Abstract method to set the matrix for the gate."""

    def __repr__(self):
        output = (
            f"{self.__name__}\n"
            f"Number of Input Bits: {self.number_of_bits}\n"
            f"Bit Linked To Output: {self.linked_qubit}\n"
            f"Theta: {self.theta}\n"
            f"Matrix:\n{self.matrix}\n"
        )
        return output

    def print_matrix(self):
        """Prints the matrix for the gate."""
        print(self.matrix.A)




class RzxGate(Gate):
    """This is the Rzx Gate.
    Args:
    number_of_bits: The number of bits in the system.
    linked_qubit: The qubit that is linked to the output. Zero indexed.
    theta: The theta value for the gate. Default is 1."""

    def __init__(self, number_of_bits, linked_qubit, theta=1):
        super().__init__(number_of_bits, linked_qubit, theta)
        self.__name__ = "RzxGate"

    def set_matrix(self):
        """This sets the matrix for a Rzx based off the current theta values. It also sets the zk"""
        p_plus = utils.p_plus(self.theta)
        p_minus = utils.p_minus(self.theta)
        d = hf.getDimensions(self.number_of_bits)
        offdiagonaloffset = int((d / 2))
        # This gets diagonal
        row = np.arange(d)
        col = np.arange(d)
        # This gets non Diagonal
        row = np.append(row, row)
        col = np.append(col, (col + offdiagonaloffset) % d)
        data = [0 for x in range(2 * d)]
        # This Zkdata essentially keeps track of if conditional bits are 0 or 1.
        zkdata = [0 for x in range(2 * d)]
        for index, j in enumerate(self.inputs):
            if j[self.linked_qubit] == 0:
                data[index] = p_plus
                data[index + d] = p_minus
                zkdata[index] = -1
                zkdata[index + d] = -1
            else:
                data[index] = p_minus
                data[index + d] = p_plus
                zkdata[index] = 1
                zkdata[index + d] = 1

        matrix = coo_matrix((data, (row, col)), shape=(d, d))
        matrix.tocsr()
        zk_matrix = coo_matrix((zkdata, (row, col)), shape=(d, d))
        zk_matrix.tocsr()
        self.zk_matrix = zk_matrix
        self.matrix = matrix


class RxxGate(Gate):
    """This is the Rxx Gate.
    Args:
    number_of_bits: The number of bits in the system.
    linked_qubit: The qubit that is linked to the output. Zero indexed.
    theta: The theta value for the gate. Default is 1."""

    def __init__(self, number_of_bits, linked_qubit, theta=1):
        super().__init__(number_of_bits, linked_qubit, theta)
        self.__name__ = "RxxGate"

    def set_matrix(self):
        """This sets the matrix for a Rzx based off the current theta values."""
        p_plus = utils.p_plus(self.theta)
        p_minus = utils.p_minus(self.theta)
        d = hf.getDimensions(self.number_of_bits)
        halfpoint = int(d / 2)
        # This gets diagonal
        row = np.arange(d)
        col = np.arange(d)
        row = np.append(row, row)

        secondcols = [0 for x in range(d)]
        for index in range(0, int(len(self.inputs) / 2)):
            temp = self.inputs[index]
            temp[self.number_of_bits - 1] = 1
            if temp[self.linked_qubit] == 0:
                temp[self.linked_qubit] = 1
            else:
                temp[self.linked_qubit] = 0
            b = "".join(map(str, temp))
            dec = int(b, 2)
            offset = int((dec - 1) / 2)
            secondcols[index] = halfpoint + offset
            secondcols[index + halfpoint] = offset
        # print(f"secondcols:{secondcols}")
        col = np.append(col, secondcols)
        data = [0 for x in range(2 * d)]
        data[:d] = [p_minus] * d  ### corrected
        data[d:] = [p_plus] * d  ### corrected
        matrix = coo_matrix((data, (row, col)), shape=(d, d))

        matrix.tocsr()
        self.matrix = matrix
