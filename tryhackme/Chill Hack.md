## TryHackMe  <> Chill Hack

![image](https://github.com/Esevka/CTF/assets/139042999/fb2397af-1c4d-452d-ad14-f9ccaf482ef1)

Enlace Maquina: https://tryhackme.com/room/chillhack

Enunciado : 
  - Conseguir Flags(user.txt y root.txt)
    
---

## Escaneo de puertos (NMAP).

-Vemos que tras lanzar un paquete ICMP a la direccion ip de la maquina victima obtenemos un ttl=63, basandonos en el ttl podriamos decir que es una maquina ---> Linux.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/chill_hack]
    └─# ping 10.10.52.28 -c1     
    PING 10.10.52.28 (10.10.52.28) 56(84) bytes of data.
    64 bytes from 10.10.52.28: icmp_seq=1 ttl=63 time=46.3 ms
    
    --- 10.10.52.28 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 46.261/46.261/46.261/0.000 ms

-Buscamos puertos abiertos en en la maquina victima.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/chill_hack]
    └─# nmap -p- --open -sS --min-rate 5000 -n -Pn -vvv 10.10.52.28 -oN open_ports   
    
    PORT   STATE SERVICE REASON
    21/tcp open  ftp     syn-ack ttl 63
    22/tcp open  ssh     syn-ack ttl 63
    80/tcp open  http    syn-ack ttl 63

-Lanzamos scripts basicos de reconocimiento sobre los puertos abiertos.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/chill_hack]
    └─# nmap -p 21,22,80 -sCV -vvv 10.10.52.28 -oN info_ports                     
    
    PORT   STATE SERVICE REASON         VERSION
    21/tcp open  ftp     syn-ack ttl 63 vsftpd 3.0.3
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
    |      At session startup, client count was 1
    |      vsFTPd 3.0.3 - secure, fast, stable
    |_End of status
    | ftp-anon: Anonymous FTP login allowed (FTP code 230)
    |_-rw-r--r--    1 1001     1001           90 Oct 03  2020 note.txt
    
    22/tcp open  ssh     syn-ack ttl 63 OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 09:f9:5d:b9:18:d0:b2:3a:82:2d:6e:76:8c:c2:01:44 (RSA)
    | ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDcxgJ3GDCJNTr2pG/lKpGexQ+zhCKUcUL0hjhsy6TLZsUE89P0ZmOoQrLQojvJD0RpfkUkDfd7ut4//Q0Gqzhbiak3AIOqEHVBIVcoINja1TIVq2v3mB6K2f+sZZXgYcpSQriwN+mKgIfrKYyoG7iLWZs92jsUEZVj7sHteOq9UNnyRN4+4FvDhI/8QoOQ19IMszrbpxQV3GQK44xyb9Fhf/Enzz6cSC4D9DHx+/Y1Ky+AFf0A9EIHk+FhU0nuxBdA3ceSTyu8ohV/ltE2SalQXROO70LMoCd5CQDx4o1JGYzny2SHWdKsOUUAkxkEIeEVXqa2pehJwqs0IEuC04sv
    |   256 1b:cf:3a:49:8b:1b:20:b0:2c:6a:a5:51:a8:8f:1e:62 (ECDSA)
    | ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBFetPKgbta+pfgqdGTnzyD76mw/9vbSq3DqgpxPVGYlTKc5MI9PmPtkZ8SmvNvtoOp0uzqsfe71S47TXIIiQNxQ=
    |   256 30:05:cc:52:c6:6f:65:04:86:0f:72:41:c8:a4:39:cf (ED25519)
    |_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKHq62Lw0h1xzNV41zO3BsfpOiBI3uy0XHtt6TOMHBhZ
    
    80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.29 ((Ubuntu))
    |_http-server-header: Apache/2.4.29 (Ubuntu)
    |_http-title: Game Info
    | http-methods: 
    |_  Supported Methods: POST OPTIONS HEAD GET
    |_http-favicon: Unknown favicon MD5: 7EEEA719D1DF55D478C68D9886707F17
    Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
    
-Segun el lauchpad del servicio OpenSSH que tenemos corriendo en el puerto 22.

![image](https://github.com/Esevka/CTF/assets/139042999/3da26bee-0bb5-4c52-950e-549db8d0f555)


## Analizamos la informacion obtenida.

--Puerto 21(ftp), permite el acceso anonimo.

  - Obtenemos toda la info del servidor ftp.

        ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/chill_hack]
        └─# ftp anonymous@10.10.52.28  
        ftp> ls
        229 Entering Extended Passive Mode (|||29161|)
        150 Here comes the directory listing.
        -rw-r--r--    1 1001     1001           90 Oct 03  2020 note.txt
        226 Directory send OK.
        ftp> get note.txt
        local: note.txt remote: note.txt
        229 Entering Extended Passive Mode (|||58849|)
        150 Opening BINARY mode data connection for note.txt (90 bytes).
        100% |******************************************************************************************************************|    90       79.90 KiB/s    00:00 ETA
        226 Transfer complete.
        90 bytes received in 00:00 (1.77 KiB/s)

  - note.txt parece ser una pista que aun no entiendo su significado.

        ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/chill_hack]
        └─# cat note.txt       
        Anurodh told me that there is some filtering on strings being put in the command -- Apaar

--Puerto 80(http)

  - Cargamos la web pero no encontramos nada que nos interese.

  - Realizamos Fuzzing web en busca de directorios.

        ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/chill_hack]
        └─# gobuster dir -u http://10.10.52.28 -w /usr/share/wordlists/dirb/common.txt -o fuzz
    
        Gobuster v3.6
        by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
        ===============================================================
        /.hta                 (Status: 403) [Size: 276]
        /.htaccess            (Status: 403) [Size: 276]
        /.htpasswd            (Status: 403) [Size: 276]
        /css                  (Status: 301) [Size: 308] [--> http://10.10.52.28/css/]
        /fonts                (Status: 301) [Size: 310] [--> http://10.10.52.28/fonts/]
        /images               (Status: 301) [Size: 311] [--> http://10.10.52.28/images/]
        /index.html           (Status: 200) [Size: 35184]
        /js                   (Status: 301) [Size: 307] [--> http://10.10.52.28/js/]
        /secret               (Status: 301) [Size: 311] [--> http://10.10.52.28/secret/] ---> Directorio Interesante
        /server-status        (Status: 403) [Size: 276]
        ===============================================================
        Finished

  - Cargamos el directorio http://10.10.52.28/secret/

    

    



    

