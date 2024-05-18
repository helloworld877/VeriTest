# from Coverage.coverage import COVERAGE_MAIN
from PARSER.Simulate import PRASER_MAIN
from PARSER.GraphAPI import GraphAPI
from PARSER.code_to_graph import code_to_graph
from encoding_utils import get_encoding, get_nodes_sizes
from PARSER.components.Gates.bitwise import bitwise
import networkx as nx
import matplotlib.pyplot as plt
import os
import json
import sys


if len(sys.argv) < 2:
    print("Usage: python main.py <argument>")
    sys.exit(1)

filename = sys.argv[1]
prediction = sys.argv[2]
# filename = "my_module.v"


G, input_output_wire = code_to_graph(filename)


input_variables = input_output_wire[0]
output_variables = input_output_wire[1]


output_json = {}
output_json["module_name"] = os.path.basename(filename)

if (prediction != "not"):
    output_json["inputs"] = [{'name': name, 'size': size}
                             for name, size in input_variables.items()]

if (prediction in ['and', 'or', 'xor', 'nand', 'nor', 'xnor']):
    output_json["type"] = prediction
    # TODO:which output variable to use

    output_json["output"] = list(output_variables.keys())[0]
    # which operation type to use
    output_json["operation_type"] = "bitwise"
