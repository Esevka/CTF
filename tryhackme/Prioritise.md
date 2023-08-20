## TryHackMe  <> Prioritise

![image](https://github.com/Esevka/CTF/assets/139042999/42583888-171e-4764-80e4-69e79bcb3c38)

Enlace Maquina: https://tryhackme.com/room/prioritise

Enunciado : Obtener flag
---
---

## Escaneo de puertos

-Lanzamos una traza ICMP(ping) para ver si la maquina esta activa, segun el ttl obtenido por proximidad al valor 64 podriamos decir que es una maquina Linux.

    ┌──(root㉿kali)-[/home/kali/Desktop/ctf/prioritise]
    └─# ping -c1 10.10.227.33  
    PING 10.10.227.33 (10.10.227.33) 56(84) bytes of data.
    64 bytes from 10.10.227.33: icmp_seq=1 ttl=63 time=51.3 ms
    
    --- 10.10.227.33 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 51.261/51.261/51.261/0.000 ms

-Reporte Nmap (Obtenemos puertos abiertos servicios y versiones que estan corriendo).

    ┌──(root㉿kali)-[/home/kali/Desktop/ctf/prioritise]
    └─# nmap -p- --open -sS --min-rate 5000 -n -Pn -vvv 10.10.227.33 -oN open_ports
    Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-19 18:36 CEST
    Initiating SYN Stealth Scan at 18:36
    
    PORT   STATE SERVICE REASON
    22/tcp open  ssh     syn-ack ttl 63
    80/tcp open  http    syn-ack ttl 62


    ┌──(root㉿kali)-[/home/kali/Desktop/ctf/prioritise]
    └─# nmap -p 22,80 -sCV 10.10.227.33 -oN info_ports                       
    Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-19 18:38 CEST
    WARNING: Service 10.10.227.33:80 had already soft-matched rtsp, but now soft-matched sip; ignoring second value
    Nmap scan report for 10.10.227.33
    Host is up (0.052s latency).
    
    PORT   STATE SERVICE VERSION
    22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   3072 3e594b164f84a6d8e8bd77fb0f0f2759 (RSA)
    |   256 c1bf6ebceb1bdb04251ec17bb71341a4 (ECDSA)
    |_  256 a4fad854d029f7d26603e2ac2db8bda2 (ED25519)
    
    80/tcp open  rtsp
    | fingerprint-strings: 
    |   FourOhFourRequest: 
    |     HTTP/1.0 404 NOT FOUND
    |     Content-Type: text/html; charset=utf-8
    |     Content-Length: 232
    |     <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
    |     <title>404 Not Found</title>
    |     <h1>Not Found</h1>
    |     <p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
    |   GetRequest: 
    |     HTTP/1.0 200 OK
    |     Content-Type: text/html; charset=utf-8
    |     Content-Length: 5062
    |     <!DOCTYPE html>
    |     <html lang="en">
    |     <head>
    |     <meta charset="utf-8" />
    |     <meta
    |     name="viewport"
    |     content="width=device-width, initial-scale=1, shrink-to-fit=no"
    |     <link
    |     rel="stylesheet"
    |     href="../static/css/bootstrap.min.css"
    |     crossorigin="anonymous"
    |     <link
    |     rel="stylesheet"
    |     href="../static/css/font-awesome.min.css"
    |     crossorigin="anonymous"
    |     <link
    |     rel="stylesheet"
    |     href="../static/css/bootstrap-datepicker.min.css"
    |     crossorigin="anonymous"
    |     <title>Prioritise</title>
    |     </head>
    |     <body>
    |     <!-- Navigation -->
    |     <nav class="navbar navbar-expand-md navbar-dark bg-dark">
    |     <div class="container">
    |     class="navbar-brand" href="/"><span class="">Prioritise</span></a>
    |     <button
    |     class="na
    |   HTTPOptions: 
    |     HTTP/1.0 200 OK
    |     Content-Type: text/html; charset=utf-8
    |     Allow: HEAD, OPTIONS, GET
    |     Content-Length: 0
    |   RTSPRequest: 
    |     RTSP/1.0 200 OK
    |     Content-Type: text/html; charset=utf-8
    |     Allow: HEAD, OPTIONS, GET
    |_    Content-Length: 0
    |_http-title: Prioritise

-Segun la version del servicio SSH que esta corriendo en el puerto 22, obtenemos su launchpad y podemos decir que estamos ante una maquina.
 
    LINUX UBUNTU Serie Focal
    
 INFO: https://launchpad.net/ubuntu/+source/openssh/1:8.2p1-4
 

## Analisis de vulnerabilidades en los servicios y explotacion de los mismos.

Sabemos que la maquina tiene un fallo de seguridad que nos permite realizar un ataque mediante SQLI.

-Cargamos la web que esta corriendo en el puerto 80

![image](https://github.com/Esevka/CTF/assets/139042999/6a130014-212e-4dfc-b284-6ee0e53f7857)

- Anadimos dos items y empezamos a buscar por donde podemos inyectar algo.
  
    ![image](https://github.com/Esevka/CTF/assets/139042999/2cb7ac74-ea37-4981-b0dd-9cce4bb948a3)


- Despues de analizar el funcionanmiento de la web, vemos que a la hora de ordenar los items por 'title' o 'date' podemos injectar codigo.
    
    ![image](https://github.com/Esevka/CTF/assets/139042999/0ea993d6-1ac4-4738-b95e-5c9fadb0ef12)

    Aqui podemos ver que nos lo orderna por title de mayor a menor inyectandole nosotros desc
    ![image](https://github.com/Esevka/CTF/assets/139042999/1a99ee1a-1430-4fbe-abb0-edd5e10d9eb9)

    Aqui podemos ver el otro ejemplo donde hacemos lo mismo pero ordenado por fecha de manera descendiente.
    ![image](https://github.com/Esevka/CTF/assets/139042999/e9657b47-e3aa-45b5-8f67-b9baaebd3ba0)


- Buscamos la manera de poder inyectar codigo en la clausula order by, encontramos esta documentacion que nos ayudo mucho a entender el funcionamiento
  INFO: https://portswigger.net/web-security/sql-injection/blind

      'Blind SQL injection by triggering conditional errors'


- Crearemos nuestra primera SQLI, a partir de este punto todo lo realizaremos con Burpsuite por comodidad.

    El Metodo que vamos a utilizar se basa en si la condicion que podemos se cumple o no, en base a si se cumple la condicion iremos obteniendo datos de la base de datos(locura total).

    La condicion 1=1 se cumple por lo que ordena por title.
  
    ![image](https://github.com/Esevka/CTF/assets/139042999/be125d64-2e32-4c68-b7a7-b292aab027a6)

    La condicion 1=1 no se cumple por lo que ordena por date.

    ![image](https://github.com/Esevka/CTF/assets/139042999/a3891239-d9ac-4e1a-a41d-71708f2db59e)

## Atacamos la BD

    Recordamos si ordena por 'title' VERDADERO, si ordena por 'date' FALSO.

-Obtenemos Motor Base de Datos para saber como tenemos que proceder con las queries.
    
INFO: https://book.hacktricks.xyz/pentesting-web/sql-injection
    
Nos guiamos del apartado 'Identifying Back-end' donde tras probar identificamos que estamos delante de ---> SQLITE.

![image](https://github.com/Esevka/CTF/assets/139042999/33cdc8e5-c423-46b5-a3d4-3e7b7aadc544)

-Obtenemos el numero de tablas que tienes la bd

INFO: https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/SQLite%20Injection.md

Explicacion de los campos de la sentencia INFO: https://www.techonthenet.com/sqlite/sys_tables/index.php

Lo podemos hacer igualando a 0,1,2,3.... hasta dar con el valido o podemos usar < o > para acotar el rango mas rapidamente y despues utilizar el = para verificarlo, en este caso determinamos que tenemos ---> 2 tablas.

    GET /?order=Case+When+(select+count(tbl_name)+from+sqlite_master+where+type='table')>3+THEN+title+ELSE+date+END --->order by date
    
	GET /?order=Case+When+(select+count(tbl_name)+from+sqlite_master+where+type='table')<2+THEN+title+ELSE+date+END --->order by title

![image](https://github.com/Esevka/CTF/assets/139042999/ff1c3c42-fbd8-4123-952b-10c7d3efadcd)


-Obtenemos el numero de caracteres que componen el nombre de las tablas.




      

      
  
  
    


    


