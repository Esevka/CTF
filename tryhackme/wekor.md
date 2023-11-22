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

  5) Crakeamos las passwords con john.

     Creamos un ficheros con estructura usuario:pass 
         


  6) Acabamos de obtener credenciales par wordpress,llegadoss a este punto sabemos que debe

         
      
         

       



       

     






    
                          

  


