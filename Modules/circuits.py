"""This is the Circuit Class File"""
from ast import Raise

from matplotlib.pyplot import get
from Modules.abstract_gate import RzxGate, RxxGate
from Modules.abstract_block import RzxBlock, RxxBlock
from scipy import sparse, linalg


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
        """This is the forward pass of the circuit. It is used to calculate the alphas, betas, xis.
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

    def get_xi(self) -> list:
        # alphas are of shape (1, N) and betas are of shape (N, 1) and transition is of shape (N, N)
        # xi is of shape (N, N)
        transistionmatrices = self.get_allgates()
        px = self.get_px()

        # Option 1
        self.xis = []
        for index, transistionmatrix in enumerate(transistionmatrices):
            unnormalisedxi = (
                self.alphas[index] @ transistionmatrix.matrix @ self.betas[index + 1]
            )
            self.xis.append(unnormalisedxi / px)

        # Option 2 - This gives a (N,N) matrix with a dot product of it and transition matrix.
        self.xis = []
        for index, transistionmatrix in enumerate(transistionmatrices):
            unnormalisedxi = (
                self.alphas[index].T
                @ self.betas[index + 1].T
                @ transistionmatrix.matrix
            )
            self.xis.append(unnormalisedxi / px)

        # Option 3 - Same as option 2 but all of it transposed again before dot with transition matrix.
        self.xis = []
        for index, transistionmatrix in enumerate(transistionmatrices):
            unnormalisedxi = (
                self.alphas[index].T @ self.betas[index + 1].T
            ).T @ transistionmatrix.matrix
            self.xis.append(unnormalisedxi / px)

        # Option 4 - Same operation for alphas and betas and then transposed but then element wise multiplied with the transition matrix.
        self.xis = []
        for index, transistionmatrix in enumerate(transistionmatrices):
            unnormalisedxi = transistionmatrix.matrix.multiply(
                (self.alphas[index].T @ self.betas[index + 1].T).T
            )
            self.xis.append(unnormalisedxi / px)

        return self.xis

    def get_px(self):
        """This is the probability of the output state.

        Returns:
            float: The probability of the output state.
        """
        return self.alphas[-1].sum()

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
