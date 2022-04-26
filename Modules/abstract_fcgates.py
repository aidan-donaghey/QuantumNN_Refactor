"""This is all of the Gates"""

from abc import ABC, abstractmethod
import numpy as np
from scipy.sparse import coo_matrix
import scipy.sparse as sp
from Modules import utils
from Modules import helperfunctions as hf


class GateAnyConnect(ABC):
    """This is an abstract Gate"""

    def __init__(self, number_of_bits, linked_qubit1,linked_qubit2, theta=1):
        if linked_qubit1 >= number_of_bits or linked_qubit2 >= number_of_bits:
            raise IndexError(
                (
                    f"Linked qubits is out of range. It is zero indexed and the last bit can not be linked to itself so it must be less or equal than number_of_bits - 2.\n\n"
                    f"For this specific case linked_qubit1 or linked_qubit2 must be less than {number_of_bits - 1}\n"
                )
            )
        if linked_qubit1 == linked_qubit2:
            raise IndexError(
                (
                    f"Linked qubits cannot be the same.\n"
                   f"For this specific case linked_qubit1 or linked_qubit2 must be different\n"
                )
            )
        self.__name__ = "Abstract_Gate"
        self.number_of_bits = number_of_bits
        self.linked_qubit1 = linked_qubit1
        self.linked_qubit2 = linked_qubit2
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
            f"Qubit {self.linked_qubit1} Linked To Qubit {self.linked_qubit2}\n"
            f"Theta: {self.theta}\n"
            f"Matrix:\n{self.matrix}\n"
        )
        return output

    def print_matrix(self):
        """Prints the matrix for the gate."""
        print(self.matrix.A)


class RzxGateAnyConnect(GateAnyConnect):
    """This is the Rzx Gate.
    Args:
    number_of_bits: The number of bits in the system.
    linked_qubit1: The qubit that is linked to the linked_qubit2. Zero indexed.
    linked_qubit2: The qubit to link to. Zero indexed.
    theta: The theta value for the gate. Default is 1."""

    def __init__(self, number_of_bits, linked_qubit1,linked_qubit2, theta=1):
        super().__init__(number_of_bits, linked_qubit1, linked_qubit2, theta)
        self.__name__ = "RzxGateAnyConnect"

    def set_matrix(self):
        """This sets the matrix for a Rzx based off the current theta values. It also sets the zk"""
        p_plus = utils.p_plus(self.theta)
        p_minus = utils.p_minus(self.theta)
        d = hf.getDimensions(self.number_of_bits)
        strVersion = ["".join(str(e) for e in x) for x in self.inputs.tolist()]
        bitsToIndexMap = {x:index for index, x in enumerate(strVersion)}
        IndexTobitsMap = {index:x for index, x in enumerate(strVersion)}
        # Move this to utils
        matrix = np.zeros((d, d))
        zkmatrix = np.zeros((d, d))
        for x in range(d):
            flippedLinked = list(IndexTobitsMap[x])
            flippedLinked[self.linked_qubit2] = "1" if flippedLinked[self.linked_qubit2] == "0" else "0"
            indexofFlippedLinked = bitsToIndexMap["".join(flippedLinked)]
            # Setting the diagonals
            if IndexTobitsMap[x][self.linked_qubit1] == "0":
                matrix[x][x] = p_plus
                matrix[x][indexofFlippedLinked] = p_minus
                zkmatrix[x][x] = -1
                zkmatrix[x][indexofFlippedLinked] = -1

            else:
                matrix[x][x] = p_minus
                matrix[x][indexofFlippedLinked] = p_plus
                zkmatrix[x][x] = 1
                zkmatrix[x][indexofFlippedLinked] = 1
            # Setting the off diagonals
            # 
        self.matrix = sp.csr_matrix(matrix) 
        self.zk_matrix = sp.csr_matrix(zkmatrix)

class RxxGateAnyConnect(GateAnyConnect):
    """This is the Rzx Gate.
    Args:
    number_of_bits: The number of bits in the system.
    linked_qubit1: The qubit that is linked to the linked_qubit2. Zero indexed.
    linked_qubit2: The qubit to link to. Zero indexed.
    theta: The theta value for the gate. Default is 1."""

    def __init__(self, number_of_bits, linked_qubit1,linked_qubit2, theta=1):
        super().__init__(number_of_bits, linked_qubit1, linked_qubit2, theta)
        self.__name__ = "RxxGateAnyConnect"

    def set_matrix(self):
        """This sets the matrix for a Rxx based off the current theta values. It also sets the zk"""
        p_plus = utils.p_plus(self.theta)
        p_minus = utils.p_minus(self.theta)
        d = hf.getDimensions(self.number_of_bits)
        strVersion = ["".join(str(e) for e in x) for x in self.inputs.tolist()]
        bitsToIndexMap = {x:index for index, x in enumerate(strVersion)}
        IndexTobitsMap = {index:x for index, x in enumerate(strVersion)}
        # Move this to utils
        matrix = np.zeros((d, d))
        for x in range(d):
            flippedLinked = list(IndexTobitsMap[x])
            flippedLinked[self.linked_qubit1] = "1" if flippedLinked[self.linked_qubit1] == "0" else "0"
            flippedLinked[self.linked_qubit2] = "1" if flippedLinked[self.linked_qubit2] == "0" else "0"
            indexofFlippedLinked = bitsToIndexMap["".join(flippedLinked)]
            # Setting the diagonals
        
            matrix[x][x] = p_minus
            matrix[x][indexofFlippedLinked] = p_plus
            
            # Setting the off diagonals
            # 
        self.matrix = sp.csr_matrix(matrix)  
