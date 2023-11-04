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

-Anadimos ironcorp.me a nuestro fichero /etc/hosts como nos dice el enunciado.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/iron_corp/nmap]
    └─# cat /etc/hosts                                                   
    127.0.0.1       localhost
    127.0.1.1       kali
    10.10.27.190    ironcorp.me

--Tenemos dos puertos en los que estan corriendo servicios http (8080,11025)

  - Puerto (8080)
    
    Encontramos que tenemos corriendo -> Dashtreme Admin
    Tras analizar la web, realizar fuzzing con gobuster y buscar la existencia de algun exploit no encontramos nada interesante.

    ![image](https://github.com/Esevka/CTF/assets/139042999/4bf944e5-caa8-41fa-8366-3f837007bf64)

  - Puerto (11025)

    Encontramos una web en construccion, indica que proximamente estara disponible poco mas.
    Tras analizar la web, realizar fuzzing con gobuster y buscar algo que nos pueda ayudar no encontramos nada.

    ![image](https://github.com/Esevka/CTF/assets/139042999/2e1c09c9-6b98-4db8-a81b-47698bb6ec8b)


--LLegados a este punto podriamos mirar la existencia de subdominios, el enuncionado hace incapie en que nuestro /etc/hosts contenga la resolucion al nombre de host -> ironcorp.me

  - Obtencion de subdominios mediante fuerza bruta con wfuzz.

    - Lanzamos el comando al puerto 8080, no tenemos resultados.
    
    - Sin embargo lanzamos el mismo comando al puerto 11025 y obtenemos dos posibles subdominios.

          ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/iron_corp]
          └─# wfuzz -u http://ironcorp.me:11025 -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -H "HOST: FUZZ.ironcorp.me" --hw 199 
          
          ********************************************************
          * Wfuzz 3.1.0 - The Web Fuzzer                         *
          ********************************************************
          
          Target: http://ironcorp.me:11025/
          Total requests: 4989
          =====================================================================
          ID           Response   Lines    Word       Chars       Payload                                                                     
          =====================================================================
          000000024:   401        47 L     132 W      1305 Ch     "admin - admin"                                                             
          000000387:   403        42 L     98 W       1086 Ch     "internal - internal"                                                       

  - Obtencion de subdominios mediante transferencia de zona DNS.

    Puerto 53(open) domain Simple DNS Plus (La maquina tiene un servidor DNS Corriendo)

        QUE ES AXFR?
    
        El comando "dig axfr" se utiliza para realizar una transferencia de zona (Zone Transfer) desde un servidor DNS.
        La transferencia de zona es un proceso mediante el cual un servidor DNS obtiene una copia completa de la base de datos de zona de otro servidor DNS.
        Esto puede ser útil para mantener copias de seguridad de la configuración de zona de un dominio o para replicar la información de zona entre servidores DNS autorizados.
    
        En resumen, el comando "dig axfr @<DNS_IP> <DOMAIN>" se utiliza para solicitar una transferencia de zona completa desde un servidor DNS específico para un dominio dado.
        Es importante tener en cuenta que no todos los servidores DNS permiten transferencias de zona a cualquier persona;
        generalmente, solo los servidores autorizados para el dominio en cuestión permitirán esta operación por razones de seguridad.

    Probamos a realizar una transferencia de zona y obtenemos los dos mismos subdominios que mediante fuerza bruta, estos apuntan al localhost de la maquina victima. 

        ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/iron_corp]
        └─# dig axfr @10.10.125.93 ironcorp.me
        
        ; <<>> DiG 9.18.16-1-Debian <<>> axfr @10.10.125.93 ironcorp.me
        ; (1 server found)
        ;; global options: +cmd
        ironcorp.me.            3600    IN      SOA     win-8vmbkf3g815. hostmaster. 3 900 600 86400 3600
        ironcorp.me.            3600    IN      NS      win-8vmbkf3g815.
        admin.ironcorp.me.      3600    IN      A       127.0.0.1
        internal.ironcorp.me.   3600    IN      A       127.0.0.1
        ironcorp.me.            3600    IN      SOA     win-8vmbkf3g815. hostmaster. 3 900 600 86400 3600
        ;; Query time: 67 msec
        ;; SERVER: 10.10.125.93#53(10.10.125.93) (TCP)
        ;; WHEN: Sat Nov 04 07:47:36 CET 2023
        ;; XFR size: 5 records (messages 1, bytes 238)


## Analizamos los subdominios encontrados.

--Por el momento tenemos:

    Dominio ------> ironcorp.me 
    Subdominios --> admin.ironcorp.me -- internal.ironcorp.me

  Anadimos los subdominios encontrados a nuestro fichero /etc/hosts

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/iron_corp]
    └─# cat /etc/hosts
    10.10.125.93    ironcorp.me admin.ironcorp.me internal.ironcorp.me


--Vamos a ver que continen estos subdominios.

  - Cargamos los subdominios en el puerto 80, no conseguimos nada.

  - Cargamos el subdominio internal.ironcorp.me
    
      - Puerto 8080 ---> Muestra el panel Dashtreme Admin , nada interesante lo mismo.
        
      - Puerto 11025 --> Muestra un  Access forbidden! Error 403
    
  - Cargamos el subdominio admin.ironcorp.me
    
      - Puerto 8080 ---> Muestra el panel Dashtreme Admin , nada interesante lo mismo.
        
      - Puerto 11025 --> Muestra un panel de autenticacion basica
        
        ![image](https://github.com/Esevka/CTF/assets/139042999/22d2d26b-7248-446d-b002-ca1071e8786d)

        Info: Como Funciona la autenticacion Basica en Apache.

        https://www.zeppelinux.es/autenticacion-basic-en-apache/#google_vignette




    







