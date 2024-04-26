
import sys
import os
import json

specs_dict = {}


def input_file_reader(file_path):
    global specs_dict
    try:
        with open(file_path, 'r') as file:
            specs_dict = json.load(file)
        return specs_dict
    except FileNotFoundError:
        print("File not found.")
        sys.exit(1)


def gate_category_generator():

    circuit_type = specs_dict["type"]
    # output_file_text
    output_code = []
    # get operation symbol
    operation_symbol = ''
    if (circuit_type in ['and', 'nand']):
        operation_symbol = '&'
    elif (circuit_type in ['or', 'nor']):
        operation_symbol = '|'
    elif (circuit_type in ['xor', 'xnor']):
        operation_symbol = '^'
    # get number of inputs
    number_of_inputs = int(len(specs_dict['inputs']))

    input_names = specs_dict["inputs"]
    output_name = specs_dict['output']

    result_line = '\tresult_int = '
    output_code.append('def compute(inputs):')

    if ("operation_type" in specs_dict and specs_dict["operation_type"] == "bitwise"):
        # bitwise operation code
        # inputs initialization
        for i in range(0, number_of_inputs):
            output_code.append(
                f'''\t{input_names[i]['name']} = inputs["{input_names[i]['name']}"]\n''')

        output_code.append(f"""\tresult_binary='' """)

        # bitwise calculation loop
        output_code.append(
            f"""\tfor i in range (0,{input_names[0]["size"]}):""")

        result_calculation_line = '\t\tresult_binary += str(bin('
        for input in input_names:

            result_calculation_line += f""" int({input["name"]}[i]) &"""
        result_calculation_line = result_calculation_line[:-2]
        result_calculation_line += '))[2:]'
        output_code.append(result_calculation_line)

        # optional bitwise code
        if circuit_type in ['nand', 'nor', 'xnor']:
            output_code.append("\tbitmask = (1 << len(result_binary)) - 1")
            output_code.append("\tbitwise_not = int(result_binary) ^ bitmask")
            output_code.append(
                "\tresult_binary = format(bitwise_not, 'b').zfill(len(result_binary))")
        # output return line
        output_code.append(
            f'\treturn{{ \'{output_name}\' : result_binary }} \n')
    else:
        # logical operation code

        # inputs initialization and result calculation line generation
        for i in range(0, number_of_inputs):

            output_code.append(
                f'''\t{input_names[i]['name']} = int(inputs["{input_names[i]['name']}"],2)\n''')
            result_line += f'{input_names[i]["name"]} {operation_symbol} '
        result_line = result_line[:-2]+"\n"
        output_code.append(result_line)
        if circuit_type in ['nand', 'nor', 'xnor']:
            output_code.append('\tresult_int = not result_int')
        output_code.append('\tresult_binary = str(bin(result_int)[2:])')

        output_code.append(
            f'\treturn{{ \'{output_name}\' : result_binary }} \n')

    # print code to file
    try:
        with open(f'{specs_dict["model_name"]}.py', 'w') as file:
            for line in output_code:
                file.write(line + '\n')
        print("specs_dict written to file successfully.")
    except IOError:
        print("Error writing to file.")


def adder_category_generator():

    category = specs_dict['type']

    # generate output code
    output_code = ['def compute(inputs):']

    number_of_inputs = int(len(specs_dict['inputs']))
    input_names = specs_dict['inputs']
    for i in range(0, number_of_inputs):
        output_code.append(
            f'''\t{input_names[i]['name']} = inputs["{input_names[i]['name']}"]\n''')

    # flags code
    output_code.append("""\tsign_flag = '0'
\tzero_flag = '0'
\todd_parity_flag = '0'
\teven_parity_flag = '0'
\todd_flag = '0'
\teven_flag = '0'
\tcarry_out= '0'
\toverflow_flag = '0'""")

    # carry in code

    if ("carry_in" in specs_dict):
        output_code.append(
            f"""\tcarry_in = int(inputs["{specs_dict["carry_in"]["name"]}"])""")
    else:
        output_code.append("\tcarry_in=0")

    result_line = "\tresult_binary = "
    if ("mode" in specs_dict and specs_dict["mode"] == "signed"):
        for x in input_names:
            name = x["name"]
            result_line += f"int({name}[1:], 2) * (1 - 2 * int({name}[0])) + "
        result_line = result_line[:-2]
    else:
        for x in input_names:
            name = x["name"]
            result_line += f"int({name}, 2) + "
        result_line = result_line[:-2]
    output_code.append(result_line)

    # flag calculation

    output_code.append(f"""\tresult_binary += carry_in
\tsign_flag = '1' if result_binary < 0 else '0'
\tzero_flag = '1' if result_binary == 0 else '0'
\todd_flag = '1' if result_binary % 2 != 0 else '0'
\teven_flag = '1' if result_binary % 2 == 0 else '0'

\tbinary_form = f'''{{abs(result_binary):0{specs_dict["output"]["size"]}b}}'''

\tif (result_binary < 0):
\t\tbinary_form = '1' + binary_form[1:]
\tresult_binary = binary_form
\tone_count = result_binary.count('1')
\tif (one_count % 2 == 0):
\t\teven_parity_flag = '1'
\t\todd_parity_flag = '0'
\telse:
\t\teven_parity_flag = '0'
\t\todd_parity_flag = '1'

""")

    # overflow flag and carry flag
    output_code.append(f"""\tif (len(result_binary) > {specs_dict["output"]["size"]}):
\t\tcarry_out = '1'
\t\toverflow_flag = '1'
\t\tresult_binary = result_binary[1:]
""")

    # return line
    return_line = "\treturn { "

    return_line += f"""'{specs_dict["output"]["name"]}':result_binary,"""

    if ("sign_flag" in specs_dict):
        return_line += f"""'{specs_dict["sign_flag"]['name']}':sign_flag,"""
    if ("zero_flag" in specs_dict):
        return_line += f"""'{specs_dict["zero_flag"]['name']}':zero_flag,"""
    if ("odd_parity_flag" in specs_dict):
        return_line += f"""'{specs_dict["odd_parity_flag"]['name']}':odd_parity_flag,"""
    if ("even_parity_flag" in specs_dict):
        return_line += f"""'{specs_dict["even_parity_flag"]['name']}':even_parity_flag,"""
    if ("odd_flag" in specs_dict):
        return_line += f"""'{specs_dict["odd_flag"]['name']}':odd_flag,"""
    if ("even_flag" in specs_dict):
        return_line += f"""'{specs_dict["even_flag"]['name']}':even_flag,"""
    if ("overflow_flag" in specs_dict):
        return_line += f"""'{specs_dict["overflow_flag"]['name']}':overflow_flag,"""
    if ("carry_out" in specs_dict):
        return_line += f"""'{specs_dict["carry_out"]['name']}':carry_out,"""

    return_line = return_line[:-1] + '}'
    output_code.append(return_line)

    # check input and output size eligibility
    output_expected_bits = max(
        specs_dict["inputs"][0]["size"], specs_dict["inputs"][1]["size"])+1

    if (len(specs_dict["inputs"]) > 2):
        for i in range(2, len(specs_dict["inputs"])):
            output_expected_bits = max(
                output_expected_bits, specs_dict["inputs"][1]["size"])+1

    if not ((output_expected_bits == specs_dict["output"]["size"] or output_expected_bits - 1 == specs_dict["output"]["size"])):

        print("ERROR => output variable size is too small")
        print(f'EXPECTED {output_expected_bits} or {output_expected_bits-1}')
        return

    # print code to file
    try:
        with open(f'{specs_dict["model_name"]}.py', 'w') as file:
            for line in output_code:
                file.write(line + '\n')
        print("specs_dict written to file successfully.")
    except IOError:
        print("Error writing to file.")


def not_category_generator():

    # generate code
    output_code = ["def compute(inputs):"]

    # read inputs lines
    for x in specs_dict["inputs_outputs"]:
        output_code.append(
            f'''\t{x['input_name']} = inputs["{x['input_name']}"]\n''')

    # calculate outputs lines
    for x in specs_dict["inputs_outputs"]:
        output_code.append(
            f'''\t{x['output_name']} = ''.join(['1' if bit == '0' else '0' for bit in {x["output_name"]}])''')

    return_line = '\treturn { '
    # return_line
    for x in specs_dict["inputs_outputs"]:
        return_line += f"""'{x["output_name"]}': {x["output_name"]},"""
    return_line = return_line[:-1] + "}"
    output_code .append(return_line)

    # print code to file

    try:
        with open(f'{specs_dict["model_name"]}.py', 'w') as file:
            for line in output_code:
                file.write(line + '\n')
        print("specs_dict written to file successfully.")
    except IOError:
        print("Error writing to file.")


def decoder_category_generator():

    input_size = 0
    output_size = 0
    # generate code
    output_code = ["def compute(inputs):"]

    # separate mode
    if (specs_dict["input_mode"] == "separate"):
        # read inputs lines
        for x in specs_dict["inputs"]:
            output_code.append(
                f'''\t{x['name']} = inputs["{x['name']}"]\n''')

        concatenation_line = f'''\tinput_string = '''
        for x in specs_dict["inputs"]:
            concatenation_line += f"{x['name']} + "
            # separate mode size calculation
            input_size += x['size']
        concatenation_line = concatenation_line[:-2]
        output_code.append(concatenation_line)

    # concatenated mode
    else:
        output_code.append(
            f"\tinput_string= inputs['{specs_dict['inputs'][0]['name']}']")
        # concatenation mode size calculation
        input_size += specs_dict['inputs'][0]['size']

    output_size = 0

    if (specs_dict["output_mode"] == "separate"):

        for x in specs_dict["output"]:
            output_size += x["size"]

    else:
        # concatenation mode size calculation
        output_size = specs_dict["output"][0]["size"]

    output_code.append(f'''\toutput_string="{"0"*output_size}"''')

    output_code.append(f'''\tdecoder_index = int(input_string, 2)''')
    output_code.append(
        f'''\toutput_string = output_string[:decoder_index] + '1' + output_string[decoder_index + 1:]''')

    if (specs_dict["output_mode"] == "separate"):
        i = 0
        for x in specs_dict["output"]:
            output_code.append(f'''\t{x['name']}=output_string[{i}]''')
            i += 1
    else:
        output_code.append(
            f'''\t{specs_dict['output'][0]['name']}=output_string''')

    return_line = "\treturn { "

    if (specs_dict["output_mode"] == "separate"):
        output_code.append(' output_string = output_string[::-1]')
        for x in specs_dict["output"]:
            return_line += (f'''"{x["name"]}": {x["name"]}, ''')
        return_line = return_line[:-2] + '}'
        output_code.append(return_line)
    else:
        return_line += f'''"{specs_dict['output'][0]['name']}": {specs_dict['output'][0]['name']} }}'''
        output_code.append(return_line)

    if (pow(2, input_size) != output_size):
        print(input_size)
        print(output_size)
        print("ERROR: Size mismatch for inputs and outputs")
        print("HINT: pow(2,number of inputs) == number of outputs")
    # print code to file

    try:
        with open(f'{specs_dict["model_name"]}.py', 'w') as file:
            for line in output_code:
                file.write(line + '\n')
        print("specs_dict written to file successfully.")
    except IOError:
        print("Error writing to file.")


def encoder_category_generator():
    input_size = 0
    output_size = 0
    # generate code
    output_code = ["def compute(inputs):"]

    # separate mode
    if (specs_dict["input_mode"] == "separate"):
        # read inputs lines
        for x in specs_dict["inputs"]:
            output_code.append(
                f'''\t{x['name']} = inputs["{x['name']}"]\n''')

        concatenation_line = f'''\tinput_string = '''
        for x in specs_dict["inputs"]:
            concatenation_line += f"{x['name']} + "
            # separate mode size calculation
            input_size += x['size']
        concatenation_line = concatenation_line[:-2]
        output_code.append(concatenation_line)

    # concatenated mode
    else:
        output_code.append(
            f"\tinput_string= inputs['{specs_dict['inputs'][0]['name']}']")
        # concatenation mode size calculation
        input_size += specs_dict['inputs'][0]['size']

    output_code.append("output_num = input_string.find('1')")
    output_code.append('f"{abs(output_num):0{2}b}"')

    if (specs_dict["output_mode"] == "separate"):
        i = 0
        for x in specs_dict["output"]:
            output_code.append(f'''\t{x['name']}=output_string[{i}]''')
            i += 1
    else:
        output_code.append(
            f'''\t{specs_dict['output'][0]['name']}=output_string''')

    return_line = "\treturn { "

    if (specs_dict["output_mode"] == "separate"):
        output_code.append(' output_string = output_string[::-1]')
        for x in specs_dict["output"]:
            return_line += (f'''"{x["name"]}": {x["name"]}, ''')
        return_line = return_line[:-2] + '}'
        output_code.append(return_line)
    else:
        return_line += f'''"{specs_dict['output'][0]['name']}": {specs_dict['output'][0]['name']} }}'''
        output_code.append(return_line)

    if (pow(2, output_size) != input_size):
        print(input_size)
        print(output_size)
        print("ERROR: Size mismatch for inputs and outputs")
        print("HINT: pow(2,number of inputs) == number of outputs")

    try:
        with open(f'{specs_dict["model_name"]}.py', 'w') as file:
            for line in output_code:
                file.write(line + '\n')
        print("specs_dict written to file successfully.")
    except IOError:
        print("Error writing to file.")


def seven_segment_generator():
    input_size = 0
    output_size = 0
    # generate code
    output_code = ["def compute(inputs):"]

    # separate mode
    if (specs_dict["input_mode"] == "separate"):
        # read inputs lines
        for x in specs_dict["inputs"]:
            output_code.append(
                f'''\t{x['name']} = inputs["{x['name']}"]\n''')

        concatenation_line = f'''\tinput_string = '''
        for x in specs_dict["inputs"]:
            concatenation_line += f"{x['name']} + "
            # separate mode size calculation
            input_size += x['size']
        concatenation_line = concatenation_line[:-2]
        output_code.append(concatenation_line)

    # concatenated mode
    else:
        output_code.append(
            f"\tinput_string= inputs['{specs_dict['inputs'][0]['name']}']")
        # concatenation mode size calculation
        input_size += specs_dict['inputs'][0]['size']

    output_code.append('\toutput_string = "0000000"')
    output_code.append('\tinput_number = int(input_string, 2)')

    output_code.append('''\tif input_number == 0:
\t\toutput_string = "1111110"
\telif input_number == 1:
\t\toutput_string = "0110000"
\telif input_number == 2:
\t\toutput_string = "1101101"
\telif input_number == 3:
\t\toutput_string = "1111001"
\telif input_number == 4:
\t\toutput_string = "0110011"
\telif input_number == 5:
\t\toutput_string = "1011011"
\telif input_number == 6:
\t\toutput_string = "1011111"
\telif input_number == 7:
\t\toutput_string = "1110000"
\telif input_number == 8:
\t\toutput_string = "1111111"
\telif input_number == 9:
\t\toutput_string = "1111011"
\telif input_number == 10:
\t\toutput_string = "1110111"
\telif input_number == 11:
\t\toutput_string = "0011111"
\telif input_number == 12:
\t\toutput_string = "1001110"
\telif input_number == 13:
\t\toutput_string = "0111101"
\telif input_number == 14:
\t\toutput_string = "1001111"
\telif input_number == 15:
\t\toutput_string = "1000111"''')

    if (specs_dict["output_mode"] == "separate"):
        output_code.append('\toutput_string = output_string[::-1]')
        i = 0
        for x in specs_dict["output"]:
            output_code.append(f'''\t{x['name']}=output_string[{i}]''')
            i += 1
    else:
        output_code.append(
            f'''\t{specs_dict['output'][0]['name']}=output_string''')

    return_line = "\treturn { "

    if (specs_dict["output_mode"] == "separate"):
        for x in specs_dict["output"]:
            return_line += (f'''"{x["name"]}": {x["name"]}, ''')
        return_line = return_line[:-2] + '}'
        output_code.append(return_line)
    else:
        return_line += f'''"{specs_dict['output'][0]['name']}": {specs_dict['output'][0]['name']} }}'''
        output_code.append(return_line)

    if (output_size == 8 and input_size == 4):
        print(input_size)
        print(output_size)
        print("ERROR: Size mismatch for inputs and outputs")
        print("HINT:  number of outputs == 8 and number of inputs == 4")

    try:
        with open(f'{specs_dict["model_name"]}.py', 'w') as file:
            for line in output_code:
                file.write(line + '\n')
        print("specs_dict written to file successfully.")
    except IOError:
        print("Error writing to file.")


def main():

    # Check if arguments are provided
    if len(sys.argv) > 1:

        specs_file = sys.argv[1:][0]

    else:
        print("No command-line arguments provided please provide the specs file filename")
        sys.exit(1)
    input_file_reader(specs_file)

    category = specs_dict['type']
    # gates category
    if (category in ['and', 'nand', 'nor', 'or', 'xnor', 'xor']):
        gate_category_generator()
    # adder category
    elif (category in ['adder', 'subtractor']):
        adder_category_generator()
    # not category
    elif (category == "not"):
        not_category_generator()
    # decoder category
    elif (category == "decoder"):
        decoder_category_generator()
    elif (category in ["encoder", "pe"]):
        encoder_category_generator()
    elif (category == "seg"):
        seven_segment_generator()


main()
