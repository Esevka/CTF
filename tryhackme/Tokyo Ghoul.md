## TryHackMe  <> Tokyo Ghoul

![image](https://github.com/Esevka/CTF/assets/139042999/b706d750-92f7-4cd7-b710-fcc39daf11da)

Enlace Maquina: https://tryhackme.com/room/tokyoghoul666

Enunciado :
  - Conseguir Flags(user.txt y root.txt)
---

## Escaneo de puertos (NMAP).

-Segun el ttl obtenito (63) despues de lanzar un paquete ICMP a la maquina victima podriamos decir que es una maquina ---> Linux.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/tokyo_ghoul]
    └─# ping 10.10.44.28 -c1
    PING 10.10.44.28 (10.10.44.28) 56(84) bytes of data.
    64 bytes from 10.10.44.28: icmp_seq=1 ttl=63 time=154 ms
    
    --- 10.10.44.28 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 154.442/154.442/154.442/0.000 ms

-Buscamos puertos abiertos en en la maquina victima.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/tokyo_ghoul/nmap]
    └─# nmap -p- --open -sS --min-rate 5000 -n -Pn -vvv 10.10.44.28 -oN open_ports 
    Starting Nmap 7.94 ( https://nmap.org ) at 2023-11-29 18:47 CET
    Initiating SYN Stealth Scan at 18:47
    
    PORT   STATE SERVICE REASON
    21/tcp open  ftp     syn-ack ttl 63
    22/tcp open  ssh     syn-ack ttl 63
    80/tcp open  http    syn-ack ttl 63

-Lanzamos scripts basicos de reconocimiento sobre los puertos abiertos.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/tokyo_ghoul/nmap]
    └─# nmap -p 21,22,80 -sCV -vvv 10.10.44.28 -oN info_ports                     
    Starting Nmap 7.94 ( https://nmap.org ) at 2023-11-29 18:49 CET
    
    PORT   STATE SERVICE REASON         VERSION
    21/tcp open  ftp     syn-ack ttl 63 vsftpd 3.0.3
    | ftp-anon: Anonymous FTP login allowed (FTP code 230)
    |_drwxr-xr-x    3 ftp      ftp          4096 Jan 23  2021 need_Help?
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
    |      At session startup, client count was 4
    |      vsFTPd 3.0.3 - secure, fast, stable
    |_End of status
    
    22/tcp open  ssh     syn-ack ttl 63 OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 fa:9e:38:d3:95:df:55:ea:14:c9:49:d8:0a:61:db:5e (RSA)
    | ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCeIXT46ZiVmp8Es0cKk8YkMs3kwCdmC2Ve/0A0F7aKUIOlbyLc9FkbTEGSrE69obV3u6VywjxZX6VWQoJRHLooPmZCHkYGjW+y5kfEoyeu7pqZr7oA8xgSRf+gsEETWqPnSwjTznFaZ0T1X0KfIgCidrr9pWC0c2AxC1zxNPz9p13NJH5n4RUSYCMOm2xSIwUr6ySL3v/jijwEKIMnwJHbEOmxhGrzaAXgAJeGkXUA0fU1mTVLlSwOClKOBTTo+FGcJdrFf65XenUVLaqaQGytKxR2qiCkr7bbTaWV0F8jPtVD4zOXLy2rGoozMU7jAukQu6uaDxpE7BiybhV3Ac1x
    |   256 ad:b7:a7:5e:36:cb:32:a0:90:90:8e:0b:98:30:8a:97 (ECDSA)
    | ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBC5o77nOh7/3HUQAxhtNqHX7LGDtYoVZ0au6UJzFVsAEJ644PyU2/pALbapZwFEQI3AUZ5JxjylwKzf1m+G5OJM=
    |   256 a2:a2:c8:14:96:c5:20:68:85:e5:41:d0:aa:53:8b:bd (ED25519)
    |_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOJwYjN/qiwrS4es9m/LgWitFMA0f6AJMTi8aHkYj7vE
    
    80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.18 ((Ubuntu))
    |_http-title: Welcome To Tokyo goul
    |_http-server-header: Apache/2.4.18 (Ubuntu)
    | http-methods: 
    |_  Supported Methods: OPTIONS GET HEAD POST
    Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

  -Segun el lauchpad del servicio OpenSSH que tenemos corriendo en el puerto 22.

  ![image](https://github.com/Esevka/CTF/assets/139042999/a0580abd-fc9c-420f-a883-c551f36a86e9)
  

## Analizamos la informacion obtenida.

--Puerto 21(ftp)



