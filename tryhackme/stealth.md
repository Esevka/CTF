## TryHackMe  <> Stealth

![image](https://github.com/Esevka/CTF/assets/139042999/4d6aa794-1d1e-4022-8edb-ffc2fe8cad19)

Enlace Maquina: https://tryhackme.com/room/stealth

Enunciado :
  - Conseguir Flags(user y root)
---

## Escaneo de puertos (NMAP).

-Segun el ttl obtenito (127) despues de lanzar un paquete ICMP a la maquina victima podriamos decir que es una maquina ---> Windows.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/stealth]
    └─# ping -c1 10.10.236.141                            
    PING 10.10.236.141 (10.10.236.141) 56(84) bytes of data.
    64 bytes from 10.10.236.141: icmp_seq=1 ttl=127 time=558 ms
    
    --- 10.10.236.141 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 557.717/557.717/557.717/0.000 ms
    
-Buscamos puertos abiertos en en la maquina victima.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/stealth]
    └─# nmap -p- --open -sS --min-rate 5000 -n -Pn 10.10.236.141 -vvv -oG open_ports
    
    PORT      STATE SERVICE       REASON
    139/tcp   open  netbios-ssn   syn-ack ttl 127
    445/tcp   open  microsoft-ds  syn-ack ttl 127
    3389/tcp  open  ms-wbt-server syn-ack ttl 127
    5985/tcp  open  wsman         syn-ack ttl 127
    8000/tcp  open  http-alt      syn-ack ttl 127
    8080/tcp  open  http-proxy    syn-ack ttl 127
    8443/tcp  open  https-alt     syn-ack ttl 127
    47001/tcp open  winrm         syn-ack ttl 127
    49664/tcp open  unknown       syn-ack ttl 127
    49665/tcp open  unknown       syn-ack ttl 127
    49666/tcp open  unknown       syn-ack ttl 127
    49667/tcp open  unknown       syn-ack ttl 127
    49668/tcp open  unknown       syn-ack ttl 127
    49669/tcp open  unknown       syn-ack ttl 127
    49672/tcp open  unknown       syn-ack ttl 127

-Extraemos los puertos de la captura anterior para lanzarles unos scripts basicos de reconocimiento.

Utilizamos un Script en bash simple pero de gran ayuda. Script--> https://github.com/Esevka/CTF/tree/main/Bash

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/stealth]
    └─# list_port open_ports 
    
    [+]Puertos Disponibles --> (Copiados en el Clipboard)
    
    139,445,3389,5985,8000,8080,8443,47001,49664,49665,49666,49667,49668,49669,49672

  -Lanzamos scripts basicos de reconocimiento sobre los puertos abiertos.

  

  ---
## Analizamos la informacion obtenida sobre los puertos.


