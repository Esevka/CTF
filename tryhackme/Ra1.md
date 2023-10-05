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

-Lanzamos scripts basicos de reconocimiento sobre los puertos abiertos.

    ┌──(root㉿kali)-[/home/…/ctf/try_ctf/ra1.1/nmap]
    └─# nmap -p 53,80,88,135,139,389,445,464,593,636,2179,3268,3269,3389,5222,5223,5229,5262,5263,5269,5270,5275,5276,5985,7070,7443,7777,9090,9091,9389,49668,49669,49672,49673,49695,49927 -sCV -n -Pn 10.10.36.177 -vvv -oN info_ports
    
    Starting Nmap 7.94 ( https://nmap.org ) at 2023-10-05 16:36 CEST
    
    PORT      STATE SERVICE             REASON          VERSION
    
    53/tcp    open  domain              syn-ack ttl 127 Simple DNS Plus
    
    80/tcp    open  http                syn-ack ttl 127 Microsoft IIS httpd 10.0
    |_http-title: Windcorp.
    | http-methods: 
    |   Supported Methods: OPTIONS TRACE GET HEAD POST
    |_  Potentially risky methods: TRACE
    |_http-server-header: Microsoft-IIS/10.0
    
    88/tcp    open  kerberos-sec        syn-ack ttl 127 Microsoft Windows Kerberos (server time: 2023-10-05 14:36:59Z)
    135/tcp   open  msrpc               syn-ack ttl 127 Microsoft Windows RPC
    139/tcp   open  netbios-ssn         syn-ack ttl 127 Microsoft Windows netbios-ssn
    389/tcp   open  ldap                syn-ack ttl 127 Microsoft Windows Active Directory LDAP (Domain: windcorp.thm0., Site: Default-First-Site-Name)
    445/tcp   open  microsoft-ds?       syn-ack ttl 127
    464/tcp   open  kpasswd5?           syn-ack ttl 127
    593/tcp   open  ncacn_http          syn-ack ttl 127 Microsoft Windows RPC over HTTP 1.0
    636/tcp   open  ldapssl?            syn-ack ttl 127
    2179/tcp  open  vmrdp?              syn-ack ttl 127
    3268/tcp  open  ldap                syn-ack ttl 127 Microsoft Windows Active Directory LDAP (Domain: windcorp.thm0., Site: Default-First-Site-Name)
    3269/tcp  open  globalcatLDAPssl?   syn-ack ttl 127
    
    3389/tcp  open  ms-wbt-server       syn-ack ttl 127 Microsoft Terminal Services
    |_ssl-date: 2023-10-05T14:38:46+00:00; +1s from scanner time.
    | rdp-ntlm-info: 
    |   Target_Name: WINDCORP
    |   NetBIOS_Domain_Name: WINDCORP
    |   NetBIOS_Computer_Name: FIRE
    |   DNS_Domain_Name: windcorp.thm
    |   DNS_Computer_Name: Fire.windcorp.thm
    |   DNS_Tree_Name: windcorp.thm
    |   Product_Version: 10.0.17763
    |_  System_Time: 2023-10-05T14:38:06+00:00
    | ssl-cert: Subject: commonName=Fire.windcorp.thm
    | Issuer: commonName=Fire.windcorp.thm
    | Public Key type: rsa
    | Public Key bits: 2048
    | Signature Algorithm: sha256WithRSAEncryption
    | Not valid before: 2023-10-04T14:20:06
    | Not valid after:  2024-04-04T14:20:06
    | MD5:   2dcd:6a16:d7ba:124d:a65e:1c8f:f5da:8542
    | SHA-1: 7074:af72:252e:f5c7:b00a:1172:b51a:f8a9:997b:008f
    | -----BEGIN CERTIFICATE-----
    | MIIC5jCCAc6gAwIBAgIQb1ZLGoaWtYdKSGc75mCbXTANBgkqhkiG9w0BAQsFADAc
    | MRowGAYDVQQDExFGaXJlLndpbmRjb3JwLnRobTAeFw0yMzEwMDQxNDIwMDZaFw0y
    | NDA0MDQxNDIwMDZaMBwxGjAYBgNVBAMTEUZpcmUud2luZGNvcnAudGhtMIIBIjAN
    | BgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA37VeTrSXCWG3rYrpxyqi9VRGioHP
    | VqFEowYVJvyj+JS+8R5WXAyKT3ha+NXib4P1y20sNls4wpTNO2DQjlfUE2ojT76H
    | d7uXP09RGs+D7OIfqJXi/OrsPW5DlFGHVU6OV54A2oZ4nupaBTrt7EhB7+wMB6pz
    | s8/BrXbP+ocdkUrFFwIe6KMmnIfzus+LLemUZxMaNUN7iUBTZ9EvzrgKBi1hr+/C
    | BioM8bdgG2F5VQwecZeJhH0b7uATYv91wtCAQiATjI++6Pf9bdH+gdBxWqYghYnl
    | bUL5HujmkLGvZv87Jx7YDjSILsk4jYtdChn6Rbbujco+90arOFh9ynpXVQIDAQAB
    | oyQwIjATBgNVHSUEDDAKBggrBgEFBQcDATALBgNVHQ8EBAMCBDAwDQYJKoZIhvcN
    | AQELBQADggEBANlgxLhTOotXYnapVbbzWyWLqAtKqI5TCfyQ8QJODfB+vsyLQSQr
    | mrW3MIFBLGhiSUDEFGEbQPrGPR5d9BBa7KBF5xZjGGqsfIbmH2NUHZffk1+xhIhE
    | 7YnfO+Z6Dfuoiw/Tz1YcfI9N1T736npglhrkON5SVhe31HrBi3NZJz0T2/xp1rtm
    | zbf5bP6QuTrpeZtpFNkUeDMtRsflV4LhBYo2CnmCgfNVH4NJXdza3Pjf1obIRoj3
    | 6sLnAi0JIfHn/n//SZv6L4Pst9FS+1+5a6nyIOxbRKCcHP7sgmnOiF69PXS4DqvC
    | M7XhZKTRvPf8nBGTcU+9j24pLtiOEXwSd9Q=
    |_-----END CERTIFICATE-----
    
    5222/tcp  open  jabber              syn-ack ttl 127
    |_ssl-date: 2023-10-05T14:38:47+00:00; +1s from scanner time.
    | xmpp-info: 
    |   STARTTLS Failed
    |   info: 
    |     stream_id: 9fq6orakaa
    |     features: 
    |     compression_methods: 
    |     capabilities: 
    |     xmpp: 
    |       version: 1.0
    |     unknown: 
    |     auth_mechanisms: 
    |     errors: 
    |       invalid-namespace
    |_      (timeout)
    | fingerprint-strings: 
    |   RPCCheck: 
    |_    <stream:error xmlns:stream="http://etherx.jabber.org/streams"><not-well-formed xmlns="urn:ietf:params:xml:ns:xmpp-streams"/></stream:error></stream:stream>
    | ssl-cert: Subject: commonName=fire.windcorp.thm
    | Subject Alternative Name: DNS:fire.windcorp.thm, DNS:*.fire.windcorp.thm
    | Issuer: commonName=fire.windcorp.thm
    | Public Key type: rsa
    | Public Key bits: 2048
    | Signature Algorithm: sha256WithRSAEncryption
    | Not valid before: 2020-05-01T08:39:00
    | Not valid after:  2025-04-30T08:39:00
    | MD5:   b715:5425:83f3:a20f:75c8:ca2d:3353:cbb7
    | SHA-1: 97f7:0772:a26b:e324:7ed5:bbcb:5f35:7d74:7982:66ae
    | -----BEGIN CERTIFICATE-----
    | MIIDLzCCAhegAwIBAgIIXUFELG7QgAIwDQYJKoZIhvcNAQELBQAwHDEaMBgGA1UE
    | AwwRZmlyZS53aW5kY29ycC50aG0wHhcNMjAwNTAxMDgzOTAwWhcNMjUwNDMwMDgz
    | OTAwWjAcMRowGAYDVQQDDBFmaXJlLndpbmRjb3JwLnRobTCCASIwDQYJKoZIhvcN
    | AQEBBQADggEPADCCAQoCggEBAKLH0/j17RVdD8eXC+0IFovAoql2REjOSf2NpJLK
    | /6fgtx3CA4ftLsj7yOpmj8Oe1gqfWd2EM/zKk+ZmZwQFxLQL93t1OD/za1gyclxr
    | IVbPVWqFoM2BUU9O3yU0VVRGP7xKDHm4bcoNmq9UNurEtFlCNeCC1fcwzfYvKD89
    | X04Rv/6kn1GlQq/iM8PGCLDUf1p1WJcwGT5FUiBa9boTU9llBcGqbodZaBKzPPP8
    | DmvSYF71IKBT8NsVzqiAiO3t/oHgApvUd9BqdbZeN46XORrOhBQV0xUpNVy9L5OE
    | UAD1so3ePTNjpPE5SfTKymT1a8Fiw5kroKODN0nzy50yP3UCAwEAAaN1MHMwMQYD
    | VR0RBCowKIIRZmlyZS53aW5kY29ycC50aG2CEyouZmlyZS53aW5kY29ycC50aG0w
    | HQYDVR0OBBYEFOtMzqgfsY11qewZNfPjiLxnGykGMB8GA1UdIwQYMBaAFOtMzqgf
    | sY11qewZNfPjiLxnGykGMA0GCSqGSIb3DQEBCwUAA4IBAQAHofv0VP+hE+5sg0KR
    | 2x0Xeg4cIXEia0c5cIJ7K7bhfoLOcT7WcMKCLIN3A416PREdkB6Q610uDs8RpezJ
    | II/wBoIp2G0Y87X3Xo5FmNJjl9lGX5fvayen98khPXvZkurHdWdtA4m8pHOdYOrk
    | n8Jth6L/y4L5WlgEGL0x0HK4yvd3iz0VNrc810HugpyfVWeasChhZjgAYXUVlA8k
    | +QxLxyNr/PBfRumQGzw2n3msXxwfHVzaHphy56ph85PcRS35iNqgrtK0fe3Qhpq7
    | v5vQYKlOGq5FI6Mf9ni7S1pXSqF4U9wuqZy4q4tXWAVootmJv1DIgfSMLvXplN9T
    | LucP
    |_-----END CERTIFICATE-----
    
    5223/tcp  open  ssl/jabber          syn-ack ttl 127
    |_ssl-date: 2023-10-05T14:38:46+00:00; +1s from scanner time.
    | xmpp-info: 
    |   STARTTLS Failed
    |   info: 
    |     features: 
    |     compression_methods: 
    |     capabilities: 
    |     xmpp: 
    |     unknown: 
    |     auth_mechanisms: 
    |     errors: 
    |_      (timeout)
    | ssl-cert: Subject: commonName=fire.windcorp.thm
    | Subject Alternative Name: DNS:fire.windcorp.thm, DNS:*.fire.windcorp.thm
    | Issuer: commonName=fire.windcorp.thm
    | Public Key type: rsa
    | Public Key bits: 2048
    | Signature Algorithm: sha256WithRSAEncryption
    | Not valid before: 2020-05-01T08:39:00
    | Not valid after:  2025-04-30T08:39:00
    | MD5:   b715:5425:83f3:a20f:75c8:ca2d:3353:cbb7
    | SHA-1: 97f7:0772:a26b:e324:7ed5:bbcb:5f35:7d74:7982:66ae
    | -----BEGIN CERTIFICATE-----
    | MIIDLzCCAhegAwIBAgIIXUFELG7QgAIwDQYJKoZIhvcNAQELBQAwHDEaMBgGA1UE
    | AwwRZmlyZS53aW5kY29ycC50aG0wHhcNMjAwNTAxMDgzOTAwWhcNMjUwNDMwMDgz
    | OTAwWjAcMRowGAYDVQQDDBFmaXJlLndpbmRjb3JwLnRobTCCASIwDQYJKoZIhvcN
    | AQEBBQADggEPADCCAQoCggEBAKLH0/j17RVdD8eXC+0IFovAoql2REjOSf2NpJLK
    | /6fgtx3CA4ftLsj7yOpmj8Oe1gqfWd2EM/zKk+ZmZwQFxLQL93t1OD/za1gyclxr
    | IVbPVWqFoM2BUU9O3yU0VVRGP7xKDHm4bcoNmq9UNurEtFlCNeCC1fcwzfYvKD89
    | X04Rv/6kn1GlQq/iM8PGCLDUf1p1WJcwGT5FUiBa9boTU9llBcGqbodZaBKzPPP8
    | DmvSYF71IKBT8NsVzqiAiO3t/oHgApvUd9BqdbZeN46XORrOhBQV0xUpNVy9L5OE
    | UAD1so3ePTNjpPE5SfTKymT1a8Fiw5kroKODN0nzy50yP3UCAwEAAaN1MHMwMQYD
    | VR0RBCowKIIRZmlyZS53aW5kY29ycC50aG2CEyouZmlyZS53aW5kY29ycC50aG0w
    | HQYDVR0OBBYEFOtMzqgfsY11qewZNfPjiLxnGykGMB8GA1UdIwQYMBaAFOtMzqgf
    | sY11qewZNfPjiLxnGykGMA0GCSqGSIb3DQEBCwUAA4IBAQAHofv0VP+hE+5sg0KR
    | 2x0Xeg4cIXEia0c5cIJ7K7bhfoLOcT7WcMKCLIN3A416PREdkB6Q610uDs8RpezJ
    | II/wBoIp2G0Y87X3Xo5FmNJjl9lGX5fvayen98khPXvZkurHdWdtA4m8pHOdYOrk
    | n8Jth6L/y4L5WlgEGL0x0HK4yvd3iz0VNrc810HugpyfVWeasChhZjgAYXUVlA8k
    | +QxLxyNr/PBfRumQGzw2n3msXxwfHVzaHphy56ph85PcRS35iNqgrtK0fe3Qhpq7
    | v5vQYKlOGq5FI6Mf9ni7S1pXSqF4U9wuqZy4q4tXWAVootmJv1DIgfSMLvXplN9T
    | LucP
    |_-----END CERTIFICATE-----
    | fingerprint-strings: 
    |   RPCCheck: 
    |_    <stream:error xmlns:stream="http://etherx.jabber.org/streams"><not-well-formed xmlns="urn:ietf:params:xml:ns:xmpp-streams"/></stream:error></stream:stream>
    
    5229/tcp  open  jaxflow?            syn-ack ttl 127
    
    5262/tcp  open  jabber              syn-ack ttl 127
    | xmpp-info: 
    |   STARTTLS Failed
    |   info: 
    |     stream_id: a0j6xx9703
    |     features: 
    |     compression_methods: 
    |     capabilities: 
    |     xmpp: 
    |       version: 1.0
    |     unknown: 
    |     auth_mechanisms: 
    |     errors: 
    |       invalid-namespace
    |_      (timeout)
    | fingerprint-strings: 
    |   RPCCheck: 
    |_    <stream:error xmlns:stream="http://etherx.jabber.org/streams"><not-well-formed xmlns="urn:ietf:params:xml:ns:xmpp-streams"/></stream:error></stream:stream>
    
    5263/tcp  open  ssl/jabber          syn-ack ttl 127 Ignite Realtime Openfire Jabber server 3.10.0 or later
    |_ssl-date: 2023-10-05T14:38:46+00:00; +1s from scanner time.
    | xmpp-info: 
    |   STARTTLS Failed
    |   info: 
    |     features: 
    |     compression_methods: 
    |     capabilities: 
    |     xmpp: 
    |     unknown: 
    |     auth_mechanisms: 
    |     errors: 
    |_      (timeout)
    | ssl-cert: Subject: commonName=fire.windcorp.thm
    | Subject Alternative Name: DNS:fire.windcorp.thm, DNS:*.fire.windcorp.thm
    | Issuer: commonName=fire.windcorp.thm
    | Public Key type: rsa
    | Public Key bits: 2048
    | Signature Algorithm: sha256WithRSAEncryption
    | Not valid before: 2020-05-01T08:39:00
    | Not valid after:  2025-04-30T08:39:00
    | MD5:   b715:5425:83f3:a20f:75c8:ca2d:3353:cbb7
    | SHA-1: 97f7:0772:a26b:e324:7ed5:bbcb:5f35:7d74:7982:66ae
    | -----BEGIN CERTIFICATE-----
    | MIIDLzCCAhegAwIBAgIIXUFELG7QgAIwDQYJKoZIhvcNAQELBQAwHDEaMBgGA1UE
    | AwwRZmlyZS53aW5kY29ycC50aG0wHhcNMjAwNTAxMDgzOTAwWhcNMjUwNDMwMDgz
    | OTAwWjAcMRowGAYDVQQDDBFmaXJlLndpbmRjb3JwLnRobTCCASIwDQYJKoZIhvcN
    | AQEBBQADggEPADCCAQoCggEBAKLH0/j17RVdD8eXC+0IFovAoql2REjOSf2NpJLK
    | /6fgtx3CA4ftLsj7yOpmj8Oe1gqfWd2EM/zKk+ZmZwQFxLQL93t1OD/za1gyclxr
    | IVbPVWqFoM2BUU9O3yU0VVRGP7xKDHm4bcoNmq9UNurEtFlCNeCC1fcwzfYvKD89
    | X04Rv/6kn1GlQq/iM8PGCLDUf1p1WJcwGT5FUiBa9boTU9llBcGqbodZaBKzPPP8
    | DmvSYF71IKBT8NsVzqiAiO3t/oHgApvUd9BqdbZeN46XORrOhBQV0xUpNVy9L5OE
    | UAD1so3ePTNjpPE5SfTKymT1a8Fiw5kroKODN0nzy50yP3UCAwEAAaN1MHMwMQYD
    | VR0RBCowKIIRZmlyZS53aW5kY29ycC50aG2CEyouZmlyZS53aW5kY29ycC50aG0w
    | HQYDVR0OBBYEFOtMzqgfsY11qewZNfPjiLxnGykGMB8GA1UdIwQYMBaAFOtMzqgf
    | sY11qewZNfPjiLxnGykGMA0GCSqGSIb3DQEBCwUAA4IBAQAHofv0VP+hE+5sg0KR
    | 2x0Xeg4cIXEia0c5cIJ7K7bhfoLOcT7WcMKCLIN3A416PREdkB6Q610uDs8RpezJ
    | II/wBoIp2G0Y87X3Xo5FmNJjl9lGX5fvayen98khPXvZkurHdWdtA4m8pHOdYOrk
    | n8Jth6L/y4L5WlgEGL0x0HK4yvd3iz0VNrc810HugpyfVWeasChhZjgAYXUVlA8k
    | +QxLxyNr/PBfRumQGzw2n3msXxwfHVzaHphy56ph85PcRS35iNqgrtK0fe3Qhpq7
    | v5vQYKlOGq5FI6Mf9ni7S1pXSqF4U9wuqZy4q4tXWAVootmJv1DIgfSMLvXplN9T
    | LucP
    |_-----END CERTIFICATE-----
    
    5269/tcp  open  xmpp                syn-ack ttl 127 Wildfire XMPP Client
    | xmpp-info: 
    |   STARTTLS Failed
    |   info: 
    |     features: 
    |     compression_methods: 
    |     capabilities: 
    |     xmpp: 
    |     unknown: 
    |     auth_mechanisms: 
    |     errors: 
    |_      (timeout)
    
    5270/tcp  open  ssl/xmpp            syn-ack ttl 127 Wildfire XMPP Client
    |_ssl-date: 2023-10-05T14:38:46+00:00; +1s from scanner time.
    | ssl-cert: Subject: commonName=fire.windcorp.thm
    | Subject Alternative Name: DNS:fire.windcorp.thm, DNS:*.fire.windcorp.thm
    | Issuer: commonName=fire.windcorp.thm
    | Public Key type: rsa
    | Public Key bits: 2048
    | Signature Algorithm: sha256WithRSAEncryption
    | Not valid before: 2020-05-01T08:39:00
    | Not valid after:  2025-04-30T08:39:00
    | MD5:   b715:5425:83f3:a20f:75c8:ca2d:3353:cbb7
    | SHA-1: 97f7:0772:a26b:e324:7ed5:bbcb:5f35:7d74:7982:66ae
    | -----BEGIN CERTIFICATE-----
    | MIIDLzCCAhegAwIBAgIIXUFELG7QgAIwDQYJKoZIhvcNAQELBQAwHDEaMBgGA1UE
    | AwwRZmlyZS53aW5kY29ycC50aG0wHhcNMjAwNTAxMDgzOTAwWhcNMjUwNDMwMDgz
    | OTAwWjAcMRowGAYDVQQDDBFmaXJlLndpbmRjb3JwLnRobTCCASIwDQYJKoZIhvcN
    | AQEBBQADggEPADCCAQoCggEBAKLH0/j17RVdD8eXC+0IFovAoql2REjOSf2NpJLK
    | /6fgtx3CA4ftLsj7yOpmj8Oe1gqfWd2EM/zKk+ZmZwQFxLQL93t1OD/za1gyclxr
    | IVbPVWqFoM2BUU9O3yU0VVRGP7xKDHm4bcoNmq9UNurEtFlCNeCC1fcwzfYvKD89
    | X04Rv/6kn1GlQq/iM8PGCLDUf1p1WJcwGT5FUiBa9boTU9llBcGqbodZaBKzPPP8
    | DmvSYF71IKBT8NsVzqiAiO3t/oHgApvUd9BqdbZeN46XORrOhBQV0xUpNVy9L5OE
    | UAD1so3ePTNjpPE5SfTKymT1a8Fiw5kroKODN0nzy50yP3UCAwEAAaN1MHMwMQYD
    | VR0RBCowKIIRZmlyZS53aW5kY29ycC50aG2CEyouZmlyZS53aW5kY29ycC50aG0w
    | HQYDVR0OBBYEFOtMzqgfsY11qewZNfPjiLxnGykGMB8GA1UdIwQYMBaAFOtMzqgf
    | sY11qewZNfPjiLxnGykGMA0GCSqGSIb3DQEBCwUAA4IBAQAHofv0VP+hE+5sg0KR
    | 2x0Xeg4cIXEia0c5cIJ7K7bhfoLOcT7WcMKCLIN3A416PREdkB6Q610uDs8RpezJ
    | II/wBoIp2G0Y87X3Xo5FmNJjl9lGX5fvayen98khPXvZkurHdWdtA4m8pHOdYOrk
    | n8Jth6L/y4L5WlgEGL0x0HK4yvd3iz0VNrc810HugpyfVWeasChhZjgAYXUVlA8k
    | +QxLxyNr/PBfRumQGzw2n3msXxwfHVzaHphy56ph85PcRS35iNqgrtK0fe3Qhpq7
    | v5vQYKlOGq5FI6Mf9ni7S1pXSqF4U9wuqZy4q4tXWAVootmJv1DIgfSMLvXplN9T
    | LucP
    |_-----END CERTIFICATE-----
    
    5275/tcp  open  jabber              syn-ack ttl 127
    | fingerprint-strings: 
    |   RPCCheck: 
    |_    <stream:error xmlns:stream="http://etherx.jabber.org/streams"><not-well-formed xmlns="urn:ietf:params:xml:ns:xmpp-streams"/></stream:error></stream:stream>
    | xmpp-info: 
    |   STARTTLS Failed
    |   info: 
    |     stream_id: rv8uc20ny
    |     features: 
    |     compression_methods: 
    |     capabilities: 
    |     xmpp: 
    |       version: 1.0
    |     unknown: 
    |     auth_mechanisms: 
    |     errors: 
    |       invalid-namespace
    |_      (timeout)
    
    5276/tcp  open  ssl/jabber          syn-ack ttl 127
    |_ssl-date: 2023-10-05T14:38:46+00:00; +1s from scanner time.
    | fingerprint-strings: 
    |   RPCCheck: 
    |_    <stream:error xmlns:stream="http://etherx.jabber.org/streams"><not-well-formed xmlns="urn:ietf:params:xml:ns:xmpp-streams"/></stream:error></stream:stream>
    | ssl-cert: Subject: commonName=fire.windcorp.thm
    | Subject Alternative Name: DNS:fire.windcorp.thm, DNS:*.fire.windcorp.thm
    | Issuer: commonName=fire.windcorp.thm
    | Public Key type: rsa
    | Public Key bits: 2048
    | Signature Algorithm: sha256WithRSAEncryption
    | Not valid before: 2020-05-01T08:39:00
    | Not valid after:  2025-04-30T08:39:00
    | MD5:   b715:5425:83f3:a20f:75c8:ca2d:3353:cbb7
    | SHA-1: 97f7:0772:a26b:e324:7ed5:bbcb:5f35:7d74:7982:66ae
    | -----BEGIN CERTIFICATE-----
    | MIIDLzCCAhegAwIBAgIIXUFELG7QgAIwDQYJKoZIhvcNAQELBQAwHDEaMBgGA1UE
    | AwwRZmlyZS53aW5kY29ycC50aG0wHhcNMjAwNTAxMDgzOTAwWhcNMjUwNDMwMDgz
    | OTAwWjAcMRowGAYDVQQDDBFmaXJlLndpbmRjb3JwLnRobTCCASIwDQYJKoZIhvcN
    | AQEBBQADggEPADCCAQoCggEBAKLH0/j17RVdD8eXC+0IFovAoql2REjOSf2NpJLK
    | /6fgtx3CA4ftLsj7yOpmj8Oe1gqfWd2EM/zKk+ZmZwQFxLQL93t1OD/za1gyclxr
    | IVbPVWqFoM2BUU9O3yU0VVRGP7xKDHm4bcoNmq9UNurEtFlCNeCC1fcwzfYvKD89
    | X04Rv/6kn1GlQq/iM8PGCLDUf1p1WJcwGT5FUiBa9boTU9llBcGqbodZaBKzPPP8
    | DmvSYF71IKBT8NsVzqiAiO3t/oHgApvUd9BqdbZeN46XORrOhBQV0xUpNVy9L5OE
    | UAD1so3ePTNjpPE5SfTKymT1a8Fiw5kroKODN0nzy50yP3UCAwEAAaN1MHMwMQYD
    | VR0RBCowKIIRZmlyZS53aW5kY29ycC50aG2CEyouZmlyZS53aW5kY29ycC50aG0w
    | HQYDVR0OBBYEFOtMzqgfsY11qewZNfPjiLxnGykGMB8GA1UdIwQYMBaAFOtMzqgf
    | sY11qewZNfPjiLxnGykGMA0GCSqGSIb3DQEBCwUAA4IBAQAHofv0VP+hE+5sg0KR
    | 2x0Xeg4cIXEia0c5cIJ7K7bhfoLOcT7WcMKCLIN3A416PREdkB6Q610uDs8RpezJ
    | II/wBoIp2G0Y87X3Xo5FmNJjl9lGX5fvayen98khPXvZkurHdWdtA4m8pHOdYOrk
    | n8Jth6L/y4L5WlgEGL0x0HK4yvd3iz0VNrc810HugpyfVWeasChhZjgAYXUVlA8k
    | +QxLxyNr/PBfRumQGzw2n3msXxwfHVzaHphy56ph85PcRS35iNqgrtK0fe3Qhpq7
    | v5vQYKlOGq5FI6Mf9ni7S1pXSqF4U9wuqZy4q4tXWAVootmJv1DIgfSMLvXplN9T
    | LucP
    |_-----END CERTIFICATE-----
    | xmpp-info: 
    |   STARTTLS Failed
    |   info: 
    |     features: 
    |     compression_methods: 
    |     capabilities: 
    |     xmpp: 
    |     unknown: 
    |     auth_mechanisms: 
    |     errors: 
    |_      (timeout)
    
    5985/tcp  open  http                syn-ack ttl 127 Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
    |_http-title: Not Found
    |_http-server-header: Microsoft-HTTPAPI/2.0
    
    7070/tcp  open  http                syn-ack ttl 127 Jetty 9.4.18.v20190429
    |_http-server-header: Jetty(9.4.18.v20190429)
    |_http-title: Openfire HTTP Binding Service
    | http-methods: 
    |_  Supported Methods: GET HEAD POST OPTIONS
    
    7443/tcp  open  ssl/http            syn-ack ttl 127 Jetty 9.4.18.v20190429
    |_http-title: Openfire HTTP Binding Service
    | http-methods: 
    |_  Supported Methods: GET HEAD POST OPTIONS
    | ssl-cert: Subject: commonName=fire.windcorp.thm
    | Subject Alternative Name: DNS:fire.windcorp.thm, DNS:*.fire.windcorp.thm
    | Issuer: commonName=fire.windcorp.thm
    | Public Key type: rsa
    | Public Key bits: 2048
    | Signature Algorithm: sha256WithRSAEncryption
    | Not valid before: 2020-05-01T08:39:00
    | Not valid after:  2025-04-30T08:39:00
    | MD5:   b715:5425:83f3:a20f:75c8:ca2d:3353:cbb7
    | SHA-1: 97f7:0772:a26b:e324:7ed5:bbcb:5f35:7d74:7982:66ae
    | -----BEGIN CERTIFICATE-----
    | MIIDLzCCAhegAwIBAgIIXUFELG7QgAIwDQYJKoZIhvcNAQELBQAwHDEaMBgGA1UE
    | AwwRZmlyZS53aW5kY29ycC50aG0wHhcNMjAwNTAxMDgzOTAwWhcNMjUwNDMwMDgz
    | OTAwWjAcMRowGAYDVQQDDBFmaXJlLndpbmRjb3JwLnRobTCCASIwDQYJKoZIhvcN
    | AQEBBQADggEPADCCAQoCggEBAKLH0/j17RVdD8eXC+0IFovAoql2REjOSf2NpJLK
    | /6fgtx3CA4ftLsj7yOpmj8Oe1gqfWd2EM/zKk+ZmZwQFxLQL93t1OD/za1gyclxr
    | IVbPVWqFoM2BUU9O3yU0VVRGP7xKDHm4bcoNmq9UNurEtFlCNeCC1fcwzfYvKD89
    | X04Rv/6kn1GlQq/iM8PGCLDUf1p1WJcwGT5FUiBa9boTU9llBcGqbodZaBKzPPP8
    | DmvSYF71IKBT8NsVzqiAiO3t/oHgApvUd9BqdbZeN46XORrOhBQV0xUpNVy9L5OE
    | UAD1so3ePTNjpPE5SfTKymT1a8Fiw5kroKODN0nzy50yP3UCAwEAAaN1MHMwMQYD
    | VR0RBCowKIIRZmlyZS53aW5kY29ycC50aG2CEyouZmlyZS53aW5kY29ycC50aG0w
    | HQYDVR0OBBYEFOtMzqgfsY11qewZNfPjiLxnGykGMB8GA1UdIwQYMBaAFOtMzqgf
    | sY11qewZNfPjiLxnGykGMA0GCSqGSIb3DQEBCwUAA4IBAQAHofv0VP+hE+5sg0KR
    | 2x0Xeg4cIXEia0c5cIJ7K7bhfoLOcT7WcMKCLIN3A416PREdkB6Q610uDs8RpezJ
    | II/wBoIp2G0Y87X3Xo5FmNJjl9lGX5fvayen98khPXvZkurHdWdtA4m8pHOdYOrk
    | n8Jth6L/y4L5WlgEGL0x0HK4yvd3iz0VNrc810HugpyfVWeasChhZjgAYXUVlA8k
    | +QxLxyNr/PBfRumQGzw2n3msXxwfHVzaHphy56ph85PcRS35iNqgrtK0fe3Qhpq7
    | v5vQYKlOGq5FI6Mf9ni7S1pXSqF4U9wuqZy4q4tXWAVootmJv1DIgfSMLvXplN9T
    | LucP
    |_-----END CERTIFICATE-----
    |_http-server-header: Jetty(9.4.18.v20190429)
    
    7777/tcp  open  socks5              syn-ack ttl 127 (No authentication; connection not allowed by ruleset)
    | socks-auth-info: 
    |_  No authentication
    
    9090/tcp  open  zeus-admin?         syn-ack ttl 127
    | fingerprint-strings: 
    |   GetRequest: 
    |     HTTP/1.1 200 OK
    |     Date: Thu, 05 Oct 2023 14:37:06 GMT
    |     Last-Modified: Fri, 31 Jan 2020 17:54:10 GMT
    |     Content-Type: text/html
    |     Accept-Ranges: bytes
    |     Content-Length: 115
    |     <html>
    |     <head><title></title>
    |     <meta http-equiv="refresh" content="0;URL=index.jsp">
    |     </head>
    |     <body>
    |     </body>
    |     </html>
    |   HTTPOptions: 
    |     HTTP/1.1 200 OK
    |     Date: Thu, 05 Oct 2023 14:37:12 GMT
    |     Allow: GET,HEAD,POST,OPTIONS
    |   JavaRMI, drda, ibm-db2-das, informix: 
    |     HTTP/1.1 400 Illegal character CNTL=0x0
    |     Content-Type: text/html;charset=iso-8859-1
    |     Content-Length: 69
    |     Connection: close
    |     <h1>Bad Message 400</h1><pre>reason: Illegal character CNTL=0x0</pre>
    |   SqueezeCenter_CLI: 
    |     HTTP/1.1 400 No URI
    |     Content-Type: text/html;charset=iso-8859-1
    |     Content-Length: 49
    |     Connection: close
    |     <h1>Bad Message 400</h1><pre>reason: No URI</pre>
    |   WMSRequest: 
    |     HTTP/1.1 400 Illegal character CNTL=0x1
    |     Content-Type: text/html;charset=iso-8859-1
    |     Content-Length: 69
    |     Connection: close
    |_    <h1>Bad Message 400</h1><pre>reason: Illegal character CNTL=0x1</pre>
    
    9091/tcp  open  ssl/xmltec-xmlmail? syn-ack ttl 127
    | ssl-cert: Subject: commonName=fire.windcorp.thm
    | Subject Alternative Name: DNS:fire.windcorp.thm, DNS:*.fire.windcorp.thm
    | Issuer: commonName=fire.windcorp.thm
    | Public Key type: rsa
    | Public Key bits: 2048
    | Signature Algorithm: sha256WithRSAEncryption
    | Not valid before: 2020-05-01T08:39:00
    | Not valid after:  2025-04-30T08:39:00
    | MD5:   b715:5425:83f3:a20f:75c8:ca2d:3353:cbb7
    | SHA-1: 97f7:0772:a26b:e324:7ed5:bbcb:5f35:7d74:7982:66ae
    | -----BEGIN CERTIFICATE-----
    | MIIDLzCCAhegAwIBAgIIXUFELG7QgAIwDQYJKoZIhvcNAQELBQAwHDEaMBgGA1UE
    | AwwRZmlyZS53aW5kY29ycC50aG0wHhcNMjAwNTAxMDgzOTAwWhcNMjUwNDMwMDgz
    | OTAwWjAcMRowGAYDVQQDDBFmaXJlLndpbmRjb3JwLnRobTCCASIwDQYJKoZIhvcN
    | AQEBBQADggEPADCCAQoCggEBAKLH0/j17RVdD8eXC+0IFovAoql2REjOSf2NpJLK
    | /6fgtx3CA4ftLsj7yOpmj8Oe1gqfWd2EM/zKk+ZmZwQFxLQL93t1OD/za1gyclxr
    | IVbPVWqFoM2BUU9O3yU0VVRGP7xKDHm4bcoNmq9UNurEtFlCNeCC1fcwzfYvKD89
    | X04Rv/6kn1GlQq/iM8PGCLDUf1p1WJcwGT5FUiBa9boTU9llBcGqbodZaBKzPPP8
    | DmvSYF71IKBT8NsVzqiAiO3t/oHgApvUd9BqdbZeN46XORrOhBQV0xUpNVy9L5OE
    | UAD1so3ePTNjpPE5SfTKymT1a8Fiw5kroKODN0nzy50yP3UCAwEAAaN1MHMwMQYD
    | VR0RBCowKIIRZmlyZS53aW5kY29ycC50aG2CEyouZmlyZS53aW5kY29ycC50aG0w
    | HQYDVR0OBBYEFOtMzqgfsY11qewZNfPjiLxnGykGMB8GA1UdIwQYMBaAFOtMzqgf
    | sY11qewZNfPjiLxnGykGMA0GCSqGSIb3DQEBCwUAA4IBAQAHofv0VP+hE+5sg0KR
    | 2x0Xeg4cIXEia0c5cIJ7K7bhfoLOcT7WcMKCLIN3A416PREdkB6Q610uDs8RpezJ
    | II/wBoIp2G0Y87X3Xo5FmNJjl9lGX5fvayen98khPXvZkurHdWdtA4m8pHOdYOrk
    | n8Jth6L/y4L5WlgEGL0x0HK4yvd3iz0VNrc810HugpyfVWeasChhZjgAYXUVlA8k
    | +QxLxyNr/PBfRumQGzw2n3msXxwfHVzaHphy56ph85PcRS35iNqgrtK0fe3Qhpq7
    | v5vQYKlOGq5FI6Mf9ni7S1pXSqF4U9wuqZy4q4tXWAVootmJv1DIgfSMLvXplN9T
    | LucP
    |_-----END CERTIFICATE-----
    | fingerprint-strings: 
    |   DNSStatusRequestTCP, DNSVersionBindReqTCP: 
    |     HTTP/1.1 400 Illegal character CNTL=0x0
    |     Content-Type: text/html;charset=iso-8859-1
    |     Content-Length: 69
    |     Connection: close
    |     <h1>Bad Message 400</h1><pre>reason: Illegal character CNTL=0x0</pre>
    |   GetRequest: 
    |     HTTP/1.1 200 OK
    |     Date: Thu, 05 Oct 2023 14:37:24 GMT
    |     Last-Modified: Fri, 31 Jan 2020 17:54:10 GMT
    |     Content-Type: text/html
    |     Accept-Ranges: bytes
    |     Content-Length: 115
    |     <html>
    |     <head><title></title>
    |     <meta http-equiv="refresh" content="0;URL=index.jsp">
    |     </head>
    |     <body>
    |     </body>
    |     </html>
    |   HTTPOptions: 
    |     HTTP/1.1 200 OK
    |     Date: Thu, 05 Oct 2023 14:37:24 GMT
    |     Allow: GET,HEAD,POST,OPTIONS
    |   Help: 
    |     HTTP/1.1 400 No URI
    |     Content-Type: text/html;charset=iso-8859-1
    |     Content-Length: 49
    |     Connection: close
    |     <h1>Bad Message 400</h1><pre>reason: No URI</pre>
    |   RPCCheck: 
    |     HTTP/1.1 400 Illegal character OTEXT=0x80
    |     Content-Type: text/html;charset=iso-8859-1
    |     Content-Length: 71
    |     Connection: close
    |     <h1>Bad Message 400</h1><pre>reason: Illegal character OTEXT=0x80</pre>
    |   RTSPRequest: 
    |     HTTP/1.1 400 Unknown Version
    |     Content-Type: text/html;charset=iso-8859-1
    |     Content-Length: 58
    |     Connection: close
    |     <h1>Bad Message 400</h1><pre>reason: Unknown Version</pre>
    |   SSLSessionReq: 
    |     HTTP/1.1 400 Illegal character CNTL=0x16
    |     Content-Type: text/html;charset=iso-8859-1
    |     Content-Length: 70
    |     Connection: close
    |_    <h1>Bad Message 400</h1><pre>reason: Illegal character CNTL=0x16</pre>
    9389/tcp  open  mc-nmf              syn-ack ttl 127 .NET Message Framing
    49668/tcp open  msrpc               syn-ack ttl 127 Microsoft Windows RPC
    49669/tcp open  ncacn_http          syn-ack ttl 127 Microsoft Windows RPC over HTTP 1.0
    49672/tcp open  msrpc               syn-ack ttl 127 Microsoft Windows RPC
    49673/tcp open  msrpc               syn-ack ttl 127 Microsoft Windows RPC
    49695/tcp open  msrpc               syn-ack ttl 127 Microsoft Windows RPC
    49927/tcp open  msrpc               syn-ack ttl 127 Microsoft Windows RPC
    
## Analizamos la informacion obtenida sobre los puertos

- Puerto 80

  -Nos muestra una web la cual contiene un boton con el titulo mas llamativo del mundo 'Reset password', este nos intenta redirecionar a un subdominio.

  ![image](https://github.com/Esevka/CTF/assets/139042999/af496387-6903-4c28-af37-400d21bf2e11)

  Editamos fichero hosts, anadimos el subdominio y dominio.

      ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/ra1.1]
      └─# cat /etc/hosts
      10.10.36.177    windcorp.thm fire.windcorp.thm

  Entramos de nuevo en la web y como vemos ya nos redirecciona correctamente.

  ![image](https://github.com/Esevka/CTF/assets/139042999/5a3b57e4-2260-4fea-9b43-11417640b75a)


  -Segun esto si tenemos un usuario y la respuesta a una de las preguntas podemos hacer un reset de la pass del usuario

  Con un simple vistazo en la web encontramos muchos posibles nombres de usuarios.

  ![image](https://github.com/Esevka/CTF/assets/139042999/54da1e33-0d49-4ea9-b794-7650f2fc59f9)
  ![image](https://github.com/Esevka/CTF/assets/139042999/75375432-26ff-4be8-b201-28093f8fb86d)

  -Tras analizar el codigo de la web y buscar y buscar vemos lo siguiente.

    ![image](https://github.com/Esevka/CTF/assets/139042999/dd84811b-4c7e-49e8-a9c2-08ff20ba5843)

      <img class="img-fluid rounded-circle mb-3" src="img/lilyleAndSparky.jpg" alt="">

    Una de las preguntas para hacer el reset de la pass es algo como ---> Como se llama tu mascota preferia?

    ![image](https://github.com/Esevka/CTF/assets/139042999/290ce1af-b2c7-4ade-afca-bfa351f97f11)

    Acabamos de conseguir hacer un reset de la pass del usuario lilyle y obtener unas credenciales.

    ![image](https://github.com/Esevka/CTF/assets/139042999/573ebce3-715f-4baf-b036-a2856814589b)


- Puerto 445 SMB

  -Como vemos tenemos credenciales validads y tenemos acceso a varias carpetas del sistema.

      ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/ra1.1]
      └─# crackmapexec smb  windcorp.thm -u lilyle -p ---pass-- --shares                    
      SMB         windcorp.thm    445    FIRE             [*] Windows 10.0 Build 17763 x64 (name:FIRE) (domain:windcorp.thm) (signing:True) (SMBv1:False)
      SMB         windcorp.thm    445    FIRE             [+] windcorp.thm\lilyle:---pass---
      SMB         windcorp.thm    445    FIRE             [+] Enumerated shares
      SMB         windcorp.thm    445    FIRE             Share           Permissions     Remark
      SMB         windcorp.thm    445    FIRE             -----           -----------     ------
      SMB         windcorp.thm    445    FIRE             ADMIN$                          Remote Admin
      SMB         windcorp.thm    445    FIRE             C$                              Default share
      SMB         windcorp.thm    445    FIRE             IPC$            READ            Remote IPC
      SMB         windcorp.thm    445    FIRE             NETLOGON        READ            Logon server share 
      SMB         windcorp.thm    445    FIRE             Shared          READ            
      SMB         windcorp.thm    445    FIRE             SYSVOL          READ            Logon server share 
      SMB         windcorp.thm    445    FIRE             Users           READ

  -Listamos la carpeta Shared

      ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/ra1.1]
      └─# smbclient //windcorp.thm/Shared -U lilyle   
      Password for [WORKGROUP\lilyle]:
      Try "help" to get a list of possible commands.
      smb: \> dir
        .                                   D        0  Sat May 30 02:45:42 2020
        ..                                  D        0  Sat May 30 02:45:42 2020
        Flag 1.txt                          A       45  Fri May  1 17:32:36 2020
        spark_2_8_3.deb                     A 29526628  Sat May 30 02:45:01 2020
        spark_2_8_3.dmg                     A 99555201  Sun May  3 13:06:58 2020
        spark_2_8_3.exe                     A 78765568  Sun May  3 13:05:56 2020
        spark_2_8_3.tar.gz                  A 123216290  Sun May  3 13:07:24 2020

        15587583 blocks of size 4096. 10914152 blocks available

  -Ya tendriamos la Flag1

      smb: \> get "Flag 1.txt"
      getting file \Flag 1.txt of size 45 as Flag 1.txt (0.2 KiloBytes/sec) (average 0.2 KiloBytes/sec)

  -



    

    

    

    

  
  



  
    

  

    
  
