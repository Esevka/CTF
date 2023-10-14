## TryHackMe  <> Fusion Corp

![image](https://github.com/Esevka/CTF/assets/139042999/f7bc6056-a728-4c36-a28e-2e1afd730143)

Enlace Maquina: https://tryhackme.com/room/fusioncorp

Enunciado : 

  - Segun el Enunciado se ha parcheado todo lo informado anteriormente y podemos volver a realizar las pruebas.
  - Conseguir 3 Flags
---
---

## Escaneo de puertos NMAP

-Buscamos puertos abiertos en en la maquina victima.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/FusionCorp]
    └─# nmap -p- -open -sS --min-rate 5000 -n -Pn -vvv 10.10.183.217 -oG open_ports
    Starting Nmap 7.94 ( https://nmap.org ) at 2023-10-14 08:16 CEST
    
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
    3268/tcp  open  globalcatLDAP    syn-ack ttl 127
    3269/tcp  open  globalcatLDAPssl syn-ack ttl 127
    3389/tcp  open  ms-wbt-server    syn-ack ttl 127
    5985/tcp  open  wsman            syn-ack ttl 127
    9389/tcp  open  adws             syn-ack ttl 127
    49666/tcp open  unknown          syn-ack ttl 127
    49668/tcp open  unknown          syn-ack ttl 127
    49669/tcp open  unknown          syn-ack ttl 127
    49670/tcp open  unknown          syn-ack ttl 127
    49673/tcp open  unknown          syn-ack ttl 127
    49689/tcp open  unknown          syn-ack ttl 127
    49700/tcp open  unknown          syn-ack ttl 127

-Captura exportado en formato grepable,por lo que vamos a extraer los puertos para lanzarles unos scripts basicos de reconocimiento.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/FusionCorp]
    └─# list_port open_ports 
    
    [+]Puertos Disponibles --> (Copiados en el Clipboard)
    
    53,80,88,135,139,389,445,464,593,636,3268,3269,3389,5985,9389,49666,49668,49669,49670,49673,49689,49700

Ya tenemos los puertos copiado en el Clipboard, un script simple pero de gran ayuda. Script-->  https://github.com/Esevka/CTF/tree/main/Bash

-Lanzamos scripts basicos de reconocimiento sobre los puertos abiertos.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/FusionCorp]
    └─# nmap -p 53,80,88,135,139,389,445,464,593,636,3268,3269,3389,5985,9389,49666,49668,49669,49670,49673,49689,49700 -sCV -n -Pn 10.10.183.217 -oN info_ports
    Starting Nmap 7.94 ( https://nmap.org ) at 2023-10-14 08:18 CEST
    Nmap scan report for 10.10.183.217
    Host is up (0.063s latency).
    
    PORT      STATE SERVICE       VERSION
    53/tcp    open  domain        Simple DNS Plus
    
    80/tcp    open  http          Microsoft IIS httpd 10.0
    | http-methods: 
    |_  Potentially risky methods: TRACE
    |_http-server-header: Microsoft-IIS/10.0
    |_http-title: eBusiness Bootstrap Template
    88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2023-10-14 06:18:39Z)
    135/tcp   open  msrpc         Microsoft Windows RPC
    139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
    389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: fusion.corp0., Site: Default-First-Site-Name)
    445/tcp   open  microsoft-ds?
    464/tcp   open  kpasswd5?
    593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
    636/tcp   open  tcpwrapped
    3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: fusion.corp0., Site: Default-First-Site-Name)
    3269/tcp  open  tcpwrapped
    3389/tcp  open  ms-wbt-server Microsoft Terminal Services
    | ssl-cert: Subject: commonName=Fusion-DC.fusion.corp
    | Not valid before: 2023-10-13T06:12:01
    |_Not valid after:  2024-04-13T06:12:01
    | rdp-ntlm-info: 
    |   Target_Name: FUSION
    |   NetBIOS_Domain_Name: FUSION
    |   NetBIOS_Computer_Name: FUSION-DC
    |   DNS_Domain_Name: fusion.corp
    |   DNS_Computer_Name: Fusion-DC.fusion.corp
    |   Product_Version: 10.0.17763
    |_  System_Time: 2023-10-14T06:19:29+00:00
    |_ssl-date: 2023-10-14T06:20:08+00:00; 0s from scanner time.
    5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
    |_http-server-header: Microsoft-HTTPAPI/2.0
    |_http-title: Not Found
    9389/tcp  open  mc-nmf        .NET Message Framing
    49666/tcp open  msrpc         Microsoft Windows RPC
    49668/tcp open  msrpc         Microsoft Windows RPC
    49669/tcp open  msrpc         Microsoft Windows RPC
    49670/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
    49673/tcp open  msrpc         Microsoft Windows RPC
    49689/tcp open  msrpc         Microsoft Windows RPC
    49700/tcp open  msrpc         Microsoft Windows RPC
    Service Info: Host: FUSION-DC; OS: Windows; CPE: cpe:/o:microsoft:windows





