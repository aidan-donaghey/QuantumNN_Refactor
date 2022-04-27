"""Main Doc String for Refactor.py"""

from Modules.abstract_gate import RzxGate, RxxGate
from Modules.abstract_fcgates import RzxGateAnyConnect, RxxGateAnyConnect
from Modules.abstract_block import RzxBlock, RxxBlock
from Modules.abstract_fcblock import RzxFullyConnectedBlock, RxxFullyConnectedBlock
from Modules.circuits import Circuit
from Modules.collectionofcircuits import Collection
from Modules import utils
import numpy as np
import random


from Modules import helperfunctions as hf

# Sample Data Sets
FOLDER = "SimpleData/"
IDENTITYDATA = FOLDER + "2Bits/" + "IDENTITY_2Bits_5samples"
IDENTITYDATASMALL = FOLDER + "2Bits/" + "IDENTITY_2Bits_2samples"
NOTDATA = FOLDER + "2Bits/" + "NOT_2Bits_5samples"

THREE_AND = FOLDER + "3Bits/AND_3bits_5samples"
THREE_OR = FOLDER + "3Bits/OR_3bits_5samples"
THREE_XOR = FOLDER + "3Bits/XOR_3bits_5samples"

FOUR_XOR = FOLDER + "4Bits/XOR_4Bits"

SIX_XOR = FOLDER + "6Bits/XOR_4Padded"


# Real Data Sets
FOLDER = "data/"
ALL_DATA = FOLDER + "data_all"



RXX = "RXX"
RZX = "RZX"
FCRXX = "FCRXX"
FCRZX = "FCRZX"
Qubits = 9
Gates = [RZX, RXX]

# Change for different DataPoints
CURRENTDATA = ALL_DATA



DataSet = hf.getDatasets(CURRENTDATA, numOfBits=Qubits)
# Due to the genitic data being ordered based off output.
random.shuffle(DataSet)
Trainingset = DataSet[:int(len(DataSet) * 0.8)]
Testingset = DataSet[int(len(DataSet) * 0.8):]
testCollection = Collection(Qubits, Trainingset, Gates)
# NOTE: IF ERROR SAYS THE FOLLOWING . THE CORRECT NUMBER IS THE LAST PARAM IN THE NORMAL FUNCTION
# IndexError: The length of thetas list is incorrect.

# For this example it should be 8 but was 2

Theta=[x for x in np.random.normal(0, 1, 16)]
# print("Theta 0: ", Theta)
testCollection.create_circuits(
    Theta = Theta
)

allcircuits = testCollection.fit(Epoch=20)

print("TestingSet: ", Testingset)
Probabilities = []
for x in Testingset:
    # print(testCollection.predict(x))
    Probabilities.append(testCollection.predict(x))
percentagesandSplits = hf.get_percentage_correct(Probabilities)
print(f"There were {percentagesandSplits[0]}% predicted Correctly.")
print(f"{percentagesandSplits[1]}% of data outputs were 0 and  {100 - percentagesandSplits[1]}% were 1")


            
    


# # print("all combinations")
# print(utils.getInputs(3))
# print(f"The Px values:{[x.get_px()for x in allcircuits]}")
# print(f"Negative Log Likihoods: {[-np.log(x.get_px()) for x in allcircuits]}")



# FCrzx = RzxFullyConnectedBlock(3, [1, 1,2,4,5,6])
# print(FCrzx)

# FCrzx.print()