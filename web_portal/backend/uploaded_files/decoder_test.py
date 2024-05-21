def compute(inputs):
	input_string= inputs['a']
	output_string="0000"
	decoder_index = int(input_string, 2)
	output_string = output_string[:decoder_index] + '1' + output_string[decoder_index + 1:]
	y=output_string
	return { "y": y }
