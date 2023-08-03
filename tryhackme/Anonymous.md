## TryHackMe  <> Anonymous
![image](https://github.com/Esevka/CTF/assets/139042999/5e26ad71-c251-438b-ba43-7eed13496eaf)

Enunciado Informacion :Responder a una serie de preguntas y  obtener las flags de usuario y root.

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

    

![image](https://github.com/Esevka/CTF/assets/139042999/dc0c9e09-884e-4105-b777-b9bf20932dab)
