## TryHackMe  <> Anonymous
![image](https://github.com/Esevka/CTF/assets/139042999/71a70ce7-add8-4c4a-b56f-98902b1e7395)

Enunciado Informacion : Responder a una serie de preguntas y  obtener las flags de usuario y root.

---
---

## Escaneo de puertos

-Lanzamos una traza ICMP(ping) para ver si la maquina esta activa, segun el ttl obtenido, por proximidad al valor 64 podriamos decir que es una maquina Linux.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/anonymous/nmap]
    └─# ping -c1 10.10.40.39
    PING 10.10.40.39 (10.10.40.39) 56(84) bytes of data.
    64 bytes from 10.10.40.39: icmp_seq=1 ttl=63 time=58.0 ms
    
    --- 10.10.40.39 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 57.973/57.973/57.973/0.000 ms

-Reporte Nmap (Obtenemos puertos abiertos servicios y versiones que estan corriendo).

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/anonymous/nmap]
    └─# nmap -p- --open -sS --min-rate 5000 -n -Pn 10.10.40.39 -oN open_ports
    Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-03 09:09 CEST
    Nmap scan report for 10.10.40.39
    Host is up (0.079s latency).
    Not shown: 50122 closed tcp ports (reset), 15409 filtered tcp ports (no-response)
    Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
    PORT    STATE SERVICE
    21/tcp  open  ftp
    22/tcp  open  ssh
    139/tcp open  netbios-ssn
    445/tcp open  microsoft-ds
                                                                                                                                                                                  
    ┌──(root㉿kali)-[/home/…/Desktop/ctf/anonymous/nmap]
    └─# nmap -p 21,22,139,445 -sCV 10.10.40.39 -oN info_ports                
    Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-03 09:10 CEST
    Nmap scan report for 10.10.40.39
    Host is up (0.18s latency).
    
    PORT    STATE SERVICE     VERSION
    21/tcp  open  ftp         vsftpd 2.0.8 or later
    | ftp-anon: Anonymous FTP login allowed (FTP code 230)
    |_drwxrwxrwx    2 111      113          4096 Jun 04  2020 scripts [NSE: writeable]
    | ftp-syst: 
    |   STAT: 
    | FTP server status:
    |      Connected to ::ffff:10.9.92.151
    |      Logged in as ftp
    |      TYPE: ASCII
    |      No session bandwidth limit
    |      Session timeout in seconds is 300
    |      Control connection is plain text
    |      Data connections will be plain text
    |      At session startup, client count was 3
    |      vsFTPd 3.0.3 - secure, fast, stable
    |_End of status
    22/tcp  open  ssh         OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 8bca21621c2b23fa6bc61fa813fe1c68 (RSA)
    |   256 9589a412e2e6ab905d4519ff415f74ce (ECDSA)
    |_  256 e12a96a4ea8f688fcc74b8f0287270cd (ED25519)
    139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
    445/tcp open  netbios-ssn Samba smbd 4.7.6-Ubuntu (workgroup: WORKGROUP)
    Service Info: Host: ANONYMOUS; OS: Linux; CPE: cpe:/o:linux:linux_kernel
    
    Host script results:
    | smb-security-mode: 
    |   account_used: guest
    |   authentication_level: user
    |   challenge_response: supported
    |_  message_signing: disabled (dangerous, but default)
    | smb-os-discovery: 
    |   OS: Windows 6.1 (Samba 4.7.6-Ubuntu)
    |   Computer name: anonymous
    |   NetBIOS computer name: ANONYMOUS\x00
    |   Domain name: \x00
    |   FQDN: anonymous
    |_  System time: 2023-08-03T07:10:44+00:00
    |_clock-skew: mean: 1s, deviation: 0s, median: 1s
    | smb2-security-mode: 
    |   311: 
    |_    Message signing enabled but not required
    | smb2-time: 
    |   date: 2023-08-03T07:10:44
    |_  start_date: N/A
    |_nbstat: NetBIOS name: ANONYMOUS, NetBIOS user: <unknown>, NetBIOS MAC: 000000000000 (Xerox)


-Recopilamos informacion de los puertos abiertos y sus versiones.

    21/tcp  open  ftp         vsftpd 2.0.8 or later | ftp-anon: Anonymous FTP login allowed (FTP code 230)
    
    22/tcp  open  ssh         OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)

    smb-security-mode: |   account_used: guest|   authentication_level: user
        
        139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
        
        445/tcp open  netbios-ssn Samba smbd 4.7.6-Ubuntu (workgroup: WORKGROUP)

   

## Analisis de vulnerabilidades en los servicios y explotacion de los mismos.

 -Segun el launchpad obtenido del servicio OpenSSH que esta corriendo en el puerto 22 podriamos decir que estamos delante de una maquina LINUX, aunque en el reporte Nmap hemos visto que el servicio samba esta corriento sobre OS: Windows 6.1'Windows 7' (Samba 4.7.6-Ubuntu).
 
![image](https://github.com/Esevka/CTF/assets/139042999/dc0c9e09-884e-4105-b777-b9bf20932dab)

-Puertos smb(139,445).

INFO:
    El puerto 139 se utiliza si SMB está configurado para ejecutarse en NetBIOS sobre TCP/IP. 
    El puerto 445 se utiliza si SMB se ejecuta directamente en TCP/IP, sin NetBIOS. 

Por lo que tenemos acceso a los mismos recursos utilizemos el puerto smb que utilizemos.
    
    ┌──(root㉿kali)-[/home/…/ctf/anonymous/content/smb]
    └─# smbmap -H 10.10.40.39 -u guest               
    [+] Guest session       IP: 10.10.40.39:445     Name: 10.10.40.39                                       
            Disk                                                    Permissions     Comment
            ----                                                    -----------     -------
            print$                                                  NO ACCESS       Printer Drivers
            pics                                                    READ ONLY       My SMB Share Directory for Pics
            IPC$                                                    NO ACCESS       IPC Service (anonymous server (Samba, Ubuntu))
                                                                                                                                                                                  
    ┌──(root㉿kali)-[/home/…/ctf/anonymous/content/smb]
    └─# smbmap -H 10.10.40.39 -u guest -P 139
    [+] Guest session       IP: 10.10.40.39:139     Name: 10.10.40.39                                       
            Disk                                                    Permissions     Comment
            ----                                                    -----------     -------
            print$                                                  NO ACCESS       Printer Drivers
            pics                                                    READ ONLY       My SMB Share Directory for Pics
            IPC$                                                    NO ACCESS       IPC Service (anonymous server (Samba, Ubuntu))

Vemos que tenemos permisos de lectura sobre la carpeta pics, nos conectamos y descargamos su contenido para analizar.

    ┌──(root㉿kali)-[/home/…/ctf/anonymous/content/smb]
    └─# smbclient //10.10.40.39/pics -U guest        
    Password for [WORKGROUP\guest]:
    Try "help" to get a list of possible commands.
    smb: \> dir
      .                                   D        0  Sun May 17 13:11:34 2020
      ..                                  D        0  Thu May 14 03:59:10 2020
      corgo2.jpg                          N    42663  Tue May 12 02:43:42 2020
      puppos.jpeg                         N   265188  Tue May 12 02:43:42 2020
    
    smb: \> lcd /home/kali/Desktop/ctf/anonymous/content/smb/
    smb: \> mget *
    Get file corgo2.jpg? y
    getting file \corgo2.jpg of size 42663 as corgo2.jpg (92.4 KiloBytes/sec) (average 92.4 KiloBytes/sec)
    Get file puppos.jpeg? y
    getting file \puppos.jpeg of size 265188 as puppos.jpeg (178.6 KiloBytes/sec) (average 158.1 KiloBytes/sec)

Despues de analizar las imagenes descargadas, no encontramos nada.


-Puerto 21(ftp)

Nos conectamos al servicio ftp, recordamos de la fase de escaneo de puertos ---> ftp-anon: Anonymous FTP login allowed 

    ┌──(root㉿kali)-[/home/…/ctf/anonymous/content/ftp]
    └─# ftp anonymous@10.10.40.39         
    Connected to 10.10.40.39.
    220 NamelessOne's FTP Server!
    331 Please specify the password.
    Password: 
    230 Login successful.
    Remote system type is UNIX.
    Using binary mode to transfer files.
    ftp> dir
    229 Entering Extended Passive Mode (|||38007|)
    150 Here comes the directory listing.
    drwxrwxrwx    2 111      113          4096 Jun 04  2020 scripts
    226 Directory send OK.
    ftp> cd scripts
    250 Directory successfully changed.
    ftp> dir
    229 Entering Extended Passive Mode (|||51387|)
    150 Here comes the directory listing.
    -rwxr-xrwx    1 1000     1000          314 Jun 04  2020 clean.sh
    -rw-rw-r--    1 1000     1000         3182 Aug 03 07:54 removed_files.log
    -rw-r--r--    1 1000     1000           68 May 12  2020 to_do.txt
    226 Directory send OK.

Vemos que dentro de la carpeta scripts tenemos una serie de ficheros, por lo que vamos a descargarlos para analizarlos.

    ftp> mget *
    local: clean.sh remote: clean.sh
    229 Entering Extended Passive Mode (|||60565|)
    150 Opening BINARY mode data connection for clean.sh (314 bytes).
    100% |*********************************************************************************************************************************|   314       58.94 KiB/s    00:00 ETA
    226 Transfer complete.
    314 bytes received in 00:00 (5.09 KiB/s)
    local: removed_files.log remote: removed_files.log
    229 Entering Extended Passive Mode (|||7906|)
    150 Opening BINARY mode data connection for removed_files.log (3311 bytes).
    100% |*********************************************************************************************************************************|  3311       70.16 MiB/s    00:00 ETA
    226 Transfer complete.
    3311 bytes received in 00:00 (56.94 KiB/s)
    local: to_do.txt remote: to_do.txt
    229 Entering Extended Passive Mode (|||59448|)
    150 Opening BINARY mode data connection for to_do.txt (68 bytes).
    100% |*********************************************************************************************************************************|    68      514.77 KiB/s    00:00 ETA
    226 Transfer complete.
    68 bytes received in 00:00 (1.17 KiB/s)


    
