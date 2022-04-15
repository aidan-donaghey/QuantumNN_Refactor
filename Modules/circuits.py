"""This is the Circuit Class File"""
from ast import Raise

from matplotlib.pyplot import get
from Modules.abstract_gate import RzxGate, RxxGate
from Modules.abstract_block import RzxBlock, RxxBlock
from scipy import sparse, linalg
from sklearn.preprocessing import normalize
import numpy as np


class Circuit:
    def __init__(self, number_of_bits, inputfeature, outputfeature, gates, thetas=1):
        """A Circuit is a instane of circuit. This contains and tracks of the
            details for a single circuit, including Input Features, Output Features,
            Transistion Matrices, after calculated also the alphas, betas, xis for the circuit.

        Args:
            numOfBits (int): It is the number of bits in a circuit. Used for sizing of Matrices
            inputfeature (int): This is the index that he input from the data is mapped to.
            outputfeature (str): This is the output label. NOTE it is a string currently but possible a int would be better.
            gates (list): This is a list of gates that make up the circuit. (Actually Blocks are more accurate)
            allThetas (list, optional): A list of the W values that will used when createCircuit is called to set the transistion matrices. Defaults to None.
        """
        # Setting Args
        self.number_of_bits = number_of_bits
        self.inputfeature = inputfeature
        self.outputfeature = outputfeature
        self.gates = gates
        self.thetas = self.__get_thetas(thetas)

        self.blocks = []
        self.alphas = []
        self.betas = []
        self.xis = []

        self.inputstate = self.__inputfeature_to_inputstate()
        self.outputstate = self.__outputfeature_to_outputstate()

        self.create_circuit()

    def create_circuit(self) -> None:
        """This creates the circuit. It calls the createLayer function for each layer."""
        for indexofgate, gate in enumerate(self.gates):
            if gate == "RZX":
                # This theta should be (number of bits - 1) * number of gates
                # We need between indexOfGate * number of bits and (indexOfGate + 1) * number of bits
                self.blocks.append(
                    RzxBlock(
                        self.number_of_bits,
                        self.thetas[
                            indexofgate
                            * (self.number_of_bits - 1) : (indexofgate + 1)
                            * (self.number_of_bits - 1)
                        ],
                    )
                )
            elif gate == "RXX":
                self.blocks.append(
                    RxxBlock(
                        self.number_of_bits,
                        self.thetas[
                            indexofgate
                            * (self.number_of_bits - 1) : (indexofgate + 1)
                            * (self.number_of_bits - 1)
                        ],
                    )
                )
            else:
                raise NotImplementedError(f"Gate {gate} is not implemented")

    def get_allgates(self) -> list:
        """This returns all the gates in the circuit.

        Returns:
            list: A list of all the gates in the circuit.
        """
        temp = [blocks for blocks in self.blocks]
        allgates = []
        for x in temp:
            for y in x.gates:
                allgates.append(y)
        return allgates

    def forward_pass(self) -> list:
        """This is the forward pass of the circuit. It is used to calculate the alphas.
            alphas take the shape (1, 2**number_of_bits)

        Returns:
            list: A list of all the gates in the circuit.
        """
        self.alphas = []
        transistionmatrices = self.get_allgates()
        self.alphas.append(self.inputstate)
        for transistionmatrix in transistionmatrices:
            self.alphas.append(self.alphas[-1] @ transistionmatrix.matrix)
            self.alphas.append(self.alphas[-1].multiply(self.outputstate.T))
        return self.alphas

    def backward_pass(self) -> list:
        """This is the backward pass of the circuit. It is used to calculate the betas, xis.
            beta take the shape (2**number_of_bits, 1)
        Returns:
            list: A list of all the gates in the circuit.
        """
        self.betas = []
        transistionmatrices = self.get_allgates()
        self.betas.append(self.outputstate)
        for transistionmatrix in reversed(transistionmatrices):
            self.betas.append(transistionmatrix.matrix.T @ (self.betas[-1].T).T)
        self.betas.reverse()
        return self.betas

    def get_xis(self) -> list:
        """This is the xis calculation.  It also runs the forward and backward pass."""
        self.forward_pass()
        self.backward_pass()
        # alphas are of shape (1, N) and betas are of shape (N, 1) and transition is of shape (N, N)
        # xi is of shape (N, N)
        transistionmatrices = self.get_allgates()
        # This is for another way to normalise the xi
        # px = self.get_px()

        self.xis = []
        for index, transistionmatrix in enumerate(transistionmatrices):
            unnormalisedxi = transistionmatrix.matrix.multiply(
                (self.alphas[index].T @ self.betas[index + 1].T).T
            )
            # Normalise the xi
            # axis = 1 is the row axis
            normalisedxi = normalize(unnormalisedxi, norm="l1", axis=1)

            self.xis.append(normalisedxi)

        return self.xis

    def get_px(self):
        """This is the probability of the output state.

        Returns:
            float: The probability of the output state.
        """
        return self.alphas[-1].sum()

    def get_numerators_and_denominators_for_circuit(self):
        """This is the numerator of the xi.

        Returns:
            list: A list of numerators for each xi.
        """
        listofdenominators = []
        listofnumerators = []
        # First lets calculate the denominators
        # This is based off of my new assumption that
        # xi is going to be the sum of every element in the array. I believe this is true
        # If it is the sum of the off and on diagonals .
        for gate, xi in zip(self.get_allgates(), self.xis):
            listofdenominators.append(xi.sum())
            if gate.__name__ == "RzxGate":
                matrix = xi.multiply(gate.zk_matrix)
            elif gate.__name__ == "RxxGate":
                matrix = xi
            sumofdiagonals = matrix.diagonal().sum()
            sumofoffdiagonals = matrix.tolil().sum()
            listofnumerators.append(sumofoffdiagonals - sumofdiagonals)

        return listofnumerators, listofdenominators

    def update_w(self, thetas):
        """This is the update of the thetas."""
        self.thetas = thetas

    # ==================================
    # Private Functions
    # ==================================
    def __repr__(self) -> str:
        return (
            f"Circuit: {self.number_of_bits} bits\n"
            f"Thetas: \n{self.thetas}\n"
            f"Input: \n{self.inputstate}\n"
            f"Output: \n{self.outputstate}\n"
            f"Blocks: \n{self.gates}\n"
        )

    def __get_thetas(self, thetas) -> list:
        """internal Method for getting thetas in the contructor.

        Args:
            thetas (list or int): Either a list of thetas or a single theta.

        Raises:
            IndexError: If passed a list that is of the wrong length.

        Returns:
            _type_: The correct thetas.
        """
        if isinstance(thetas, list):
            if len(thetas) != ((self.number_of_bits - 1) * len(self.gates)):
                raise IndexError(
                    (
                        "The length of thetas list must be equal to (number_of_bits - 1) * number_of_gate\n\n"
                        f"For this example it should be {(self.number_of_bits - 1) * len(self.gates)} but was {len(thetas)}"
                    )
                )
            finaltheta = thetas
        else:
            finaltheta = [thetas] * ((self.number_of_bits - 1) * len(self.gates))
        return finaltheta

    def __inputfeature_to_inputstate(self) -> sparse.csr_matrix:
        """This adds the First Layer. This is an internal function that should be called outside. It populates the first Layer as a coo_matrix.
        This is the onehot encoded layer.
        """
        dimension = 2 ** (self.number_of_bits)
        inputlist = [self.inputfeature]
        J = [0]
        V = [1]
        A = sparse.coo_matrix((V, (J, inputlist)), shape=(1, dimension))
        A.tocsr()
        return A

    def __outputfeature_to_outputstate(self) -> sparse.csr_matrix:
        """This adds the Output Mask Layer."""
        d = int(2 ** (self.number_of_bits))
        row = [x for x in range(d)]
        col = [0 for x in range(d)]
        data = [0 for x in range(d)]
        if int(self.outputfeature) == 1:
            data[int(d / 2) :] = [1] * int(d / 2)
        else:
            data[: int(d / 2)] = [1] * int(d / 2)
        A = sparse.coo_matrix((data, (row, col)), shape=(d, 1))
        A.tocsr()
        return A
