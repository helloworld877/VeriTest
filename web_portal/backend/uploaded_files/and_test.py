def compute(inputs):
	a = int(inputs["a"],2)

	b = int(inputs["b"],2)

	result_int = a & b 

	result_binary = str(bin(result_int)[2:])
	return{ 'out' : result_binary } 

