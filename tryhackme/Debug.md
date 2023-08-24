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

    Despues de analizar todo vemos que lo interesante esta en:
    
        --> index.php (fichero con una funcion php que podemos explotar para conseguir un RCE)
    
        --> http://10.10.5.207/backup/index.php.bak (fichero copia de index.php, a traves de este fichero hemos estudiado el codigo de index.php)

    Fichero index.php, contiene un formulario con un boton submit que es el encargado de ejecutar el codigo php vulnerable de la pagina.
    
      ![image](https://github.com/Esevka/CTF/assets/139042999/160fec18-0919-48b4-b03a-74db2218c860)
      ![image](https://github.com/Esevka/CTF/assets/139042999/936e8029-4dee-4392-b4a0-38bfa9727e00)- 

    Nos descargamos el fichero index.php.bak

        ┌──(root㉿kali)-[/home/…/Desktop/ctf/debug/content]
        └─# curl http://10.10.5.207/backup/index.php.bak -o index.php 
          % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                         Dload  Upload   Total   Spent    Left  Speed
        100  6399  100  6399    0     0  36317      0 --:--:-- --:--:-- --:--:-- 36357


  - Analizamos el codigo php y lo explotamos

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
                                              en la funcion SaveMessage() y __destruct(Esto es un magic method de php)

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
        
      ---Explotacion del codigo:
    
      - Serialización de objetos            --> https://www.php.net/manual/es/language.oop5.serialization.php
        
      - Deserialización de objetos          --> https://www.php.net/manual/es/function.unserialize.php
        
      - Magic Method __destruct() en php       --> https://www.w3schools.com/php/php_oop_destructor.asp
  
          ![image](https://github.com/Esevka/CTF/assets/139042999/ff8dfb2d-e516-4eb9-8fcd-1899fbd6dfda)

      - Unserialize to RCE ---> https://notsosecure.com/remote-code-execution-php-unserialize

      - EXPLICACION,espero que se entienda--

            Funcion unserialize(), le debemos pasar un string(serializado) que contenga una clase llamada 'FormSubmit' con las variables
            $form_file y $message con unos valores especificos.
    
            Lo que intentamos es crear mediante la funcion unserialize() otra instancia en memoria de la clase 'FormSubmit', por lo que tendriamos la instancia creada con unserialize() y la
            creada de manera regular en el codigo.
        
            Php las tratara como dos instancias independiente de una misma clase con propiedades(valores de variables) diferentes, al ser la misma clase el metodo __destruct (es el mismo)
             por lo que se ejecutara dos veces uno con los valores de las variables del formulario y otra con los valores de las variables que pasamos mediante la funcion unserialize()
     
            De este modo podemos suplantar el valor de las variables en el metodo __destruct consiguiendo crear nuestro fichero.

    





      

      

    
        



        


    
    
