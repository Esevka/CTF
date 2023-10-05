## TryHackMe  <> Year of the Owl

![image](https://github.com/Esevka/CTF/assets/139042999/ca6e2244-bb5a-4fb4-ad4a-c543249c58a3)

Enlace Maquina: https://tryhackme.com/room/ra

Enunciado : 

  - You have gained access to the internal network of WindCorp
  - Next step would be to take their crown jewels and get full access to their internal network. You have spotted a new windows machine
  - Conseguir 3 Flags

## Escaneo de puertos NMAP

-Buscamos puertos abiertos en en la maquina victima.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/ra1.1/nmap]
    └─# nmap -p- --open -sS --min-rate 5000 -n -Pn 10.10.36.177 -vvv -oG open_ports
    Starting Nmap 7.94 ( https://nmap.org ) at 2023-10-05 16:27 CEST
    
    PORT      STATE SERVICE          REASON
    53/tcp    open  domain           syn-ack ttl 127
    80/tcp    open  http             syn-ack ttl 127
    88/tcp    open  kerberos-sec     syn-ack ttl 127
    135/tcp   open  msrpc            syn-ack ttl 127
    139/tcp   open  netbios-ssn      syn-ack ttl 127
    389/tcp   open  ldap             syn-ack ttl 127
    445/tcp   open  microsoft-ds     syn-ack ttl 127
    464/tcp   open  kpasswd5         syn-ack ttl 127
    593/tcp   open  http-rpc-epmap   syn-ack ttl 127
    636/tcp   open  ldapssl          syn-ack ttl 127
    2179/tcp  open  vmrdp            syn-ack ttl 127
    3268/tcp  open  globalcatLDAP    syn-ack ttl 127
    3269/tcp  open  globalcatLDAPssl syn-ack ttl 127
    3389/tcp  open  ms-wbt-server    syn-ack ttl 127
    5222/tcp  open  xmpp-client      syn-ack ttl 127
    5223/tcp  open  hpvirtgrp        syn-ack ttl 127
    5229/tcp  open  jaxflow          syn-ack ttl 127
    5262/tcp  open  unknown          syn-ack ttl 127
    5263/tcp  open  unknown          syn-ack ttl 127
    5269/tcp  open  xmpp-server      syn-ack ttl 127
    5270/tcp  open  xmp              syn-ack ttl 127
    5275/tcp  open  unknown          syn-ack ttl 127
    5276/tcp  open  unknown          syn-ack ttl 127
    5985/tcp  open  wsman            syn-ack ttl 127
    7070/tcp  open  realserver       syn-ack ttl 127
    7443/tcp  open  oracleas-https   syn-ack ttl 127
    7777/tcp  open  cbt              syn-ack ttl 127
    9090/tcp  open  zeus-admin       syn-ack ttl 127
    9091/tcp  open  xmltec-xmlmail   syn-ack ttl 127
    9389/tcp  open  adws             syn-ack ttl 127
    49668/tcp open  unknown          syn-ack ttl 127
    49669/tcp open  unknown          syn-ack ttl 127
    49672/tcp open  unknown          syn-ack ttl 127
    49673/tcp open  unknown          syn-ack ttl 127
    49695/tcp open  unknown          syn-ack ttl 127
    49927/tcp open  unknown          syn-ack ttl 127
    
-Esta captura la hemos exportado en formato grepable,por lo que vamos a extraer los puertos para lanzarles unos scripts basicos de reconocimiento.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/ra1.1/nmap]
    └─# list_port open_ports 
    
    [+]Puertos Disponibles --> (Copiados en el Clipboard)
    
    53,80,88,135,139,389,445,464,593,636,2179,3268,3269,3389,5222,5223,5229,5262,5263,5269,5270,5275,5276,5985,7070,7443,7777,9090,9091,9389,49668,49669,49672,49673,49695,49927

  Ya tenemos los puertos copiado en el Clipboard, un script simple pero de gran ayuda. Script-->  https://github.com/Esevka/CTF/tree/main/Bash

