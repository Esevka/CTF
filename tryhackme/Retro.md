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
    
