"""This is the Block Class"""

from abc import ABC, abstractmethod
from Modules.abstract_gate import RzxGate, RxxGate, Gate
from Modules import utils


class Block(ABC):
    """Abstract Block Class."""

    def __init__(self, number_of_bits, thetas=1):
        self.__name__ = "Abstract_Block"
        self.number_of_bits = number_of_bits
        if isinstance(thetas, list):
            if len(thetas) != number_of_bits - 1:
                raise IndexError(
                    "The length of thetas list must be equal to number_of_bits - 1"
                )
            self.thetas = thetas
        else:
            self.thetas = [thetas] * (number_of_bits - 1)
        self.gates = []
        self.create_block()

    @abstractmethod
    def create_block(self):
        """Abstract method to create the block."""

    def __repr__(self):
        output = (
            f"{self.__name__}\n"
            f"Number of Input Bits: {self.number_of_bits}\n"
            f"Number of Gates: {len(self.gates)}\n"
            f"Thetas: {self.thetas}\n"
        )
        return output

    def print(self):
        """Prints the block in np.array format."""
        for i in self.gates:
            print(i)


# Concrete Block Classes
class RzxBlock(Block):
    """This is the Rzx Block. A block is a collection of gates, with each sequencial gate linking each possible linked qubit.
    Args:
    number_of_bits: [int] The number of bits in the system.
    theta: [list] The theta values for the each of the Gates. Default is 1 for all."""

    def __init__(self, number_of_bits, thetas=1):
        super().__init__(number_of_bits, thetas)
        self.__name__ = "RzxBlock"

    def create_block(self):
        """Creates the block."""
        for i in range(self.number_of_bits - 1):
            self.gates.append(RzxGate(self.number_of_bits, i, self.thetas[i]))


class RxxBlock(Block):
    """This is the Rxx Block. A block is a collection of gates, with each sequencial gate linking each possible linked qubit.
    Args:
    number_of_bits: [int] The number of bits in the system.
    theta: [list] The theta values for the each of the Gates. Default is 1 for all."""

    def __init__(self, number_of_bits, thetas=1):
        super().__init__(number_of_bits, thetas)
        self.__name__ = "RxxBlock"

    def create_block(self):
        """Creates the block."""
        for i in range(self.number_of_bits - 1):
            self.gates.append(RxxGate(self.number_of_bits, i, self.thetas[i]))
