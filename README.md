openvpn-python-mysql-auth
=========================

Quick and easy wrapper script for openvpn authentication using Python, pbkdf2_sha512 hashed passwords, and prepared SQL statements

Primary Goal
------------

- Provide quick and secure way to deploy OpenVPN in a multi-user setup.

Secondary Goals
---------------

- Stability
- Collect enough data to facilitate easy auditing after a security event
- Audit properly for a multi-admin environment
- Add fields useful to tracking changes (added by: sysadmin A and authorized by: manager B, etc)
- Document excessively

Tertiary Goals
--------------

- Finally get a project on Github :)
- Support ipv4; it's developed in ipv6 so no worries there.

Non-Goals
---------

- A web interface
- Any web interface, ever
- A multi-tenant multi-user environment (i.e. VPN hosting)
