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



