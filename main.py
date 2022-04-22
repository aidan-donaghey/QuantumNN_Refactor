"""Main Doc String for Refactor.py"""

from Modules.abstract_gate import RzxGate, RxxGate
from Modules.abstract_block import RzxBlock, RxxBlock
from Modules.circuits import Circuit
from Modules.collectionofcircuits import Collection
from Modules import utils
import numpy as np

# # Testing the RZX gate
# rzx = RzxGate(2, 1, 1)
# print(rzx)

# # Testing the Blocks
# rzxBlock = RzxBlock(3, [2, 10])
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
Qubits = 2

# Gates = [RZX,RZX]
Gates = [RZX]
# Change for different DataPoints
CURRENTDATA = IDENTITYDATA

DataSet = hf.getDatasets(CURRENTDATA, numOfBits=Qubits)

testCollection = Collection(Qubits, DataSet, Gates)

testCollection.create_circuits(Theta=[0.9])

# testCircuit = Circuit(Qubits, DataSet[1][0], DataSet[1][1], Gates)
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
allcircuits = testCollection.fit(Epoch=6)


# hf.printallinfo(allcircuits)


print(testCollection.predict(DataSet[0]))
print(testCollection.predict(DataSet[1]))
print(testCollection.predict(DataSet[2]))
print(testCollection.predict(DataSet[3]))
# # print("all combinations")
# # print(utils.getInputs(2))
# print(f"The Px values:{[x.get_px()for x in allcircuits]}")
# print(f"Negative Log Likihoods: {[-np.log(x.get_px()) for x in allcircuits]}")
