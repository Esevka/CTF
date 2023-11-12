## TryHackMe  <> Overpass

![image](https://github.com/Esevka/CTF/assets/139042999/262f5142-59aa-4483-b9ba-6034c32a93a6)

Enlace Maquina: https://tryhackme.com/room/overpass

Enunciado : 

  - Conseguir Flags(user.txt y root.txt)
  - BONUS --> Conseguir codigo de subscripcion.
---

## Escaneo de puertos (NMAP).

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

## Analizamos la informacion obtenida.

-

