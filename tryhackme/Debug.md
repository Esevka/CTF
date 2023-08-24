![image](https://github.com/Esevka/CTF/assets/139042999/1b6dac48-d25b-40cb-9e01-a8541e425b16)

## TryHackMe  <> Debug

![image](https://github.com/Esevka/CTF/assets/139042999/0e76fc7e-29b5-4463-91c8-9e8f6285f71e)

Enlace Maquina: https://tryhackme.com/room/debug

Enunciado : 
  - The main idea of this room is to make you learn more about php deserialization!
  - Obtener flag

## Escaneo de puertos

- Lanzamos una traza ICMP(ping) para ver si la maquina esta activa, segun el ttl obtenido por proximidad al valor 64 podriamos decir que es una maquina Linux.

      ┌──(root㉿kali)-[/home/…/Desktop/ctf/debug/nmap]
      └─# ping -c1 10.10.5.207 
      PING 10.10.5.207 (10.10.5.207) 56(84) bytes of data.
      64 bytes from 10.10.5.207: icmp_seq=1 ttl=63 time=67.4 ms
      
      --- 10.10.5.207 ping statistics ---
      1 packets transmitted, 1 received, 0% packet loss, time 0ms
      rtt min/avg/max/mdev = 67.421/67.421/67.421/0.000 m

- Reporte Nmap (Obtenemos puertos abiertos servicios y versiones que estan corriendo).

      ┌──(root㉿kali)-[/home/…/Desktop/ctf/debug/nmap]
      └─# nmap -p- --open --min-rate 5000 -n -Pn -vvv 10.10.5.207 -oN open_ports 
      Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-24 15:43 CEST
      Initiating SYN Stealth Scan at 15:43
  
      PORT   STATE SERVICE REASON
      22/tcp open  ssh     syn-ack ttl 63
      80/tcp open  http    syn-ack ttl 63
      
      ┌──(root㉿kali)-[/home/…/Desktop/ctf/debug/nmap]
      └─# nmap -p 22,80 -sCV 10.10.5.207 -v -oN info_ports
      Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-24 15:45 CEST
      
      PORT   STATE SERVICE VERSION
      22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
      | ssh-hostkey: 
      |   2048 44ee1eba072a5469ff11e349d7dba901 (RSA)
      |   256 8b2a8fd8409533d5fa7a406a7f29e403 (ECDSA)
      |_  256 6559e4402ac2d70577b3af60dacdfc67 (ED25519)
  
      80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
      |_http-server-header: Apache/2.4.18 (Ubuntu)
      | http-methods: 
      |_  Supported Methods: GET HEAD POST OPTIONS
      |_http-title: Apache2 Ubuntu Default Page: It works
      Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

- Segun la version del servicio SSH que esta corriendo en el puerto 22, obtenemos su launchpad y podemos decir que estamos ante una maquina.

    ![image](https://github.com/Esevka/CTF/assets/139042999/a9663e95-1dde-4f20-9d53-54921d85b725)


## Analisis de vulnerabilidades en los servicios y explotacion de los mismos.

- Puerto 80,  nos carga lo siguiente y tras revisar el codigo no encontramos nada que nos pueda ayudar.

    ![image](https://github.com/Esevka/CTF/assets/139042999/19769df1-30d9-472b-8e34-470ea7a6db9c)

  - Utilizamos Gobuster para fuzzear la web por fuerza bruta en busca de directorios ocultos, como vemos hemos encontrado varios directorios interesantes.
 
        ┌──(root㉿kali)-[/home/…/Desktop/ctf/debug/nmap]
        └─# gobuster dir -u http://10.10.5.207 -w /usr/share/wordlists/dirb/common.txt -o fuzz
        ===============================================================
        Gobuster v3.5
        by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
        ===============================================================
        /.hta                 (Status: 403) [Size: 276]
        /.htaccess            (Status: 403) [Size: 276]
        /.htpasswd            (Status: 403) [Size: 276]
        /backup               (Status: 301) [Size: 311] [--> http://10.10.5.207/backup/]
        /grid                 (Status: 301) [Size: 309] [--> http://10.10.5.207/grid/]
        /index.php            (Status: 200) [Size: 5732]
        /index.html           (Status: 200) [Size: 11321]
        /javascripts          (Status: 301) [Size: 316] [--> http://10.10.5.207/javascripts/]
        /javascript           (Status: 301) [Size: 315] [--> http://10.10.5.207/javascript/]
        /server-status        (Status: 403) [Size: 276]
        Progress: 4607 / 4615 (99.83%)
        ===============================================================
        2023/08/24 15:55:34 Finished
        ===============================================================

    Despues de analizar todo vemos que lo interesante esta en:
    
        --> index.php (fichero con una funcion php que podemos explotar para conseguir un RCE)
    
        --> http://10.10.5.207/backup/index.php.bak (fichero copia de index.php, a traves de este fichero hemos estudiado el codigo de index.php)

    Nos descargamos el fichero index.php.bak

        ┌──(root㉿kali)-[/home/…/Desktop/ctf/debug/content]
        └─# curl http://10.10.5.207/backup/index.php.bak -o index.php 
          % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                         Dload  Upload   Total   Spent    Left  Speed
        100  6399  100  6399    0     0  36317      0 --:--:-- --:--:-- --:--:-- 36357

  - Analizamos el codigo php y lo explotamos

    


    
    
