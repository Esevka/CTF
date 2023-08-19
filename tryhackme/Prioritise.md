## TryHackMe  <> Prioritise

![image](https://github.com/Esevka/CTF/assets/139042999/42583888-171e-4764-80e4-69e79bcb3c38)

Enlace Maquina: https://tryhackme.com/room/prioritise

Enunciado : Obtener flag
---
---

## Escaneo de puertos

-Lanzamos una traza ICMP(ping) para ver si la maquina esta activa, segun el ttl obtenido por proximidad al valor 64 podriamos decir que es una maquina Linux.

    ┌──(root㉿kali)-[/home/kali/Desktop/ctf/prioritise]
    └─# ping -c1 10.10.227.33  
    PING 10.10.227.33 (10.10.227.33) 56(84) bytes of data.
    64 bytes from 10.10.227.33: icmp_seq=1 ttl=63 time=51.3 ms
    
    --- 10.10.227.33 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 51.261/51.261/51.261/0.000 ms

-Reporte Nmap (Obtenemos puertos abiertos servicios y versiones que estan corriendo).

    ┌──(root㉿kali)-[/home/kali/Desktop/ctf/prioritise]
    └─# nmap -p- --open -sS --min-rate 5000 -n -Pn -vvv 10.10.227.33 -oN open_ports
    Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-19 18:36 CEST
    Initiating SYN Stealth Scan at 18:36
    
    PORT   STATE SERVICE REASON
    22/tcp open  ssh     syn-ack ttl 63
    80/tcp open  http    syn-ack ttl 62


    ┌──(root㉿kali)-[/home/kali/Desktop/ctf/prioritise]
    └─# nmap -p 22,80 -sCV 10.10.227.33 -oN info_ports                       
    Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-19 18:38 CEST
    WARNING: Service 10.10.227.33:80 had already soft-matched rtsp, but now soft-matched sip; ignoring second value
    Nmap scan report for 10.10.227.33
    Host is up (0.052s latency).
    
    PORT   STATE SERVICE VERSION
    22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   3072 3e594b164f84a6d8e8bd77fb0f0f2759 (RSA)
    |   256 c1bf6ebceb1bdb04251ec17bb71341a4 (ECDSA)
    |_  256 a4fad854d029f7d26603e2ac2db8bda2 (ED25519)
    
    80/tcp open  rtsp
    | fingerprint-strings: 
    |   FourOhFourRequest: 
    |     HTTP/1.0 404 NOT FOUND
    |     Content-Type: text/html; charset=utf-8
    |     Content-Length: 232
    |     <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
    |     <title>404 Not Found</title>
    |     <h1>Not Found</h1>
    |     <p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
    |   GetRequest: 
    |     HTTP/1.0 200 OK
    |     Content-Type: text/html; charset=utf-8
    |     Content-Length: 5062
    |     <!DOCTYPE html>
    |     <html lang="en">
    |     <head>
    |     <meta charset="utf-8" />
    |     <meta
    |     name="viewport"
    |     content="width=device-width, initial-scale=1, shrink-to-fit=no"
    |     <link
    |     rel="stylesheet"
    |     href="../static/css/bootstrap.min.css"
    |     crossorigin="anonymous"
    |     <link
    |     rel="stylesheet"
    |     href="../static/css/font-awesome.min.css"
    |     crossorigin="anonymous"
    |     <link
    |     rel="stylesheet"
    |     href="../static/css/bootstrap-datepicker.min.css"
    |     crossorigin="anonymous"
    |     <title>Prioritise</title>
    |     </head>
    |     <body>
    |     <!-- Navigation -->
    |     <nav class="navbar navbar-expand-md navbar-dark bg-dark">
    |     <div class="container">
    |     class="navbar-brand" href="/"><span class="">Prioritise</span></a>
    |     <button
    |     class="na
    |   HTTPOptions: 
    |     HTTP/1.0 200 OK
    |     Content-Type: text/html; charset=utf-8
    |     Allow: HEAD, OPTIONS, GET
    |     Content-Length: 0
    |   RTSPRequest: 
    |     RTSP/1.0 200 OK
    |     Content-Type: text/html; charset=utf-8
    |     Allow: HEAD, OPTIONS, GET
    |_    Content-Length: 0
    |_http-title: Prioritise
