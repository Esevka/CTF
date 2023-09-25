## TryHackMe  <> Year of the Owl

![image](https://github.com/Esevka/CTF/assets/139042999/019512fc-ca13-4343-a942-7a7325593e6f)

Enlace Maquina: https://tryhackme.com/room/yearoftheowl

Enunciado : 

  - Consejo: When the labyrinth is before you and you lose your way, sometimes thinking outside the walls is the way forward.
  - Conseguir Flags.

## Escaneo de puertos

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/year_ofthe_owl/nmap]
    └─# nmap -p- --open -sS --min-rate 5000 -n -Pn 10.10.42.63 -oN open_ports              
    Starting Nmap 7.94 ( https://nmap.org ) at 2023-09-25 13:24 CEST

    PORT      STATE SERVICE
    80/tcp    open  http
    139/tcp   open  netbios-ssn
    443/tcp   open  https
    445/tcp   open  microsoft-ds
    3306/tcp  open  mysql
    3389/tcp  open  ms-wbt-server
    5985/tcp  open  wsman
    47001/tcp open  winrm

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/year_ofthe_owl/nmap]
    └─# nmap -p 80,139,443,445,3306,3389,5985,47001 -sCV --min-rate 5000 -n -Pn 10.10.42.63 -oN info_ports
    Starting Nmap 7.94 ( https://nmap.org ) at 2023-09-25 13:29 CEST
    
    PORT      STATE SERVICE       VERSION
    80/tcp    open  http          Apache httpd 2.4.46 ((Win64) OpenSSL/1.1.1g PHP/7.4.10)
    |_http-title: Year of the Owl
    |_http-server-header: Apache/2.4.46 (Win64) OpenSSL/1.1.1g PHP/7.4.10
    
    139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
    
    443/tcp   open  ssl/http      Apache httpd 2.4.46 ((Win64) OpenSSL/1.1.1g PHP/7.4.10)
    |_http-title: Year of the Owl
    | tls-alpn: 
    |_  http/1.1
    |_http-server-header: Apache/2.4.46 (Win64) OpenSSL/1.1.1g PHP/7.4.10
    | ssl-cert: Subject: commonName=localhost
    | Not valid before: 2009-11-10T23:48:47
    |_Not valid after:  2019-11-08T23:48:47
    |_ssl-date: TLS randomness does not represent time
    
    445/tcp   open  microsoft-ds?
    
    3306/tcp  open  mysql?
    | fingerprint-strings: 
    |   NULL: 
    |_    Host 'ip-10-8-64-232.eu-west-1.compute.internal' is not allowed to connect to this MariaDB server
    
    3389/tcp  open  ms-wbt-server Microsoft Terminal Services
    |_ssl-date: 2023-09-25T11:30:44+00:00; -1s from scanner time.
    | ssl-cert: Subject: commonName=year-of-the-owl
    | Not valid before: 2023-09-24T08:51:09
    |_Not valid after:  2024-03-25T08:51:09
    | rdp-ntlm-info: 
    |   Target_Name: YEAR-OF-THE-OWL
    |   NetBIOS_Domain_Name: YEAR-OF-THE-OWL
    |   NetBIOS_Computer_Name: YEAR-OF-THE-OWL
    |   DNS_Domain_Name: year-of-the-owl
    |   DNS_Computer_Name: year-of-the-owl
    |   Product_Version: 10.0.17763
    |_  System_Time: 2023-09-25T11:30:04+00:00
    
    5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
    |_http-server-header: Microsoft-HTTPAPI/2.0
    |_http-title: Not Found
    
    47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
    |_http-title: Not Found
    |_http-server-header: Microsoft-HTTPAPI/2.0
    1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
    SF-Port3306-TCP:V=7.94%I=7%D=9/25%Time=65116F30%P=x86_64-pc-linux-gnu%r(NU
    SF:LL,68,"d\0\0\x01\xffj\x04Host\x20'ip-10-8-64-232\.eu-west-1\.compute\.i
    SF:nternal'\x20is\x20not\x20allowed\x20to\x20connect\x20to\x20this\x20Mari
    SF:aDB\x20server");
    Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
    
    Host script results:
    | smb2-time: 
    |   date: 2023-09-25T11:30:05
    |_  start_date: N/A
    | smb2-security-mode: 
    |   3:1:1: 
    |_    Message signing enabled but not required
    |_clock-skew: mean: -1s, deviation: 0s, median: -1s
    

-Despues de unas cuantas horas buscando por los servicios activos de la maquina no encontramos ningun punto de entrada.

    RECOPILACION:   
        WEB
        80,443 ----> No encontramos nada de valor 
        
        SMB
        139,445 ---> No tenemos credenciales 
        
        MySQL
        3306 ----> No tenemos credenciales (is not allowed to connect to this MariaDB server)
        
        TerminalService
        3389 ----->No tenemos credenciales  
        
        WinRM
        5985,47001 --->No tenemos credenciales  

-El tip que da el enunciado, me hizo recordar que por defecto siempre escanemos los puertos en TCP(EL protocolo TCP no es el unico), por lo que me dio por mirar en UDP.

  
        
  
    

## Analisis de vulnerabilidades en los servicios y explotacion de los mismos.

  



    


