from Modules.circuits import Circuit
import numpy as np
from typing import Union
import sys

class Collection:
    """Creates a new CircuitCollection Object. It creates a circuit with the correct input and output features based on the dataset that is provided."""

    def __init__(self, number_of_bits, DataSet, Gates):
        """Creates a new CircuitCollection Object. It creates a circuit with the correct input and output features based on the dataset that is provided.

        Args:
            numOfInputBits (int): The number of qubits that you are planning to simulate
            DataSet (list): It is a list with each element containing a list of inputfeature and output features
            Gates (list): This is a list with each element being the name of the type of gate in the order you want them. "RXX" or "RZX"
        """
        self.__name__ = "CircuitCollection"
        self.number_of_bits = number_of_bits
        self.DataSet = DataSet
        self.Gates = Gates
        self.circuits = []
        self.trainedModel = None

    def create_circuits(self, Theta:Union[list,float]=None, intialTheta:Union[list,float]=None):
        """This creates an entire collection of circuits. Basically a circuit for each Datapoint.

        Args:
            Theta (List[Float], optional): This is used to create new circuits with specfic W values.It will
            have length of the transistion matrices in the circuit.Defaults to None.
            intialTheta ( Float, optional): A single float that will populate all W values with the same W. Defaults to None.
            intialTheta ( List[Float], optional): This is used to create new circuits with specfic W values.It will
            have length of the transistion matrices in the circuit.

        Raises:
            Exception: It will tell you if you have asked to place a gate that doesnt exist.
        """
        if Theta is not None:
            thetas = self.__check_theta(Theta)
        elif intialTheta is not None:
            thetas = self.__check_intial_theta(intialTheta)
        # else:
        #     thetas = [1 for i in range((self.number_of_bits - 1) * len(self.Gates))]

        listofcircuits = []
        for data in self.DataSet:
            print(data)
            circuit = Circuit(self.number_of_bits, *data, self.Gates, thetas=thetas)
            listofcircuits.append(circuit)
        self.circuits = listofcircuits

    def fit(self, Epoch=10):
        """This will fit the circuits in the collection.

        Args:
            Epoch (int, optional): The number of epochs to run the circuit for. Defaults to 10.
        """

        allepochs = []
        allepochs.append(self.circuits[0])
        for epoch in range(Epoch):
            print(f"Epoch {epoch}")
            # self.print_transistion_matrices()
            self.create_circuits(self.__calculate_ws())
            allepochs.append(self.circuits[0])
        self.trainedModel = self.__calculate_ws()
        return allepochs

    def predict(self, Datapoint):
        """This will predict the output of the circuit.

        Args:
            input_features (List[Float]): The input features that you want to predict the output of.

        Returns:
            List[Float]: The output features of the circuit.
        """
        circuit = Circuit(
            self.number_of_bits, *Datapoint, self.Gates, self.trainedModel
        )
        # This returns the last alpha which is the forward pass including the mask
        return circuit.predict()

    def __calculate_ws(self):
        """Calculates the W values for each circuit in the collection."""
        nums_and_denoms = self.__sum_of_nums_and_denums()
        terms_inside_tan = [x / y for x, y in zip(*nums_and_denoms)]
        print("Terms inside the tan func1")
        print(terms_inside_tan)
        w = [np.arctanh(term) if np.abs(term) < 0.99 else np.sign(term) * 100 for term in terms_inside_tan]

        # w = list(np.arctanh(terms_inside_tan))
        print("W VALUESE")
        print(w)
        return w

    def __sum_of_nums_and_denums(self):
        allnums = []
        alldenums = []
        for circuit in self.circuits:
            circuit.get_xis()
            num, denum = circuit.get_numerators_and_denominators_for_circuit()
            allnums.append(num)
            alldenums.append(denum)

        sumofnums = [sum(x) for x in zip(*allnums)]
        sumofdenums = [sum(x) for x in zip(*alldenums)]
        return sumofnums, sumofdenums

    def __check_theta(self, theta):
        numberOfThetas:int = 0
        for x in self.Gates:
            if x == "RZX" or x == "RXX":
                numberOfThetas += (self.number_of_bits - 1)
            elif x == "FCRZX" or x == "FCRXX":
                numberOfThetas += ((self.number_of_bits**2)  - self.number_of_bits)  
        if isinstance(theta, list):
            if len(theta) != (numberOfThetas):
                raise IndexError(
                    (
                        "The length of thetas list is incorrect. \n\n"
                        f"For this example it should be {numberOfThetas} but was {len(theta)}"
                    )
                )
            finaltheta = theta
        else:
            finaltheta = [theta] * (numberOfThetas)
        return finaltheta

    def __check_intial_theta(self, inital_theta):
        numberOfThetas:int = 0
        for x in self.Gates:
            if x == "RZX" or x == "RXX":
                numberOfThetas += (self.number_of_bits - 1)
            elif x == "FCRZX" or x == "FCRXX":
                numberOfThetas += ((self.number_of_bits**2)  - self.number_of_bits)
              
        if isinstance(inital_theta, list):
            if len(inital_theta) != (numberOfThetas):
                raise IndexError(
                    (
                        "The length of thetas list is incorrect. \n\n"
                        f"For this example it should be {numberOfThetas} but was {len(inital_theta)}"
                    )
                )
            finaltheta = inital_theta
        else:
            finaltheta = [inital_theta] * (numberOfThetas)
        return finaltheta

    def __repr__(self) -> str:
        output = (
            f"=======================\n{self.__name__}\n=======================\n"
            f"Number of Input Bits: {self.number_of_bits}\n"
            f"Datapoints: {len(self.DataSet)}\n"
            f"{len(self.Gates)}: {self.Gates}\n"
        )
        return output

    def print_transistion_matrices(self):
        for gate in self.circuits[0].get_allgates():
            gate.print_matrix()

    