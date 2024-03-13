import subprocess

def brute(line):

	result = subprocess.run(['steghide extract -sf twitter.jpg_large -p {}'.format(line)],shell=True,capture_output=True,text=True)

	if 'steghide: could not extract any data' in result.stderr:
		print('[-]Clave Incorrecta --> {}'.format(line))
	else:
		print('[+]Clave --> {}'.format(line))
		exit()


def main():

	with open('/usr/share/wordlists/rockyou_limpio.txt','r') as passwd:
		for line in passwd:
			brute(line.strip())

if __name__ == '__main__':
	main()