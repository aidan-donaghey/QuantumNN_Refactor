"""Main Doc String for Refactor.py"""

from Modules.abstract_gate import RzxGate, RxxGate
from Modules.abstract_fcgates import RzxGateAnyConnect, RxxGateAnyConnect
from Modules.abstract_block import RzxBlock, RxxBlock
from Modules.abstract_fcblock import RzxFullyConnectedBlock, RxxFullyConnectedBlock
from Modules.circuits import Circuit
from Modules.collectionofcircuits import Collection
from Modules import utils
import numpy as np

# Testing the RZX gate
# rzx = RzxGate(3, 1, 1)
# print(rzx.matrix)

# # Testing the Blocks
# rzxBlock = RzxBlock(3, [1, 1])
# rzxBlock.print()

# # Testing the Blocks
# rxxBlock = RxxBlock(3, [2, 10])
# rxxBlock.print()


from Modules import helperfunctions as hf

FOLDER = "SimpleData/"
IDENTITYDATA = FOLDER + "2Bits/" + "IDENTITY_2Bits_5samples"
IDENTITYDATASMALL = FOLDER + "2Bits/" + "IDENTITY_2Bits_2samples"
NOTDATA = FOLDER + "2Bits/" + "NOT_2Bits_5samples"

THREE_AND = FOLDER + "3Bits/AND_3bits_5samples"
THREE_OR = FOLDER + "3Bits/OR_3bits_5samples"
THREE_XOR = FOLDER + "3Bits/XOR_3bits_5samples"

FOUR_XOR = FOLDER + "4Bits/XOR_4Bits"

SIX_XOR = FOLDER + "6Bits/XOR_4Padded"


RXX = "RXX"
RZX = "RZX"
FCRXX = "FCRXX"
FCRZX = "FCRZX"
Qubits = 6
# Gates = [RZX,RZX]
Gates = [RZX]

# Change for different DataPoints
CURRENTDATA = SIX_XOR



DataSet = hf.getDatasets(CURRENTDATA, numOfBits=Qubits)

testCollection = Collection(Qubits, DataSet, Gates)

Theta=[x for x in np.random.normal(0, 1, 5)]
print("Theta 0: ", Theta)
testCollection.create_circuits(
    Theta = Theta
)

# testCircuit = Circuit(Qubits, DataSet[1][0], DataSet[1][1], Gates,thetas=[x for x in np.random.normal(0, 1, 8)])
# testCircuit.get_xis()
# print(f"testCircuit Transitions Before any Update:\n{testCircuit.get_allgates()}")
# print(f"testCircuit ZK Before any Update:\n{testCircuit.get_allgates()[0].zk_matrix}")
# print(f"testCircuit.alphas:\n{[x.A for x in testCircuit.alphas]}")
# print(f"testCircuit.betas:\n{[x.A for x in testCircuit.betas]}")
# print(f"testCircuit.xis:\n{[x.A for x in testCircuit.xis]}")
# print(
#     f"testCircuit Numerator and Denominiator:\n{testCircuit.get_numerators_and_denominators_for_circuit()}"
# )

# # ws = testCollection.calculate_ws()
# # print(ws)
allcircuits = testCollection.fit(Epoch=10)


# # hf.printallinfo(allcircuits)

for x in range(4):
    print(DataSet[x])
    print(testCollection.predict(DataSet[x]))



# # print("all combinations")
# print(utils.getInputs(3))
# print(f"The Px values:{[x.get_px()for x in allcircuits]}")
# print(f"Negative Log Likihoods: {[-np.log(x.get_px()) for x in allcircuits]}")



# FCrzx = RzxFullyConnectedBlock(3, [1, 1,2,4,5,6])
# print(FCrzx)

# FCrzx.print()