## TryHackMe  <> Overpass

![image](https://github.com/Esevka/CTF/assets/139042999/262f5142-59aa-4483-b9ba-6034c32a93a6)

Enlace Maquina: https://tryhackme.com/room/overpass

Enunciado : 

  - Conseguir Flags(user.txt y root.txt)
  - BONUS --> Conseguir codigo de subscripcion.
---

## Escaneo de puertos (NMAP).

-Segun el ttl obtenito a la hora de lanzar un ping a la maquina victima podriamos decir que es una maquina ---> Linux.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/overpass/nmap]
    └─# ping 10.10.181.35 -c1
    PING 10.10.181.35 (10.10.181.35) 56(84) bytes of data.
    64 bytes from 10.10.181.35: icmp_seq=1 ttl=63 time=582 ms
    
    --- 10.10.181.35 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 581.984/581.984/581.984/0.000 ms

-Buscamos puertos abiertos en en la maquina victima.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/overpass/nmap]
    └─# nmap -p- --open -sS --min-rate 5000 -n -Pn 10.10.181.35 -oN open_ports
    Starting Nmap 7.94 ( https://nmap.org ) at 2023-11-12 11:29 CET

    PORT   STATE SERVICE
    22/tcp open  ssh
    80/tcp open  http

-Lanzamos scripts basicos de reconocimiento sobre los puertos abiertos.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/overpass/nmap]
    └─# nmap -p 22,80 -sCV -n -Pn 10.10.181.35 -oN info_ports
    Starting Nmap 7.94 ( https://nmap.org ) at 2023-11-12 11:35 CET
    
    PORT   STATE SERVICE VERSION
    22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 37:96:85:98:d1:00:9c:14:63:d9:b0:34:75:b1:f9:57 (RSA)
    |   256 53:75:fa:c0:65:da:dd:b1:e8:dd:40:b8:f6:82:39:24 (ECDSA)
    |_  256 1c:4a:da:1f:36:54:6d:a6:c6:17:00:27:2e:67:75:9c (ED25519)
    
    80/tcp open  http    Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
    |_http-title: Overpass
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

-Segun el lauchpad del servicio OpenSSH que tenemos corriendo en el puerto 22.

  ![image](https://github.com/Esevka/CTF/assets/139042999/1bf3f6e8-0dbc-4f89-a3e3-d9f95bca992b)


## Analizamos la informacion obtenida.

-Por el momento tenemos:

  - Maquina Linux (Ubuntu Bionic 18.04)
  - Puertos 80(Http) y 22 (SSH)

-Puerto 80.

  - Web titulada Overpass
  
    ![image](https://github.com/Esevka/CTF/assets/139042999/5a258f78-d81a-4cac-959e-930ed30e9ece)

  - En el apartado --> About Us, encontramos posibles usuarios.

    ![image](https://github.com/Esevka/CTF/assets/139042999/2e11e1f2-9212-4358-98cf-3ca15bfc95fa)

  - En el apartado --> Downloads, encontramos la app para diferentes sistemas y el codigo original de la app.

    ![image](https://github.com/Esevka/CTF/assets/139042999/88593c8d-3509-4b30-9414-4a2921f7afc8)

  - Fuzzeamos la web en busqueda de directorios con la ayuda de --> Gobuster.

        ┌──(root㉿kali)-[/home/…/ctf/try_ctf/overpass/files]
        └─# gobuster dir -u http://10.10.181.35/ -w /usr/share/wordlists/dirb/common.txt -o fuzz
        ===============================================================
        Gobuster v3.6
        by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
        ===============================================================
        /aboutus              (Status: 301) [Size: 0] [--> aboutus/]
        /admin                (Status: 301) [Size: 42] [--> /admin/]  ---> directorio que nos interesa.
        /css                  (Status: 301) [Size: 0] [--> css/]
        /downloads            (Status: 301) [Size: 0] [--> downloads/]
        /img                  (Status: 301) [Size: 0] [--> img/]
        /index.html           (Status: 301) [Size: 0] [--> ./]

  - Cargamos el directorio y encontramos un panel de login.

    ![image](https://github.com/Esevka/CTF/assets/139042999/28d69fc5-7f5a-42e1-a34a-82551fd94329)

    - Vamos a analizar el codigo web del panel de login, en busca de algun fallo.
   
      ![image](https://github.com/Esevka/CTF/assets/139042999/fd4e81fe-14c3-4ce3-8665-adb8fd007602)

    - Creamos una cookie para ver si podemos saltarnos el panel de login y recargamos la web. Bingo obtenemos una private key.
   
      ![image](https://github.com/Esevka/CTF/assets/139042999/3c07e9ad-3796-46e9-99a3-d1dc1b07ee93)



      





    

  

