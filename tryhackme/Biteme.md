## TryHackMe  <> Biteme

![image](https://github.com/Esevka/CTF/assets/139042999/77c9b6a2-d31a-4c55-a2af-473a9c2aa32c)

Enlace Maquina: https://tryhackme.com/room/biteme

Enunciado : 
  - Start the machine and get the flags...

    
## Escaneo de puertos

- Lanzamos una traza ICMP(ping) para ver si la maquina esta activa, segun el ttl obtenido por proximidad al valor 64 podriamos decir que es una maquina Linux.

      ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/biteme]
      └─# ping 10.10.81.190 -c1 
      PING 10.10.81.190 (10.10.81.190) 56(84) bytes of data.
      64 bytes from 10.10.81.190: icmp_seq=1 ttl=63 time=54.3 ms
      
      --- 10.10.81.190 ping statistics ---
      1 packets transmitted, 1 received, 0% packet loss, time 0ms
      rtt min/avg/max/mdev = 54.274/54.274/54.274/0.000 ms
  
- Reporte Nmap (Obtenemos puertos abiertos servicios y versiones que estan corriendo).

      ┌──(root㉿kali)-[/home/…/ctf/try_ctf/biteme/nmap]
      └─# nmap -p- --open --min-rate 5000 -n -Pn 10.10.81.190 -oN open_ports                                                           
      Starting Nmap 7.94 ( https://nmap.org ) at 2023-09-10 04:07 EDT
      PORT   STATE SERVICE
      22/tcp open  ssh
      80/tcp open  http
      
      ┌──(root㉿kali)-[/home/…/ctf/try_ctf/biteme/nmap]
      └─# nmap -p 22,80 -sCV 10.10.81.190 -oN info_ports
      Starting Nmap 7.94 ( https://nmap.org ) at 2023-09-10 04:09 EDT
      Nmap scan report for 10.10.81.190
      Host is up (0.055s latency).
      
      PORT   STATE SERVICE VERSION
      22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.6 (Ubuntu Linux; protocol 2.0)
      | ssh-hostkey: 
      |   2048 89:ec:67:1a:85:87:c6:f6:64:ad:a7:d1:9e:3a:11:94 (RSA)
      |   256 7f:6b:3c:f8:21:50:d9:8b:52:04:34:a5:4d:03:3a:26 (ECDSA)
      |_  256 c4:5b:e5:26:94:06:ee:76:21:75:27:bc:cd:ba:af:cc (ED25519)
      80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
      |_http-title: Apache2 Ubuntu Default Page: It works
      |_http-server-header: Apache/2.4.29 (Ubuntu)
      Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

- Segun la version del servicio SSH que esta corriendo en el puerto 22, obtenemos su launchpad y podemos decir que estamos ante una maquina.

  ![image](https://github.com/Esevka/CTF/assets/139042999/1029ca00-f307-487b-a84a-67da00f632f2)


## Analisis de vulnerabilidades en los servicios y explotacion de los mismos.

- Puerto 80,  nos carga lo siguiente y tras revisar el codigo no encontramos nada que nos pueda ayudar.

  ![image](https://github.com/Esevka/CTF/assets/139042999/cefd2d9c-d713-489e-a325-1572ef51d440)

    - Utilizamos Gobuster para fuzzear la web por fuerza bruta en busca de directorios ocultos, como vemos hemos encontrado varios directorios interesantes.
 
      

