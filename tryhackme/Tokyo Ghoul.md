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

  - Anonymous FTP login allowed, nos descargamos todo el contenido interesante del ftp.

        ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/tokyo_ghoul]
        └─# ftp anonymous@10.10.44.28 -i
        Connected to 10.10.44.28.
        220 (vsFTPd 3.0.3)
        230 Login successful.
        Remote system type is UNIX.
        Using binary mode to transfer files.
        ftp> ls
        229 Entering Extended Passive Mode (|||44814|)
        150 Here comes the directory listing.
        drwxr-xr-x    3 ftp      ftp          4096 Jan 23  2021 need_Help?
        226 Directory send OK.
        ftp> cd need_Help?
        250 Directory successfully changed.
        ftp> ls -la
        229 Entering Extended Passive Mode (|||42985|)
        150 Here comes the directory listing.
        drwxr-xr-x    3 ftp      ftp          4096 Jan 23  2021 .
        drwxr-xr-x    3 ftp      ftp          4096 Jan 23  2021 ..
        -rw-r--r--    1 ftp      ftp           480 Jan 23  2021 Aogiri_tree.txt
        drwxr-xr-x    2 ftp      ftp          4096 Jan 23  2021 Talk_with_me
        ftp> mget Aogiri_tree.txt
        local: Aogiri_tree.txt remote: Aogiri_tree.txt
        229 Entering Extended Passive Mode (|||44571|)
        150 Opening BINARY mode data connection for Aogiri_tree.txt (480 bytes).
        100% |************************************************************************************|   480        8.80 MiB/s    00:00 ETA
        226 Transfer complete.
        480 bytes received in 00:00 (8.65 KiB/s)
        ftp> cd Talk_with_me
        250 Directory successfully changed.
        ftp> ls -la
        229 Entering Extended Passive Mode (|||40631|)
        150 Here comes the directory listing.
        drwxr-xr-x    2 ftp      ftp          4096 Jan 23  2021 .
        drwxr-xr-x    3 ftp      ftp          4096 Jan 23  2021 ..
        -rwxr-xr-x    1 ftp      ftp         17488 Jan 23  2021 need_to_talk
        -rw-r--r--    1 ftp      ftp         46674 Jan 23  2021 rize_and_kaneki.jpg
        226 Directory send OK.
        ftp> mget *
        local: need_to_talk remote: need_to_talk
        229 Entering Extended Passive Mode (|||42016|)
        150 Opening BINARY mode data connection for need_to_talk (17488 bytes).
        100% |************************************************************************************| 17488       66.68 KiB/s    00:00 ETA
        226 Transfer complete.
        17488 bytes received in 00:00 (55.09 KiB/s)
        local: rize_and_kaneki.jpg remote: rize_and_kaneki.jpg
        229 Entering Extended Passive Mode (|||48594|)
        150 Opening BINARY mode data connection for rize_and_kaneki.jpg (46674 bytes).
        100% |************************************************************************************| 46674      109.29 KiB/s    00:00 ETA
        226 Transfer complete.
        46674 bytes received in 00:00 (96.90 KiB/s)
        ftp> exit
        221 Goodbye.
    
  - Analizamos todo lo encontrado en el ftp
      
        ┌──(root㉿kali)-[/home/…/try_ctf/tokyo_ghoul/contenido/ftp]
        └─# ls -la
        total 80
        drwxr-xr-x 2 root root  4096 Nov 29 19:01 .
        drwxr-xr-x 3 root root  4096 Nov 29 18:59 ..
        -rw-r--r-- 1 root root   480 Jan 23  2021 Aogiri_tree.txt
        -rw-r--r-- 1 root root 17488 Jan 23  2021 need_to_talk
        -rw-r--r-- 1 root root 46674 Jan 23  2021 rize_and_kaneki.jpg

      - Aogiri_tree.txt --> nada interesante.
        
      - need_to_talk(es un fichero ELF 64-bits).
   
        1) Damos permiso para poder ejecutarlo.
               
                ┌──(root㉿kali)-[/home/…/try_ctf/tokyo_ghoul/contenido/ftp]
                └─# chmod +x need_to_talk
        
        2) Ejecutamos

                ┌──(root㉿kali)-[/home/…/try_ctf/tokyo_ghoul/contenido/ftp]
                └─# ./need_to_talk 
                Hey Kaneki finnaly you want to talk 
                Unfortunately before I can give you the kagune you need to give me the paraphrase
                Do you have what I'm looking for?
                
                > exit
                Hmm. I don't think this is what I was looking for.
                Take a look inside of me. rabin2 -z

            - Hacemos uso del comando 'strings' para obtener todas las cadenas de string del binario.
              
                  ┌──(root㉿kali)-[/home/…/try_ctf/tokyo_ghoul/contenido/ftp]
                  └─# strings need_to_talk 
              ![image](https://github.com/Esevka/CTF/assets/139042999/e0e8467f-9c8c-4c05-bd8c-9807de2bc0fa)

              Volvemos a ejecutar y bingo obtenemos un string que por el momento no sabemos para que es.

                  ┌──(root㉿kali)-[/home/…/try_ctf/tokyo_ghoul/contenido/ftp]
                  └─# ./need_to_talk 
                  Hey Kaneki finnaly you want to talk 
                  Unfortunately before I can give you the kagune you need to give me the paraphrase
                  Do you have what I'm looking for?
                  
                  > kamishiro
                  Good job. I believe this is what you came for:
                  You_found_1t
              
        3) 






