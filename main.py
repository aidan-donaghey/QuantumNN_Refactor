"""Main Doc String for Refactor.py"""

from Modules.abstract_gate import RzxGate, RxxGate
from Modules.abstract_block import RzxBlock, RxxBlock
from Modules.circuits import Circuit
from Modules.collectionofcircuits import Collection

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
Qubits = 3

# Gates = [RZX,RZX]
Gates = [RXX, RZX, RZX]
# Change for different DataPoints
CURRENTDATA = IDENTITYDATA

DataSet = hf.getDatasets(CURRENTDATA, numOfBits=Qubits)
DataPoint = DataSet[0]
testCircuit = Circuit(Qubits, *DataPoint, Gates, [1, 2, 3, 4, 5, 6])
# print(testCircuit)

# print("The XI values are:\n", [x.A for x in testCircuit.get_xis()])
# print("XI Values from the circuit:\n", [x.A for x in testCircuit.get_xis()])
# testCircuit.get_xis()
# print(
#     "The numerator and Denominator:",
#     testCircuit.get_numerators_and_denominators_for_circuit(),
# )
# # print([x.A for x in testCircuit.alphas])

# testCircuit.backward_pass()

# # print(*[f"beta {index}:\n{x.A}\n" for index, x in enumerate(testCircuit.betas)])

# print([xi.A for xi in testCircuit.get_xi()])

testCollection = Collection(Qubits, DataSet, Gates)
testCollection.create_circuits()
# ws = testCollection.calculate_ws()
# print(ws)
testCollection.fit(Epoch=10)
print(testCollection.predict(DataPoint))
