from abc import ABC, abstractmethod
from Modules.abstract_gate import RzxGate, RxxGate, Gate
from Modules.abstract_fcgates import RzxGateAnyConnect, RxxGateAnyConnect
from Modules import utils

class FCBlock(ABC):
    """Abstract FCBlock Class."""

    def __init__(self, number_of_bits, thetas=1):
        self.__name__ = "Abstract_FCBlock"
        self.number_of_bits = number_of_bits
        if isinstance(thetas, list):
            if len(thetas) != number_of_bits**2 - number_of_bits:
                raise IndexError(
                    "The length of thetas list must be equal to  number_of_bits**2 - number_of_bits"
                )
            self.thetas = thetas
        else:
            self.thetas = [thetas] * ( number_of_bits**2 - number_of_bits)
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



class RxxFullyConnectedBlock(FCBlock):
    """This is the Rxx Fuly Connected Block. A block is a collection of gates, with each sequencial gate linking each qubit with each other possible qubit.
    Args:
    number_of_bits: [int] The number of bits in the system.
    theta: [list] The theta values for the each of the Gates. Default is 1 for all."""

    def __init__(self, number_of_bits, thetas=1):
        super().__init__(number_of_bits, thetas)
        self.__name__ = "RxxFullyConnectedBlock"
        

    def create_block(self):
        """Creates the block."""
        thetaIndex = 0 
        for i in range(self.number_of_bits-1):
            for j in range(self.number_of_bits):
                if i != j:
                    self.gates.append(RxxGateAnyConnect(self.number_of_bits, i, j, self.thetas[thetaIndex]))
                    thetaIndex += 1


class RzxFullyConnectedBlock(FCBlock):
    """This is the Rzx Fuly Connected Block. A block is a collection of gates, with each sequencial gate linking each qubit with each other possible qubit.
    Args:
    number_of_bits: [int] The number of bits in the system.
    theta: [list] The theta values for the each of the Gates. Default is 1 for all."""

    def __init__(self, number_of_bits, thetas=1):
        super().__init__(number_of_bits, thetas)
        self.__name__ = "RzxFullyConnectedBlock"

    def create_block(self):
        """Creates the block."""
        thetaIndex = 0 
        for i in range(self.number_of_bits):
            for j in range(self.number_of_bits):
                 if i != j:
                    self.gates.append(RzxGateAnyConnect(self.number_of_bits, i, j, self.thetas[thetaIndex]))
                    thetaIndex += 1
