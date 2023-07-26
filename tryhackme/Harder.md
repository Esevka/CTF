## TryHackMe  <> Blueprint

![image](https://github.com/Esevka/CTF/assets/139042999/3ea2cca3-c8e7-4fcf-84d8-2d880db182e5)

Enunciado Informacion : There is a second way to get root access without using any key

---
---

## Escaneo de puertos

Lanzamos una traza ICMP(ping) para ver si la maquina esta activa, segun el ttl obtenido, por proximidad al valor 64(LINUX) podriamos decir que es una maquina Linux.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/harder/nmap]
    └─# ping 10.10.54.78 -c1
    PING 10.10.54.78 (10.10.54.78) 56(84) bytes of data.
    64 bytes from 10.10.54.78: icmp_seq=1 ttl=63 time=73.5 ms
    
    --- 10.10.54.78 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 73.542/73.542/73.542/0.000 ms

Reporte Nmap (Obtenemos puertos abiertos servicios y versiones que estan corriendo.)

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/harder/nmap]
    └─# nmap -p- --open -sS --min-rate 5000 -n -Pn 10.10.54.78 -vvv -oN open_ports                  
    Starting Nmap 7.93 ( https://nmap.org ) at 2023-07-26 13:03 CEST
    Initiating SYN Stealth Scan at 13:03
    Scanning 10.10.54.78 [65535 ports]
    Discovered open port 22/tcp on 10.10.54.78
    Discovered open port 80/tcp on 10.10.54.78
    Completed SYN Stealth Scan at 13:04, 24.15s elapsed (65535 total ports)
    Nmap scan report for 10.10.54.78
    Host is up, received user-set (0.068s latency).
    Scanned at 2023-07-26 13:03:57 CEST for 24s
    Not shown: 41750 closed tcp ports (reset), 23783 filtered tcp ports (no-response)
    Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
    PORT   STATE SERVICE REASON
    22/tcp open  ssh     syn-ack ttl 62
    80/tcp open  http    syn-ack ttl 62
    
    Read data files from: /usr/bin/../share/nmap
    Nmap done: 1 IP address (1 host up) scanned in 24.26 seconds
               Raw packets sent: 117285 (5.161MB) | Rcvd: 48663 (1.947MB)


    ┌──(root㉿kali)-[/home/…/Desktop/ctf/harder/nmap]
    └─# nmap -p 22,80 -sCV 10.10.54.78 -vvv -oN info_ports                        
    Starting Nmap 7.93 ( https://nmap.org ) at 2023-07-26 13:07 CEST

    PORT   STATE SERVICE REASON         VERSION
    22/tcp open  ssh     syn-ack ttl 62 OpenSSH 8.3 (protocol 2.0)
    | ssh-hostkey: 
    |   4096 cfe2d927d2d9f3f78e5dd2f99da4fb66 (RSA)
    | ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCns4FcsZGpefUl1pFm7KRPBXz7nIQ590yiEd6aNm6DEKKVQOUUT4TtSEpCaUhnDU/+XHFBJfXdm73tzEwCgN7fyxmXSCWDWu1tC1zui3CA/sr/g5k+Az0u1yTvoc3eUSByeGvVyShubpuCB5Mwa2YZJxiHu/WzFrtDbGIGiVcQgLJTXdXE+aK7hbsx6T9HMJpKEnneRvLY4WT6ZNjw8kfp6oHMFvz/lnDffyWMNxn9biQ/pSkZHOsBzLcAfAYXIp6710byAWGwuZL2/d6Yq1jyLY3bic6R7HGVWEX6VDcrxAeED8uNHF8kPqh46dFkyHekOOye6TnALXMZ/uo3GSvrJd1OWx2kZ1uPJWOl2bKj1aVKKsLgAsmrrRtG1KWrZZDqpxm/iUerlJzAl3YdLxyqXnQXvcBNHR6nc4js+bJwTPleuCOUVvkS1QWkljSDzJ878AKBDBxVLcFI0vCiIyUm065lhgTiPf0+v4Et4IQ7PlAZLjQGlttKeaI54MZQPM53JPdVqASlVTChX7689Wm94//boX4/YlyWJ0EWz/a0yrwifFK/fHJWXYtQiQQI02gPzafIy7zI6bO3N7CCkWdTbBPmX+zvw9QcjCxaq1T+L/v04oi0K1StQlCUTE12M4fMeO/HfAQYCRm6tfue2BlAriIomF++Bh4yO73z3YeNuQ==
    |   256 1e457b0ab5aa87e61bb1b79f5d8f8570 (ED25519)
    |_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIB+INGLWU0nf9OkPJkFoW9Gx2tdNEjLVXHrtZg17ALjH
    80/tcp open  http    syn-ack ttl 62 nginx 1.18.0
    |_http-server-header: nginx/1.18.0
    | http-methods: 
    |_  Supported Methods: GET HEAD POST
    |_http-title: Error
    
## Analisis de puertos y servicios




