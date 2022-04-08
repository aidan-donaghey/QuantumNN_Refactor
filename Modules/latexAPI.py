import numpy as np
from pylatex import (
    Document,
    Section,
    Subsection,
    Subsubsection,
    Math,
    Matrix,
    VectorName,
)


def inputMatrix(data, name=None):
    a = data[0].InputState.A
    doc = Document()
    section = Section("QML Data")
    subsection = Subsection("Input Array")

    vec = Matrix(a)
    vec_name = VectorName("a")
    math = Math(data=[vec_name, "=", vec])

    subsection.append(math)
    section.append(subsection)

    doc.append(section)
    doc.generate_pdf("numpy_ex", clean_tex=False)


def outMask(data, name=None):
    a = data[0].OutputState.A
    doc = Document()
    section = Section("QML Data")
    subsection = Subsection("Output Mask")

    vec = Matrix(a)
    vec_name = VectorName("a")
    math = Math(data=[vec_name, "=", vec])

    subsection.append(math)
    section.append(subsection)

    doc.append(section)
    doc.generate_pdf("numpy_ex", clean_tex=False)


def AllGates(data, datapoint=0, epoch=None):
    a = data[0].InputState.A
    doc = Document()
    section = Section("QML Data")
    subsection = Subsection("Input Array")

    vec = Matrix(a)
    vec_name = VectorName("a")
    math = Math(data=[vec_name, "=", vec])

    subsection.append(math)
    section.append(subsection)

    a = data[0].OutputState.A
    subsection = Subsection("Output Mask")

    vec = Matrix(a)
    vec_name = VectorName("a")
    math = Math(data=[vec_name, "=", vec])

    subsection.append(math)
    section.append(subsection)
    doc.append(section)
    section = Section("Transition Matrices")

    if epoch is not None:
        data = data[epoch : epoch + 1]
    for index, y in enumerate(data):
        temp = y
        subsection = Subsection(f"Epoch : {(index + epoch) if epoch else index }")
        for index, x in enumerate(temp.TransistionLayers):
            subsubsection = Subsubsection(f"Transistion Matrix {index +1}")
            print(x)
            a = ["{:0.2f}".format(y) for y in x.A]
            vec = Matrix(a)
            math = Math(data=[vec])
            subsubsection.append(math)

            subsection.append(subsubsection)
        section.append(subsection)

    doc.append(section)
    doc.generate_pdf("numpy_ex", clean_tex=False)
