import subprocess

def brute(line,x):
	result = subprocess.run(['steghide extract -sf **IMG** -f -p {}'.format(line)],shell=True,capture_output=True,text=True)

	if(result.returncode==1):
		print('[{}-5000]Clave Incorrecta --> {}'.format(x,line))
	else:
		print('[+]Clave --> {}'.format(line))
		print('[+]INFO --> {}'.format(result.stderr))
		exit()
		
def main():
	x=0
	
	with open('**Diccionario**','r') as passwd:
		for line in passwd:
			x+=1
			brute(line.strip(),x)

if __name__ == '__main__':
	main()
