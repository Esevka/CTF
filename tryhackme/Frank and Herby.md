## TryHackMe  <> Frank and Herby try again...
![image](https://github.com/Esevka/CTF/assets/139042999/386d8ae0-d46d-4510-8079-6a754f3f684a)

Enlace Maquina : https://tryhackme.com/room/frankandherbytryagain

Enunciado : Obtener las flags de usuario y root.
---
---

## Escaneo de puertos

-Lanzamos una traza ICMP(ping) para ver si la maquina esta activa, segun el ttl obtenido, por proximidad al valor 64 podriamos decir que es una maquina Linux.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/frank-herby/nmap]
    └─# ping -c1 10.10.62.132 
    PING 10.10.62.132 (10.10.62.132) 56(84) bytes of data.
    64 bytes from 10.10.62.132: icmp_seq=1 ttl=63 time=654 ms
    
    --- 10.10.62.132 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 653.867/653.867/653.867/0.000 ms

-Reporte Nmap (Obtenemos puertos abiertos servicios y versiones que estan corriendo).

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/frank-herby/nmap]
    └─# nmap -p- --open -sS --min-rate 5000 -n -Pn 10.10.62.132 -oN open_ports -vvv
    Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-10 17:10 CEST
    Initiating SYN Stealth Scan at 17:10
    [...]
    PORT      STATE SERVICE      REASON
    22/tcp    open  ssh          syn-ack ttl 63
    10250/tcp open  unknown      syn-ack ttl 63
    10255/tcp open  unknown      syn-ack ttl 63
    10257/tcp open  unknown      syn-ack ttl 63
    10259/tcp open  unknown      syn-ack ttl 63
    16443/tcp open  unknown      syn-ack ttl 63
    25000/tcp open  icl-twobase1 syn-ack ttl 63
    30679/tcp open  unknown      syn-ack ttl 62

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/frank-herby/nmap]
    └─# nmap -p 22,10250,10255,10257,10259,16443,25000,30679 -sCV 10.10.62.132 -oN info_ports
    Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-10 17:12 CEST
    Nmap scan report for 10.10.62.132
    Host is up (0.40s latency).
    
    PORT      STATE SERVICE     VERSION
    22/tcp    open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   3072 99bf3f0eb2950e76e50f288ae925bdb1 (RSA)
    |   256 df48b7b2a2bc5a7ef9bbb8542a980309 (ECDSA)
    |_  256 ad09e8fd583ba13e377e62d244207af2 (ED25519)
    10250/tcp open  ssl/http    Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
    |_http-title: Site doesn't have a title (text/plain; charset=utf-8).
    | ssl-cert: Subject: commonName=microk8s@1647797913
    | Subject Alternative Name: DNS:microk8s
    | Not valid before: 2022-03-20T16:38:32
    |_Not valid after:  2023-03-20T16:38:32
    |_ssl-date: TLS randomness does not represent time
    | tls-alpn: 
    |   h2
    |_  http/1.1
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
    |     Date: Thu, 10 Aug 2023 15:12:53 GMT
    |     Content-Length: 185
    |     {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"forbidden: User "system:anonymous" cannot get path "/"","reason":"Forbidden","details":{},"code":403}
    |   HTTPOptions: 
    |     HTTP/1.0 403 Forbidden
    |     Cache-Control: no-cache, private
    |     Content-Type: application/json
    |     X-Content-Type-Options: nosniff
    |     Date: Thu, 10 Aug 2023 15:12:53 GMT
    |     Content-Length: 189
    |_    {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"forbidden: User "system:anonymous" cannot options path "/"","reason":"Forbidden","details":{},"code":403}
    | ssl-cert: Subject: commonName=localhost@1691679913
    | Subject Alternative Name: DNS:localhost, DNS:localhost, IP Address:127.0.0.1
    | Not valid before: 2023-08-10T14:05:12
    |_Not valid after:  2024-08-09T14:05:12
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
    |     Date: Thu, 10 Aug 2023 15:12:53 GMT
    |     Content-Length: 185
    |     {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"forbidden: User "system:anonymous" cannot get path "/"","reason":"Forbidden","details":{},"code":403}
    |   HTTPOptions: 
    |     HTTP/1.0 403 Forbidden
    |     Cache-Control: no-cache, private
    |     Content-Type: application/json
    |     X-Content-Type-Options: nosniff
    |     Date: Thu, 10 Aug 2023 15:12:53 GMT
    |     Content-Length: 189
    |_    {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"forbidden: User "system:anonymous" cannot options path "/"","reason":"Forbidden","details":{},"code":403}
    | ssl-cert: Subject: commonName=localhost@1691679912
    | Subject Alternative Name: DNS:localhost, DNS:localhost, IP Address:127.0.0.1
    | Not valid before: 2023-08-10T14:05:12
    |_Not valid after:  2024-08-09T14:05:12
    | tls-alpn: 
    |   h2
    |_  http/1.1
    |_ssl-date: TLS randomness does not represent time
    16443/tcp open  ssl/unknown
    | fingerprint-strings: 
    |   FourOhFourRequest: 
    |     HTTP/1.0 401 Unauthorized
    |     Audit-Id: bc87c6de-7a21-4558-9d7a-881b541a5571
    |     Cache-Control: no-cache, private
    |     Content-Type: application/json
    |     Date: Thu, 10 Aug 2023 15:13:21 GMT
    |     Content-Length: 129
    |     {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"Unauthorized","reason":"Unauthorized","code":401}
    |   GenericLines, Help, Kerberos, RTSPRequest, SSLSessionReq, TLSSessionReq, TerminalServerCookie: 
    |     HTTP/1.1 400 Bad Request
    |     Content-Type: text/plain; charset=utf-8
    |     Connection: close
    |     Request
    |   GetRequest: 
    |     HTTP/1.0 401 Unauthorized
    |     Audit-Id: 0c28ba2a-4ff2-4375-9326-0b124c4d8c00
    |     Cache-Control: no-cache, private
    |     Content-Type: application/json
    |     Date: Thu, 10 Aug 2023 15:12:53 GMT
    |     Content-Length: 129
    |     {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"Unauthorized","reason":"Unauthorized","code":401}
    |   HTTPOptions: 
    |     HTTP/1.0 401 Unauthorized
    |     Audit-Id: 2d8fc79d-a5ba-4388-b20d-9b968bb8174e
    |     Cache-Control: no-cache, private
    |     Content-Type: application/json
    |     Date: Thu, 10 Aug 2023 15:12:53 GMT
    |     Content-Length: 129
    |_    {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"Unauthorized","reason":"Unauthorized","code":401}
    | tls-alpn: 
    |   h2
    |_  http/1.1
    |_ssl-date: TLS randomness does not represent time
    | ssl-cert: Subject: commonName=127.0.0.1/organizationName=Canonical/stateOrProvinceName=Canonical/countryName=GB
    | Subject Alternative Name: DNS:kubernetes, DNS:kubernetes.default, DNS:kubernetes.default.svc, DNS:kubernetes.default.svc.cluster, DNS:kubernetes.default.svc.cluster.local, IP Address:127.0.0.1, IP Address:10.152.183.1, IP Address:10.10.62.132
    | Not valid before: 2023-08-10T15:04:01
    |_Not valid after:  2024-08-09T15:04:01
    25000/tcp open  ssl/http    Gunicorn 19.7.1
    |_http-title: 404 Not Found
    | ssl-cert: Subject: commonName=127.0.0.1/organizationName=Canonical/stateOrProvinceName=Canonical/countryName=GB
    | Subject Alternative Name: DNS:kubernetes, DNS:kubernetes.default, DNS:kubernetes.default.svc, DNS:kubernetes.default.svc.cluster, DNS:kubernetes.default.svc.cluster.local, IP Address:127.0.0.1, IP Address:10.152.183.1, IP Address:10.10.62.132
    | Not valid before: 2023-08-10T15:04:01
    |_Not valid after:  2024-08-09T15:04:01
    |_http-server-header: gunicorn/19.7.1
    |_ssl-date: TLS randomness does not represent time
    30679/tcp open  http        PHP cli server 5.5 or later (PHP 8.1.0-dev)
    |_http-title: FRANK RULEZZ!

Despues de lanzar los scripts basicos de reconocimiento de nmap hemos obtenido toda esta cantidad de informacion, la cual  despues de analizarla hemos encontrado algo en el puerto
    
      30679/tcp open  http        PHP cli server 5.5 or later (PHP 8.1.0-dev)
    |_http-title: FRANK RULEZZ!

## Analisis de vulnerabilidades en los servicios y explotacion de los mismos.

- Analizamos los launchpad de los servicios, pero no tenemos muy claro la Distribucion y series del sistema, ya la veremos cuando ganemos acceso a la maquina.

- Puerto 30679
  
  Analizamos la web y no vemos nada.
  
  Fuzzeamos la web en busca de directorios que nos puedan valer, encontramos  un info.php

      ┌──(root㉿kali)-[/home/…/Desktop/ctf/frank-herby/nmap]
      └─# gobuster dir -u http://10.10.62.132:30679 -w /usr/share/wordlists/dirb/common.txt -o fuzz --exclude-length 640
      ===============================================================
      Gobuster v3.5
      by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
      ===============================================================
      /info.php             (Status: 200) [Size: 66724]
      Progress: 4614 / 4615 (99.98%)
  
  ![image](https://github.com/Esevka/CTF/assets/139042999/433b67b9-738a-4b4d-80cc-2fc0cb5e67cb)

  Buscando info sobre la version de php que esta corriendo la maquina encontramos un backdoor para esta version que nos permite realizar un RCE.

  INFO: https://www.exploit-db.com/exploits/49933

  Analizamos el backdoor y vemos que enviando en la cabecera de la solicitud  ---- "User-Agentt": "zerodiumsystem('" + cmd + "');" ---- podemos ejecutar comandos.

- Montamos nuestra Request y probamos.

    

    
    
  
  


