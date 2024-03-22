import subprocess

def brute(line):
	result = subprocess.run(['steghide extract -sf **IMG** -p {}'.format(line)],shell=True,capture_output=True,text=True)

	if(result.returncode==0):
		print('[-]Clave Incorrecta --> {}'.format(line))
	else:
		print('[+]Clave --> {}'.format(line))
		exit()
		
def main():
	with open('**Diccionario**','r') as passwd:
		for line in passwd:
			brute(line.strip())

if __name__ == '__main__':
	main()
