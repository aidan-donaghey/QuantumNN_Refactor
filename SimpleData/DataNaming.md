## Naming Conventions
### Data Type
It will be the relation for the data - Current Supported => AND, IDENTITY, NOT, RANDOM, XOR.

### Number of Qubits 
This is the number of total bits in the system including the output qubit.
Looks like : ` _#Bits_`

### How many data points
Last Number is the number of DataPoints. 
Looks like: `#samples`

### Version or Notes
After the sample number if more information is needed simply add it here.

#### Examples

`AND_3Bits_5samples`
`OR_3Bits_10samples`
`IDENTITY_10Bits_10000samples`
`AND_3Bits_5samples_ByHand`

### Current Data Table
| Name                     | Notes                                                                                        |
|--------------------------|----------------------------------------------------------------------------------------------|
| OR_3Bits_5samples        | There is atleast 1 of each possibility in the data. 4 out of 5 results result in a 1 output. |
| XOR_3Bits_5samples       | There is atleast 1 of each possibility in the data. 3 out of 5 results result in a 1 output. |
| AND_3Bits_5samples       | There is atleast 1 of each possibility in the data. 2 out of 5 results result in a 1 output. |
| INDENTITY_2Bits_5samples | There is atleast 1 of each possibility in the data. 3 out of 5 results result in a 1 output. |
| NOT_2Bits_5samples       | There is atleast 1 of each possibility in the data. 3 out of 5 results result in a 1 output. |
