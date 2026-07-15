
def getFactorial(num):
	if num < 0:
		raise Exception("Number must be nonnegative")
	elif num <= 1:
		return 1
	else:
		print(num)
		return num*getFactorial(num-1) 


def generateFibonacci(num_elements):
	if num_elements <= 0:
		raise Exception("Fibonacci elements must be at least 1")
	elif num_elements == 1:
		return [0]
	elif num_elements == 2:
		return [0, 1]
	else:
		reference_fib = generateFibonacci(num_elements-1)
		return reference_fib + [reference_fib[-1] + reference_fib[-2]] 

