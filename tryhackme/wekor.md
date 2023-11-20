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

-Puerto 80(HTTP)

  -Incluimos el dominio 'wekor.thm' en nuestro fichero hosts.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/wekor/nmap]
    └─# cat /etc/hosts                              
    127.0.0.1       localhost
    10.10.120.22    wekor.thm

  -Visualizamos la web en busqueda de informacion y encontramos esto.

  ![image](https://github.com/Esevka/CTF/assets/139042999/ed54338e-091f-4234-a47e-b3a363163874)

  -Segun la info obtenida con nmap tenemos disponible el fichero robots.txt con una serie de directorios.

    | http-robots.txt: 9 disallowed entries 
    | /workshop/ /root/ /lol/ /agent/ /feed /crawler /boot 
    |_/comingreallysoon /interesting

    NOTA: 


    
                          

  


